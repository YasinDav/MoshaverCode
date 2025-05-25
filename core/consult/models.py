from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# get defult user model
User = get_user_model()

# A General Class that creates for even users' request to consult
# every information such as time, result of consult and questions or etc like them
class Consult(models):

    # time
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    # user
    user = models.ForeignKey(User, on_delete=models.SET_NULL)

class Question(models):
    # a text or command that ai module recive to generate question
    # NOTE: for fisrt of all consult is same. but even module's anwer brings its self prompt to generate next question
    prompt = models.TextField()

    # in use to that prompt that ai module recive, gives a question to ask from user
    question = models.TextField()

    # user's anwer to question
    answer = models.TextField()

    # a prompt else to generate another next question
    next_prompt = models.TextField()