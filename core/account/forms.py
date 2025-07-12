from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'graduation_year', 'grade_point_average', 'sub_field_of_education',
                  'academic_interest', 'major', 'expected_graduation_year', 'bio', 'gender', 'phone_number',
                  'profile_pic']


class AuthenticationFormCaptcha(AuthenticationForm):
    captcha = CaptchaField()


class UserCreationFormCaptcha(UserCreationForm):
    captcha = CaptchaField()
