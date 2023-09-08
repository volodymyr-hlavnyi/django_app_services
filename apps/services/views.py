from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.services.forms import ClientForm
from apps.services.models import Client


def home(request):
    return render(request, "services/home.html")


# Create your views here.
def client_edit(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('services:client_list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'services/client_edit.html', {'form': form, 'client': client})


def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        client.delete()
        return redirect('services:client_list')

    return render(request, 'services/client_delete.html', {'client': client})

class ClientsCreateView(CreateView):
    model = Client
    fields = ("name",)
    success_url = reverse_lazy("services:client_list")


class ClientListView(ListView):
    model = Client
    context_object_name = "client_list"

