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
from django.http import HttpResponseForbidden
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

def get_user_role_name(user):
    """
    Obtiene el nombre del rol del usuario
    """
    if not user.is_authenticated:
        return None
    
    groups = user.groups.all()
    if groups.exists():
        return groups.first().name
    
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

def can_edit_own_profile(user, usuario_id):
    """
    Verifica si el usuario puede editar un perfil específico.
    
    Reglas:
    - Administrador: puede editar cualquier perfil
    - Analista Financiero: no puede editar ningún perfil (ni el suyo)
    - Otros roles: solo pueden editar su propio perfil
    
    Args:
        user: Usuario autenticado
        usuario_id: ID del usuario a editar
    
    Returns:
        bool: True si puede editar, False si no
    """
    if user.is_superuser:
        return True
    
    role_name = get_user_role_name(user)
    
    # Analista financiero no puede editar nada
    if role_name == 'analista_financiero':
        return False
    
    # Administrador puede editar cualquier perfil
    if role_name == 'administrador':
        return True
    
    # Otros roles solo pueden editar su propio perfil
    # Necesitamos obtener el usuario_id del usuario autenticado
    from dispositivos.models import Usuario
    try:
        usuario_actual = Usuario.objects.get(username=user.username)
        return usuario_actual.idUsuario == int(usuario_id)
    except Usuario.DoesNotExist:
        return False

def can_assign_roles(user):
    """
    Solo el administrador puede asignar roles.
    """
    if user.is_superuser:
        return True
    
    role_name = get_user_role_name(user)
    return role_name == 'administrador'

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


def require_module_permission(module_code, permission_type='view', check_own_profile=False):
    """
    Decorador para proteger vistas que requieren permisos específicos.
    
    Args:
        module_code: Código del módulo
        permission_type: Tipo de permiso requerido ('view', 'add', 'change', 'delete')
        check_own_profile: Si True, verifica que el usuario solo pueda editar su propio perfil
    
    Uso:
        @require_module_permission('productos', 'add')
        def crear_producto(request):
            ...
        
        @require_module_permission('usuarios', 'change', check_own_profile=True)
        def editar_usuario(request, usuario_id):
            ...
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
                    f'No tienes permiso para realizar esta acción en {module_code}.'
                )
                return redirect('dashboard')
            
            # Verificación adicional para edición de perfil propio
            if check_own_profile and permission_type == 'change':
                # Obtener el ID del usuario a editar desde GET o POST
                usuario_id = request.GET.get('edit_id') or request.POST.get('edit_id')
                
                if usuario_id and not can_edit_own_profile(request.user, usuario_id):
                    messages.error(
                        request, 
                        'Solo puedes editar tu propio perfil.'
                    )
                    return redirect('Formulario')
                
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
    
    Uso en templates:
        {% if 'productos' in user_module_codes %}
            <a href="...">Ver Productos</a>
        {% endif %}
        
        {% if can_add_productos %}
            <button>Crear Producto</button>
        {% endif %}
    """
    if request.user.is_authenticated:
        modules = get_user_modules(request.user)
        module_codes = [m.code for m in modules]
        role_name = get_user_role_name(request.user)

        # Crear diccionarios de permisos por módulo
        can_add = {}
        can_change = {}
        can_delete = {}
        
        for module in modules:
            code = module.code
            can_add[f'can_add_{code}'] = user_can_add_module(request.user, code)
            can_change[f'can_change_{code}'] = user_can_change_module(request.user, code)
            can_delete[f'can_delete_{code}'] = user_can_delete_module(request.user, code)
        
        context = {
            'user_modules': modules,
            'user_module_codes': module_codes,
            'user_role': get_user_role(request.user),
            'user_role_name': role_name,
            'is_admin': role_name == 'administrador',
            'is_analyst': role_name == 'analista_financiero',
            'can_assign_roles': can_assign_roles(request.user),
        }
        
        # Agregar permisos específicos al contexto
        context.update(can_add)
        context.update(can_change)
        context.update(can_delete)
        
        return context
    
    return {
        'user_modules': [],
        'user_module_codes': [],
        'user_role': None,
        'user_role_name': None,
        'is_admin': False,
        'is_analyst': False,
        'can_assign_roles': False,
    }