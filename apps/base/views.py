# import datetime

from django.shortcuts import render

import core.settings


def home_page(request):
    # now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")

    return render(
        request=request,
        template_name="base/home_page.html",
        context={
            "greetings_text": f"DJANGO ENVIRONMENT: "
            f" DEBUG={core.settings.DEBUG} "
            f" ALLOWED_HOST={core.settings.ALLOWED_HOSTS} ",
            "title": "Django base project",
        },
    )


def about_us_page(request):
    # now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
    text_for_page = "Short description about us"
    return render(
        request=request,
        template_name="base/about_us_page.html",
        context={
            "text_for_page": f"{text_for_page}",
            "title": "About us",
        },
    )


def contacts_page(request):
    # now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
    text_for_page = (
        "Our contacts:" "  phone number: 212121212" "  email: tyruetyurey@erithyreuiyt" "  address: stree F, 4587 City"
    )

    return render(
        request=request,
        template_name="base/contacts_page.html",
        context={
            "text_for_page": f"{text_for_page}",
            "title": "Our contacts",
        },
    )
