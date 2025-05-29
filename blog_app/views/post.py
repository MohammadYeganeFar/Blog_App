from django.http import JsonResponse
from blog_app.forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from blog_app.models import Post, Like, Comment
from blog_app.forms.search import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse
from blog_app.models import Tag
from blog_app.forms.post import PostForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from blog_app.views.utils import clean_tags
from blog_app.models.post import Post
from blog_app.models.user import CustomUser


@permission_required('blog_app.publish_post')
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            user_tags = form.cleaned_data['tags']
            clean_tags_list = clean_tags(user_tags)
            post.set_tags(clean_tags_list)
            post.save()
            print(f'post.tags: {post.tags.all()}')
            return redirect(
                reverse(
                    'blog_app:post_detail',
                    args=[user.username, post.slug]))
        else:
            messages.error(request, 'Invalid form!')
            return render(
                request,
                'blog_app/post/create.html',
                {'form': form, 'is_editing': False}
            )
    else:
        form = PostForm()
        return render(
            request,
            'blog_app/post/create.html',
            {'form': form, 'is_editing': False}
        )

def edit_post(request, username, slug):
    post = get_object_or_404(Post, author__username=username, slug=slug)
    user = request.user

    if not (user == post.author or user.is_staff):
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('blog_app:post_detail', username=post.author.username, slug=post.slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        
        if form.is_valid():
            post = form.save(commit=False)
            user_tags = form.cleaned_data['tags']
            clean_tags_list = clean_tags(user_tags)
            post.set_tags(clean_tags_list)
            post.save()
            return redirect(reverse('blog_app:post_detail', args=[user.username, post.slug]))
        else:
            return render(
                request,
                'blog_app/post/create.html',
                {'form': form, 'post':post, 'is_editing': True}
            )
    else:
        form = PostForm(instance=post)
        return render(
                request,
                'blog_app/post/create.html',
                {'form': form, 'post':post, 'is_editing': True}
            )
        
def post_list(request):
    all_posts_list = Post.objects.filter(status='published').order_by('-created_at')
    paginator = Paginator(all_posts_list, per_page=2)

    page_number = request.GET.get('page')
    try:
        posts_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        posts_page_obj = paginator.page(1)
    except EmptyPage:
        posts_page_obj = paginator.page(paginator.num_pages)

    context = {'posts': posts_page_obj, 'page_obj': posts_page_obj}
    
    return render(request, 'blog_app/post/list.html', context)


@csrf_exempt
@login_required
def like_post(request, username, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    user = request.user
    like_instance, created = Like.objects.get_or_create(post=post, user=user)

    if not created:
        like_instance.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})


def post_detail(request, username, slug):
    post = get_object_or_404(Post, author__username=username, slug=slug)
    comments = post.comments.all().order_by('created_at')
    comment_form = CommentForm()
    recently_viewed_posts_slugs = request.session.get('recently_viewed', [])

    user_to_detail = get_object_or_404(CustomUser, username=username)

    if not (request.user == user_to_detail or request.user.is_staff):
        messages.error(request, "sorry! you don't have permission for this!!!")
        if hasattr(request.user, 'id'):
             return redirect('blog_app:user_profile', request.user.username)
        return redirect('blog_app:post_list')

    if post.slug not in recently_viewed_posts_slugs:
        recently_viewed_posts_slugs.insert(0, post.slug)
        request.session['recently_viewed'] = recently_viewed_posts_slugs[:5] 

    recent_posts_objects = Post.objects.filter(
        slug__in=request.session.get('recently_viewed', []), 
        status='published'
    ).order_by('-created_at') 

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'recently_viewed_posts': recent_posts_objects,
        'username': username
    }
    return render(
        request,
        'blog_app/post/detail.html',
        context=context
    )


def search_results(request):
    search_form = SearchForm(request.GET)
    query = request.GET.get('q')
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(
        (Q(title__contains=query) | Q(content__contains=query)) & Q(status="published"))
        
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


@login_required
@permission_required('blog_app.create_comment', raise_exception=True)
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment was added successfully.')
            return redirect('blog_app:post_detail', username=post.author.username ,slug=post.slug)
        else:
            error_summary = []
            for field, errors in form.errors.items():
                label = field.capitalize() if field != '__all__' else 'Form'
                error_summary.append(f"{label}: {', '.join(errors)}")
            messages.error(request, f"Error! Please retry: {'; '.join(error_summary)}")
    else:
        form = CommentForm()

    return redirect('blog_app:post_detail', username=post.author.username, slug=post.slug)


