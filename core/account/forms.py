from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=256, required=True)
    last_name = forms.CharField(max_length=256, required=True)
    email = forms.EmailField(required=True)

    tags = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ['user', 'created_at', 'updated_at', 'experience',]


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'profile_pic':
                field.widget.attrs['class'] = 'avatar-upload-input'
            elif name in ['gender', 'graduation_year']:
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        # مقداردهی اولیه فیلدهای یوزر
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        # به‌روزرسانی اطلاعات یوزر
        if profile.user_id:
            user = profile.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()

        if commit:
            profile.save()
            self.save_m2m()  # ضروری برای skills (TaggableManager)

        return profile


class AuthenticationFormCaptcha(AuthenticationForm):
    captcha = CaptchaField()


class UserCreationFormCaptcha(UserCreationForm):
    captcha = CaptchaField()
