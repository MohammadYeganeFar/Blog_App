from django.shortcuts import render
from blog_app.models.post_model import Post


def list_post(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(
        request,
        'post/list_post.html',
        context
    )