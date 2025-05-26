from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blog_app.models import CustomUser
from blog_app.forms import UserProfile


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