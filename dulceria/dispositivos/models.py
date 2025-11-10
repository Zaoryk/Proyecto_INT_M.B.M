from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash

class Usuario(models.Model):
    ROLES = [
        ("administrador", "Administrador"),
        ("operador_compras", "Operador de Compras"),
        ("operador_inventario", "Operador de Inventario"),
        ("operador_produccion", "Operador de Producción"),
        ("operador_ventas", "Operador de Ventas"),
        ("analista_financiero", "Analista Financiero"),
    ]
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
        ("bloqueado", "Bloqueado")
    ]
    MFA_OPTIONS = [
        ("habilitado", "Habilitado"),
        ("deshabilitado", "Deshabilitado"),
    ]
    idUsuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    email = models.CharField(max_length=100, blank=True, null=True, unique=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    rol = models.CharField(max_length=50, choices=ROLES, default="operador_ventas")
    estado = models.CharField(max_length=50, choices=ESTADOS, default="activo")
    mfa_habilitado = models.CharField(max_length=50, choices=MFA_OPTIONS, default="deshabilitado")
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario'

    def __str__(self):
        return f"{self.username} - {self.nombre} {self.apellido}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        if not self.password:
            return False
        return check_password(raw_password, self.password)

    # traté de corregir el sync porque literalmente no sincroniza
    def sync_to_auth_user(self, request=None):
        try:
            auth_user = User.objects.filter(username=self.username).first()
            if auth_user:
                auth_user.email = self.email or ''
                auth_user.first_name = self.nombre or ''
                auth_user.last_name = self.apellido or ''
                auth_user.is_active = (self.estado == 'activo')
                if self.password and not auth_user.check_password(self.password):
                    if self.password.startswith('pbkdf2_'):
                        auth_user.password = self.password
                    else:
                        auth_user.set_password(self.password)
                # Actualizar username si cambió
                if auth_user.username != self.username:
                    auth_user.username = self.username
                auth_user.save()
                # Actualiza la sesión si corresponde
                if request is not None and request.user.id == auth_user.id:
                    update_session_auth_hash(request, auth_user)
            else:
                auth_user = User.objects.create_user(
                    username=self.username,
                    email=self.email or '',
                    first_name=self.nombre or '',
                    last_name=self.apellido or '',
                    is_active=(self.estado == 'activo')
                )
                if self.password:
                    if self.password.startswith('pbkdf2_'):
                        auth_user.password = self.password
                        auth_user.save()
                    else:
                        auth_user.set_password(self.password)
                        auth_user.save()
            auth_user.groups.clear()
            try:
                group = Group.objects.get(name=self.rol)
                auth_user.groups.add(group)
            except Group.DoesNotExist:
                pass
            return auth_user
        except Exception as e:
            print(f"Error sincronizando usuario {self.username}: {e}")
            return None

    # save admite rqeuest
    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Permite pasar request si es necesario
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)
        self.sync_to_auth_user(request=request)


class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    sku = models.CharField(unique=True, max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    uom_compra = models.CharField(max_length=45, blank=True, null=True)
    uom_venta = models.CharField(max_length=45, blank=True, null=True)
    factor_conversion = models.IntegerField(blank=True, null=True)
    impuesto_iva = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    perishable = models.IntegerField(blank=True, null=True)
    lote = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Producto'

    def __str__(self):
        return f"{self.sku} - {self.nombre}"


class Proveedor(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
        ("bloqueado", "Bloqueado"),
    ]

    idProveedor = models.AutoField(primary_key=True)
    rut_nif = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=255)
    nombre_fantasia = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=254)
    pais = models.CharField(max_length=64, default="Chile")
    condiciones_pago = models.CharField(max_length=45, blank=True, null=True)
    moneda = models.CharField(max_length=8, default="CLP")
    estado = models.CharField(max_length=15, choices=ESTADOS, default="activo")
    usuario = models.ForeignKey(
        Usuario, models.DO_NOTHING, db_column="Usuario_idUsuario", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Proveedor"

    def __str__(self):
        return self.razon_social


class ProductoProveedor(models.Model):
    TIPOS_MOVIMIENTO = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
        ("ajuste", "Ajuste"),
    ]
    idProducto_Proveedor = models.AutoField(primary_key=True)
    tipo_movimiento = models.CharField(max_length=100, choices=TIPOS_MOVIMIENTO, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    fecha_movimiento = models.DateTimeField(blank=True, null=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='Producto_idProducto')
    proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='Proveedor_idProveedor')

    class Meta:
        managed = False
        db_table = 'Producto_Proveedor'


class Bodega(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]
    idbodega = models.AutoField(db_column='idBodega', primary_key=True)
    nombre = models.CharField(max_length=120, unique=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    capacidad = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="activo")

    class Meta:
        managed = False
        db_table = 'bodega'


class Categoria(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]
    idCategoria = models.AutoField(db_column='idCategoria', primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=False, null=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="activo")

    class Meta:
        managed = False
        db_table = 'categoria'


class Cliente(models.Model):
    idcliente = models.AutoField(db_column='idCliente', primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Costo(models.Model):
    idcosto = models.AutoField(db_column='idCosto', primary_key=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='Producto_idProducto')

    class Meta:
        managed = False
        db_table = 'costo'
        unique_together = (('idcosto', 'producto'),)


class ListarPrecios(models.Model):
    idlistarprecios = models.AutoField(db_column='idListarPrecios', primary_key=True)
    canal = models.CharField(db_column='Canal', max_length=50, blank=True, null=True)
    temporada = models.CharField(db_column='Temporada', max_length=45, blank=True, null=True)
    valor = models.IntegerField(db_column='Valor', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='Cliente_idCliente')

    class Meta:
        managed = False
        db_table = 'listarprecios'
        unique_together = (('idlistarprecios', 'cliente'),)


class MovimientoInventario(models.Model):
    idmovimiento = models.AutoField(db_column='idMovimientoInventario', primary_key=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    bodega = models.ForeignKey(Bodega, models.DO_NOTHING, db_column='Bodega_idBodega', null=True, blank=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='Producto_idProducto')

    class Meta:
        managed = False
        db_table = 'movimientoinventario'
        unique_together = (('idmovimiento', 'bodega', 'producto'),)


class OrdenDeCompra(models.Model):
    ESTADOS = [
        ("no_iniciado", "No iniciado"),
        ("en_proceso", "En proceso"),
        ("cerrada", "Cerrada"),
    ]
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="no_iniciado")
    monto_total = models.IntegerField(blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column="proveedor_id_proveedor")

    class Meta:
        managed = False
        db_table = 'ordendecompra'
        unique_together = (('id', 'proveedor'),)


class OrdenProduccion(models.Model):
    id = models.AutoField(primary_key=True)
    fechainicio = models.DateField(db_column='fechaInicio', blank=True, null=True)
    fechafin = models.DateField(db_column='fechaFin', blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Usuario_id')
    producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='Producto_idProducto')

    class Meta:
        managed = False
        db_table = 'ordenproduccion'
        unique_together = (('id', 'usuario', 'producto'),)


class Pedido(models.Model):
    idpedido = models.AutoField(db_column='idPedido', primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    monto_total = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Usuario_id')
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='Cliente_idCliente')
    ordendecompra = models.ForeignKey(OrdenDeCompra, models.DO_NOTHING, db_column='OrdendeCompra_id')

    class Meta:
        managed = False
        db_table = 'pedido'
        unique_together = (('idpedido', 'usuario', 'cliente', 'ordendecompra'),)
