from django import forms
from django.core.exceptions import ValidationError
from dispositivos.models import (
    Usuario, Producto, Proveedor, ProductoProveedor, 
    MovimientoInventario, OrdenDeCompra, Costo, ListarPrecios, Pedido
)


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Verificar si el username ya existe
        qs = Usuario.objects.filter(username=username)
        
        # Si estamos editando, excluir el registro actual
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError(f"El username '{username}' ya está en uso.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Verificar si el email ya existe
        qs = Usuario.objects.filter(email=email)
        
        # Si estamos editando, excluir el registro actual
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError(f"El email '{email}' ya está en uso.")
        
        return email


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
