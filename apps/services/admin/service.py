from django.contrib import admin

from apps.services.models.service import Service, Action


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


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = (
        "user",  # "user",
        "service",  # "service",
        "client",  # "client",
        "status",
        "manually_closed",
    )
