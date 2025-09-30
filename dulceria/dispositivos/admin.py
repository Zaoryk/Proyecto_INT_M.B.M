from django.contrib import admin
from .models import Proveedor, Producto, PerfilUsuario

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'email')
    search_fields = ('nombre', 'contacto')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'proveedor')
    list_filter = ('proveedor',)
    search_fields = ('nombre',)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'email', 'rol')
    list_filter = ('rol',)
    search_fields = ('user__username', 'telefono')