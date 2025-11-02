from django.db import models
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string

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

"""
Clase para reseteo de cotraseña
"""
class PasswordResetCode(models.Model):
    """
    Modelo para almacenar códigos de recuperación de contraseña
    """
    email = models.EmailField(verbose_name="Email del usuario")
    code = models.CharField(max_length=6, verbose_name="Código de verificación")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    expires_at = models.DateTimeField(verbose_name="Fecha de expiración")
    is_used = models.BooleanField(default=False, verbose_name="¿Usado?")
    
    class Meta:
        verbose_name = "Código de Recuperación"
        verbose_name_plural = "Códigos de Recuperación"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.code} ({'Usado' if self.is_used else 'Válido'})"
    
    @staticmethod
    def generate_code():
        """Genera un código de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    @classmethod
    def create_code(cls, email):
        """
        Crea un nuevo código de recuperación para un email
        Invalida códigos anteriores
        """
        # Invalidar códigos anteriores no usados
        cls.objects.filter(email=email, is_used=False).update(is_used=True)
        
        # Crear nuevo código
        code = cls.generate_code()
        expires_at = timezone.now() + timedelta(minutes=15)  # Válido por 15 minutos
        
        return cls.objects.create(
            email=email,
            code=code,
            expires_at=expires_at
        )
    
    def is_valid(self):
        """Verifica si el código es válido"""
        return not self.is_used and timezone.now() < self.expires_at
    
    def mark_as_used(self):
        """Marca el código como usado"""
        self.is_used = True
        self.save()

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