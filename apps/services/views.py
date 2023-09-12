from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.services.models import Client, KindOfService, Service
from apps.services.forms import ClientForm, KindOfServiceForm

import requests
def home(request):
    return render(request, "services/home.html")

def currency_view(request):
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url)

    if response.status_code == 200:
        exchange_rates = response.json()

        # Получите список всех доступных валют
        available_currencies = [currency["cc"] for currency in exchange_rates]

        selected_currency = request.GET.get("currency", "USD")  # По умолчанию USD

        # Проверьте, выбрана ли валюта из списка доступных
        if selected_currency not in available_currencies:
            return render(request, "services/currency_template.html", {"error_message": "Выбранной валюты нет в списке"})

        currency_rate = None

        for currency in exchange_rates:
            if currency["cc"] == selected_currency:
                currency_rate = currency["rate"]
                break

        if currency_rate is not None:
            context = {
                "available_currencies": available_currencies,
                "selected_currency": selected_currency,
                "currency_rate": currency_rate,
            }
            return render(request, "services/currency_template.html", context)
        else:
            return render(request, "services/currency_template.html", {"error_message": "Курс валюты не найден"})
    else:
        return render(request, "services/currency_template.html", {"error_message": "Не удалось получить доступ к API"})


def client_edit(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("services:client_list")
    else:
        form = ClientForm(instance=client)

    return render(request, "services/client_edit.html", {"form": form, "client": client})


def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == "POST":
        client.delete()
        return redirect("services:client_list")

    return render(request, "services/client_delete.html", {"client": client})


class ClientsCreateView(CreateView):
    model = Client
    fields = ("name",)
    success_url = reverse_lazy("services:client_list")


class ClientListView(ListView):
    model = Client
    context_object_name = "client_list"


class KindOfServiceListView(ListView):
    model = KindOfService
    context_object_name = "kindofservice_list"


class KindOfServiceCreateView(CreateView):
    model = KindOfService
    fields = ("name",)
    success_url = reverse_lazy("services:kindofservice_list")


class ServiceListView(ListView):
    model = Service
    context_object_name = "service_list"


class ServiceCreateView(CreateView):
    model = Service
    fields = ("date", "client", "kind_of_service", "time_hours")
    success_url = reverse_lazy("services:service_list")


def kindofservice_delete(request, kind_id):
    kind = get_object_or_404(KindOfService, id=kind_id)
    if request.method == "POST":
        kind.delete()
        return redirect("services:kindofservice_list")
    return render(request, "services/kindofservice_delete.html", {"client": kind})


def kindofservice_edit(request, kind_id):
    kind = get_object_or_404(KindOfService, id=kind_id)

    if request.method == "POST":
        form = KindOfServiceForm(request.POST, instance=kind)
        if form.is_valid():
            form.save()
            return redirect("services:kindofservice_list")
    else:
        form = KindOfServiceForm(instance=kind)

    return render(request, "services/kindofservice_edit.html", {"form": form, "kind": kind})


