from django.shortcuts import render
from blog_app.models.post import Post


def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(
        request,
        'post/post_list.html',
        context
    )