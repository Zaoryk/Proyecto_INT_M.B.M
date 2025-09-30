from django.db import models


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=50, blank=True, null=True)
    permisos = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario'


class SolicitudCompra(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    monto_total = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_id')

    class Meta:
        managed = False
        db_table = 'solicitudCompra'


class PedidoDeVenta(models.Model):
    id_pedido_de_venta = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    monto_total = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_id')

    class Meta:
        managed = False
        db_table = 'Pedido_de_venta'


class Producto(models.Model):
    idproducto = models.AutoField(db_column='idProducto', primary_key=True)
    nombre = models.CharField(max_length=120, blank=True, null=True)
    lote = models.CharField(unique=True, max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Producto'


class Receta(models.Model):
    idreceta = models.AutoField(db_column='idReceta', primary_key=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    insumos_necesarios = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Receta'


class OrdenProduccion(models.Model):
    id = models.AutoField(primary_key=True)
    fechainicio = models.DateField(db_column='fechaInicio', blank=True, null=True)
    fechafin = models.DateField(db_column='fechaFin', blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_id')
    producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='Producto_idProducto')
    receta = models.ForeignKey('Receta', models.DO_NOTHING, db_column='Receta_idReceta')

    class Meta:
        managed = False
        db_table = 'OrdenProduccion'


class Proveedor(models.Model):
    id_proveedor = models.AutoField(db_column='id_Proveedor', primary_key=True)
    nombre = models.CharField(max_length=130, blank=True, null=True)
    contacto = models.CharField(max_length=200, blank=True, null=True)
    condicionescomerciales = models.CharField(db_column='condicionesComerciales', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Proveedor'


class OrdenDeCompra(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    monto_total = models.IntegerField(blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor_id_proveedor')
    solicitudcompra = models.ForeignKey('SolicitudCompra', models.DO_NOTHING, db_column='solicitudCompra_id')

    class Meta:
        managed = False
        db_table = 'ordendeCompra'


class Bodega(models.Model):
    idbodega = models.AutoField(db_column='idBodega', primary_key=True)
    nombre = models.CharField(max_length=120, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bodega'


class MovimientoInventario(models.Model):
    idmovimientoinventario = models.AutoField(db_column='idMovimientoInventario', primary_key=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    cantidad = models.CharField(max_length=45, blank=True, null=True)
    bodega = models.ForeignKey('Bodega', models.DO_NOTHING, db_column='Bodega_idBodega')
    producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='Producto_idProducto')

    class Meta:
        managed = False
        db_table = 'MovimientoInventario'


class Costo(models.Model):
    idcosto = models.AutoField(db_column='idCosto', primary_key=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='Producto_idProducto')

    class Meta:
        managed = False
        db_table = 'Costo'
