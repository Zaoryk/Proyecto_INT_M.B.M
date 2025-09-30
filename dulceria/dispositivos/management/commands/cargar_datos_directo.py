# dispositivos/management/commands/cargar_datos_directo.py
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dulceria.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dispositivos.models import Proveedor, Producto, PerfilUsuario

class Command(BaseCommand):
    help = 'Carga datos directamente en la base de datos'

    def handle(self, *args, **options):
        User = get_user_model()
        
        print("Limpiando datos existentes...")
        PerfilUsuario.objects.all().delete()
        Producto.objects.all().delete()
        Proveedor.objects.all().delete()
        # NO eliminamos usuarios para evitar problemas

        print("Creando datos...")
        
        # Crear o obtener superusuario
        try:
            admin_user = User.objects.get(username='admin')
            print("Usuario admin ya existe, actualizando...")
            admin_user.email = 'admin@empresa.com'
            admin_user.first_name = 'Administrador'
            admin_user.last_name = 'Principal'
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password('admin123')
            admin_user.save()
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@empresa.com',
                password='admin123',
                first_name='Administrador',
                last_name='Principal',
                is_staff=True,
                is_superuser=True
            )

        # Crear o obtener usuario normal
        try:
            vendedor_user = User.objects.get(username='vendedor1')
            print("Usuario vendedor1 ya existe, actualizando...")
            vendedor_user.email = 'vendedor@empresa.com'
            vendedor_user.first_name = 'Carlos'
            vendedor_user.last_name = 'Vendedor'
            vendedor_user.set_password('vendedor123')
            vendedor_user.save()
        except User.DoesNotExist:
            vendedor_user = User.objects.create_user(
                username='vendedor1',
                email='vendedor@empresa.com',
                password='vendedor123',
                first_name='Carlos',
                last_name='Vendedor'
            )

        # Crear o actualizar perfiles - SIN campo telefono
        try:
            perfil_admin = PerfilUsuario.objects.get(user=admin_user)
            perfil_admin.email = 'admin@empresa.com'
            perfil_admin.rol = 'admin'
            perfil_admin.save()
            print("Perfil admin actualizado")
        except PerfilUsuario.DoesNotExist:
            PerfilUsuario.objects.create(
                user=admin_user,
                email='admin@empresa.com',
                rol='admin'
            )
            print("Perfil admin creado")

        try:
            perfil_vendedor = PerfilUsuario.objects.get(user=vendedor_user)
            perfil_vendedor.email = 'vendedor@empresa.com'
            perfil_vendedor.rol = 'cliente'
            perfil_vendedor.save()
            print("Perfil vendedor actualizado")
        except PerfilUsuario.DoesNotExist:
            PerfilUsuario.objects.create(
                user=vendedor_user,
                email='vendedor@empresa.com',
                rol='cliente'
            )
            print("Perfil vendedor creado")

        # Crear proveedores
        proveedor1, created = Proveedor.objects.get_or_create(
            nombre='Proveedor ABC S.A.',
            defaults={
                'contacto': 'Juan Pérez',
                'telefono': '+56911223344',
                'email': 'contacto@proveedorabc.com'
            }
        )
        if created:
            print("Proveedor 1 creado")
        else:
            print("Proveedor 1 ya existe")

        proveedor2, created = Proveedor.objects.get_or_create(
            nombre='Distribuidora XYZ Ltda.',
            defaults={
                'contacto': 'María González',
                'telefono': '+56955667788',
                'email': 'ventas@xyz.com'
            }
        )
        if created:
            print("Proveedor 2 creado")
        else:
            print("Proveedor 2 ya existe")

        # Fechas de vencimiento (1 año desde hoy)
        fecha_vencimiento = datetime.now() + timedelta(days=365)

        # Crear productos CON fecha_vencimiento
        producto1, created = Producto.objects.get_or_create(
            nombre='Chocolate Amargo 70%',
            defaults={
                'precio': 3500,
                'stock': 150,
                'proveedor': proveedor1,
                'fecha_vencimiento': fecha_vencimiento
            }
        )
        if created:
            print("Producto 1 creado")
        else:
            print("Producto 1 ya existe")

        producto2, created = Producto.objects.get_or_create(
            nombre='Caramelo de Fruta Mix',
            defaults={
                'precio': 1200,
                'stock': 300,
                'proveedor': proveedor2,
                'fecha_vencimiento': fecha_vencimiento
            }
        )
        if created:
            print("Producto 2 creado")
        else:
            print("Producto 2 ya existe")

        producto3, created = Producto.objects.get_or_create(
            nombre='Gomitas de Ositos',
            defaults={
                'precio': 1800,
                'stock': 200,
                'proveedor': proveedor2,
                'fecha_vencimiento': fecha_vencimiento
            }
        )
        if created:
            print("Producto 3 creado")
        else:
            print("Producto 3 ya existe")

        print("¡Datos cargados exitosamente!")
        print("Usuarios disponibles: admin / admin123, vendedor1 / vendedor123")