from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class CustomUserModel(TimeStampModel):
    first_name = models.CharField(max_length=120, blank=False, null=False)
    last_name = models.CharField(max_length=120, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)

    def get_full_name(self):
        return f"{self.fname} {self.lname}"
    
    def get_short_name(self):
        return self.fname
    
    def __str__(self):
        return self.get_full_name()