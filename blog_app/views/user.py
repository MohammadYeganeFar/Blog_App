from django.shortcuts import render, redirect
from django.contrib.auth import login # not yet added ours I add our login later
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