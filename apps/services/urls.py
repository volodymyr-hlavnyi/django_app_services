from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("list/", views.ClientListView.as_view(), name="client_list"),
    path("create/", views.ClientsCreateView.as_view(), name="create_client"),
    path("edit/<int:client_id>/", views.client_edit, name="client_edit"),
    path("delete/<int:client_id>/", views.client_delete, name="client_delete"),
    #
    path("list_kind/", views.KindOfServiceListView.as_view(), name="kindofservice_list"),
    path("create_kind/", views.KindOfServiceCreateView.as_view(), name="kindofservice_create"),
    path("edit_kind/<int:kind_id>/", views.kindofservice_edit, name="kindofservice_edit"),
    path("delete_kind/<int:kind_id>/", views.kindofservice_delete, name="kindofservice_delete"),
    # path("update/<int:pk>/", views.ContactUpdateView.as_view(), name="contacts_update"),
    # #
    # path("generate/", views.generate_contacts_view, name="contacts_generate"),
    # #
    # path("createdetails/<int:pk>/", views.ContactDetailCreateView.as_view(), name="contacts_details_create"),
    # # path("createdetails/<int:pk>/", views.contact_info_detail_view, name="contacts_details_create"),
    path("list_service/", views.ServiceListView.as_view(), name="service_list"),
    path("create_service/", views.ServiceCreateView.as_view(), name="service_create"),
]
