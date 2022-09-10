from django.contrib import admin
from .models import Notes, Images


@admin.register(Notes)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'tags']
    search_fields = ['title']
    list_filter = ['title', 'owner']
    ordering = ['created_at']


admin.site.register(Images)
