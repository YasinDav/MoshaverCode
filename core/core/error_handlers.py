from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse


def render_error(request: HttpRequest, error_code: int, error_title: str, error_message: str,
                 redirect_to: str, button_value: str = 'بازگشت') -> HttpResponse:
    return render(request, "error page.html", {
        "error_code": error_code,
        "error_title": error_title,
        "error_message": error_message,
        "return_url": redirect_to,
        "button_value": button_value,
    })


def handler403(request, exception=None):
    return render_error(
        request,
        error_code=403,
        error_title="دسترسی غیرمجاز",
        error_message="شما اجازه دسترسی به این صفحه را ندارید.",
        redirect_to=reverse("index")
    )


def handler404(request, exception=None):
    return render_error(
        request,
        error_code=404,
        error_title="صفحه پیدا نشد",
        error_message="صفحه‌ای که به دنبال آن بودید وجود ندارد یا حذف شده است.",
        redirect_to=reverse("index")
    )


def handler405(request, exception=None):
    return render_error(
        request,
        error_code=405,
        error_title="روش درخواست نامعتبر",
        error_message="این صفحه فقط از روش‌های خاصی (مثلاً GET یا POST) پشتیبانی می‌کند.",
        redirect_to=reverse("index")
    )


def handler500(request):
    return render_error(
        request,
        error_code=500,
        error_title="خطای داخلی سرور",
        error_message="مشکلی در سرور رخ داده است. لطفاً بعداً دوباره تلاش کنید.",
        redirect_to=reverse("index")
    )