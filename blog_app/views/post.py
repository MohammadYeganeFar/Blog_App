from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from blog_app.models import Post, Like
from blog_app.forms.search import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse
from blog_app.models import Tag
from blog_app.forms.post import PostForm




def clean_tags(tag_string):
    return [tag.strip() for tag in tag_string.split(',') if tag.strip()]

def set_tags(tags_list, post):
    tags_objects = []
    print(f"tags_list: {tags_list}\n\nclean_tags_list: {tags_list}")
    for tag_name in tags_list:
        tag_object, created = Tag.objects.get_or_create(tag_name=tag_name)
        tags_objects.append(tag_object)
    print(f'tags_objects: {tags_objects}')
    post.tags.set(tags_objects)

@permission_required('blog_app.publish_post')
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            # here we are adding tags to the post
            user_tags = form.cleaned_data['tags']
            clean_tags_list = clean_tags(user_tags)
            set_tags(clean_tags_list, post)
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
                {'form': form}
            )
    else:
        form = PostForm()
        return render(
            request,
            'blog_app/post/create.html',
            {'form': form}
        )

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        
        if form.is_valid():
            post = form.save(commit=False)
            # here we are adding tags to the post
            user_tags = form.cleaned_data['tags']
            clean_tags_list = clean_tags(user_tags)
            set_tags(clean_tags_list, post)
            post.save()
            # I always forget "returen" in "return redirect"
            return redirect(reverse('blog_app:post_detail', args=[user.username, post.slug]))
        else:
            return render(
                request,
                'blog_app/post/create.html',
                {'form': form}
            )
    else:
        form = PostForm(instance=post)
        return render(
                request,
                'blog_app/post/create.html',
                {'form': form}
            )
        
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
        posts = Post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
        
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
