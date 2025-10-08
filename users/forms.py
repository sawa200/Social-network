from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='🔒 Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='🔒 Повтор пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ('nickname', 'email')
        widgets = {
            'nickname': forms.TextInput(attrs={'placeholder': 'Ваш никнейм 🌟'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email 📧'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if not p1 or not p2:
            raise forms.ValidationError("Оба поля пароля обязательны ⚠️")
        if p1 != p2:
            raise forms.ValidationError("Пароли не совпадают ❌")
        return p2

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("Этот никнейм уже занят 😢")
        return nickname

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class AvatarForm (forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Никнейм", widget=forms.TextInput(attrs={'placeholder': 'Ваш никнейм 🌟'}))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ['nickname', 'avatar']


