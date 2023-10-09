from django.db import models

# from datetime import datetime

from django.contrib.auth import get_user_model

from apps.services.models.client import Client

User = get_user_model()


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField(blank=False, null=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    kind_of_service = models.ForeignKey("KindOfService", on_delete=models.CASCADE)
    time_hours = models.DecimalField(max_digits=4, decimal_places=2)

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

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        super().save()

        if Action.objects.filter(user=self.user, service=Service.objects.get(pk=self.pk), client=self.client).exists():
            pass
        else:
            Action.objects.create(
                user=self.user,
                service=Service.objects.get(pk=self.pk),
                client=self.client,
            )

    class Meta:
        ordering = ["-date", "date"]


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="Started")
    manually_closed = models.BooleanField(default=False)

    def close(self):
        self.status = "Closed"
        self.manually_closed = True
        super().save()

    def save(self, *args, **kwargs):
        super().save()
