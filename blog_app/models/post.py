from django.db import models
from blog_app.models.custom_user import TimeStampModel, CustomUser
from blog_app.models.tag import Tag




class Post(TimeStampModel):
    STATUS_CHOICES = {
        'published': 'Published',
        'archived': 'Archived',
        'drafted': 'Drafted'
        }
    content = models.TextField()     
    title = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Drafted'
    )
    tags = models.ManyToManyField(Tag)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title}'