from django import forms
from .models import Post
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Напишите комментарий...'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image',"video",  'youtube_url']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Можно загружать только изображения (JPG, PNG, GIF).")
        return image
    def clean_video(self):
        video = self.cleaned_data.get("video")
        if video:
            allowed_types = ["video/mp4", "video/avi", "video/mpeg"]
            if video.content_type not in allowed_types:
                raise forms.ValidationError("Можно загружать только видео (mp4, avi, mpeg)")
        return video

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/zip',
                'text/plain'
            ]
            if file.content_type not in allowed_types:
                raise forms.ValidationError("Недопустимый тип файла. Разрешены PDF, DOC/DOCX, ZIP, TXT.")
        return file

    def clean_youtube_url(self):
        url = self.cleaned_data.get('youtube_url')
        if url and not ("youtube.com" in url or "youtu.be" in url):
            raise forms.ValidationError("Введите корректную ссылку на YouTube.")
        return url
