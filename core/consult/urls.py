from django.urls import path
from .views import *

urlpatterns = [
    # path("api/advice/", advisor_chat, name="advisor_chat"),
    path('test/<int:id>/', test_secreted_url, name='test'),
    path('consult/', consult_panel, name='consult'),
    path('consult/new/', new_consult, name='new_consult'),
    path("<int:consult_id>/<str:question_model_id_hash>/", question, name="question")
]
