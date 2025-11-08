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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from dispositivos.views import CATEGORIAS
        choices = [('', 'Seleccione...')] + list(CATEGORIAS)
        data = None
        if args:
            data = args[0]
        if data and hasattr(data, 'get'):
            val = data.get('categoria')
            if val and val not in [v for v, t in CATEGORIAS] and val != "":
                choices.append((val, val))
        self.fields['categoria'] = forms.ChoiceField(
            choices=choices, required=False,
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'categoriaSelect'})
        )
        self.fields['nombre'].required = False
        self.fields['uom_compra'].required = False
        self.fields['uom_venta'].required = False
        self.fields['stock_minimo'].required = False

    def clean(self):
        cleaned = super().clean()
        custom_msgs = {
            "nombre": "Debes ingresar un nombre.",
            "categoria": "Debes seleccionar o ingresar una categoría.",
            "uom_compra": "Debes seleccionar unidad de compra.",
            "uom_venta": "Debes seleccionar unidad de venta.",
            "stock_minimo": "Debes ingresar el stock mínimo."
        }
        for field, msg in custom_msgs.items():
            if not self.cleaned_data.get(field):
                self.add_error(field, msg)
        return cleaned

    class Meta:
        model = Producto
        fields = '__all__'

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProductoProveedorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODOS los campos requeridos custom
        self.fields['fecha_movimiento'].required = False
        self.fields['tipo_movimiento'].required = False
        self.fields['producto'].required = False
        self.fields['cantidad'].required = False
        self.fields['proveedor'].required = False

    def clean(self):
        cleaned = super().clean()
        required = {
            'fecha_movimiento': 'Debes ingresar la fecha del movimiento.',
            'tipo_movimiento': 'Debes seleccionar el tipo de movimiento.',
            'producto': 'Debes seleccionar un producto.',
            'cantidad': 'Debes ingresar la cantidad.',
            'proveedor': 'Debes seleccionar un proveedor.',
        }
        for field, msg in required.items():
            if not self.cleaned_data.get(field):
                self.add_error(field, msg)
        # Lógica adicional para cantidad positiva
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad is not None and cantidad <= 0:
            self.add_error("cantidad", "La cantidad debe ser mayor a cero.")
        return cleaned

    class Meta:
        model = ProductoProveedor
        fields = '__all__'



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

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'avatar']

    avatar = forms.ImageField(required=False)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if hasattr(avatar, 'content_type'):
                if avatar.content_type not in ['image/png', 'image/jpeg', 'image/jpg']:
                    raise forms.ValidationError("Solo se aceptan imágenes PNG/JPG/JPEG.")
                # Valida tamano maximo (2MB por ejemplo)
                if avatar.size > 2 * 1024 * 1024:
                    raise forms.ValidationError("La imagen no debe superar 2MB.")
        return avatar


    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Usuario.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(f"El email '{email}' ya está en uso.")
        return email
    
class PasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}),
        label="Nueva contraseña",
        min_length=8
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
        label="Confirmar contraseña",
        min_length=8
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("new_password1")
        p2 = cleaned.get("new_password2")
        if p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        import re
        # Validación de mayúsculas y números
        if not re.search(r"[A-Z]", p1):
            raise ValidationError("Debe contener al menos una mayúscula.")
        if not re.search(r"\d", p1):
            raise ValidationError("Debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", p1):
            raise ValidationError("Debe contener al menos un carácter especial.")
        return cleaned

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual', 'class': 'form-control'}),
        label="Contraseña actual",
        min_length=8
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña', 'class': 'form-control'}),
        label="Nueva contraseña",
        min_length=8
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'class': 'form-control'}),
        label="Confirmar contraseña",
        min_length=8
    )

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)   # Recibe usuario por instancia
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        old = cleaned.get("old_password")
        p1 = cleaned.get("new_password1")
        p2 = cleaned.get("new_password2")
        # Validar antiguo usando el método del modelo
        if self.usuario and not self.usuario.check_password(old):
            raise ValidationError("La contraseña actual es incorrecta.")
        if p1 != p2:
            raise ValidationError("Las contraseñas nuevas no coinciden.")
        if not re.search(r"[A-Z]", p1 or ""):
            raise ValidationError("Debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", p1 or ""):
            raise ValidationError("Debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", p1 or ""):
            raise ValidationError("Debe contener al menos un carácter especial.")
        return cleaned
