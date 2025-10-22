from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def default_now():
    return timezone.now()
class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=250, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_events")
    created_at = models.DateTimeField(default=default_now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start"]

    def __str__(self):
        return f"{self.title} ({self.start:%Y-%m-%d %H:%M})"
