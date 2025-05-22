from django.db import models
from blog_app.models.custom_user_model import TimeStampModel

class PostModel(TimeStampModel):
    content = models.TextField()     
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title}'