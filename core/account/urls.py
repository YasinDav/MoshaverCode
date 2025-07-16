from django.urls import path
from django.views.generic import edit

from .views import *
urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', edit_profile_view, name='edit_profile')
]