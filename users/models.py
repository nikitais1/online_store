from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    phone = models.CharField(max_length=150, **NULLABLE, verbose_name='телефон')
    country = models.CharField(max_length=100, **NULLABLE, verbose_name='страна')

    is_active = models.BooleanField(default=False, verbose_name='подтвержден ли аккаунт')
    verification_token = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
