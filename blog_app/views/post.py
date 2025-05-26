from django.shortcuts import render
from django.shortcuts import get_object_or_404
from blog_app.models.post import Post


def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(
        request,
        'post/post_list.html',
        context
    )

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(
        request,
        'blog_app/post/detail.html',
        context={'post': post}
    )