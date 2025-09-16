from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.friend_requests, name='friend_requests'),
]
