from django.contrib import admin
from .models import Images, Post, SubPost


@admin.register(Post)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['created_at']


admin.site.register(SubPost)
admin.site.register(Images)
