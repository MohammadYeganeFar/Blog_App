from django.urls import path
from blog_app.views import post_views


urlpatterns = [
    path('posts/', post.list_post, name='list_post')
]