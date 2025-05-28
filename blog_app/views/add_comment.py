from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from blog_app.models import Post
from blog_app.forms import CommentForm

@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        messages.success(request, 'Your comment added successfully.')
    else:
        error_summary = []
        for field, errors in form.errors.items():
            if field != '__all__':
                label = field.capitalize() 
            else:
                label = "Form"
            error_summary.append(f"{label}: {', '.join(errors)}")
        messages.error(request, f"error! please retry if you want: {' '.join(error_summary)}")

    return redirect('blog_app:post_detail', username=post.author.username, slug=post.slug)
