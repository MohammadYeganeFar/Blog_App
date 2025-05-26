from django.contrib import admin
from blog_app.admin import BaseAdmin
from blog_app.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseAdmin):
    pass