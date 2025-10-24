from django import forms
from dispositivos.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellido', 'rol', 'estado', 'mfa_habilitado']
