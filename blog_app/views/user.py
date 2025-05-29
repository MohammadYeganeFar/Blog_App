from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth import logout, authenticate, login
from blog_app.models import CustomUser, Post
from blog_app.forms.user import CustomLoginForm
from blog_app.forms import UserProfile
from django.contrib import messages
from blog_app.forms.user import UserRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.conf import settings


def user_register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('blog_app:post_list')

    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Registration successful, {user.username}! You are now logged in.')
            return redirect('blog_app:post_list')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        error_messages.append(f"{error}")
                    else:
                        error_messages.append(f"{form.fields[field].label or field.capitalize()}: {error}")
            if error_messages:
                messages.error(request, "Please correct the errors below: " + "; ".join(error_messages))
            else:
                messages.error(request, 'Please correct the errors.')
    else:
        form = UserRegistration()

    return render(request, 'registration/signup.html', {'form': form})


def custom_user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)            
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
            request=request,
            username=username,
            password=password
            )
            if user :
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
                message = f'welcome {user.username}'
            else:
                message = 'wrong data!'
        else:
            message = 'wrong form!'
            
        context = {'form': form, 'message': message}   
        return render(request, 'blog_app/user/custom_login.html', context=context) 
    
    form = CustomLoginForm()
    context = {'form': form}
    
    return render(request, 'blog_app/user/custom_login.html', context=context) 


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    else:
        messages.info(request, "You are not currently logged in.")
    
    return redirect('blog_app:post_list')


def user_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    user_posts = Post.objects.filter(
        author=profile_user,
        ).order_by('-created_at')

    context = {
    'profile_user': profile_user,
    'user_posts': user_posts,
    }
    return render(request, 'blog_app/user/user_profile.html', context)


@login_required
def edit_profile(request, username):
    user_to_edit = get_object_or_404(CustomUser, username=username)

    if not (request.user == user_to_edit or request.user.is_staff):
        messages.error(request, "sorry! you don't have permission for this!!!")
        if hasattr(request.user, 'id'):
             return redirect('blog_app:user_profile', request.user.username)
        return redirect('blog_app:post_list')

    if request.method == 'POST':
        form = UserProfile(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            new_username = form.cleaned_data['username']
            messages.success(request, 'Your profile updated successfully!')
            return redirect('blog_app:user_profile', username=new_username)
        else:
            error_list = []
            for field, errors in form.errors.items():
                error_list.append(f"{field.capitalize()}: {', '.join(errors)}")
            messages.error(request, f"Please fix errors: {'; '.join(error_list)}")
    else:
        form = UserProfile(instance=user_to_edit)

    context = {
        'form': form,
        'profile_user': user_to_edit
    }
    return render(request, 'blog_app/user/user_profile_form.html', context)