from django.urls import path
from blog_app.views import post
from blog_app.views import user


urlpatterns = [
    path('posts/', post.post_list, name='post_list'),
    path('login/', user.custom_user_login, name='login'),
    path('@<str:user>/<slug:slug>/', post.post_detail, name='post_detail'),
    path('new/', post.create_post, name='create_post'),
    path('<slug:slug>/edit/', post.edit_post, name='edit_post')
]