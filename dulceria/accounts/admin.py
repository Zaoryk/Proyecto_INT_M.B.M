from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Module, Role, RoleModulePermission


class RoleModulePermissionInline(admin.TabularInline):
    """
    Inline para gestionar permisos de módulos dentro de un Rol
    """
    model = RoleModulePermission
    extra = 0
    fields = ('module', 'can_view', 'can_add', 'can_change', 'can_delete')
    verbose_name = "Permiso de Módulo"
    verbose_name_plural = "Permisos de Módulos"


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    Administración de Módulos del sistema
    """
    list_display = ('name', 'code', 'order', 'icon')
    list_editable = ('order',)
    search_fields = ('name', 'code')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'name', 'order')
        }),
        ('Detalles', {
            'fields': ('description', 'icon'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Administración de Roles con permisos de módulos
    """
    list_display = ('group', 'description')
    search_fields = ('group__name', 'description')
    inlines = [RoleModulePermissionInline]
    
    fieldsets = (
        ('Configuración del Rol', {
            'fields': ('group', 'description')
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza la consulta para incluir el grupo relacionado"""
        qs = super().get_queryset(request)
        return qs.select_related('group')


@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    """
    Vista directa de permisos (opcional, también se gestiona via inline)
    """
    list_display = ('role', 'module', 'can_view', 'can_add', 'can_change', 'can_delete')
    list_filter = ('role', 'module', 'can_view', 'can_add', 'can_change', 'can_delete')
    search_fields = ('role__group__name', 'module__name')
    
    fieldsets = (
        ('Asignación', {
            'fields': ('role', 'module')
        }),
        ('Permisos', {
            'fields': ('can_view', 'can_add', 'can_change', 'can_delete')
        }),
    )


class UserRoleInline(admin.StackedInline):
    """
    Muestra información del rol del usuario en el admin
    """
    model = User.groups.through
    extra = 0
    verbose_name = "Rol/Grupo"
    verbose_name_plural = "Roles/Grupos"
    can_delete = True

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin personalizado para usuarios con mejor visualización de roles
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    def get_groups(self, obj):
        """Muestra los grupos/roles del usuario"""
        return ", ".join([g.name for g in obj.groups.all()]) or "Sin rol"
    get_groups.short_description = "Roles"
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': (),
            'description': 'Asigna roles al usuario desde la sección "Grupos" arriba.'
        }),
    )