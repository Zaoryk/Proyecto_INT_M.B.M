from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dispositivos.views import dashboard, formularioUsuario, gestionProductos, gestionProveedores, moduloTransaccional, perfilusuario, gestionCategorias, gestionBodegas
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.shortcuts import render
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),
    path("", dashboard, name="dashboard"),
    path("formulariousuario/", formularioUsuario, name="Formulario"),
    path("gestionproductos/", gestionProductos, name="Productos"),
    path("gestionproveedores/", gestionProveedores, name="Proveedores"),
    path("modulotransaccional/", moduloTransaccional, name="Transaccional"),
    path("perfilusuario/", perfilusuario, name="perfil_usuario"),
    path("gestioncategorias/", gestionCategorias, name="Categorias"),
    path("gestionbodegas/", gestionBodegas, name="Bodegas"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def error_404_view(request, exception):
    return render(request, 'dispositivos/Error404.html', status=404)

def error_500_view(request):
    return render(request, 'dispositivos/Error500.html', status=500)

handler404 = error_404_view
handler500 = error_500_view