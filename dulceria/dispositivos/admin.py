from django.contrib import admin
from .models import Bodega, Cliente, Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, OrdenProduccion, Pedido, Producto, Proveedor, Usuario

admin.site.register(Bodega)
admin.site.register(Cliente)
admin.site.register(Costo)
admin.site.register(ListarPrecios)
admin.site.register(MovimientoInventario)
admin.site.register(OrdenDeCompra)
admin.site.register(OrdenProduccion)
admin.site.register(Pedido)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Usuario)