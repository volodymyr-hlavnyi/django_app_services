from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visual_theme = models.CharField(
        max_length=20,
        choices=(
            ("light", "Light mode"),
            ("dark", "Dark mode"),
        ),
        default="light",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False,
    )

    # def __str__(self):
    #     return self.user
