from django.urls import path

from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('guide/', guide_view, name='guide'),
    path('contact/', contact_view, name='contact'),
    path("logs/", log_list_view, name="log_list"),
]
