from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")

    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Токен")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
