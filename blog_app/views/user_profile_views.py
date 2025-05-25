from django.shortcuts import render, get_object_or_404
from blog_app.models import CustomUser, Post


def user_profile(request, user_id):
    profile_user = get_object_or_404(CustomUser, pk=user_id)
    user_posts = Post.objects.filter(
        author=profile_user,
        status='published'
        ).order_by('-created_at')

    context = {
    'profile_user': profile_user,
    'user_posts': user_posts,
    }
    return render(request, 'user/profile_detail.html', context) # I will add this 'user/profile_detail.html' later