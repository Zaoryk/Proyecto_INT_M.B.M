"""
Backend de autenticación personalizado para permitir login con username o email
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from dispositivos.models import Usuario


class EmailOrUsernameBackend(ModelBackend):
    """
    Backend que permite autenticación con username o email
    Sincroniza automáticamente con la tabla usuario personalizada
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Intentar buscar en la tabla usuario personalizada primero
            # Buscar por username o email
            usuario_custom = Usuario.objects.filter(
                models.Q(username=username) | models.Q(email=username)
            ).first()
            
            if usuario_custom:
                # Verificar si el usuario está activo
                if usuario_custom.estado != 'activo':
                    return None
                
                # Sincronizar con auth_user si no existe
                auth_user = usuario_custom.sync_to_auth_user()
                
                # Verificar contraseña
                if auth_user and auth_user.check_password(password):
                    return auth_user
            
            # Si no se encontró en usuario personalizada, buscar directamente en auth_user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    return None
            
            # Verificar contraseña
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
                
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return None
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# Importar Q para las consultas
from django.db import models