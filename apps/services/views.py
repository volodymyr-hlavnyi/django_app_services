
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.services.models import Client, KindOfService, Service, User, Action, CurrencyRate
from apps.services.forms import ClientForm, KindOfServiceForm, ServiceForm

from django.contrib.auth import login, logout
from .forms import SignupForm, LoginForm

import requests
import logging

from .services import get_currency_rate, get_graph


# import logging

# from django.contrib.auth.decorators import login_required

# DataTuple = namedtuple('DataTuple', ['action_fields', 'action_data'])


def home(request):
    return render(request, "services/home.html")


def currency_view(request):
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url)
    # :TODO: move drive code to services
    if response.status_code == 200:
        exchange_rates = response.json()

        # Получите список всех доступных валют
        available_currencies = [currency["cc"] for currency in exchange_rates]

        selected_currency = request.GET.get("currency", "USD")  # По умолчанию USD

        # Проверьте, выбрана ли валюта из списка доступных
        if selected_currency not in available_currencies:
            return render(
                request, "services/currency_template.html", {"error_message": "Выбранной валюты нет в списке"}
            )

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
            form.user = request.user
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ClientListView(ListView):
    model = Client
    context_object_name = "client_list"

    def get_queryset(self):
        logger = logging.getLogger("django")

        queryset = Client.objects.filter(user=self.request.user.id)

        logger.info(f"----- queryset is {queryset}.")

        return queryset


class KindOfServiceListView(ListView):
    model = KindOfService
    context_object_name = "kindofservice_list"

    def get_queryset(self):
        return KindOfService.objects.filter(user=self.request.user.id)


class KindOfServiceCreateView(CreateView):
    model = KindOfService
    fields = ("name",)
    success_url = reverse_lazy("services:kindofservice_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ServiceListView(ListView):
    model = Service
    context_object_name = "service_list"

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user.id)


def action_list(request):
    logger = logging.getLogger("django")
    request = request
    rate = get_currency_rate()

    action_query = Action.objects.filter(user=request.user.id)
    time_query = action_query.values("service__time_hours")
    earnings = [float(item['service__time_hours']) * rate for item in time_query]

    combined_list = zip(action_query, earnings)

    closed_action_query = Action.objects.filter(user=request.user.id).filter(status='Closed')
    closed_time_query = action_query.values("service__time_hours").filter(status='Closed')
    closed_earnings = [float(item['service__time_hours']) * rate for item in closed_time_query]
    client_list = list(closed_action_query.values_list('client__name', flat=True))
    logger.info(f"----- client_list: {client_list}")
    graph = get_graph(closed_earnings, client_list)    # :TODO: pass only closed actions
    logger.info(f"----- graph: {graph}")

    return render(request,
                  "services/action_list.html",
                  {
                    "combined_list": combined_list,
                    "action_list": action_query,
                    "graph": graph,
                  }
    )


class ServiceCreateView(CreateView):
    model = Service
    fields = ("date", "client", "kind_of_service", "time_hours")
    success_url = reverse_lazy("services:service_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def service_edit(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.user = request.user
            form.save()
            return redirect("services:service_list")
    else:
        form = ServiceForm(instance=service)

    return render(request, "services/service_edit.html", {"form": form, "service": service})


def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        service.delete()
        return redirect("services:service_list")
    return render(request, "services/service_delete.html", {"service": service})


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
            form.user = request.user
            form.save()
            return redirect("services:kindofservice_list")
    else:
        form = KindOfServiceForm(instance=kind)

    return render(request, "services/kindofservice_edit.html", {"form": form, "kind": kind})


def client_info(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    services_for_client = Service.objects.filter(client=client)
    service_kinds = [item.kind_of_service for item in services_for_client]

    return render(
        request=request,
        template_name="services/client_info.html",
        context={"client": client, "service_kinds": service_kinds},
    )


def action_close(request, action_id):
    action = Action.objects.filter(id=action_id)
    if request.method == "POST":
        action[0].close()
        return redirect("services:action_list")
    return render(request, "services/action_close.html", {"action": action})

def action_delete(request, action_id):
    pass
    action = Action.objects.filter(id=action_id)
    if request.method == "POST":
        action[0].delete()
        return redirect("services:action_list")
    return render(request, "services/action_delete.html", {"action": action})

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()

    return render(request, "services/sing_in_up/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "services/sing_in_up/signin.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")
