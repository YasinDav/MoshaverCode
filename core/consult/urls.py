from django.urls import path
from .views import advisor_chat

urlpatterns = [
    path("api/advice/", advisor_chat, name="advisor_chat"),
]