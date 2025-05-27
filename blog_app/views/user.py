from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from blog_app.models import CustomUser, Post
from blog_app.forms.user.login import CustomLoginForm
from blog_app.forms import UserProfile
from django.contrib import messages
from blog_app.forms.user_registration import UserRegistration
from django.contrib.auth.decorators import login_required


def user_register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('blog_app:list_post')
    
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Registration successful, {user.username}! You are now logged in.')
            return redirect('blog_app:list_post')
        
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
    
    return render(request, 'user/register.html', {'form': form})


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
                message = f'welcome {user.username}'
            else:
                message = 'wrong data!'
        else:
            message = 'wrong form!'
            
        context = {'form': form, 'message': message}   
        return render(request, 'user/custom_login.html', context=context) 
    
    form = CustomLoginForm()
    context = {'form': form}
    
    return render(request, 'user/custom_login.html', context=context) 


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    else:
        messages.info(request, "You are not currently logged in.")
    
    return redirect('blog_app:post_list')


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
    return render(request, 'user/profile_detail.html', context)


@login_required
def edit_profile(request, user_id):
    user_to_edit = get_object_or_404(CustomUser, pk=user_id)

    if not (request.user == user_to_edit or request.user.is_staff):
        messages.error(request, "sorry! you don't have permission for this!!!")
        if hasattr(request.user, 'id'):
             return redirect('blog_app:user_profile', user_id=request.user.id)
        return redirect('blog_app:list_post')

    if request.method == 'POST':
        form = UserProfile(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile updated successfully!')
            return redirect('blog_app:edit_profile', user_id=user_to_edit.id)
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
    return render(request, 'user/edit_profile.html', context)