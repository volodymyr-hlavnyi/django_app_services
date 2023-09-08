from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.services.models import Client, KindOfService


def home(request):
    return render(request, "services/home.html")


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
