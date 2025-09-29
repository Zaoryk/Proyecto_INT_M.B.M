from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'nombre', 'rut', 'email', 'is_staff']
    search_fields = ['username', 'nombre', 'rut', 'email']
    list_filter = ['is_staff', 'is_active']
    ordering = ['nombre']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {
            'fields': ('nombre', 'rut', 'permisos')
        }),
    )

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id_proveedor', 'nombre', 'contacto', 'condiciones']
    search_fields = ['nombre', 'contacto']
    list_filter = ['condiciones']
    ordering = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'nombre', 'base', 'precio', 'stock', 'fecha_elaboracion']
    search_fields = ['nombre', 'base']
    list_filter = ['base', 'fecha_elaboracion']
    ordering = ['nombre']

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['id_receta', 'version', 'manejo_necesario']
    search_fields = ['version']
    ordering = ['-id_receta']

@admin.register(RecetaProducto)
class RecetaProductoAdmin(admin.ModelAdmin):
    list_display = ['receta', 'producto', 'cantidad']
    search_fields = ['receta__version', 'producto__nombre']
    list_filter = ['producto__base']
    ordering = ['receta']
    list_select_related = ['receta', 'producto']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id_cliente', 'nombre', 'condiciones', 'desde']
    search_fields = ['nombre', 'condiciones']
    list_filter = ['condiciones']
    ordering = ['nombre']

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['id_bodega', 'nombre', 'ubicacion']
    search_fields = ['nombre', 'ubicacion']
    ordering = ['nombre']

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['id_inventario', 'fecha', 'producto', 'cantidad', 'bodega', 'lote']
    search_fields = ['producto__nombre', 'lote']
    list_filter = ['fecha', 'bodega']
    ordering = ['-fecha']
    list_select_related = ['producto', 'bodega']

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ['id_orden', 'fecha_inicio', 'fecha_limite', 'estado', 'receta']
    search_fields = ['estado', 'receta__version']
    list_filter = ['estado', 'fecha_inicio']
    ordering = ['-fecha_inicio']
    list_select_related = ['receta']

@admin.register(PedidoVenta)
class PedidoVentaAdmin(admin.ModelAdmin):
    list_display = ['id_pedido_venta', 'fecha', 'estado', 'monto_total', 'vendedor', 'cliente']
    search_fields = ['estado', 'vendedor__nombre', 'cliente__nombre']
    list_filter = ['estado', 'fecha']
    ordering = ['-fecha']
    list_select_related = ['vendedor', 'cliente']

@admin.register(SolicitudCompra)
class SolicitudCompraAdmin(admin.ModelAdmin):
    list_display = ['id_solicitud', 'fecha', 'estado', 'monto_total', 'solicitante']
    search_fields = ['estado', 'solicitante__nombre']
    list_filter = ['estado', 'fecha']
    ordering = ['-fecha']
    list_select_related = ['solicitante']

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id_orden_compra', 'fecha', 'estado', 'monto_total', 'proveedor', 'solicitud_compra']
    search_fields = ['estado', 'proveedor__nombre']
    list_filter = ['estado', 'fecha']
    ordering = ['-fecha']
    list_select_related = ['proveedor', 'solicitud_compra']

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id_factura', 'fecha', 'total', 'pedido_venta']
    search_fields = ['pedido_venta__cliente__nombre']
    list_filter = ['fecha']
    ordering = ['-fecha']
    list_select_related = ['pedido_venta']

@admin.register(ListaPrecios)
class ListaPreciosAdmin(admin.ModelAdmin):
    list_display = ['id_lista_precios', 'nombre', 'temporada', 'valor', 'cliente', 'producto']
    search_fields = ['nombre', 'temporada', 'cliente__nombre', 'producto__nombre']
    list_filter = ['temporada']
    ordering = ['-id_lista_precios']
    list_select_related = ['cliente', 'producto']

# Models inline para detalles
class DetallePedidoVentaInline(admin.TabularInline):
    model = DetallePedidoVenta
    extra = 1

class DetalleSolicitudCompraInline(admin.TabularInline):
    model = DetalleSolicitudCompra
    extra = 1

class DetalleOrdenCompraInline(admin.TabularInline):
    model = DetalleOrdenCompra
    extra = 1

# Agregar inlines a los modelos principales
PedidoVentaAdmin.inlines = [DetallePedidoVentaInline]
SolicitudCompraAdmin.inlines = [DetalleSolicitudCompraInline]
OrdenCompraAdmin.inlines = [DetalleOrdenCompraInline]