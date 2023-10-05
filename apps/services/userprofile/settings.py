from apps.services.models.userprofile import UserProfile


def get_user_theme(user_id: int) -> str:
    if user_id is None:
        thema = "light"
    else:
        userprofile = UserProfile.objects.get(user_id=user_id)
        thema = userprofile.visual_theme

    return thema
