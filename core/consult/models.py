from django.db import models
from django.contrib.auth import get_user_model
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
        return f"{self.id}_ {self.created_date.date()} - {self.user}"

    # def get_absolute_url(self):


class Question(models.Model):
    # a text or command that AI module receive to generate question
    # NOTE: for first of all consult is same. but even module's answer brings its self prompt to generate next question
    prompt = models.TextField()

    # in use to that prompt that AI module receive, gives a question to ask from user
    question = models.TextField()

    # user's answer to question
    answer = models.TextField()

    # a prompt else to generate another next question
    next_prompt = models.TextField()

    def __str__(self):
        return f"{self.id}_ {self.question[:10]}... - {self.answer[:10]}..."
