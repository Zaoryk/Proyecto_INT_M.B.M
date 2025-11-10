from django import forms
import re
from django.core.exceptions import ValidationError
from dispositivos.models import (
    Usuario, Producto, Proveedor, ProductoProveedor, 
    MovimientoInventario, OrdenDeCompra, Costo, ListarPrecios, Pedido, Categoria, Bodega
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
        fields = '__all__'  # Incluye todos los campos actuales y nuevos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Categorías dinámicas
        categorias_db = Producto.objects.values_list('categoria', flat=True).distinct()
        categorias_validas = sorted(set([c.strip() for c in categorias_db if c and c.strip()]))
        choices = [('', 'Seleccione...')] + [(c, c) for c in categorias_validas] + [("Otras", "Otra...")]
        self.fields['categoria'] = forms.ChoiceField(
            choices=choices,
            required=False,
            widget=forms.Select(attrs={
                'class': 'form-select',
                'id': 'categoriaSelect'
            })
        )
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
        custom_msgs = {
            "nombre": "Debes ingresar un nombre.",
            "categoria": "Debes seleccionar o ingresar una categoría.",
            "uom_compra": "Debes seleccionar unidad de compra.",
            "uom_venta": "Debes seleccionar unidad de venta.",
            "stock_minimo": "Debes ingresar el stock mínimo."
        }
        if categoria == "Otras":
            if not categoria_nueva or not categoria_nueva.strip():
                self.add_error("categoria_nueva", "Debe ingresar un nombre para la nueva categoría.")
            else:
                cleaned["categoria"] = categoria_nueva.strip()
        for field, msg in custom_msgs.items():
            if not cleaned.get(field):
                self.add_error(field, msg)
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
            'rut_nif': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'nombre_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'pais': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'condiciones_pago': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'moneda': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'estado': forms.Select(attrs={'class': 'form-select', 'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut_nif")
        email = cleaned_data.get("email")

        if not rut:
            self.add_error("rut_nif", "El RUT/NIF es obligatorio.")
        if not email:
            self.add_error("email", "El correo electrónico es obligatorio.")

        return cleaned_data


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

# PARA CRUDS PARA BACK END BORRAR DESPUES
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        
        if not nombre:
            raise ValidationError("El nombre es obligatorio.")
        
        if len(nombre) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        
        if len(nombre) > 100:
            raise ValidationError("El nombre no puede superar 100 caracteres.")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-]+$', nombre):
            raise ValidationError("El nombre solo puede contener letras, números, espacios y guiones.")
        
        qs = Categoria.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(f"Ya existe una categoría con el nombre '{nombre}'.")
        
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        
        if not descripcion:
            raise ValidationError("La descripción es obligatoria.")
        if len(descripcion) < 10:
            raise ValidationError("La descripción debe tener al menos 10 caracteres.")
        if len(descripcion) > 255:
            raise ValidationError("La descripción no puede superar 255 caracteres.")
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-]+$', descripcion):
            raise ValidationError("La descripcion solo puede contener letras, números, espacios y guiones.")
        
        return descripcion


class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        
        if not nombre:
            raise ValidationError("El nombre es obligatorio.")
        
        if len(nombre) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        
        if len(nombre) > 120:
            raise ValidationError("El nombre no puede superar 120 caracteres.")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-]+$', nombre):
            raise ValidationError("El nombre solo puede contener letras, números, espacios y guiones.")
        
        qs = Bodega.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError(f"Ya existe una bodega con el nombre exacto '{nombre}'.")
        
        return nombre
    
    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion', '').strip()
        
        # NUEVO: Campo obligatorio
        if not ubicacion:
            raise ValidationError("La ubicación es obligatoria.")
        
        if len(ubicacion) > 255:
            raise ValidationError("La ubicación no puede superar 255 caracteres.")
        
        return ubicacion
    
    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        
        # NUEVO: Campo obligatorio y validación mejorada
        if capacidad is None or capacidad == '':
            raise ValidationError("La capacidad es obligatoria.")
        
        try:
            capacidad = int(capacidad)
        except (ValueError, TypeError):
            raise ValidationError("La capacidad debe ser un número válido.")
        
        if capacidad <= 0:
            raise ValidationError("La capacidad debe ser mayor a 0.")
        
        if capacidad > 999999:
            raise ValidationError("La capacidad máxima es 999,999 unidades.")
        
        return capacidad