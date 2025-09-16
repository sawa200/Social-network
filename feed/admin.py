from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # что показывать в списке
    search_fields = ('title', 'content', 'author__nickname')  # поиск
    list_filter = ('created_at',)
