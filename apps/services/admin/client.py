from django.contrib import admin

from apps.services.models.client import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "user",  # "user",
        "name",
        "created_at",
        "modified_at",
    )


# class ClientInline(admin.TabularInline):
#    model = models.Client


# class KindOfServiceInline(admin.TabularInline):
#    model = models.KindOfService
