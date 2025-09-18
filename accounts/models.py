from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # extended the default User model with additional fields
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)
    verify_token = models.CharField(max_length=6, blank=True, null=True)
    reset_token = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
