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


def post_list(request):
    all_posts_list = Post.objects.filter(status='published').order_by('-created_at')
    paginator = Paginator(all_posts_list, per_page=10)

    page_number = request.GET.get('page')
    try:
        posts_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        posts_page_obj = paginator.page(1)
    except EmptyPage:
        posts_page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj': posts_page_obj}
    
    return render(request, 'blog_app/post/post_list.html', context)



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


def search_results(request):
    search_form = SearchForm(request.GET)
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()

    if query:
        search_query = SearchQuery(query)
        search_vector = SearchVector('title') + SearchVector('content')
        
        posts = Post.objects.annotate(
            search=search_vector
        ).filter(search=search_query)

        if not posts.exists():
            messages.info(request, f"No posts found for '{query}'.")


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