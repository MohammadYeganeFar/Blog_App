from django.urls import path
from blog_app.views import post
from blog_app.views import user


urlpatterns = [
    path('posts/', post.list_post, name='list_post'),
    path('login/', user.custom_user_login, name='login')
]