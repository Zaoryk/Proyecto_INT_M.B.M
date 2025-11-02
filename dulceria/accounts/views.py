from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dispositivos.models import Usuario

def login_view(request):
    """
    Vista de login híbrido:
    - Acepta usuarios de Django (User)
    - Acepta usuarios de la tabla Usuario (MySQL)
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        next_url = request.POST.get('next') or request.GET.get('next')

        # 1️⃣ Intentar autenticación con usuarios de Django
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            return redirect(next_url or 'dashboard')

        # 2️⃣ Intentar autenticación con tu tabla Usuario
        try:
            u = Usuario.objects.get(username__iexact=username)
            if (u.estado or '').lower() != 'activo':
                messages.error(request, "Tu usuario está inactivo o bloqueado.")
            elif (u.password or '').strip() == password:
                request.session['usuario_id'] = u.idUsuario
                request.session['usuario_nombre'] = u.nombre or u.username
                request.session['usuario_rol'] = u.rol
                messages.success(request, f"Bienvenido {u.nombre or u.username}")
                return redirect(next_url or 'dashboard')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")

    return render(request, 'accounts/login.html')


def dashboard(request):
    """
    Mantiene el dashboard original, con contador de visitas
    y muestra nombre del usuario (de Django o de tu tabla).
    """
    # Contador de visitas
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1

    # Nombre del usuario según el origen
    if request.user.is_authenticated:
        nombre = request.user.username
    else:
        nombre = request.session.get('usuario_nombre')

    return render(request, 'dispositivos/dashboard.html', {
        'visitas': visitas,
        'nombre': nombre,
    })


def logout_view(request):
    """
    Cierra sesión para ambos tipos de usuario.
    """
    logout(request)
    request.session.flush()
    return redirect('login')
