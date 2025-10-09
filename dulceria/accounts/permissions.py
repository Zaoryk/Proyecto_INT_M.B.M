"""
Utilidades para manejo de permisos y roles en Dulcería Lilis.

Incluye:
- Decoradores para proteger vistas
- Funciones helper para verificar permisos
- Context processors para templates
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from accounts.models import RoleModulePermission


def get_user_role(user):
    """
    Obtiene el rol (Role) del usuario.
    Retorna None si el usuario no tiene rol asignado.
    """
    if not user.is_authenticated:
        return None
    
    # Un usuario debe tener exactamente un grupo/rol
    groups = user.groups.all()
    if groups.exists():
        group = groups.first()  # Tomamos el primer grupo
        return getattr(group, 'role', None)
    
    return None


def has_module_permission(user, module_code, permission_type='view'):
    """
    Verifica si un usuario tiene un permiso específico sobre un módulo.
    
    Args:
        user: Usuario de Django
        module_code: Código del módulo (ej: 'inventarios', 'compras')
        permission_type: Tipo de permiso ('view', 'add', 'change', 'delete')
    
    Returns:
        bool: True si tiene el permiso, False si no
    """
    # Superusuarios tienen todos los permisos
    if user.is_superuser:
        return True
    
    # Obtener el rol del usuario
    role = get_user_role(user)
    if not role:
        return False
    
    # Buscar el permiso específico
    try:
        perm = RoleModulePermission.objects.get(
            role=role,
            module__code=module_code
        )
        
        permission_map = {
            'view': perm.can_view,
            'add': perm.can_add,
            'change': perm.can_change,
            'delete': perm.can_delete
        }
        
        return permission_map.get(permission_type, False)
    
    except RoleModulePermission.DoesNotExist:
        return False


def get_user_modules(user):
    """
    Obtiene todos los módulos a los que el usuario tiene acceso (can_view=True).
    
    Returns:
        QuerySet de Module o lista vacía
    """
    if user.is_superuser:
        from accounts.models import Module
        return Module.objects.all().order_by('order')
    
    role = get_user_role(user)
    if not role:
        return []
    
    # Obtener módulos con permiso de visualización
    perms = RoleModulePermission.objects.filter(
        role=role,
        can_view=True
    ).select_related('module').order_by('module__order')
    
    return [perm.module for perm in perms]


def require_module_permission(module_code, permission_type='view', redirect_url='dashboard'):
    """
    Decorador para proteger vistas que requieren permisos específicos.
    
    Uso:
        @require_module_permission('inventarios', 'add')
        def crear_producto(request):
            ...
    
    Args:
        module_code: Código del módulo
        permission_type: Tipo de permiso requerido
        redirect_url: URL de redirección si no tiene permiso
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar autenticación
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder.')
                return redirect('login')
            
            # Verificar permiso
            if not has_module_permission(request.user, module_code, permission_type):
                messages.error(
                    request, 
                    f'No tienes permiso para realizar esta acción en el módulo {module_code}.'
                )
                return redirect(redirect_url)
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def user_can_view_module(user, module_code):
    """Shortcut para verificar permiso de visualización"""
    return has_module_permission(user, module_code, 'view')


def user_can_add_module(user, module_code):
    """Shortcut para verificar permiso de adición"""
    return has_module_permission(user, module_code, 'add')


def user_can_change_module(user, module_code):
    """Shortcut para verificar permiso de modificación"""
    return has_module_permission(user, module_code, 'change')


def user_can_delete_module(user, module_code):
    """Shortcut para verificar permiso de eliminación"""
    return has_module_permission(user, module_code, 'delete')


# Context Processor para usar en templates
def permissions_context(request):
    """
    Context processor que agrega información de permisos a todos los templates.
    
    Agregar en settings.py:
        'context_processors': [
            ...
            'accounts.permissions.permissions_context',
        ]
    
    Uso en templates:
        {% if 'inventarios' in user_modules %}
            <a href="...">Ver Inventarios</a>
        {% endif %}
    """
    if request.user.is_authenticated:
        modules = get_user_modules(request.user)
        module_codes = [m.code for m in modules]
        
        return {
            'user_modules': modules,
            'user_module_codes': module_codes,
            'user_role': get_user_role(request.user),
        }
    
    return {
        'user_modules': [],
        'user_module_codes': [],
        'user_role': None,
    }
