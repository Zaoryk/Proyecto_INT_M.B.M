from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import RoleModulePermission
from dispositivos.models import (
    Usuario, Producto, Proveedor, ProductoProveedor, Bodega, Cliente, 
    Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, 
    OrdenProduccion, Pedido
)

class PermissionMixin:
    """
    Mixin para controlar permisos basados en roles y módulos
    """
    module_code = None 
    
    def has_module_permission(self, request):
        """Verifica si el usuario tiene permiso para ver el módulo"""
        if request.user.is_superuser:
            return True
        
        if not self.module_code:
            return False
            
        # Verificar permisos del rol
        return RoleModulePermission.objects.filter(
            role__group__in=request.user.groups.all(),
            module__code=self.module_code,
            can_view=True
        ).exists()
    
    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        
        if not self.module_code:
            return False
            
        return RoleModulePermission.objects.filter(
            role__group__in=request.user.groups.all(),
            module__code=self.module_code,
            can_add=True
        ).exists()
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        if not self.module_code:
            return False
            
        return RoleModulePermission.objects.filter(
            role__group__in=request.user.groups.all(),
            module__code=self.module_code,
            can_change=True
        ).exists()
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        if not self.module_code:
            return False
            
        return RoleModulePermission.objects.filter(
            role__group__in=request.user.groups.all(),
            module__code=self.module_code,
            can_delete=True
        ).exists()

# Forms actualizados
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo and stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo.")
        return stock_minimo
        
    def clean_factor_conversion(self):
        factor_conversion = self.cleaned_data.get('factor_conversion')
        if factor_conversion and factor_conversion < 0:
            raise ValidationError("El factor de conversión no puede ser negativo.")
        return factor_conversion
        
    def clean_impuesto_iva(self):
        impuesto_iva = self.cleaned_data.get('impuesto_iva')
        if impuesto_iva and impuesto_iva < 0:
            raise ValidationError("El impuesto IVA no puede ser negativo.")
        return impuesto_iva

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoProveedorForm(forms.ModelForm):
    class Meta:
        model = ProductoProveedor
        fields = '__all__'
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad and cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        return cantidad

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

# Forms existentes que se mantienen
class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')
        producto = cleaned_data.get('producto')
            
        if tipo == "Salida" and producto and cantidad:
            # Esta validación podría necesitar ajustarse según la nueva estructura
            if hasattr(producto, 'stock') and cantidad > producto.stock:
                raise ValidationError({
                    'cantidad': f"No puedes registrar una salida mayor al stock disponible."
                })
        
        if cantidad and cantidad <= 0:
            raise ValidationError({
                'cantidad': "La cantidad debe ser un número positivo mayor a cero."
            })
        
        return cleaned_data

class OrdenDeCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenDeCompra
        fields = '__all__'
    
    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if monto_total and monto_total < 0:
            raise ValidationError("El monto total no puede ser negativo.")
        return monto_total

class CostoForm(forms.ModelForm):
    class Meta:
        model = Costo
        fields = '__all__'
    
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto and monto < 0:
            raise ValidationError("El monto del costo no puede ser negativo.")
        return monto

class ListarPreciosForm(forms.ModelForm):
    class Meta:
        model = ListarPrecios
        fields = '__all__'
    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor and valor < 0:
            raise ValidationError("El valor no puede ser negativo.")
        return valor

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
    
    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if monto_total and monto_total < 0:
            raise ValidationError("El monto total no puede ser negativo.")
        return monto_total

# Inlines
class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 1
    form = ProductoProveedorForm

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 1
    fields = ("tipo", "fecha", "cantidad", "bodega")

# Admin classes para las nuevas tablas
@admin.register(Usuario)
class UsuarioAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'usuarios'
    form = UsuarioForm
    list_display = ("username", "email", "nombre", "apellido", "rol", "estado", "mfa_habilitado")
    list_filter = ("rol", "estado", "mfa_habilitado")
    search_fields = ("username", "email", "nombre", "apellido")

@admin.register(Producto)
class ProductoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'productos'
    form = ProductoForm
    list_display = ("sku", "nombre", "categoria", "uom_compra", "uom_venta", "stock_minimo")
    list_filter = ("categoria",)
    search_fields = ("sku", "nombre", "categoria")
    inlines = [ProductoProveedorInline, MovimientoInventarioInline]

@admin.register(Proveedor)
class ProveedorAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'proveedores'
    form = ProveedorForm
    list_display = ("rut_nif", "razon_social", "nombre_fantasia", "email", "estado", "usuario")
    list_filter = ("estado", "pais")
    search_fields = ("rut_nif", "razon_social", "nombre_fantasia", "email")
    inlines = [ProductoProveedorInline]

@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'producto_proveedor'
    form = ProductoProveedorForm
    list_display = ("producto", "proveedor", "tipo_movimiento", "cantidad", "fecha_movimiento")
    list_filter = ("tipo_movimiento", "fecha_movimiento")
    search_fields = ("producto__nombre", "proveedor__razon_social")

# Admin classes existentes que se mantienen (con pequeños ajustes)
@admin.register(Bodega)
class BodegaAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'bodegas'
    list_display = ("nombre", "ubicacion")
    search_fields = ("nombre", "ubicacion")

@admin.register(Cliente)
class ClienteAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'clientes'
    list_display = ("nombre", "tipo")
    list_filter = ("tipo",)
    search_fields = ("nombre",)

@admin.register(Costo)
class CostoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'costos'
    form = CostoForm
    list_display = ("tipo", "monto", "producto")
    list_filter = ("tipo", "producto")
    search_fields = ("tipo", "producto__nombre")

@admin.register(ListarPrecios)
class ListarPreciosAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'listar_precios'
    form = ListarPreciosForm
    list_display = ("cliente", "canal", "temporada", "valor")
    list_filter = ("canal", "temporada", "cliente")
    search_fields = ("cliente__nombre", "canal")

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'movimiento_inventario'
    form = MovimientoInventarioForm
    list_display = ("tipo", "fecha", "producto", "cantidad", "bodega")
    list_filter = ("tipo", "fecha", "bodega")
    search_fields = ("producto__nombre", "bodega__nombre")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['producto']
        return []

@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'orden_compra'
    form = OrdenDeCompraForm
    list_display = ("id", "proveedor", "fecha", "estado", "monto_total")
    list_filter = ("estado", "fecha", "proveedor")
    search_fields = ("id", "proveedor__razon_social")
    actions = ["marcar_en_proceso", "marcar_cerrada", "marcar_no_iniciado"]

    @admin.action(description="Marcar seleccionadas como No iniciadas")
    def marcar_no_iniciado(self, request, queryset):
        updated = queryset.update(estado="no_iniciado")
        self.message_user(request, f"{updated} órdenes marcadas como 'No iniciadas'.")

    @admin.action(description="Marcar seleccionadas como En Proceso")
    def marcar_en_proceso(self, request, queryset):
        updated = queryset.update(estado="en_proceso")
        self.message_user(request, f"{updated} órdenes marcadas como 'En proceso'.")

    @admin.action(description="Marcar seleccionadas como Cerrada")
    def marcar_cerrada(self, request, queryset):
        updated = queryset.update(estado="cerrada")
        self.message_user(request, f"{updated} órdenes marcadas como 'Cerradas'.")

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'orden_produccion'
    list_display = ("id", "fechainicio", "fechafin", "estado", "producto", "usuario")
    list_filter = ("estado", "fechainicio", "fechafin")
    search_fields = ("producto__nombre", "usuario__nombre")

@admin.register(Pedido)
class PedidoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'pedidos'
    form = PedidoForm
    list_display = ("idpedido", "fecha", "cliente", "monto_total", "usuario")
    list_filter = ("fecha", "cliente", "usuario")
    search_fields = ("cliente__nombre", "usuario__nombre")