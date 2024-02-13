from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish',)
    list_filter = ('title',)
    search_fields = ('title', 'is_publish',)
    prepopulated_fields = {'slug': ('title',)}
