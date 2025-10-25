from django import forms
from dispositivos.models import Usuario, Proveedor, Producto, ProductoProveedor

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellido', 'rol', 'estado', 'mfa_habilitado']


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['rut_nif', 'razon_social', 'nombre_fantasia', 'email', 'pais', 
                  'condiciones_pago', 'moneda', 'estado', 'usuario']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'categoria', 'uom_compra', 'uom_venta', 
                  'factor_conversion', 'impuesto_iva', 'stock_minimo', 
                  'perishable', 'lote']

class ProductoProveedorForm(forms.ModelForm):
    class Meta:
        model = ProductoProveedor
        fields = ['tipo_movimiento', 'cantidad', 'fecha_movimiento', 'producto', 'proveedor']