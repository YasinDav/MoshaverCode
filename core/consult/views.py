from hashlib import sha256

from core.error_handlers import render_error
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from index.views import profile_complete_required

from .forms import ConsultFormRange, ConsultFormInput
from .models import Consult, Question
from .simulator import ai_request, ai_request_result, ai_request_percentage


def find_secreted_url(consult: Consult, complete_url: bool = False):
    if consult is not None:

        question = Question.objects.filter(consult=consult).order_by("created_date").last()

        if question is not None:
            question_model_id_hash = sha256(str(question.id).encode()).hexdigest()
            if complete_url:
                return reverse("question",
                               kwargs={"consult_id": consult.id, "question_model_id_hash": question_model_id_hash})
            else:
                return question_model_id_hash
        else:
            return None
    else:
        return None


type_mood = {
    "range": True,
    "input": False
}

starting_prompt = "just a text for test"


@profile_complete_required
@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def question_view(request, consult_id, question_model_id_hash):
    consult = get_object_or_404(Consult, id=consult_id)

    if not consult.status:  # if status be False, it means consult is disable and finished
        return render_error(request, 410, "مشاوره به پایان رسیده",
                            "این مشاوره قبلاً تکمیل شده و امکان ادامه یا ویرایش آن وجود ندارد.", reverse("consult"))

    questions_of_consult_model = Question.objects.filter(consult_id=consult_id)

    if request.method == 'POST':

        if consult.question_set.count() >= 10:
            consult.status = False
            consult.content = ai_request_result()
            consult.agreeableness = ai_request_percentage("agreeableness")
            consult.extraversion = ai_request_percentage("extraversion")
            consult.neuroticism = ai_request_percentage("neuroticism")
            consult.conscientiousness = ai_request_percentage("conscientiousness")
            consult.openness = ai_request_percentage("openness")

            consult.save()

            return reverse_lazy("result", kwargs={"id": consult.id})

        questions = questions_of_consult_model.filter(Q(answer__isnull=True) | Q(answer=""))

        question_model = None
        for question in questions:
            if sha256(str(question.id).encode()).hexdigest() == question_model_id_hash:
                question_model = question
                break

        if question_model is None:
            return render_error(request, 404, "سؤال یافت نشد", "سؤالی با این شناسه پیدا نشد یا ممکن است حذف شده باشد.",
                                reverse("consult"))

        if question_model.answer:
            return render_error(request, 410, "سوال پاسخ داده شده",
                                "این سوال قبلاً تکمیل شده و امکان ویرایش آن وجود ندارد. میتوانید به ادامه ی مشاوره بپردازید.",
                                find_secreted_url(consult, True), button_value='ادامه سوالات')

        if question_model.type:
            form = ConsultFormRange(request.POST)
        else:
            form = ConsultFormInput(request.POST)

        if form.is_valid():
            answer = form.cleaned_data["answer"]
            question_model.answer = answer
            response = ai_request(t="a", question=question_model.question, user_input=answer)
            question_model.next_prompt = response
            question_model.save()

            # create new question model
            if questions_of_consult_model.count() == 0:
                prompt = starting_prompt
            else:
                prompt = questions_of_consult_model.order_by("created_date").last()
                prompt = prompt.next_prompt

            response = ai_request(t="q", prompt=prompt)
            question_model = Question.objects.create(
                type=type_mood[response["type"]],
                question=response["question"],
                consult=consult,
                prompt=prompt
            )

            # if question_model.type:
            #     form = ConsultFormRange()
            # else:
            #     form = ConsultFormInput()

            return redirect(reverse("question", kwargs={
                "consult_id": consult_id,
                "question_model_id_hash": sha256(str(question_model.id).encode()).hexdigest()
            }))

            # return render(request, "consult form.html", {"form": form})
        else:
            messages.error(request, "فرم ارسالی معتبر نیست. لطفاً ورودی‌ها را بررسی کنید.")
            return redirect(reverse("question", kwargs={
                "consult_id": consult_id,
                "question_model_id_hash": sha256(str(question_model.id).encode()).hexdigest()
            }))
    elif request.method == 'GET':

        question_model = None
        for question in questions_of_consult_model:
            if sha256(str(question.id).encode()).hexdigest() == question_model_id_hash:
                question_model = Question.objects.get(id=question.id)
                break

        if question_model is None:
            return render_error(request, 404, "سؤال یافت نشد", "سؤالی با این شناسه پیدا نشد یا ممکن است حذف شده باشد.",
                                reverse("consult"))
        elif question_model.answer:
            return render_error(request, 410, "سوال پاسخ داده شده",
                                "این سوال قبلاً تکمیل شده و امکان ویرایش آن وجود ندارد. میتوانید به ادامه ی مشاوره بپردازید.",
                                find_secreted_url(consult, True), button_value='ادامه سوالات')

        elif question_model is not None:
            if question_model.type:
                form = ConsultFormRange()
                type = "range"
            else:
                form = ConsultFormInput()
                type = "input"

            return render(request, "consult form.html",
                          {"form": form, "consult_id": consult_id,
                           "question_id": sha256(str(question_model.id).encode()).hexdigest(),
                           "question": question_model.question,
                           "type": type})
    else:
        return render_error(
            request,
            error_code=405,
            error_title="متد نامعتبر",
            error_message="درخواست ارسالی با متدی غیرمجاز انجام شده است.",
            redirect_to=request.path,
            button_value="بازگشت به فرم"
        )


@profile_complete_required
@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def consult_panel_view(request):
    consults = Consult.objects.filter(user=request.user)
    consults_with_urls = {}

    for consult in consults:
        consults_with_urls[consult] = find_secreted_url(consult)
    # consults_with_urls.
    return render(request, "consults panel.html", {"consults": consults_with_urls})


@profile_complete_required
@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def new_consult_view(request):
    if request.method == "POST":
        c = Consult.objects.create(
            user=request.user,
            status=True,
        )

        return redirect(reverse_lazy("question",
                                     kwargs={"question_model_id_hash": find_secreted_url(consult=c, complete_url=False),
                                             "consult_id": c.id}))

    return redirect(reverse("consult"))


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def delete_consult_view(request, id):
    if request.method == "POST":
        consult = get_object_or_404(Consult, id=id)
        if request.user == consult.user:
            consult.delete()
    return redirect(reverse("consult"))


@profile_complete_required
@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def result_consult_view(request, id):
    consult = get_object_or_404(Consult, id=id)
    if consult.user == request.user:
        if not consult.status:

            content = consult.content.split("\n")

            context = {
                "content": content,
                "extraversion": consult.extraversion,
                "agreeableness": consult.agreeableness,
                "neuroticism": consult.neuroticism,
                "openness": consult.openness,
                "conscientiousness": consult.conscientiousness
            }
            return render(request, "consult result.html", context)
        else:
            return render_error(request, 410, "مشاوره در جریان است",
                                "مشاوره هنوز به پایان نرسیده. ابتدا به سوالات جواب دهید",
                                find_secreted_url(consult, True), button_value='ادامه سوالات')

    else:
        return render_error(request, 404, "مشاوره یافت نشد.",
                            "این مشاوره وجود ندارد یا ممکن است حذف شده باشد.", reverse("consult"))
