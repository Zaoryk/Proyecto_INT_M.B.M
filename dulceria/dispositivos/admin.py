from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import RoleModulePermission
from dispositivos.models import Bodega, Cliente, Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, OrdenProduccion, Pedido, Producto, Proveedor, Usuario

# ========== MIXIN PARA CONTROL DE PERMISOS ==========

class PermissionMixin:
    """
    Mixin para controlar permisos basados en roles y módulos
    """
    module_code = None  # Debe ser definido en cada admin
    
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

# ========== FORMS CON VALIDACIONES ==========

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio < 0:
            raise ValidationError("El precio no puede ser negativo.")
        return precio
        
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        return stock

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')
        producto = cleaned_data.get('producto')
            
        # Validación de salida mayor al stock disponible
        if tipo == "Salida" and producto and cantidad:
            if cantidad > producto.stock:
                raise ValidationError({
                    'cantidad': f"No puedes registrar una salida mayor al stock disponible. Stock actual: {producto.stock}"
                })
        
        # Validación por cantidad positiva
        if cantidad and cantidad <= 0:
            raise ValidationError({
                'cantidad': "La cantidad debe ser un número positivo mayor a cero."
            })
        
        return cleaned_data

# ========== INLINES SIMPLES ==========

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 1
    fields = ("tipo", "fecha", "cantidad")

# ========== ADMIN CLASSES CON PERMISOS ==========

@admin.register(Producto)
class ProductoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'productos'
    form = ProductoForm
    list_display = ("nombre", "precio", "stock")
    search_fields = ("nombre",)
    inlines = [MovimientoInventarioInline]

@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'orden_compra'
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

# ========== REGISTROS BÁSICOS CON PERMISOS ==========

@admin.register(Cliente)
class ClienteAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'clientes'

@admin.register(Bodega)
class BodegaAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'bodegas'

@admin.register(ListarPrecios)
class ListarPreciosAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'listar_precios'

@admin.register(Costo)
class CostoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'costos'

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'movimiento_inventario'

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'orden_produccion'

@admin.register(Pedido)
class PedidoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'pedidos'

@admin.register(Proveedor)
class ProveedorAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'proveedores'

@admin.register(Usuario)
class UsuarioAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'usuarios'