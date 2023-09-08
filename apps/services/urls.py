from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("list/", views.ClientListView.as_view(), name="client_list"),
    path("/edit/<int:client_id>/", views.client_edit, name="client_edit"),
    path("/delete/<int:client_id>/", views.client_delete, name="client_delete"),
    #
    path("list_kind/", views.KindOfServiceListView.as_view(), name="kindofservice_list"),
    # path("delete/<int:pk>/", views.ContactDeleteView.as_view(), name="contacts_delete"),
    # #
    # path("update/<int:pk>/", views.ContactUpdateView.as_view(), name="contacts_update"),
    # #
    # path("generate/", views.generate_contacts_view, name="contacts_generate"),
    # #
    path("create/", views.ClientsCreateView.as_view(), name="create_client"),
    path("create_kind/", views.KindOfServiceCreateView.as_view(), name="kindofservice_create"),
    # path("createdetails/<int:pk>/", views.ContactDetailCreateView.as_view(), name="contacts_details_create"),
    # # path("createdetails/<int:pk>/", views.contact_info_detail_view, name="contacts_details_create"),
    # #
    # path("detail/<int:pk>/", views.ContactDetailView.as_view(), name="contacts_detail"),
]
