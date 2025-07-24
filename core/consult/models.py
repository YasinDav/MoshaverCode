from account.models import Profile
from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .simulator import ai_request, first_prompt

# from django.utils.translation import gettext_lazy as _

# get default user model
User = get_user_model()


# A General Class that creates for even users' request to consult
# every information such as time, result of consult and questions or etc. like them
class Consult(models.Model):
    # time
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    # user
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # status of consult model, that show the end of consulting
    status = models.BooleanField(default=False)

    experience = models.IntegerField(null=True, blank=True,
                                     choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)])

    #  Result of consultation
    extraversion = models.IntegerField(null=True, blank=True)  # برون‌گرایی
    agreeableness = models.IntegerField(null=True, blank=True)  # توافق‌پذیری
    conscientiousness = models.IntegerField(null=True, blank=True)  # وظیفه‌شناسی
    neuroticism = models.IntegerField(null=True, blank=True)  # روان‌رنجوری
    openness = models.IntegerField(null=True, blank=True)  # گشودگی به تجربه

    content = models.TextField(null=True, blank=True)

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
    # creating first question
    if created:
        response = ai_request(t="q", prompt=first_prompt)
        Question.objects.create(
            consult=instance,
            type=type_mood_reverse[response["type"]],
            question=response["question"],
            prompt=first_prompt
        )
    else:
        # handel experience
        if not instance.status and instance.experience is not None:
            consults = Consult.objects.filter(status=False, experience__isnull=False)

            sum = 0
            for consult in consults:
                sum += consult.experience

            profile = Profile.objects.get(user=instance.user)
            print(profile)
            profile.experience = round(sum / consults.count(), 1)
            profile.save()


@receiver(post_save, sender=Question)
def update_consult(created, instance, **kwargs):
    if created:
        consult = instance.consult
        consult.updated_date = timezone.now()
        consult.save()


auditlog.register(Consult)
auditlog.register(Question)
