from account.models import Profile
from auditlog.models import LogEntry
from consult.models import Consult
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from .forms import ContactUsForm
from .models import Developer, Guide, SubGuide


def index_view(request):
    developers = Developer.objects.all()
    return render(request, 'index.html', {'developers': developers})


def guide_view(request):
    sub_guides = SubGuide.objects.all()
    guides = Guide.objects.all()

    sub_guide_dict = {}

    for i in sub_guides:
        sub_guide_dict[i] = guides.filter(sub_guide=i)

    return render(request, 'guide.html', {'guides_dict': sub_guide_dict})


def contact_view(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('contact'))
        else:
            return HttpResponse('Something went wrong')
    else:
        form = ContactUsForm()

        developers = Developer.objects.all()

        context = {'developers': developers, 'form': form}

        if request.user.is_authenticated:
            context['user'] = request.user

        return render(request, 'contact.html', context)


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def dashboard_view(request):
    consults = Consult.objects.filter(user=request.user)
    finished_consults = consults.filter(status=False)
    unfinished_consults = consults.filter(status=True)

    profile = Profile.objects.get(user=request.user)
    experience = profile.experience

    logs = LogEntry.objects.filter(actor=profile.user).order_by('-timestamp')[:50]

    filtered_logs = []
    for log in logs:
        changes = log.changes_dict or {}
        if list(changes.keys()) == ['experience']:
            continue  # اگر فقط experience تغییر کرده بود، ردش کن
        filtered_logs.append(log)

    return render(request, 'dashboard.html', {'consults': consults, 'finished_consults': finished_consults,
                                              'unfinished_consults': unfinished_consults, 'experience': experience,
                                              'logs': filtered_logs[:10]})
