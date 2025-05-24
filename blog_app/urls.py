from django.urls import path
from blog_app.views import post_views, user_views


urlpatterns = [
    path('posts/', post_views.list_post, name='list_post'),
    path('login/', user_views.custom_user_login, name='login')
]