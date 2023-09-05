from django.urls import path

from . import views

app_name = "base"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("aboutus/", views.about_us_page, name="about_us_page"),
    path("contacts/", views.contacts_page, name="contacts_page"),
]
