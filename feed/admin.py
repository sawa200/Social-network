from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    """Позволяет видеть и редактировать комментарии прямо в посте"""
    model = Comment
    extra = 0  # не добавлять пустые строки
    readonly_fields = ('author', 'content', 'created_at')  # чтобы нельзя было менять автора
    can_delete = True  # разрешаем удаление комментариев


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content', 'author__nickname')
    list_filter = ('created_at',)
    inlines = [CommentInline]  # вот тут добавляем комментарии


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('author__nickname', 'content')
    list_filter = ('created_at',)
