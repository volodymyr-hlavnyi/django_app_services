from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visual_theme = models.CharField(
        max_length=20,
        choices=(
            ("light", "light theme"),
            ("dark", "Dark theme"),
        ),
        default="light",
    )

    def __str__(self):
        return self.name
