from apps.services.models.currency import CurrencyRate


def get_currency_rate(currency, user, date):
    """
    Get currency rate from database
    """
    currency_rate = CurrencyRate.objects.filter(currency=currency, date=date, user=user).first()
    return currency_rate.rate
