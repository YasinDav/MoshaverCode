from django import template

register = template.Library()


@register.simple_tag()
def consult_questions_number():
    return "hi"
