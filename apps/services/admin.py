from django.contrib import admin

from apps.services import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "modified_at",
    )


@admin.register(models.KindOfService)
class KindOfServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "modified_at",
    )


# class ClientInline(admin.TabularInline):
#    model = models.Client


# class KindOfServiceInline(admin.TabularInline):
#    model = models.KindOfService


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "client",
        "kind_of_service",
        "time_hours",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "date",
        "client",
        "kind_of_service",
        "time_hours",
        "created_at",
        "modified_at",
    )


#    inlines = [
#        ClientInline,
#        KindOfServiceInline,
#    ]
