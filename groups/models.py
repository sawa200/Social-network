from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Group(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(
        User, related_name='created_groups', on_delete=models.CASCADE
    )
    admins = models.ManyToManyField(
        User, related_name='admin_groups', blank=True
    )
    members = models.ManyToManyField(
        User, related_name='group_memberships', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    require_approval = models.BooleanField(default=True)  # нужно ли одобрение перед вступлением

    def is_admin(self, user):
        return user == self.creator or user in self.admins.all()

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content[:20]}"


class GroupJoinRequest(models.Model):
    group = models.ForeignKey(Group, related_name='join_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.group.name}"
