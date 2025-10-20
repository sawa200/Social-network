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

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Аватар успешно обновлён!")
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
            messages.success(request, "Профиль обновлён!")
            return redirect('users:profile')
    else:
        form = AvatarForm(instance=user)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def user_profile(request, user_id):
    """Профиль другого пользователя"""
    profile_user = get_object_or_404(User, id=user_id)
    total_posts = profile_user.post_set.count()
    total_likes = profile_user.post_set.aggregate(total_likes=Count("likes"))["total_likes"] or 0

    accepted_requests = FriendRequest.objects.filter(
        accepted=True
    ).filter(Q(from_user=profile_user) | Q(to_user=profile_user))
    total_friends = accepted_requests.count()

    followers = profile_user.followers.all()
    following = profile_user.following.all()
    total_followers = followers.count()
    total_following = following.count()

    is_subscribed = request.user.following.filter(id=profile_user.id).exists()

    return render(request, "users/user_profile.html", {
        "profile_user": profile_user,
        "total_posts": total_posts,
        "total_likes": total_likes,
        "total_friends": total_friends,
        "followers": followers,
        "following": following,
        "total_followers": total_followers,
        "total_following": total_following,
        "is_subscribed": is_subscribed,
    })


@login_required
def add_friend(request, user_id):
    """Отправить заявку в друзья"""
    friend = get_object_or_404(User, id=user_id)

    if friend == request.user:
        messages.error(request, "Нельзя добавить себя в друзья 🙃")
        return redirect("users:user_profile", user_id=user_id)

    existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=friend).first()
    reverse_request = FriendRequest.objects.filter(from_user=friend, to_user=request.user).first()

    if existing_request or reverse_request:
        messages.info(request, "Заявка уже существует.")
        return redirect("users:user_profile", user_id=user_id)

    FriendRequest.objects.create(from_user=request.user, to_user=friend)
    messages.success(request, f"Заявка отправлена пользователю {friend.nickname or friend.email}")
    return redirect("users:user_profile", user_id=user_id)


@login_required
def accept_friend(request, request_id):
    """Принять заявку в друзья"""
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.accepted = True
    fr.save()
    messages.success(request, f"Вы приняли заявку от {fr.from_user.nickname or fr.from_user.email}")
    return redirect("users:friends_list")


@login_required

def delete_friend_request(request, request_id):
    friend_request = FriendRequest.objects.filter(
        id=request_id
    ).filter(
        to_user=request.user
    ).first()

    if not friend_request:
        messages.error(request, "Эта заявка уже удалена или не существует.")
        return redirect('friends_list')

    friend_request.delete()
    messages.success(request, "Заявка успешно удалена.")
    return redirect('friends_list')



@login_required
def delete_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    
    
    frs = FriendRequest.objects.filter(
        accepted=True
    ).filter(
        (Q(from_user=request.user) & Q(to_user=friend)) |
        (Q(from_user=friend) & Q(to_user=request.user))
    )

    if frs.exists():
        frs.delete()  
        messages.success(request, f"{friend.nickname or friend.email} видалений із друзів")
    else:
        messages.error(request, "Цей користувач не є вашим другом")
    return redirect("users:friends_list")



@login_required
def friends_list(request):
    """Список друзей и заявок"""
    accepted_requests = FriendRequest.objects.filter(
        accepted=True
    ).filter(Q(from_user=request.user) | Q(to_user=request.user))

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

    accepted_requests = FriendRequest.objects.filter(
        accepted=True
    ).filter(Q(from_user=user) | Q(to_user=user))

    friends_ids = set()
    for fr in accepted_requests:
        if fr.from_user == user:
            friends_ids.add(fr.to_user.id)
        else:
            friends_ids.add(fr.from_user.id)
    friends = User.objects.filter(id__in=friends_ids)

    my_friends_reqs = FriendRequest.objects.filter(
        accepted=True
    ).filter(Q(from_user=request.user) | Q(to_user=request.user))
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


@login_required
def subscribe(request, user_id):
    """Подписаться на пользователя"""
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "Нельзя подписаться на себя!")
        return redirect('users:user_profile', user_id=user_id)

    target_user.followers.add(request.user)
    messages.success(request, f"Вы подписались на {target_user.nickname or target_user.email}")
    return redirect('users:user_profile', user_id=user_id)


@login_required
def unsubscribe(request, user_id):
    """Отписаться от пользователя"""
    target_user = get_object_or_404(User, id=user_id)
    target_user.followers.remove(request.user)
    messages.success(request, f"Вы отписались от {target_user.nickname or target_user.email}")
    return redirect('users:user_profile', user_id=user_id)
