from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from dispositivos.models import Usuario
from accounts.models import PasswordResetCode
from django.db.models import Q

# Create your views here.
from django.shortcuts import render
def dashboard(request):
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1
    return render(request, 'accounts/dashboard.html', {'visitas': visitas})

# VIEWS PARA EL RESETEO DE CONTRASEÑA
def password_solicitud(request):
    """
    Vista para solicitar recuperación de contraseña
    Envía código de 6 dígitos al email
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Por favor ingrese un correo electrónico.')
            return render(request, 'accounts/password_solicitud.html')
        
        # Buscar usuario en la tabla personalizada
        usuario = Usuario.objects.filter(
            Q(email=email) | Q(username=email)
        ).first()
        
        if not usuario:
            # Buscar en auth_user
            auth_user = User.objects.filter(
                Q(email=email) | Q(username=email)
            ).first()
            
            if not auth_user:
                messages.error(request, 'No se encontró ningún usuario con ese correo.')
                return render(request, 'accounts/password_solicitud.html')
            
            email_to_use = auth_user.email
        else:
            email_to_use = usuario.email
        
        if not email_to_use:
            messages.error(request, 'Este usuario no tiene un correo registrado.')
            return render(request, 'accounts/password_solicitud.html')
        
        # Crear código de recuperación
        reset_code = PasswordResetCode.create_code(email_to_use)
        
        # Enviar email
        try:
            # Verificar configuración antes de enviar
            if not settings.EMAIL_HOST_USER:
                messages.error(
                    request,
                    'Error de configuración: El servidor de correo no está configurado correctamente. Contacte al administrador.'
                )
                return render(request, 'accounts/password_solicitud.html')
            
            send_mail(
                subject='Código de Recuperación - Dulcería Lilis',
                message=f'''
Hola,

Has solicitado recuperar tu contraseña en Dulcería Lilis.

Tu código de verificación es: {reset_code.code}

Este código es válido por 15 minutos.

Si no solicitaste este código, puedes ignorar este mensaje.

Saludos,
Equipo de Dulcería Lilis
                ''',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email_to_use],
                fail_silently=False,
            )
            
            messages.success(
                request, 
                f'Se ha enviado un código de verificación a {email_to_use}'
            )
            
            # Guardar email en sesión para el siguiente paso
            request.session['reset_email'] = email_to_use
            
            return redirect('password_validar')
            
        except Exception as e:
            # Log del error completo para debugging
            import traceback
            print("="*60)
            print("ERROR AL ENVIAR CORREO:")
            print(traceback.format_exc())
            print("="*60)
            
            messages.error(
                request, 
                f'Error al enviar el correo. Verifica tu configuración de email o contacta al administrador.'
            )
            return render(request, 'accounts/password_solicitud.html')
    
    return render(request, 'accounts/password_solicitud.html')


def password_validar(request):
    """
    Vista para verificar el código de 6 dígitos
    """
    email = request.session.get('reset_email')
    
    if not email:
        messages.error(request, 'Sesión expirada. Por favor solicita un nuevo código.')
        return redirect('password_solicitud')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        if not code:
            messages.error(request, 'Por favor ingrese el código.')
            return render(request, 'accounts/password_validar.html', {'email': email})
        
        # Buscar código válido
        reset_code = PasswordResetCode.objects.filter(
            email=email,
            code=code,
            is_used=False
        ).first()
        
        if not reset_code:
            messages.error(request, 'Código inválido.')
            return render(request, 'accounts/password_validar.html', {'email': email})
        
        if not reset_code.is_valid():
            messages.error(request, 'El código ha expirado. Solicita uno nuevo.')
            return render(request, 'accounts/password_validar.html', {'email': email})
        
        # Código válido - guardar en sesión
        request.session['verified_code'] = code
        
        return redirect('password_cambio')
    
    return render(request, 'accounts/password_validar.html', {'email': email})


def password_cambio(request):
    """
    Vista para establecer nueva contraseña
    """
    email = request.session.get('reset_email')
    verified_code = request.session.get('verified_code')
    
    if not email or not verified_code:
        messages.error(request, 'Sesión inválida. Por favor comienza de nuevo.')
        return redirect('password_solicitud')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        if not password1 or not password2:
            messages.error(request, 'Por favor complete ambos campos.')
            return render(request, 'accounts/password_cambio.html')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'accounts/password_cambio.html')
        
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'accounts/password_cambio.html')
        
        # Buscar y marcar código como usado
        reset_code = PasswordResetCode.objects.filter(
            email=email,
            code=verified_code,
            is_used=False
        ).first()
        
        if not reset_code or not reset_code.is_valid():
            messages.error(request, 'Código inválido o expirado.')
            return redirect('password_solicitud')
        
        # Actualizar contraseña en Usuario personalizado
        usuario = Usuario.objects.filter(email=email).first()
        
        if usuario:
            # Guardar con hash automático (gracias al método save() mejorado)
            usuario.password = password1  # El save() lo hasheará automáticamente
            usuario.save()  # Esto también sincronizará con auth_user
            
            reset_code.mark_as_used()
            
            # Limpiar sesión
            del request.session['reset_email']
            del request.session['verified_code']
            
            messages.success(
                request, 
                'Contraseña actualizada exitosamente. Ya puedes iniciar sesión.'
            )
            return redirect('login')
        else:
            # Actualizar solo en auth_user si no existe en Usuario
            auth_user = User.objects.filter(email=email).first()
            
            if auth_user:
                auth_user.set_password(password1)
                auth_user.save()
                
                reset_code.mark_as_used()
                
                del request.session['reset_email']
                del request.session['verified_code']
                
                messages.success(
                    request, 
                    'Contraseña actualizada exitosamente. Ya puedes iniciar sesión.'
                )
                return redirect('login')
            else:
                messages.error(request, 'Usuario no encontrado.')
                return redirect('password_solicitud')
    
    return render(request, 'accounts/password_cambio.html')

