from django.contrib.auth import get_user_model
from django.db import models
# from django.utils import timezone
from datetime import timedelta, datetime

User = get_user_model()


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

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
        return self.name

    class Meta:
        ordering = ["-modified_at", "name"]


class KindOfService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

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
        return self.name

    class Meta:
        ordering = ["-modified_at", "name"]


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
        return self.date

    def save(self, *args, **kwargs):
        super().save()

        Action.objects.create(
            user=self.user,
            service=Service.objects.get(pk=self.pk),
            client=self.client,
        )

    class Meta:
        ordering = ["-date", "date"]


class CurrencyRate(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class UserProfile(models.Model):
#     #user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Started')
    manually_closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        current_date = datetime.now()

        if not self.manually_closed:
            # if current_date >= self.service.date + self.service.time_hours:
            if current_date: # >= self.service.date + timedelta(days=1):
                self.status = 'Expired'
        else:
            self.status = 'Closed'

        super().save()
