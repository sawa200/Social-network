from django.db import models
from users.models import CustomUser

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({'Accepted' if self.accepted else 'Pending'})"
