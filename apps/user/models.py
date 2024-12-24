from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.EmailField(null=False, blank=False, unique=True)


class Profile(models.Model):
    full_name = models.CharField(max_length=250)
    avatar = models.FileField(blank=True, null=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
