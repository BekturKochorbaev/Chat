from django.contrib import admin
from .models import Slide

@admin.register(Slide)
class SlidetAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'title', 'created_at')
    search_fields = ('keyword', 'title')
    list_filter = ('created_at',)