from django.contrib import admin
from blog_app.admin import BaseAdmin
from blog_app.models import Post
from blog_app.models import Like
from blog_app.models import Tag

 
@admin.register(Post)
class PostAdmin(BaseAdmin):
   list_display = ('title', 'author', 'status', 'is_published', 'created_at')
   search_fields = ('title', 'content', 'author')
   list_filter = ('status', 'tags', 'author')



@admin.register(Like)
class LikeAdmin(BaseAdmin):
    pass


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    pass
