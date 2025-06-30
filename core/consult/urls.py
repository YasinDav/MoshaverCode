from django.urls import path
from .views import *

urlpatterns = [
    # path("api/advice/", advisor_chat, name="advisor_chat"),
    path("<int:question_id>/<int:consult_id>/", answers, name="Answers")
]