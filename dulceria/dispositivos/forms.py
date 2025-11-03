from django import forms
from dispositivos.models import Usuario, Proveedor, Producto, ProductoProveedor

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'nombre', 'apellido', 'rol', 'estado', 'mfa_habilitado']


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        rut_nif = cleaned_data.get('rut_nif')
        razon_social = cleaned_data.get('razon_social')
        usuario = cleaned_data.get('usuario')
        pais = cleaned_data.get('pais')

        errores = []

        if not rut_nif:
            errores.append("RUT/NIF")
        if not razon_social:
            errores.append("Razón social")
        if not usuario:
            errores.append("Usuario responsable")

        # ⚠️ Ejemplo: si también quieres que el país sea obligatorio, descomenta esta línea:
        # if not pais:

        if errores:
            raise forms.ValidationError(
                f"Campos obligatorios faltantes: {', '.join(errores)}"
            )

        return cleaned_data


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