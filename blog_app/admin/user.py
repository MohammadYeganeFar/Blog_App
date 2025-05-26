from django.contrib import admin
from blog_app.admin import BaseAdmin
from blog_app.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseAdmin):
    list_display = ('user_name', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined', 'is_active' )
    search_fields = ('user_name', 'first_name__icontains', 'last_name__icontains', 'email', 'date_joined', 'is_active')  
    list_filter = ('is_staff', 'date_joined', 'is_active')
