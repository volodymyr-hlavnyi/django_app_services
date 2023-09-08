from django import forms
from .models import Client, KindOfService, Service


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
