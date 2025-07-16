from datetime import datetime
from persiantools.jdatetime import JalaliDate
from account.models import Profile
from django import template

register = template.Library()


@register.inclusion_tag("user aouth.html")
def show_question(user):
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = None
    return {"is_authenticated": user.is_authenticated, "profile": profile, "user": user}


@register.filter
def multiply(value, arg):
    return value * arg


number_to_graduation_year = {'7': 'هفتم متوسطه اول', '8': 'هشتم متوسطه اول',
                             '9': 'نهم متوسطه اول', '10': 'دهم متوسطه دوم',
                             '11': 'یازدهم متوسطه دوم',
                             '12': 'دوازدهم متوسطه دوم'}


@register.filter
def change_number_to_graduation_year(number: str):
    return number_to_graduation_year[number]

@register.filter
def format_date(date: datetime):
    return str(JalaliDate(date)).replace("-", "/")

