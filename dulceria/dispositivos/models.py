# models.py
from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


# Perfil de usuario extendido
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=200, blank=True, null=True)
    rol = models.CharField(
    max_length=50,
    choices=[
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('compras', 'Operador de Compras'),
        ('inventario', 'Operador de Inventario'),
        ('produccion', 'Operador de Producción'),
        ('ventas', 'Operador de Ventas'),
        ('finanzas', 'Analista Financiero'),
    ]
)

    def __str__(self):
        return self.user.username