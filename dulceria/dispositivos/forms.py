from django import forms
import re
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
    categoria_nueva = forms.CharField(required=False, label="Nueva categoría")

    class Meta:
        model = Producto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # NO redefinir self.fields['categoria'] como ChoiceField aquí

        # tus reglas de required que ya tenías
        self.fields['nombre'].required = False
        self.fields['uom_compra'].required = False
        self.fields['uom_venta'].required = False
        self.fields['stock_minimo'].required = False

        for fname in [
            'ean_upc', 'marca', 'modelo', 'descripcion',
            'stock_maximo', 'punto_reorden',
            'costo_estandar', 'costo_promedio', 'precio_venta',
            'imagen_url', 'ficha_tecnica_url'
        ]:
            if fname in self.fields:
                self.fields[fname].required = False

    def clean(self):
        cleaned = super().clean()
        categoria = cleaned.get("categoria")
        categoria_nueva = cleaned.get("categoria_nueva")

        # si eligió "Otras" en el select, en el POST vendrá categoria = "Otras"
        if categoria == "Otras":
            if not categoria_nueva or not categoria_nueva.strip():
                self.add_error("categoria_nueva", "Debe ingresar un nombre para la nueva categoría.")
            else:
                cleaned["categoria"] = categoria_nueva.strip()

        # validaciones mínimas
        if not cleaned.get("categoria"):
            self.add_error("categoria", "Debes seleccionar o ingresar una categoría.")
        if not cleaned.get("nombre"):
            self.add_error("nombre", "Debes ingresar un nombre.")
        if not cleaned.get("uom_compra"):
            self.add_error("uom_compra", "Debes seleccionar unidad de compra.")
        if not cleaned.get("uom_venta"):
            self.add_error("uom_venta", "Debes seleccionar unidad de venta.")
        if not cleaned.get("stock_minimo"):
            self.add_error("stock_minimo", "Debes ingresar el stock mínimo.")

        return cleaned

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'rut_nif',
            'razon_social',
            'nombre_fantasia',
            'email',
            'pais',
            'condiciones_pago',
            'moneda',
            'estado',
        ]
        widgets = {
            'rut_nif': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'maxlength': 20,
            }),
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'maxlength': 255,
            }),
            'nombre_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 255,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required': True,
                'maxlength': 255,   # input HTML
            }),
            'pais': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'condiciones_pago': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'moneda': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
        }

    def clean_estado(self):
        estado = (self.cleaned_data.get("estado") or "").lower()
        # Normaliza y valida contra las choices del modelo
        valid_values = [choice[0] for choice in Proveedor.ESTADOS]
        if estado not in valid_values:
            raise forms.ValidationError("El estado seleccionado no es válido.")
        return estado

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut_nif")
        email = cleaned_data.get("email")

        if not rut:
            self.add_error("rut_nif", "El RUT/NIF es obligatorio.")
        if not email:
            self.add_error("email", "El correo electrónico es obligatorio.")

        if email and len(email) > 254:
            self.add_error("email", "El correo electrónico no debe superar los 254 caracteres.")

        return cleaned_data

class ProductoProveedorForm(forms.ModelForm):
    class Meta:
        model = ProductoProveedor
        fields = [
            'fecha_movimiento',
            'tipo_movimiento',
            'producto',
            'proveedor',
            'bodega',
            'cantidad',
            'manejo_lotes',
            'manejo_series',
            'perecible',
            'lote',
            'serie',
            'fecha_vencimiento',
            'doc_referencia',
            'motivo',
            'observaciones',
        ]
        widgets = {
            'fecha_movimiento': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_movimiento': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'doc_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        fecha = cleaned.get("fecha_movimiento")
        tipo = cleaned.get("tipo_movimiento")
        producto = cleaned.get("producto")
        cantidad = cleaned.get("cantidad")
        proveedor = cleaned.get("proveedor")
        perecible = cleaned.get("perecible")
        fecha_vencimiento = cleaned.get("fecha_vencimiento")

        if not fecha:
            self.add_error("fecha_movimiento", "Debes ingresar la fecha del movimiento.")
        if not tipo:
            self.add_error("tipo_movimiento", "Debes seleccionar el tipo de movimiento.")
        if not producto:
            self.add_error("producto", "Debes seleccionar un producto.")
        if not cantidad or cantidad <= 0:
            self.add_error("cantidad", "La cantidad debe ser mayor a cero.")
        if not proveedor:
            self.add_error("proveedor", "Debes seleccionar un proveedor.")

        if perecible and fecha_vencimiento:
            from datetime import date
            if fecha_vencimiento < date.today():
                self.add_error("fecha_vencimiento", "La fecha de vencimiento no puede ser anterior a hoy.")

        return cleaned



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