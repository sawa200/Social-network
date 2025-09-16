from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок поста'}),
            'content': forms.Textarea(attrs={'placeholder': 'Текст поста', 'rows':5}),
        }
