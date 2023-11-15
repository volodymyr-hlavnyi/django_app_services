import requests
import logging
from datetime import datetime
from celery import shared_task

from apps.services.models.currency import CurrencyRate, RefOfCurrency


@shared_task
def get_rate_currency_by_all():
    logger = logging.getLogger("django")
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url)

    if response.status_code == 200:
        exchange_rates = response.json()

        for selected_currency in RefOfCurrency.objects.all():
            logger.info(f"Start from {selected_currency.code} user {selected_currency.user}")
            currency_rate = None
            currency_date = None

            for currency in exchange_rates:
                currency_from_json = int(currency["r030"])

                if currency_from_json == int(selected_currency.code):
                    currency_rate = currency["rate"]
                    currency_date = datetime.strptime(currency["exchangedate"], "%d.%m.%Y")

                    check_qs = CurrencyRate.objects.filter(
                        currency=selected_currency, date=currency_date, user=selected_currency.user
                    )
                    if check_qs.count() > 0:
                        logger.info(
                            f"Currency rate for {selected_currency.code} "
                            f"is {currency_rate} on {currency_date} already exists"
                        )

                    else:
                        CurrencyRate(
                            currency=selected_currency,
                            rate=currency_rate,
                            date=currency_date,
                            user=selected_currency.user,
                        ).save()
                        logger.info(f"Save New to currency rate for {selected_currency.code} is {currency_rate}")
                        break

    return
