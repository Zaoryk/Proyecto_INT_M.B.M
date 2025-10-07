from django.contrib import admin
from dispositivos.models import Bodega, Cliente, Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, OrdenProduccion, Pedido, Producto, Proveedor, Usuario

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 1
    fields = ("tipo", "fecha", "cantidad")


admin.site.register(Cliente)
admin.site.register(Bodega)
admin.site.register(ListarPrecios)
admin.site.register(Costo)
admin.site.register(MovimientoInventario)
admin.site.register(OrdenDeCompra)
admin.site.register(OrdenProduccion)
admin.site.register(Pedido)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock")
    search_fields = ("nombre",)
    inlines = [MovimientoInventarioInline]
admin.site.register(Proveedor)
admin.site.register(Usuario)
admin.register(ListarPrecios)
