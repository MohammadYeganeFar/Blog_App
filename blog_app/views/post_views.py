from django.shortcuts import render
from blog_app.models.post_model import PostModel


def list_post(request):
    posts = PostModel.objects.all()
    context = {'posts': posts}
    return render(
        request,
        'post/list_post.html',
        context
    )