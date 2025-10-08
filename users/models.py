from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.conf import settings

# Модель для заявок в друзья
class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_friend_requests",  # уникальное имя
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_friend_requests",  # уникальное имя
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({'Принято' if self.accepted else 'Ожидание'})"

# Модель дружбы (для истории принятых друзей)
class Friendship(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friendships_sent",
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friendships_received",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user") 

    def __str__(self):
        return f"{self.from_user} ➝ {self.to_user}"

# Менеджер для кастомного пользователя
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Кастомная модель пользователя
class CustomUser(AbstractBaseUser, PermissionsMixin): 
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'nickname'  
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nickname or self.email
