from django.shortcuts import redirect
from django.urls import resolve, reverse, Resolver404

from dispositivos.models import Usuario


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                resolver_match = resolve(request.path_info)
            except Resolver404:
                return self.get_response(request)

            url_name = resolver_match.url_name
            app_name = resolver_match.app_name

            allowed_names = {
                "login",
                "logout",
                "force_password_change",
            }

            allowed_apps = {
                "admin",
            }

            if url_name not in allowed_names and app_name not in allowed_apps:
                usuario = Usuario.objects.filter(email=request.user.email).first()
                if usuario and usuario.password_temporal:
                    return redirect(reverse("force_password_change"))

        response = self.get_response(request)
        return response
