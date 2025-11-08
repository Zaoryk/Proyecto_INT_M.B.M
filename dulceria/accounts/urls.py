from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView 
from .forms import LoginForm
from .views import (dashboard, password_solicitud, password_validar, password_cambio)

urlpatterns = [
    path("login/", LoginView.as_view(
        template_name="accounts/login.html",
        authentication_form=LoginForm,
        redirect_authenticated_user=True
    ), name="login"),

    path("logout/", LogoutView.as_view(), name="logout"),

    path("dashboard/", dashboard, name="dashboard"),
    path("password-reset/", password_solicitud, name="password_solicitud"),
    path("password-reset/verify/", password_validar, name="password_validar"),
    path("dashboard-reset/confirm/", password_cambio, name="password_cambio"),

]
