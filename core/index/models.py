from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()
from auditlog.registry import auditlog


# from django_summernote.fields

class Developer(models.Model):
    full_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    github = models.URLField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default="default_user_profile_photo.jpg", blank=True)
    role = models.CharField(max_length=512)

    def __str__(self):
        return self.full_name


class SubGuide(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Guide(models.Model):
    sub_guide = models.ForeignKey(SubGuide, on_delete=models.CASCADE, null=True, blank=True)
    guide_name = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.guide_name

    def get_absolute_url(self):
        return f"{reverse('guide')}#{self.guide_name}"


class ContactUs(models.Model):
    username = models.CharField(max_length=256)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()

    def __str__(self):
        return self.subject


auditlog.register(ContactUs)
auditlog.register(Developer)
