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
from dispositivos.models import Usuario, Proveedor, Producto, Bodega, Receta

class Command(BaseCommand):
    help = 'Carga datos directamente en la base de datos con nuevos modelos'

    def handle(self, *args, **options):
        print("=== CARGANDO DATOS CON NUEVOS MODELOS ===")
        
        print("Limpiando datos existentes...")
        self.limpiar_datos()
        
        print("Creando datos...")
        
        # Crear usuarios
        usuarios = self.crear_usuarios()
        
        # Crear proveedores
        proveedores = self.crear_proveedores()
        
        # Crear productos
        productos = self.crear_productos(proveedores)
        
        # Crear bodegas
        bodegas = self.crear_bodegas()
        
        # Crear recetas
        recetas = self.crear_recetas()
        
        print("¡Datos cargados exitosamente!")
        print("=== USUARIOS DISPONIBLES ===")
        print("Administrador: admin123")
        print("Vendedor: vendedor123") 
        print("Comprador: comprador123")

    def limpiar_datos(self):
        """Limpia los datos existentes"""
        # Limpiar en orden inverso de dependencias
        Producto.objects.all().delete()
        Bodega.objects.all().delete()
        Receta.objects.all().delete()
        Proveedor.objects.all().delete()
        Usuario.objects.all().delete()

    def crear_usuarios(self):
        """Crea usuarios del sistema"""
        print("--- Creando usuarios ---")
        
        usuarios_data = [
            {
                'nombre': 'Administrador Principal',
                'rol': 'admin',
                'permisos': 'superusuario',
                'password': 'admin123',
                'email': 'admin@empresa.com'
            },
            {
                'nombre': 'Carlos Vendedor',
                'rol': 'vendedor',
                'permisos': 'ventas,consultas',
                'password': 'vendedor123',
                'email': 'vendedor@empresa.com'
            },
            {
                'nombre': 'Ana Compradora', 
                'rol': 'comprador',
                'permisos': 'compras,proveedores',
                'password': 'comprador123',
                'email': 'comprador@empresa.com'
            }
        ]
        
        usuarios_creados = []
        for data in usuarios_data:
            usuario, created = Usuario.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            status = "creado" if created else "ya existía"
            print(f"✓ Usuario {usuario.nombre} ({status})")
            usuarios_creados.append(usuario)
            
        return usuarios_creados

    def crear_proveedores(self):
        """Crea proveedores"""
        print("--- Creando proveedores ---")
        
        proveedores_data = [
            {
                'nombre': 'Proveedor ABC S.A.',
                'contacto': 'Juan Pérez',
                'condicionescomerciales': 'Pago a 30 días'
            },
            {
                'nombre': 'Distribuidora XYZ Ltda.',
                'contacto': 'María González', 
                'condicionescomerciales': 'Pago contado 5% descuento'
            },
            {
                'nombre': 'Dulces Nacionales S.A.',
                'contacto': 'Roberto Silva',
                'condicionescomerciales': 'Pago a 60 días'
            }
        ]
        
        proveedores_creados = []
        for data in proveedores_data:
            proveedor, created = Proveedor.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            status = "creado" if created else "ya existía"
            print(f"✓ Proveedor {proveedor.nombre} ({status})")
            proveedores_creados.append(proveedor)
            
        return proveedores_creados

    def crear_productos(self, proveedores):
        """Crea productos"""
        print("--- Creando productos ---")
        
        fecha_vencimiento = datetime.now() + timedelta(days=365)
        
        productos_data = [
            {
                'nombre': 'Chocolate Amargo 70%',
                'lote': 'LOTE-CHOCO-001',
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 3500,
                'stock': 150,
                'proveedor': proveedores[0]  # Proveedor ABC
            },
            {
                'nombre': 'Caramelo de Fruta Mix',
                'lote': 'LOTE-CARAM-001',
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 1200,
                'stock': 300,
                'proveedor': proveedores[1]  # Distribuidora XYZ
            },
            {
                'nombre': 'Gomitas de Ositos',
                'lote': 'LOTE-GOMI-001',
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 1800,
                'stock': 200,
                'proveedor': proveedores[1]  # Distribuidora XYZ
            },
            {
                'nombre': 'Galletas de Mantequilla',
                'lote': 'LOTE-GALL-001', 
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 2800,
                'stock': 80,
                'proveedor': proveedores[0]  # Proveedor ABC
            },
            {
                'nombre': 'Bombones Surtidos',
                'lote': 'LOTE-BOMB-001',
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 4200,
                'stock': 60,
                'proveedor': proveedores[2]  # Dulces Nacionales
            }
        ]
        
        productos_creados = []
        for data in productos_data:
            producto, created = Producto.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            status = "creado" if created else "ya existía"
            print(f"✓ Producto {producto.nombre} - ${producto.precio} ({status})")
            productos_creados.append(producto)
            
        return productos_creados

    def crear_bodegas(self):
        """Crea bodegas"""
        print("--- Creando bodegas ---")
        
        bodegas_data = [
            {
                'nombre': 'Bodega Principal',
                'ubicacion': 'Local Central'
            },
            {
                'nombre': 'Bodega Secundaria',
                'ubicacion': 'Almacén Norte'
            }
        ]
        
        bodegas_creadas = []
        for data in bodegas_data:
            bodega, created = Bodega.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            status = "creada" if created else "ya existía"
            print(f"✓ Bodega {bodega.nombre} ({status})")
            bodegas_creadas.append(bodega)
            
        return bodegas_creadas

    def crear_recetas(self):
        """Crea recetas"""
        print("--- Creando recetas ---")
        
        recetas_data = [
            {
                'version': '1.0',
                'insumos_necesarios': 18.50
            },
            {
                'version': '2.1', 
                'insumos_necesarios': 22.00
            }
        ]
        
        recetas_creadas = []
        for data in recetas_data:
            receta, created = Receta.objects.get_or_create(
                version=data['version'],
                defaults=data
            )
            status = "creada" if created else "ya existía"
            print(f"✓ Receta versión {receta.version} ({status})")
            recetas_creadas.append(receta)
            
        return recetas_creadas