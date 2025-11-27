import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password


class FirstLoginPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")

        if not password:
            raise forms.ValidationError("Debes ingresar una contraseña.")

        validate_password(password, self.user)

        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("La contraseña debe incluir al menos una letra minúscula.")
        if not re.search(r"\d", password):
            raise forms.ValidationError("La contraseña debe incluir al menos un dígito numérico.")
        if not re.search(r"[^\w\s]", password):
            raise forms.ValidationError("La contraseña debe incluir al menos un carácter especial.")

        return password
