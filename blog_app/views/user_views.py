from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from blog_app.forms.user.login import CustomLoginForm


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
            

