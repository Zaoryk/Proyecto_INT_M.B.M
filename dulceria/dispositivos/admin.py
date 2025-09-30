from django.contrib import admin
from .models import Bodega, Cliente, Costo, Listarprecios, Movimientoinventario, Ordendecompra, Ordenproduccion, Pedido, Producto, Proveedor, Usuario

admin.site.register(Bodega)
admin.site.register(Cliente)
admin.site.register(Costo)
admin.site.register(Listarprecios)
admin.site.register(Movimientoinventario)
admin.site.register(Ordendecompra)
admin.site.register(Ordenproduccion)
admin.site.register(Pedido)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Usuario)