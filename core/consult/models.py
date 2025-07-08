from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .simulator import simulate_ai_request

# from django.utils.translation import gettext_lazy as _

# get default user model
User = get_user_model()


# A General Class that creates for even users' request to consult
# every information such as time, result of consult and questions or etc. like them
class Consult(models.Model):
    # time
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # user
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # status of consult model, that show the end of consulting
    status = models.BooleanField(default=False)

    def __str__(self):
        user_extra = ""
        if not len(str(self.user)) <= 10:
            user_extra = "..."
        return f"{self.id}_ {self.created_date.date()} - {str(self.user)[:10]}{user_extra}"

    # def get_absolute_url(self):


type_mood = [
    (True, "range"),
    (False, "input")
]


class Question(models.Model):
    type = models.BooleanField(choices=type_mood)
    # connect to a consult model
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE)

    # time
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # a text or command that AI module receive to generate question
    # NOTE: for first of all consult is same. but even module's answer brings its self prompt to generate next question
    prompt = models.TextField()

    # in use to that prompt that AI module receive, gives a question to ask from user
    question = models.TextField()

    # user's answer to question
    answer = models.TextField(null=True, blank=True)

    # a prompt else to generate another next question
    next_prompt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}_ {self.created_date}"


type_mood_reverse = {
    "range": True,
    "input": False
}


@receiver(post_save, sender=Consult)
def create_first_question(instance, created, **kwargs):
    if created:
        response = simulate_ai_request("q")
        q = Question.objects.create(
            consult=instance,
            type=type_mood_reverse[response["type"]],
            question=response["question"],
            prompt="just a text for test"
        )
        q.save()


@receiver(post_save, sender=Question)
def update_consult(created, instance, **kwargs):
    if created:
        consult = instance.consult
        print(instance.id, consult.updated_date)
        consult.updated_date = timezone.now()
        consult.save()
        print(instance.id, consult.updated_date)
        print(consult.id, timezone.now())
