from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """Modelo de usuario personalizado"""
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=50, unique=True)
    permisos = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.nombre} ({self.rut})"

class Proveedor(models.Model):
    """Modelo de proveedor"""
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    contacto = models.CharField(max_length=200)
    condiciones = models.CharField(max_length=45, blank=True)
    
    class Meta:
        db_table = 'Proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    """Modelo de producto"""
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    base = models.CharField(max_length=45)
    fecha_elaboracion = models.DateField()
    precio = models.IntegerField()
    stock = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'Producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    def __str__(self):
        return self.nombre

class Receta(models.Model):
    """Modelo de receta"""
    id_receta = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20)
    manejo_necesario = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        db_table = 'Receta'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
    
    def __str__(self):
        return f"Receta v{self.version}"

class RecetaProducto(models.Model):
    """Tabla intermedia para Receta-Producto"""
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    class Meta:
        db_table = 'RecetaProducto'
        verbose_name = 'Receta Producto'
        verbose_name_plural = 'Recetas Productos'
        unique_together = ['receta', 'producto']

class Cliente(models.Model):
    """Modelo de cliente"""
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    condiciones = models.CharField(max_length=100, blank=True)
    desde = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'Cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return self.nombre

class Bodega(models.Model):
    """Modelo de bodega"""
    id_bodega = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    ubicacion = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
    
    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"

class Inventario(models.Model):
    """Modelo de inventario"""
    id_inventario = models.AutoField(primary_key=True)
    lote = models.CharField(max_length=45, blank=True)
    fecha = models.DateField()
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Inventario'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
    
    def __str__(self):
        return f"Inventario {self.fecha} - {self.producto.nombre}"

class OrdenProduccion(models.Model):
    """Modelo de orden de producción"""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    id_orden = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()
    estado = models.CharField(max_length=45, choices=ESTADOS)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'OrdenProduccion'
        verbose_name = 'Orden de Producción'
        verbose_name_plural = 'Órdenes de Producción'
    
    def __str__(self):
        return f"Orden {self.id_orden} - {self.estado}"

class PedidoVenta(models.Model):
    """Modelo de pedido de venta"""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('despachado', 'Despachado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id_pedido_venta = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=45, choices=ESTADOS)
    monto_total = models.IntegerField()
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'PedidoVenta'
        verbose_name = 'Pedido de Venta'
        verbose_name_plural = 'Pedidos de Venta'
    
    def __str__(self):
        return f"Pedido {self.id_pedido_venta} - {self.estado}"

class DetallePedidoVenta(models.Model):
    """Detalle de pedido de venta"""
    pedido_venta = models.ForeignKey(PedidoVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    
    class Meta:
        db_table = 'DetallePedidoVenta'
        verbose_name = 'Detalle Pedido Venta'
        verbose_name_plural = 'Detalles Pedidos Venta'

class SolicitudCompra(models.Model):
    """Modelo de solicitud de compra"""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('completada', 'Completada'),
    ]
    
    id_solicitud = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=45, choices=ESTADOS)
    monto_total = models.IntegerField()
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'SolicitudCompra'
        verbose_name = 'Solicitud de Compra'
        verbose_name_plural = 'Solicitudes de Compra'
    
    def __str__(self):
        return f"Solicitud {self.id_solicitud} - {self.estado}"

class DetalleSolicitudCompra(models.Model):
    """Detalle de solicitud de compra"""
    solicitud_compra = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_estimado = models.IntegerField()
    
    class Meta:
        db_table = 'DetalleSolicitudCompra'
        verbose_name = 'Detalle Solicitud Compra'
        verbose_name_plural = 'Detalles Solicitudes Compra'

class OrdenCompra(models.Model):
    """Modelo de orden de compra"""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    
    id_orden_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=45, choices=ESTADOS)
    monto_total = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    solicitud_compra = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'OrdenCompra'
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
    
    def __str__(self):
        return f"OC {self.id_orden_compra} - {self.proveedor.nombre}"

class DetalleOrdenCompra(models.Model):
    """Detalle de orden de compra"""
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    
    class Meta:
        db_table = 'DetalleOrdenCompra'
        verbose_name = 'Detalle Orden Compra'
        verbose_name_plural = 'Detalles Ordenes Compra'

class Factura(models.Model):
    """Modelo de factura"""
    id_factura = models.AutoField(primary_key=True)
    fecha = models.DateField()
    total = models.IntegerField()
    pedido_venta = models.ForeignKey(PedidoVenta, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
    
    def __str__(self):
        return f"Factura {self.id_factura} - ${self.total}"

class ListaPrecios(models.Model):
    """Modelo de lista de precios"""
    id_lista_precios = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    temporada = models.CharField(max_length=45, blank=True)
    valor = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ListaPrecios'
        verbose_name = 'Lista de Precios'
        verbose_name_plural = 'Listas de Precios'
        unique_together = ['cliente', 'producto']
    
    def __str__(self):
        return f"Lista {self.nombre} - {self.temporada}"