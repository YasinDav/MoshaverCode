from django.urls import path
from .views import *

urlpatterns = [
    # path("api/advice/", advisor_chat, name="advisor_chat"),
    path('', consult_panel_view, name='consult'),
    path('new/', new_consult_view, name='new_consult'),
    path('delete/<int:id>/', delete_consult_view, name='delete_consult'),
    path("<int:consult_id>/<str:question_model_id_hash>/", question_view, name="question")
]
