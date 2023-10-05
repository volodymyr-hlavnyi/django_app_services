from apps.services.models.userprofile import UserProfile


def get_user_theme(user_id: int) -> str:
    userprofile = UserProfile.objects.get(user_id=user_id)
    return userprofile.visual_theme
