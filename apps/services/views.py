from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

# from apps.services.models.currency import CurrencyRate
from apps.services.models.client import Client
from apps.services.models.kindofservice import KindOfService
from apps.services.models.service import Service, Action
from apps.services.forms import (
    ClientForm,
    KindOfServiceForm,
    ServiceForm,
    UserProfileForm,
    CurrencyForm,
    CurrencyRateForm,
)

from django.contrib.auth import login, logout

from .forms import SignupForm, LoginForm

from .models.currency import CurrencyRate, RefOfCurrency
from .models.userprofile import UserProfile
from .additionally import add_suffix_to_duplicates, get_graph

from django.contrib.auth import get_user_model

# from core.celery import app as celery_app
from .tasks import get_rate_currency_by_all

User = get_user_model()


# import logging

# from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "services/home.html")


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

    return render(request, "services/client/client_edit.html", {"form": form, "client": client})


def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == "POST":
        client.delete()
        return redirect("services:client_list")

    return render(request, "services/client/client_delete.html", {"client": client})


class ClientsCreateView(CreateView):
    model = Client
    fields = ("name",)
    success_url = reverse_lazy("services:client_list")
    template_name = "services/client/client_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ClientListView(ListView):
    model = Client
    context_object_name = "client_list"
    template_name = "services/client/client_list.html"

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user.id)


class KindOfServiceListView(ListView):
    model = KindOfService
    context_object_name = "kindofservice_list"
    template_name = "services/kindofservice/kindofservice_list.html"

    def get_queryset(self):
        return KindOfService.objects.filter(user=self.request.user.id)


class KindOfServiceCreateView(CreateView):
    model = KindOfService
    fields = ("name",)
    success_url = reverse_lazy("services:kindofservice_list")
    template_name = "services/kindofservice/kindofservice_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ServiceListView(ListView):
    model = Service
    context_object_name = "service_list"
    template_name = "services/service/service_list.html"

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user.id)


def action_list(request):
    # logger = logging.getLogger("django")
    request = request
    rate = 39  # get_currency_rate()

    action_query = Action.objects.filter(user=request.user.id)
    time_query = action_query.values("service__time_hours")
    earnings = [float(item["service__time_hours"]) * rate for item in time_query]

    combined_list = zip(action_query, earnings)

    closed_action_query = Action.objects.filter(user=request.user.id).filter(status="Closed")
    closed_time_query = action_query.values("service__time_hours").filter(status="Closed")
    closed_earnings = [float(item["service__time_hours"]) * rate for item in closed_time_query]
    client_list = list(closed_action_query.values_list("client__name", flat=True))
    client_list = add_suffix_to_duplicates(client_list)
    graph = get_graph(closed_earnings, client_list)
    # logger.info(f"----- graph: {graph}")

    return render(
        request,
        "services/action/action_list.html",
        {
            "combined_list": combined_list,
            "action_list": action_query,
            "graph": graph,
        },
    )


class ServiceCreateView(CreateView):
    model = Service
    fields = ("date", "client", "kind_of_service", "time_hours")
    success_url = reverse_lazy("services:service_list")
    template_name = "services/service/service_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
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

    return render(request, "services/service/service_edit.html", {"form": form, "service": service})


@login_required
def userprofile_edit(request, user_id):
    if UserProfile.objects.filter(user_id=user_id).exists():
        userprofile = UserProfile.objects.get(user_id=user_id)
    else:
        userprofile = UserProfile.objects.create(user_id=user_id)
        userprofile.visual_theme = "light"
        userprofile.save()

    # userprofile = get_object_or_404(UserProfile, pk=user_id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=userprofile)
        if form.is_valid():
            form.user = request.user
            form.save()
            return render(
                request,
                "services/user_profile/userprofile_edit.html",
                {"form": form, "user": request.user, "is_saved": True},
            )
    else:
        form = UserProfileForm(instance=userprofile)

    return render(
        request, "services/user_profile/userprofile_edit.html", {"form": form, "user": request.user, "is_saved": False}
    )


def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        service.delete()
        return redirect("services:service_list")
    return render(request, "services/service/service_delete.html", {"service": service})


def kindofservice_delete(request, kind_id):
    kind = get_object_or_404(KindOfService, id=kind_id)
    if request.method == "POST":
        kind.delete()
        return redirect("services:kindofservice")
    return render(request, "services/kindofservice/kindofservice_delete.html", {"client": kind})


@login_required
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

    return render(request, "services/kindofservice/kindofservice_edit.html", {"form": form, "kind": kind})


def client_info(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    services_for_client = Service.objects.filter(client=client)
    service_kinds = [item.kind_of_service for item in services_for_client]

    # logger = logging.getLogger("django")
    # logger.info(f"services_for_client list is {service_kinds} for name {client.name} with {client.id}")

    # if request.method == "GET":
    #    pass
    #       client.delete()
    #       return redirect("services:client_list")

    return render(
        request=request,
        template_name="services/client/client_info.html",
        context={"client": client, "service_kinds": service_kinds},
    )


def action_close(request, action_id):
    action = Action.objects.filter(id=action_id)
    client_name = action[0].client.name

    if request.method == "POST":
        action[0].close()
        return redirect("services:action_list")
    return render(
        request,
        "services/action/action_close.html",
        {
            "action": action,
            "client_name": client_name,
        },
    )


def action_delete(request, action_id):
    # pass
    action = Action.objects.filter(id=action_id)
    client_name = action[0].client.name

    if request.method == "POST":
        action[0].delete()
        return redirect("services:action_list")
    return render(
        request,
        "services/action/action_delete.html",
        {
            "action": action[0],
            "client_name": client_name,
        },
    )


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


class CurrencyRateListView(ListView):
    result = get_rate_currency_by_all.delay()
    model = CurrencyRate
    context_object_name = "currencyrate_list"
    template_name = "services/currency/currencyrate_list.html"

    def get_queryset(self):
        return CurrencyRate.objects.filter(user=self.request.user.id)


class CurrencyRateCreateView(CreateView):
    model = CurrencyRate
    fields = ("currency", "rate", "date")
    success_url = reverse_lazy("services:currencyrate_list")
    template_name = "services/currency/currencyrate_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def currency_rate_edit(request, currencyrate_id):
    currencyrate = get_object_or_404(CurrencyRate, pk=currencyrate_id)

    if request.method == "POST":
        form = CurrencyRateForm(request.POST, instance=currencyrate)
        if form.is_valid():
            form.user = request.user
            form.save()
            return redirect("services:currencyrate_list")
    else:
        form = CurrencyRateForm(instance=currencyrate)

    return render(request, "services/currency/currencyrate_edit.html", {"form": form, "currencyrate": currencyrate})


def currency_rate_delete(request, currencyrate_id):
    currencyrate = get_object_or_404(CurrencyRate, pk=currencyrate_id)

    if request.method == "POST":
        currencyrate.delete()
        return redirect("services:currencyrate_list")

    return render(request, "services/currency/currencyrate_delete.html", {"currencyrate": currencyrate})


class CurrencyListView(ListView):
    model = RefOfCurrency
    context_object_name = "currency_list"
    template_name = "services/currency/currency_list.html"

    def get_queryset(self):
        return RefOfCurrency.objects.filter(user=self.request.user.id)


class CurrencyCreateView(CreateView):
    model = RefOfCurrency
    fields = ("name", "code")
    success_url = reverse_lazy("services:currency_list")
    template_name = "services/currency/currency_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def currency_edit(request, currency_id):
    currency = get_object_or_404(RefOfCurrency, pk=currency_id)

    if request.method == "POST":
        form = CurrencyForm(request.POST, instance=currency)
        if form.is_valid():
            form.user = request.user
            form.save()
            return redirect("services:currency_list")
    else:
        form = CurrencyForm(instance=currency)

    return render(request, "services/currency/currency_edit.html", {"form": form, "currency": currency})


def currency_delete(request, currency_id):
    currency = get_object_or_404(RefOfCurrency, pk=currency_id)

    if request.method == "POST":
        currency.delete()
        return redirect("services:currency_list")

    return render(request, "services/currency/currency_delete.html", {"currency": currency})
