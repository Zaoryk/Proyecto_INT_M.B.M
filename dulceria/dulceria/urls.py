from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dispositivos.views import dashboard, formularioUsuario, gestionProductos, gestionProveedores, moduloTransaccional, perfilusuario, gestionCategorias, gestionBodegas

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