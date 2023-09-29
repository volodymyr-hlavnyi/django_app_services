from django import forms

# from django.template.context_processors import request

from .models import Client, KindOfService, Service
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.users.models import User


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
        fields = ["client", "kind_of_service", "time_hours", "date"]


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
