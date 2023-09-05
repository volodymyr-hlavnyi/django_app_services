from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.services.models import Client


def home(request):
    return render(request, "services/home.html")


# Create your views here.


class ClientsCreateView(CreateView):
    model = Client
    fields = ("name",)
    success_url = reverse_lazy("services:home")


class ClientListView(ListView):
    model = Client
    context_object_name = "client_list"
