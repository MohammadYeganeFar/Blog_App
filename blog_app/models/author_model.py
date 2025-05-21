from django.db import models
from blog_app.models import CustomUserModel


class AuthorModel(CustomUserModel):
    bio = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f"Author: {self.username}"