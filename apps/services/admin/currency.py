from django.contrib import admin

from apps.services.models.currency import CurrencyRate, RefOfCurrency


@admin.register(RefOfCurrency)
class RefOfCurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "code",
        "name_special",
        "last_updated",
    )

    list_filter = (
        "user",
        "name",
        "code",
        "name_special",
        "last_updated",
    )


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "currency",
        "rate",
        "date",
        "last_updated",
    )

    list_filter = (
        "user",
        "currency",
        "rate",
        "date",
        "last_updated",
    )
