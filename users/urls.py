from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

app_name = "users"

urlpatterns = [
    # Аутентификация
    path("login/", auth_views.LoginView.as_view(
        template_name="users/login.html",
        authentication_form=CustomAuthenticationForm
    ), name="login"),

    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register, name="register"),

    # Профили
    path("profile/", views.profile, name="profile"),
    path("profile/<int:user_id>/", views.user_profile, name="user_profile"),
    path('profile/<int:user_id>/friends/', views.user_friends, name='user_friends'),
    path("profile/<int:user_id>/friends/", views.user_friends, name="user_friends"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # Друзья
    path("friends/", views.friends_list, name="friends_list"),
    path("friends/add/<int:user_id>/", views.add_friend, name="add_friend"),
    path("friends/accept/<int:request_id>/", views.accept_friend, name="accept_friend"),
    path("friends/delete/<int:request_id>/", views.delete_friend_request, name="delete_friend_request"),
    
]
