from django.db import models
from django.contrib.auth.models import Group, User
from django.conf import settings

class Module(models.Model):
    """
    Representa un módulo del sistema ERP de Dulcería Lilis.
    """
    code = models.SlugField(max_length=50, unique=True, help_text="Código único del módulo (ej: 'inventarios')")
    name = models.CharField(max_length=100, help_text="Nombre descriptivo del módulo (ej: 'Inventarios')")
    icon = models.CharField(max_length=50, blank=True, help_text="Icono para el menú (opcional)")
    description = models.TextField(blank=True, help_text="Descripción del módulo")
    order = models.IntegerField(default=0, help_text="Orden de visualización en el menú")
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Role(models.Model):
    """
    Rol del sistema vinculado a un Group de Django.
    """
    group = models.OneToOneField(
        Group, 
        on_delete=models.CASCADE,
        related_name="role",
        help_text="Grupo de Django asociado al rol"
    )
    description = models.TextField(blank=True, help_text="Descripción del rol")
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
    
    def __str__(self):
        return self.group.name


class RoleModulePermission(models.Model):
    """
    Define los permisos que un rol tiene sobre un módulo específico.
    """
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE,
        related_name="module_perms"
    )
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE,
        related_name="role_perms"
    )
    can_view = models.BooleanField(default=False, help_text="Puede ver/listar registros")
    can_add = models.BooleanField(default=False, help_text="Puede agregar nuevos registros")
    can_change = models.BooleanField(default=False, help_text="Puede modificar registros existentes")
    can_delete = models.BooleanField(default=False, help_text="Puede eliminar registros")
    
    class Meta:
        verbose_name = "Permiso de Módulo"
        verbose_name_plural = "Permisos de Módulos"
        unique_together = ("role", "module")
    
    def __str__(self):
        perms = []
        if self.can_view: perms.append("Ver")
        if self.can_add: perms.append("Agregar")
        if self.can_change: perms.append("Modificar")
        if self.can_delete: perms.append("Eliminar")
        
        return f"{self.role} → {self.module} ({', '.join(perms) if perms else 'Sin permisos'})"


# Módulos predefinidos del sistema
MODULOS_SISTEMA = [
    # Módulos de Dispositivos
    ('bodegas', 'Bodegas', 'warehouse', 1),
    ('clientes', 'Clientes', 'people', 2),
    ('productos', 'Productos', 'inventory_2', 3),
    ('proveedores', 'Proveedores', 'local_shipping', 4),
    ('costos', 'Costos', 'attach_money', 5),
    ('listar_precios', 'Listar Precios', 'price_check', 6),
    ('movimiento_inventario', 'Movimiento Inventario', 'swap_horiz', 7),
    ('orden_compra', 'Orden de Compra', 'shopping_cart', 8),
    ('orden_produccion', 'Orden de Producción', 'build', 9),
    ('pedidos', 'Pedidos', 'receipt', 10),
    ('usuarios', 'Usuarios', 'person', 11),
]