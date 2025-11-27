from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from dispositivos.models import Usuario
from .forms_temp_password import FirstLoginPasswordChangeForm


@login_required
def force_password_change(request):
    usuario = Usuario.objects.filter(email=request.user.email).first()

    if usuario and not usuario.password_temporal:
       return redirect('dashboard')

    if request.method == "POST":
        form = FirstLoginPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            if usuario:
                usuario.password_temporal = False
                usuario.password = user.password
                usuario.save()
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect('dashboard')
    else:
        form = FirstLoginPasswordChangeForm(user=request.user)

    return render(request, "accounts/force_password_change.html", {"form": form})
