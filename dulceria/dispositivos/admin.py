from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from dispositivos.models import Bodega, Cliente, Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, OrdenProduccion, Pedido, Producto, Proveedor, Usuario

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
        
        # validación de sklalida mayor al stock disponible
        if tipo == "Salida" and producto and cantidad:
            if cantidad > producto.stock:
                raise ValidationError({
                    'cantidad': f"No puedes registrar una salida mayor al stock disponible. Stock actual: {producto.stock}"
                })
        
        # validacion por cantidad positiva, aka mayor a 0
        if cantidad and cantidad <= 0:
            raise ValidationError({
                'cantidad': "La cantidad debe ser un número positivo mayor a cero."
            })
        
        return cleaned_data

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 1
    fields = ("tipo", "fecha", "cantidad", "bodega", "producto")

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        #peero si tamos editando un producto en especficio, esto limita las opciones
        if obj and isinstance(obj, Producto):
            formset.form.base_fields['producto'].queryset = Producto.objects.filter(idproducto=obj.idproducto)
            formset.form.base_fields['producto'].initial = obj
            return formset

#validacion de orden de compra :3, ya que no puede ser un monto negativo
class OrdenDeCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenDeCompra
        fields = '__all__'
    
    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if monto_total and monto_total < 0:
            raise ValidationError("El monto total no puede ser negativo.")
        return monto_total

# vlaidación de costo
class CostoForm(forms.ModelForm):
    class Meta:
        model = Costo
        fields = '__all__'
    
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto and monto < 0:
            raise ValidationError("El monto del costo no puede ser negativo.")
        return monto
# nada puede ser monto negativo asi que ,,,, lol
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
# admin para producto con inline
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm
    list_display = ("nombre", "precio", "stock", "lote", "fecha_vencimiento")
    list_filter = ("fecha_vencimiento",)
    search_fields = ("nombre", "lote")
    inlines = [MovimientoInventarioInline]
    
    def get_inline_instances(self, request, obj=None):
        # esto sirve par m ostrar el inline si estamos editando UN producto existente
        if obj:
            return [MovimientoInventarioInline(self.model, self.admin_site)]
        return []

# admin para OrdenDeCompra con validaciones
@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(admin.ModelAdmin):
    form = OrdenDeCompraForm
    list_display = ("id", "proveedor", "fecha", "estado", "monto_total")
    list_filter = ("estado", "fecha", "proveedor")
    search_fields = ("id", "proveedor__nombre")
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

# admin para Costo con validaciones
@admin.register(Costo)
class CostoAdmin(admin.ModelAdmin):
    form = CostoForm
    list_display = ("tipo", "monto", "producto")
    list_filter = ("tipo", "producto")
    search_fields = ("tipo", "producto__nombre")

#admin para ListarPrecios con validaciones
@admin.register(ListarPrecios)
class ListarPreciosAdmin(admin.ModelAdmin):
    form = ListarPreciosForm
    list_display = ("cliente", "canal", "temporada", "valor")
    list_filter = ("canal", "temporada", "cliente")
    search_fields = ("cliente__nombre", "canal")

#amin para Pedido con validaciones
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    form = PedidoForm
    list_display = ("idpedido", "fecha", "cliente", "monto_total", "usuario")
    list_filter = ("fecha", "cliente", "usuario")
    search_fields = ("cliente__nombre", "usuario__nombre")

#admin para MovimientoInventario con validaciones
@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    form = MovimientoInventarioForm
    list_display = ("tipo", "fecha", "producto", "cantidad", "bodega")
    list_filter = ("tipo", "fecha", "bodega")
    search_fields = ("producto__nombre", "bodega__nombre")
    
    def get_readonly_fields(self, request, obj=None):
        # si el movimiento existe solamente hacerlo modo lectura
        if obj:
            return ['producto']
        return []

# registros con validaciones basicas
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "rol")
    list_filter = ("rol",)
    search_fields = ("nombre", "email")

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "contacto")
    search_fields = ("nombre", "email")

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion")
    search_fields = ("nombre", "ubicacion")

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo")
    list_filter = ("tipo",)
    search_fields = ("nombre",)

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ("id", "fechainicio", "fechafin", "estado", "producto", "usuario")
    list_filter = ("estado", "fechainicio", "fechafin")
    search_fields = ("producto__nombre", "usuario__nombre")