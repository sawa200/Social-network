from django.contrib import admin
from django.utils.html import format_html
from users.models import CustomUser
from .models import PrivateMessage

@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('sender__nickname', 'receiver__nickname', 'content')
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'email', 'private_chat_link')
    search_fields = ('nickname', 'email')

    def private_chat_link(self, obj):
        if obj.pk:
            return format_html(
                '<a class="button" href="/chat/private/{}/">💬 Личный чат</a>', obj.nickname
            )
        return "-"
    private_chat_link.short_description = "Личный чат"
    private_chat_link.allow_tags = True

admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
