from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from blog_app.models import Post
from blog_app.forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect


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
