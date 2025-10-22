from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path('add/', views.add_event, name='add_event'),
    path("", views.events_list, name="events_list"),
    path("api/events/", views.events_api, name="events_api"),
    path("create/", views.event_create, name="event_create"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
    path("<int:event_id>/edit/", views.event_edit, name="event_edit"),
    path("<int:event_id>/delete/", views.event_delete, name="event_delete"),
]
