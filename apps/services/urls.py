from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.home, name="home"),
    path("list/", views.ClientListView.as_view(), name="client_list"),
    path("create/", views.ClientsCreateView.as_view(), name="create_client"),
    path("edit/<int:client_id>/", views.client_edit, name="client_edit"),
    path("delete/<int:client_id>/", views.client_delete, name="client_delete"),
    path("currency/", views.currency_view, name="currency_view"),
    path("list_kind/", views.KindOfServiceListView.as_view(), name="kindofservice_list"),
    path("create_kind/", views.KindOfServiceCreateView.as_view(), name="kindofservice_create"),
    path("edit_kind/<int:kind_id>/", views.kindofservice_edit, name="kindofservice_edit"),
    path("delete_kind/<int:kind_id>/", views.kindofservice_delete, name="kindofservice_delete"),
    path("list_service/", views.ServiceListView.as_view(), name="service_list"),
    path("create_service/", views.ServiceCreateView.as_view(), name="service_create"),
    path("edit_service/<int:service_id>/", views.service_edit, name="service_edit"),
    path("delete_service/<int:service_id>/", views.service_delete, name="service_delete"),
    # Login/Logout
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Actions
    # path("actions/", views.ActionListView.as_view(), name="action_list"),
    path("actions/", views.action_list, name="action_list"),
    path("action_close/<int:action_id>", views.action_close, name="action_close"),
    path("actions/<int:action_id>", views.action_delete, name="action_delete"),
    # User (settings)
    path("edit_userprofile/<int:user_id>", views.userprofile_edit, name="userprofile_edit"),
]
