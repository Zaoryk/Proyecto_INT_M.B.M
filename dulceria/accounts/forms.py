from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
import re
from dispositivos.models import Usuario
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Usuario o email"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Contraseña"
        })
def validar_password(value):
    if len(value) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("Debe contener al menos una letra mayúscula.")
    if not re.search(r"[a-z]", value):
        raise ValidationError("Debe contener al menos una letra minúscula.")
    if not re.search(r"\d", value):
        raise ValidationError("Debe contener al menos un número.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise ValidationError("Debe contener al menos un carácter especial (!@#$ etc).")

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese una contraseña segura'}),
        label="Contraseña",
        validators=[validar_password]
    )

    class Meta:
        model = Usuario
        fields = '__all__'