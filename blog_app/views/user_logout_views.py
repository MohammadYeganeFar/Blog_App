from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    else:
        messages.info(request, "You are not currently logged in.")
    
    return redirect('blog_app:list_post')
