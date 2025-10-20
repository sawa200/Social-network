from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_list, name="chat_list"),
    path("<int:chat_id>/", views.chat_detail, name="chat_detail"),
    path("<int:chat_id>/send/", views.send_message, name="send_message"),
    path("private/", views.private_messages, name="private_messages"),
    path("private/<int:user_id>/send/", views.send_private_message, name="send_private_message"),
    path("private/<str:nickname>/", views.private_chat, name="private_chat")
    
]
