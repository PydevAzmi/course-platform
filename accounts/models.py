from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

def profile_image_path(instance, file_name):
    return f'profile_images/users/{instance.username}/{file_name}'

ROLE = [
    ("Student", _("Student")),
    ("Professor", _("Professor")),
]

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(_("role"), max_length=50, choices=ROLE)
    phone_number = models.CharField( max_length=14, null=True,blank=True)
    profile_image = models.ImageField(upload_to=profile_image_path, null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']


class Professor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, verbose_name=_("User"), related_name="professor_profile", on_delete=models.CASCADE)
    bio = models.CharField(_("Bio"), max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return f'Prof. {self.user.username}'

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, verbose_name=_("User"), related_name="student_profile", on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, verbose_name=_("Date of Birth"), null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username}'

@receiver(post_save, sender=User)  
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'Student':
            Student.objects.create(user=instance)
        elif instance.role == 'Professor':
            Professor.objects.create(user=instance)
