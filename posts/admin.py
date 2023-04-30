from django.contrib import admin
from .models import Folder, Images, Post


@admin.register(Post)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    list_filter = ['title']
    ordering = ['created_at']


admin.site.register(Folder)
admin.site.register(Images)
