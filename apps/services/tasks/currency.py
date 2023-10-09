from celery import Celery
import requests
import os
import django

from apps.services.models.currency import CurrencyRate

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

app = Celery("myapp", broker="redis://localhost:6379/0")


@app.task
def fetch_currency():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url)

    if response.status_code == 200:
        exchange_rates = response.json()

        selected_currency = "USD"
        currency_rate = None

        for currency in exchange_rates:
            if currency["cc"] == selected_currency:
                currency_rate = currency["rate"]
                break

        if currency_rate is not None:
            rate_entry = CurrencyRate(currency_code=selected_currency, rate=currency_rate)
            rate_entry.save()
