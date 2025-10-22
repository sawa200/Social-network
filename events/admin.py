# events/admin.py
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'creator', 'all_day')  # колонки в списке
    list_filter = ('start', 'creator', 'all_day')                   # фильтры справа
    search_fields = ('title', 'description', 'location')           # поиск
    ordering = ('start',)                                           # сортировка
