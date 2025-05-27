from django.contrib import admin
from blog_app.admin import BaseAdmin
from blog_app.models import Post
from blog_app.models import Like
from blog_app.models import Tag

 
@admin.register(Post)
class PostAdmin(BaseAdmin):
   list_display = ('title', 'author', 'status', 'created_at')
   search_fields = ('title', 'content', 'author')
   list_filter = ('status', 'tags', 'author')



@admin.register(Like)
class LikeAdmin(BaseAdmin):
    list_display = ('user', 'post')
    search_fields = ('user', 'post')
    list_filter = ('user',)


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)
    list_filter = ('tag_name',)
    
    
