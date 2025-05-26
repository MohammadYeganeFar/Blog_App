from django.db import models
from blog_app.models.user import TimeStampModel, CustomUser


class Tag(models.Model):
    tag_name = models.CharField(max_length=10)


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
    

class Comment(TimeStampModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()


class Like(TimeStampModel):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'Like by {self.user.username} on {self.post.title}'