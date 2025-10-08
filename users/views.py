from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, Q
from .forms import CustomUserCreationForm, AvatarForm
from .models import FriendRequest

User = get_user_model()


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно! Войдите в аккаунт.")
            return redirect('users:login')
        else:
            messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Профиль текущего пользователя"""
    posts = request.user.post_set.all()
    total_likes = posts.aggregate(total=Count("likes"))["total"] or 0

    # Форма для загрузки аватара
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Аватар успешно обновлен!")
            return redirect('users:profile')
    else:
        form = AvatarForm(instance=request.user)

    return render(request, "users/profile.html", {
        "total_likes": total_likes,
        "posts": posts,
        "form": form,
        "avatar_url": request.user.avatar.url if request.user.avatar else "/static/default_avatar.png"
    })


@login_required
def edit_profile(request):
    """Редактирование профиля и аватара"""
    user = request.user
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен!")
            return redirect('users:profile')
    else:
        form = AvatarForm(instance=user)

    return render(request, "users/edit_profile.html", {"form": form})


def user_profile(request, user_id):
    """Профиль другого пользователя"""
    profile_user = get_object_or_404(User, id=user_id)

    total_posts = profile_user.post_set.count()
    total_likes = profile_user.post_set.aggregate(total_likes=Count("likes"))["total_likes"] or 0
    total_friends = FriendRequest.objects.filter(
        accepted=True
    ).filter(
        Q(from_user=profile_user) | Q(to_user=profile_user)
    ).count()

    return render(request, "users/user_profile.html", {
        "profile_user": profile_user,
        "total_posts": total_posts,
        "total_likes": total_likes,
        "total_friends": total_friends,
        "avatar_url": profile_user.avatar.url if profile_user.avatar else "/static/default_avatar.png"
    })


@login_required
def add_friend(request, user_id):
    """Отправить заявку в друзья"""
    friend = get_object_or_404(User, id=user_id)

    if friend == request.user:
        messages.error(request, "Нельзя добавить себя в друзья 🙃")
        return redirect("users:user_profile", user_id=user_id)

    existing_request = FriendRequest.objects.filter(
        from_user=request.user, to_user=friend
    ).first()
    reverse_request = FriendRequest.objects.filter(
        from_user=friend, to_user=request.user
    ).first()

    if existing_request or reverse_request:
        messages.info(request, "Заявка уже существует.")
        return redirect("users:user_profile", user_id=user_id)

    FriendRequest.objects.create(from_user=request.user, to_user=friend)
    messages.success(request, f"Заявка отправлена пользователю {friend.email}")
    return redirect("users:user_profile", user_id=user_id)


@login_required
def accept_friend(request, request_id):
    """Принять заявку в друзья"""
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.accepted = True
    fr.save()
    messages.success(request, f"Вы приняли заявку от {fr.from_user.email}")
    return redirect("users:friends_list")


@login_required
def delete_friend_request(request, request_id):
    """Удалить заявку (входящую или исходящую)"""
    fr = get_object_or_404(FriendRequest, id=request_id)

    if fr.from_user == request.user or fr.to_user == request.user:
        fr.delete()
        messages.success(request, "Заявка удалена")
    else:
        messages.error(request, "Вы не можете удалить эту заявку")
    return redirect("users:friends_list")


@login_required
def friends_list(request):
    """Список друзей и заявок"""
    accepted_requests = FriendRequest.objects.filter(
        accepted=True
    ).filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    )

    friends_ids = set()
    for fr in accepted_requests:
        if fr.from_user == request.user:
            friends_ids.add(fr.to_user.id)
        else:
            friends_ids.add(fr.from_user.id)

    friends = User.objects.filter(id__in=friends_ids)

    incoming_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    outgoing_requests = FriendRequest.objects.filter(from_user=request.user, accepted=False)

    return render(request, "users/friends_list.html", {
        "friends": friends,
        "incoming_requests": incoming_requests,
        "outgoing_requests": outgoing_requests,
    })


@login_required
def user_friends(request, user_id):
    """Друзья другого пользователя + общие друзья"""
    user = get_object_or_404(User, id=user_id)

    accepted_requests = FriendRequest.objects.filter(accepted=True).filter(
        Q(from_user=user) | Q(to_user=user)
    )

    friends_ids = set()
    for fr in accepted_requests:
        if fr.from_user == user:
            friends_ids.add(fr.to_user.id)
        else:
            friends_ids.add(fr.from_user.id)

    friends = User.objects.filter(id__in=friends_ids)

    my_friends_reqs = FriendRequest.objects.filter(accepted=True).filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    )
    my_friends_ids = set()
    for fr in my_friends_reqs:
        if fr.from_user == request.user:
            my_friends_ids.add(fr.to_user.id)
        else:
            my_friends_ids.add(fr.from_user.id)

    mutual_friends = friends.filter(id__in=my_friends_ids)

    return render(request, "users/user_friends.html", {
        "profile_user": user,
        "friends": friends,
        "mutual_friends": mutual_friends
    })
