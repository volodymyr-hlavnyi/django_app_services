import requests

url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

response = requests.get(url)

if response.status_code == 200:
    exchange_rates = response.json()

    usd_rate = None
    eur_rate = None
    for currency in exchange_rates:
        if currency["cc"] == "USD":
            usd_rate = currency["rate"]
        elif currency["cc"] == "EUR":
            eur_rate = currency["rate"]

    if usd_rate and eur_rate:
        print(f"Курс доллара (USD): {usd_rate}")
        print(f"Курс евро (EUR): {eur_rate}")
    else:
        print("Курсы валют не найдены")
else:
    print("Не удалось получить доступ к API")
