from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login # not yet added ours I add our login later
from django.contrib.auth import logout
from blog_app.models import CustomUser, Post



from django.contrib import messages
#from  blog_app.forms.user_registration import UserRegistration


# def user_register(request):
#     if request.user.is_authenticated:
#         messages.info(request, "You are already logged in.")
#         return redirect('blog_app:list_post')
    
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             messages.success(request, f'Registration successful, {user.username}! You are now logged in.')
#             return redirect('blog_app:list_post')
        
#         else:
#             error_messages = []
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     if field == '__all__':
#                          error_messages.append(f"{error}")
#                     else:
#                         error_messages.append(f"{form.fields[field].label or field.capitalize()}: {error}")
#             if error_messages:
#                  messages.error(request, "Please correct the errors below: " + "; ".join(error_messages))
#             else:
#                  messages.error(request, 'Please correct the errors.')


#     else:
#         form = UserRegisterForm()
    
#     return render(request, 'user/register.html', {'form': form}) # user/register.html will be added soon

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    else:
        messages.info(request, "You are not currently logged in.")
    
    return redirect('blog_app:list_post')

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