from django import forms
from .models import Client, KindOfService, Service
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name"]


class KindOfServiceForm(forms.ModelForm):
    class Meta:
        model = KindOfService
        fields = ["name"]


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["client", "kind_of_service", "time_hours", "date"]


class SignupForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, help_text="Required. Enter your full name.")

    class Meta:
        model = User
        fields = ("name", "username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
