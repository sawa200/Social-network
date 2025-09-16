from django.contrib import admin
from .models import FriendRequest

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'accepted', 'created_at')
