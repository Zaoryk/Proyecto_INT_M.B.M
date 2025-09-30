from django.contrib import admin
from .models import (
    Usuario,
    SolicitudCompra,
    PedidoDeVenta,
    Producto,
    Receta,
    OrdenProduccion,
    Proveedor,
    OrdenDeCompra,
    Bodega,
    MovimientoInventario,
    Costo,
)

# Registro directo de todos los modelos
admin.site.register(Usuario)
admin.site.register(SolicitudCompra)
admin.site.register(PedidoDeVenta)
admin.site.register(Producto)
admin.site.register(Receta)
admin.site.register(OrdenProduccion)
admin.site.register(Proveedor)
admin.site.register(OrdenDeCompra)
admin.site.register(Bodega)
admin.site.register(MovimientoInventario)
admin.site.register(Costo)