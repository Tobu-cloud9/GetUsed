from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = 'CustomUser'

    def __str__(self):
        return self.username