from django.contrib import admin
from dispositivos.models import Bodega, Cliente, Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, OrdenProduccion, Pedido, Producto, Proveedor, Usuario
class ListarPreciosInline(admin.TabularInline):
    model = ListarPrecios
    extra = 0
    fields = ("canal", "temporada", "valor")
    show_change_link = True

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo")
    inlines = [ListarPreciosInline]
admin.site.register(Bodega)
admin.site.register(ListarPrecios)
admin.site.register(Costo)
admin.site.register(MovimientoInventario)
admin.site.register(OrdenDeCompra)
admin.site.register(OrdenProduccion)
admin.site.register(Pedido)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Usuario)
admin.register(ListarPrecios)
