from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# class CurrencyRate(models.Model):
#     currency_code = models.CharField(max_length=3, default="USD")
#     rate = models.DecimalField(max_digits=10, decimal_places=4)
#     date = models.DateTimeField(auto_now_add=True)


class CurrencyRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey("RefOfCurrency", on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} {self.currency} {self.rate}"


class RefOfCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=3, blank=False)
    # name_special = models.CharField(max_length=3)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Reference of Currencies"

    def __str__(self):
        return f"{self.name} ({self.code} )"
