from django.contrib import admin

from apps.services.models.kindofservice import KindOfService


@admin.register(KindOfService)
class KindOfServiceAdmin(admin.ModelAdmin):
    list_display = (
        "user",  # "user",
        "name",
        "created_at",
        "modified_at",
    )
