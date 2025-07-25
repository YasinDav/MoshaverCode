from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default_user_profile_photo.jpg', blank=True)

    phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)])

    gender = models.CharField(max_length=10, choices=[('زن', 'زن'), ('مرد', 'مرد'), ('دیگر', 'دیگر')],
                              default='Other')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    bio = models.TextField()

    experience = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

    expected_graduation_year = models.IntegerField(null=True)
    academic_interest = models.CharField(max_length=512)
    major = models.CharField(max_length=512)
    sub_field_of_education = models.CharField(max_length=512, blank=True, null=True)
    grade_point_average = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    graduation_year = models.CharField(max_length=4, choices=[('7', 'هفتم متوسطه اول'), ('8', 'هشتم متوسطه اول'),
                                                              ('9', 'نهم متوسطه اول'), ('10', 'دهم متوسطه دوم'),
                                                              ('11', 'یازدهم متوسطه دوم'),
                                                              ('12', 'دوازدهم متوسطه دوم'), ])
    school = models.CharField(max_length=256)
    skills = TaggableManager(blank=True)

    def __str__(self):
        return self.user.username

    @property
    def display_name(self):
        """Returns the best available name representation"""
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.username

    @property
    def display_email(self):
        """Returns email or warning"""
        return self.user.email or "No email set"


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


auditlog.register(User)
auditlog.register(Profile)
