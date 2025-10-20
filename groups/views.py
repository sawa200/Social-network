from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, GroupMessage, GroupJoinRequest
from users.models import CustomUser

# 🔹 Список всех групп
@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, "groups/group_list.html", {"groups": groups})

# 🔹 Детальная страница группы с чатами
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = group.members.all()

    is_creator = request.user == group.creator
    is_admin = request.user in group.admins.all()
    user_can_manage = is_creator or is_admin

    # Заявки на вступление, которые ещё не одобрены
    pending_requests = group.join_requests.filter(approved=False)

    return render(request, 'groups/group_detail.html', {
        'group': group,
        'members': members,
        'is_creator': is_creator,
        'is_admin': is_admin,
        'user_can_manage': user_can_manage,
        'pending_requests': pending_requests,  # передаём в шаблон
    })


# 🔹 Создание новой группы
@login_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            group = Group.objects.create(name=name, creator=request.user)
            group.members.add(request.user)
            return redirect("groups:group_detail", group_id=group.id)
    return render(request, "groups/create_group.html")

# 🔹 Присоединение к группе
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    return redirect("groups:group_detail", group_id=group.id)

# 🔹 Выход из группы
@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user in group.members.all() and request.user != group.creator:
        group.members.remove(request.user)
    return redirect("groups:group_detail", group_id=group.id)

# 🔹 Удаление пользователя из группы (только админ/создатель)
@login_required
def remove_member(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user == group.creator or request.user in group.admins.all():
        member = get_object_or_404(CustomUser, id=member_id)
        if member != group.creator:
            group.members.remove(member)
    return redirect("groups:group_detail", group_id=group.id)

# 🔹 Назначение админа (только создатель)
@login_required
def add_admin(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user == group.creator:
        member = get_object_or_404(CustomUser, id=member_id)
        group.admins.add(member)
    return redirect("groups:group_detail", group_id=group.id)

# 🔹 Удаление админа (только создатель)
@login_required
def remove_admin(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user == group.creator:
        member = get_object_or_404(CustomUser, id=member_id)
        group.admins.remove(member)
    return redirect("groups:group_detail", group_id=group.id)

# 🔹 Удаление группы (только создатель)
@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user == group.creator:
        group.delete()
    return redirect("groups:group_list")

# 🔹 Отправка сообщения
@login_required
def send_message(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            GroupMessage.objects.create(
                group=group,
                author=request.user,
                content=content
            )
    return redirect("groups:group_detail", group_id=group.id)

# 🔹 Редактирование сообщения
@login_required
def edit_message(request, group_id, message_id):
    message = get_object_or_404(GroupMessage, id=message_id, group_id=group_id)
    if request.user != message.author:
        return redirect("groups:group_detail", group_id=group_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            message.content = content
            message.save()
            return redirect("groups:group_detail", group_id=group_id)
    return render(request, "groups/edit_message.html", {"message": message})

# 🔹 Удаление сообщения
@login_required
def delete_message(request, group_id, message_id):
    message = get_object_or_404(GroupMessage, id=message_id, group_id=group_id)
    group = message.group
    if request.user == message.author or request.user == group.creator or request.user in group.admins.all():
        message.delete()
    return redirect("groups:group_detail", group_id=group_id)

# 🔹 Создание заявки на вступление
@login_required
def request_join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        GroupJoinRequest.objects.get_or_create(group=group, user=request.user)
    return redirect("groups:group_detail", group_id=group.id)

# 🔹 Одобрение заявки на вступление
@login_required
def approve_join_request(request, request_id):
    join_request = get_object_or_404(GroupJoinRequest, id=request_id)
    group = join_request.group
    if request.user == group.creator or request.user in group.admins.all():
        join_request.approved = True
        join_request.save()
        group.members.add(join_request.user)
    return redirect("groups:group_detail", group_id=group.id)
