from django import forms

from .models.client import Client
from .models.kindofservice import KindOfService
from .models.service import Service
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.users.models import User
from .models.userprofile import UserProfile


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name"]


class KindOfServiceForm(forms.ModelForm):
    class Meta:
        model = KindOfService
        fields = ["name"]


# @login_required
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["date", "client", "kind_of_service", "time_hours"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(user=self.instance.user_id)
        self.fields["kind_of_service"].queryset = KindOfService.objects.filter(user=self.instance.user_id)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["visual_theme"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["user"].queryset = User.objects.filter(id=self.instance.id)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
