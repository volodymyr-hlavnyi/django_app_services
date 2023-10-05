from django.contrib.auth.models import AbstractUser

# from apps.services.models.userprofile import UserProfile


class User(AbstractUser):
    pass


# def save(self, *args, **kwargs):
#     super().save(*args, **kwargs)
#     if not hasattr(self, "userprofile"):
#         UserProfile.objects.create(user=self)
