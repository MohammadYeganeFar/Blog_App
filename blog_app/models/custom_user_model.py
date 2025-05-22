from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class CustomUserModel(TimeStampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.get_full_name()