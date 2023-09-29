from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.services.models import Client, KindOfService, Service


class User(AbstractUser):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    kind_of_service = models.ForeignKey(KindOfService, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
