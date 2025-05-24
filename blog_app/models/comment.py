from django.db import models
from blog_app.models.post import PostModel
from blog_app.models.custom_user import TimeStampModel, CustomUser


class Comment(TimeStampModel):
    post = models.ForeignKey(PostModel, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()


class Like(TimeStampModel):
    post = models.ForeignKey(PostModel, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
