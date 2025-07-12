from django.db import models


class Developer(models.Model):
    full_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    github = models.URLField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default="default_user_profile_photo.jpg", blank=True)
    role = models.CharField(max_length=512)

    def __str__(self):
        return self.full_name
