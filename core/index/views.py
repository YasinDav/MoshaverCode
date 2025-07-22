from functools import wraps

from account.models import Profile
from auditlog.models import LogEntry
from consult.models import Consult
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.shortcuts import render

from .forms import ContactUsForm
from .models import Developer, Guide, SubGuide


def profile_complete_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            profile = getattr(user, 'profile', None)
            if profile:
                if not profile.bio or not profile.phone_number:
                    messages.warning(request, 'لطفاً ابتدا پروفایل خود را کامل کنید.')
                    return redirect(reverse('edit_profile'))
            else:
                messages.warning(request, 'لطفاً ابتدا پروفایل خود را کامل کنید.')
                return redirect(reverse('edit_profile'))
        return view_func(request, *args, **kwargs)

    return _wrapped_view


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


@profile_complete_required
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


@profile_complete_required
@staff_member_required
def log_list_view(request):
    logs = LogEntry.objects.select_related('actor', 'content_type').order_by('-timestamp')

    # دریافت پارامترها از GET
    action = request.GET.get('action')
    models_selected = request.GET.getlist('model')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # فیلتر نوع عملیات
    if action in ['0', '1', '2']:
        logs = logs.filter(action=action)

    # فیلتر مدل
    if models_selected:
        logs = logs.filter(content_type__model__in=models_selected)

    # فیلتر تاریخ
    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)

    # لیست مدل‌ها برای منوی کشویی
    models = ContentType.objects.values_list('model', flat=True).distinct()

    # نمودار
    log_counts = (
        logs.annotate(date=TruncDate('timestamp'))  # تبدیل تاریخ‌ و زمان به فقط "تاریخ"
        .values('date')  # فقط تاریخ رو نگه می‌داریم
        .annotate(count=Count('id'))  # شمارش تعداد لاگ‌ها در هر تاریخ
        .order_by('date')  # مرتب‌سازی صعودی بر اساس تاریخ
    )

    chart_labels = [entry['date'].strftime('%Y-%m-%d') for entry in log_counts]
    chart_data = [entry['count'] for entry in log_counts]

    return render(request, 'logs.html', {
        'logs': logs,
        'models': models,
        'selected_action': action,
        'selected_model': models_selected,
        'date_from': date_from,
        'date_to': date_to,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })
