
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    telegram = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to="users", null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    activation_code = models.CharField(max_length=50, null=True, blank=True)
    activated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

