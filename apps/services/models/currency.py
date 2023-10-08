from django.db import models


class CurrencyRate(models.Model):
    currency_code = models.CharField(max_length=3, default="USD")
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateTimeField(auto_now_add=True)
