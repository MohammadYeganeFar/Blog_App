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


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    recently_viewed_posts_slugs = request.session.get('recently_viewed', [])

    if post.slug not in recently_viewed_posts_slugs:
        recently_viewed_posts_slugs.insert(0, post.slug)
        request.session['recently_viewed'] = recently_viewed_posts_slugs[:5] 

    recent_posts_objects = Post.objects.filter(
        slug__in=request.session.get('recently_viewed', []), 
        status='published'
    ).order_by('created_at') 

    context = {
        'post': post,
        'recently_viewed_posts': recent_posts_objects,
    }
    print(recent_posts_objects)
    return render(
        request,
        'blog_app/post/detail.html',
        context=context
    )