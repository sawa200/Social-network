from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message, PrivateMessage
from django.contrib.auth import get_user_model
from django.db.models import Q, Max

User = get_user_model()


@login_required
def chat_list(request):
    """Показывает список всех чатов пользователя"""
    chats = request.user.chats.all()
    return render(request, "chat/chat_list.html", {"chats": chats})


@login_required
def chat_detail(request, chat_id):
    """Открывает конкретный чат"""
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all().order_by("timestamp")
    return render(request, "chat/chat_detail.html", {"chat": chat, "messages": messages})


@login_required
def send_message(request, chat_id):
    """Отправка сообщения в чат"""
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)
    return redirect("chat:chat_detail", chat_id=chat.id)


@login_required
def private_messages(request):
    # Берем всех пользователей, с кем у текущего есть переписка
    chats = (
        PrivateMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .values('sender', 'receiver')
        .annotate(last_message_time=Max('created_at'))
        .order_by('-last_message_time')
    )

    # Собираем список собеседников
    partners = set()
    for chat in chats:
        if chat['sender'] != request.user.id:
            partners.add(chat['sender'])
        if chat['receiver'] != request.user.id:
            partners.add(chat['receiver'])

    users = User.objects.filter(id__in=partners)

    return render(request, "chat/private_messages.html", {"users": users})
@login_required
def send_private_message(request, user_id):
    """Отправка личного сообщения"""
    receiver = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            PrivateMessage.objects.create(sender=request.user, receiver=receiver, content=content)
    return redirect("chat:private_messages")
@login_required
def private_chat(request, nickname):
    other_user = get_object_or_404(User, nickname=nickname)
    messages = PrivateMessage.objects.filter(
        Q(sender=request.user, receiver=other_user)
        | Q(sender=other_user, receiver=request.user)
    ).order_by("created_at")

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            PrivateMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect("chat:private_chat", nickname=other_user.nickname)

    return render(request, "chat/private_chat.html", {
        "other_user": other_user,
        "messages": messages
    })

