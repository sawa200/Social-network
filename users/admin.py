from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('nickname', 'email', 'avatar', 'is_staff', 'is_active')  # добавили nickname
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'password', 'avatar')}),  # добавили nickname
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('nickname', 'email')  # теперь можно искать по никнейму
    ordering = ('nickname', 'email')
    filter_horizontal = ()  

admin.site.register(CustomUser, CustomUserAdmin)
