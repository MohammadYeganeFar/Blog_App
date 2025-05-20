from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class CustomUserModel(AbstractUser, TimeStampModel):
    first_name = None
    last_name = None 
    fname = models.CharField(verbose_name='First Name', max_length=120)
    lname = models.CharField(verbose_name='Last Name', max_length=120)
    email = models.EmailField(verbose_name='Email Address', unique=True)
    username = models.CharField(max_length=150, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return f"{self.fname} {self.lname}"
    
    def get_short_name(self):
        return self.fname
    
    def __str__(self):
        return self.get_full_name()