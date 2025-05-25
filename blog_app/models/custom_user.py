from django.contrib.auth.models import User, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class CustomUser(TimeStampModel, AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name = 'custom_user_sett'
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.get_full_name()