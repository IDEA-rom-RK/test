from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)
    other_interests = models.TextField(blank=True)
    interests = models.JSONField(default=dict, blank=True)
    search_goals = models.JSONField(default=list, blank=True)
    important = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.user.username
