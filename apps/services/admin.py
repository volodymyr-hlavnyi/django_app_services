from django.contrib import admin

from apps.services.models.client import Client
from apps.services.models.kindofservice import KindOfService
from apps.services.models.service import Service
from apps.services.models.userprofile import UserProfile


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "user",  # "user",
        "name",
        "created_at",
        "modified_at",
    )


@admin.register(KindOfService)
class KindOfServiceAdmin(admin.ModelAdmin):
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "user",  # "user",
        "date",
        "client",
        "kind_of_service",
        "time_hours",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "user",  # "user",
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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",  # "user",
        "visual_theme",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "user",  # "user",
        "visual_theme",
        "created_at",
        "modified_at",
    )
