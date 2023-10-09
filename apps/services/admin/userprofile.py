from django.contrib import admin

from apps.services.models.userprofile import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",  # "user",
        "visual_theme",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "user",  # "user",
        "visual_theme",
        "created_at",
        "modified_at",
    )
