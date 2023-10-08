# import requests

# :TODO: make function to get currency rate


def get_currency_rate():
    # url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    # response = requests.get(url)
    # exchange_rates = response.json()
    #
    # if response.status_code == 200:
    #     exchange_rates = response.json()
    #
    #     selected_currency = request.GET.get("currency", "USD")
    #
    #     for currency in exchange_rates:
    #         if currency["cc"] == selected_currency:
    #             currency_rate = currency["rate"]
    #             break
    # else:
    #     exchange_rates = None
    #
    #     return exchange_rates
    currency_rate = 37

    return currency_rate
