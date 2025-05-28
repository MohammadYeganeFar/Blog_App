from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from blog_app.models import Post, Like
from blog_app.forms.search import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def post_list(request):
    all_posts_list = Post.objects.filter(status='published').order_by('-created_at')
    paginator = Paginator(all_posts_list, per_page=1)

    page_number = request.GET.get('page')
    try:
        posts_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        posts_page_obj = paginator.page(1)
    except EmptyPage:
        posts_page_obj = paginator.page(paginator.num_pages)

    context = {'posts': posts_page_obj}
    
    return render(request, 'blog_app/post/list.html', context)



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Allows AJAX requests without CSRF validation
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    user = request.user
    like_instance, created = Like.objects.get_or_create(post=post, user=user)

    if not created:
        like_instance.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})




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
        context={'post': post}
    )


def search_results(request):
    search_form = SearchForm(request.GET)
    query = request.GET.get('q')
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
        
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    context = {
        'search_form': search_form,
        'query': query,
        'page_obj': page_obj,
        'posts':posts
    }
    return render(request, 'blog_app/post/search_results.html', context)