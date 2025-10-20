from django.contrib import admin
from dulceria.dispositivos.modelsbackup import Bodega, Cliente, Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, OrdenProduccion, Pedido, Producto, Proveedor, Usuario

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 1
    fields = ("tipo", "fecha", "cantidad")


admin.site.register(Cliente)
admin.site.register(Bodega)
admin.site.register(ListarPrecios)
admin.site.register(Costo)
admin.site.register(MovimientoInventario)
@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(admin.ModelAdmin):
    list_display = ("id", "proveedor", "fecha", "estado", "monto_total")
    actions = ["marcar_en_proceso", "marcar_cerrada", "marcar_no_iniciado"]

    @admin.action(description="Marcar seleccionadas como No iniciadas")
    def marcar_no_iniciado(self, request, queryset):
        queryset.update(estado="no_iniciado")

    @admin.action(description="Marcar seleccionadas como En Proceso")
    def marcar_en_proceso(self, request, queryset):
        queryset.update(estado="en_proceso")

    @admin.action(description="Marcar seleccionadas como Cerrada")
    def marcar_cerrada(self, request, queryset):
        queryset.update(estado="cerrada")

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
