from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.FileField(upload_to="videos/", blank=True, null=True)


    
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='liked_posts', 
        blank=True
    )
    
    
    
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
