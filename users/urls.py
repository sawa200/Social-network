from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
