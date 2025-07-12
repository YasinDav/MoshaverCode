from django.urls import path
from .views import *
urlpatterns = [
    path('', edit_profile, name='profile')
]