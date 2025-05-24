from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    
    list_display = []
    list_filter = []
    search_fields = []
    