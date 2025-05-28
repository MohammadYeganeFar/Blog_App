from django.urls import path
from blog_app.views import post
from blog_app.views import user
from blog_app.views.add_comment import add_comment
from blog_app.views.contact_views import contact_view


app_name = 'blog_app'

urlpatterns = [
    path('', post.post_list, name='post_list'),
    path('@<str:username>/<slug:slug>/like/', post.like_post, name='like_post'),
    path('account/signup/', user.user_register, name='signup'),
    path('account/@<str:username>/', user.user_profile, name='user_profile'),
    path('account/@<str:username>/edit/', user.edit_profile, name='edit_profile'),
    path('account/login/', user.custom_user_login, name='login'),
    path('search', post.search_results, name='search_results'),
    path('account/logout/', user.user_logout, name='logout'),
    path('contact/',contact_view, name='contact_view'),
    path('@<str:username>/<slug:slug>/', post.post_detail, name='post_detail'),
    path('new/', post.create_post, name='create_post'),
    path('<slug:slug>/edit/', post.edit_post, name='edit_post'),
    path('<slug:slug>/add_comment/', add_comment, name='add_comment'),
    ]
