from django.contrib import admin
from django.core.exceptions import ValidationError, PermissionDenied
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from accounts.models import RoleModulePermission

from dispositivos.models import (
    Bodega, Cliente, Producto, Costo, ListarPrecios, 
    MovimientoInventario, Proveedor, OrdenDeCompra, 
    Usuario, OrdenProduccion, Pedido
)

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
        
        if tipo == "Salida" and producto and cantidad:
            if cantidad > producto.stock:
                raise ValidationError({
                    'cantidad': f"No puedes registrar una salida mayor al stock disponible. Stock actual: {producto.stock}"
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

# ========== INLINES ==========

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    form = MovimientoInventarioForm
    extra = 1
    fields = ("tipo", "fecha", "cantidad", "bodega", "producto")
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        if obj and isinstance(obj, Producto):
            formset.form.base_fields['producto'].queryset = Producto.objects.filter(idproducto=obj.idproducto)
            formset.form.base_fields['producto'].initial = obj
        
        return formset

# ========== ADMIN CLASSES CON PERMISOS ==========

@admin.register(Producto)
class ProductoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'productos'
    form = ProductoForm
    list_display = ("nombre", "precio", "stock", "lote", "fecha_vencimiento")
    list_filter = ("fecha_vencimiento",)
    search_fields = ("nombre", "lote")
    inlines = [MovimientoInventarioInline]
    
    def get_inline_instances(self, request, obj=None):
        if obj and self.has_change_permission(request, obj):
            return [MovimientoInventarioInline(self.model, self.admin_site)]
        return []

@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'orden_compra'
    form = OrdenDeCompraForm
    list_display = ("id", "proveedor", "fecha", "estado", "monto_total")
    list_filter = ("estado", "fecha", "proveedor")
    search_fields = ("id", "proveedor__nombre")
    actions = ["marcar_en_proceso", "marcar_cerrada", "marcar_no_iniciado"]

    @admin.action(description="Marcar seleccionadas como No iniciadas", permissions=['change'])
    def marcar_no_iniciado(self, request, queryset):
        updated = queryset.update(estado="no_iniciado")
        self.message_user(request, f"{updated} órdenes marcadas como 'No iniciadas'.")

    @admin.action(description="Marcar seleccionadas como En Proceso", permissions=['change'])
    def marcar_en_proceso(self, request, queryset):
        updated = queryset.update(estado="en_proceso")
        self.message_user(request, f"{updated} órdenes marcadas como 'En proceso'.")

    @admin.action(description="Marcar seleccionadas como Cerrada", permissions=['change'])
    def marcar_cerrada(self, request, queryset):
        updated = queryset.update(estado="cerrada")
        self.message_user(request, f"{updated} órdenes marcadas como 'Cerradas'.")

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

@admin.register(Pedido)
class PedidoAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'pedidos'
    form = PedidoForm
    list_display = ("idpedido", "fecha", "cliente", "monto_total", "usuario")
    list_filter = ("fecha", "cliente", "usuario")
    search_fields = ("cliente__nombre", "usuario__nombre")

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

# Registros simples con permisos
@admin.register(Usuario)
class UsuarioAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'usuarios'
    list_display = ("nombre", "email", "rol")
    list_filter = ("rol",)
    search_fields = ("nombre", "email")

@admin.register(Proveedor)
class ProveedorAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'proveedores'
    list_display = ("nombre", "email", "contacto")
    search_fields = ("nombre", "email")

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

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(PermissionMixin, admin.ModelAdmin):
    module_code = 'orden_produccion'
    list_display = ("id", "fechainicio", "fechafin", "estado", "producto", "usuario")
    list_filter = ("estado", "fechainicio", "fechafin")
    search_fields = ("producto__nombre", "usuario__nombre")