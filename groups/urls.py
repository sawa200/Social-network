from django.urls import path
from . import views

app_name = "groups"

urlpatterns = [
    # 🔹 Основное
    path("", views.group_list, name="group_list"),
    path("create/", views.create_group, name="create_group"),
    path("<int:group_id>/", views.group_detail, name="group_detail"),
    path("check_new_messages/<int:group_id>/", views.check_new_messages, name="check_new_messages"),
    path('my/', views.my_groups, name='my_groups'),
    path('<int:group_id>/invite/', views.invite_to_group, name='invite_to_group'),
    # 🔹 Участие
    path("<int:group_id>/join/", views.join_group, name="join_group"),
    path("<int:group_id>/leave/", views.leave_group, name="leave_group"),
    path("<int:group_id>/send_message/", views.send_message, name="send_message"),

    # 🔹 Управление участниками и админами
    path("<int:group_id>/remove/<int:member_id>/", views.remove_member, name="remove_member"),
    path("<int:group_id>/add_admin/<int:member_id>/", views.add_admin, name="add_admin"),
    path("<int:group_id>/delete/", views.delete_group, name="delete_group"),
    path("<int:group_id>/remove_admin/<int:member_id>/", views.remove_admin, name="remove_admin"),
    path('group/<int:group_id>/message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('group/<int:group_id>/message/<int:message_id>/delete/', views.delete_message, name='delete_message'),

    # 🆕 Заявки на вступление
    path("<int:group_id>/request_join/", views.request_join_group, name="request_join_group"),
    path("approve/<int:request_id>/", views.approve_join_request, name="approve_join_request"),
]
