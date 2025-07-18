# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# import json
# import requests
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from hashlib import sha256

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy

from .forms import ConsultFormRange, ConsultFormInput
from .models import Consult, Question
from .simulator import simulate_ai_request

# OLLAMA_URL = "http://localhost:11500/api/chat"
# OLLAMA_MODEL = "mistral"
#
#
# @csrf_exempt
# # @require_POST
# # @login_required
# def advisor_chat(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             user_input = data.get("question")
#
#             if not user_input:
#                 return JsonResponse({"error": "Missing 'question' field."}, status=400)
#
#             # Create a consult object for the user if not exists (optional logic)
#             # consult = Consult.objects.create(user=request.user)
#
#             # پیام‌های مکالمه با نقش مشخص (برای context بیشتر)
#             messages = [
#                 {"role": "system", "content": "You are a helpful academic advisor who recommends careers and "
#                                               "university majors based on interests."},
#                 {"role": "user", "content": user_input}
#             ]
#
#             # ارسال درخواست به Ollama
#             response = requests.post(
#                 OLLAMA_URL,
#                 json={
#                     "model": OLLAMA_MODEL,
#                     "messages": messages,
#                     "stream": False
#                 }
#             )
#             response.raise_for_status()
#             result = response.json()
#
#             # ذخیره پرسش و پاسخ در دیتابیس
#             # Question.objects.create(
#             #     prompt=messages[1]["content"],
#             #     question=user_input,
#             #     answer=result["message"]["content"],
#             #     next_prompt=""  # فعلاً خالی می‌گذاریم تا ساختار کامل‌تر شود
#             # )
#
#             return JsonResponse({"response": result["message"]["content"]})
#
#         except requests.RequestException as e:
#             return JsonResponse({"error": "Failed to contact model.", "details": str(e)}, status=502)
#
#         except Exception as e:
#             return JsonResponse({"error": "Internal server error.", "details": str(e)}, status=500)
#     else:
#         return HttpResponse("bad request")
type_mood = {
    "range": True,
    "input": False
}

starting_prompt = "just a text for test"


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def question_view(request, consult_id, question_model_id_hash):
    consult = get_object_or_404(Consult, id=consult_id)

    if not consult.status:  # if status be False, it means consult is disable and finished
        return HttpResponse("consult is finished")

    questions_of_consult_model = Question.objects.filter(consult_id=consult_id)

    if request.method == 'POST':

        questions = questions_of_consult_model.filter(Q(answer__isnull=True) | Q(answer=""))

        question_model = None
        for question in questions:
            if sha256(str(question.id).encode()).hexdigest() == question_model_id_hash:
                question_model = question
                break

        if question_model is None:
            return HttpResponse("question not found")

        if question_model.answer:
            return HttpResponse("question already answered")

        if question_model.type:
            form = ConsultFormRange(request.POST)
        else:
            form = ConsultFormInput(request.POST)

        if form.is_valid():
            answer = form.cleaned_data["answer"]
            question_model.answer = answer
            response = simulate_ai_request("a")
            question_model.next_prompt = response
            question_model.save()

            # create new question model
            if questions_of_consult_model.count() == 0:
                prompt = starting_prompt
            else:
                prompt = questions_of_consult_model.order_by("created_date").last()
                prompt = prompt.next_prompt

            response = simulate_ai_request("q")
            question_model = Question.objects.create(
                type=type_mood[response["type"]],
                question=response["question"],
                consult=consult,
                prompt=prompt
            )

            if question_model.type:
                form = ConsultFormRange()
            else:
                form = ConsultFormInput()

            return render(request, "consult form.html",
                          {"form": form, "consult_id": consult_id,
                           "question_id": sha256(str(question_model.id).encode()).hexdigest(),
                           "question": question_model.question})

            # return render(request, "consult form.html", {"form": form})
        else:
            return HttpResponse("bad request")
    elif request.method == 'GET':

        question_model = None
        for question in questions_of_consult_model:
            if sha256(str(question.id).encode()).hexdigest() == question_model_id_hash:
                question_model = Question.objects.get(id=question.id)
                break

        if question_model is None:
            return HttpResponse("question not found")
        elif question_model.answer:
            return HttpResponse("question already answered")

        elif question_model is not None:
            if question_model.type:
                form = ConsultFormRange()
            else:
                form = ConsultFormInput()

            return render(request, "consult form.html",
                          {"form": form, "consult_id": consult_id,
                           "question_id": sha256(str(question_model.id).encode()).hexdigest(),
                           "question": question_model.question})

    else:
        return HttpResponse("Bad request")


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


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def consult_panel_view(request):
    consults = Consult.objects.filter(user=request.user)
    consults_with_urls = {}

    for consult in consults:
        consults_with_urls[consult] = find_secreted_url(consult)
    # consults_with_urls.
    return render(request, "consults panel.html", {"consults": consults_with_urls})


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
