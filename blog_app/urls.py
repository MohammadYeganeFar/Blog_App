from django.urls import path
from blog_app.views import post
from blog_app.views import user


urlpatterns = [
    path('posts/', post.post_list, name='post_list'),
    path('login/', user.custom_user_login, name='login')
]