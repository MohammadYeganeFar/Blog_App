from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from blog_app.models import Post, Like


def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(
        request,
        'post/post_list.html',
        context
    )


@login_required
@require_POST
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    user = request.user
    like_instance, created = Like.objects.get_or_create(post=post, user=user)

    if not created:
        like_instance.delete()
        liked = False
    else:
        liked = True

    like_count = post.likes.count()

    return JsonResponse({'liked':liked, 'like_count': like_count})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(
        request,
        'blog_app/post/detail.html',
        context={'post': post}
    )