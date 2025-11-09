from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dispositivos import views  # ✅ Importa el módulo entero, NO funciones individuales

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),

    # --- Dashboard ---
    path("", views.dashboard, name="dashboard"),

    # --- Módulo Usuarios ---
    path("formulariousuario/", views.formularioUsuario, name="Formulario"),

    # --- Módulo Productos ---
    path("gestionproductos/", views.gestionProductos, name="Productos"),

    # --- Módulo Proveedores ---
    path("gestionproveedores/", views.gestionProveedores, name="Proveedores"),

    # --- Módulo Transaccional ---
    path("modulotransaccional/", views.moduloTransaccional, name="Transaccional"),

    # --- Perfil de Usuario ---
    path("perfilusuario/", views.perfilusuario, name="perfil_usuario"),

    # --- CRUDs de backend ---
    path("gestioncategorias/", views.gestionCategorias, name="Categorias"),
    path("gestionbodegas/", views.gestionBodegas, name="Bodegas"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
