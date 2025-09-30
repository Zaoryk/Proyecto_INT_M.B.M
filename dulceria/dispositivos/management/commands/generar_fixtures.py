# dispositivos/management/commands/generar_fixtures.py
import os
import sys
import django

# Configurar Django ANTES de importar modelos
try:
    # Calcular la ruta del proyecto Django
    current_file = __file__
    commands_dir = os.path.dirname(current_file)
    management_dir = os.path.dirname(commands_dir)
    apps_dir = os.path.dirname(management_dir)
    project_dir = os.path.dirname(apps_dir)
    
    # Agregar al path y configurar Django
    sys.path.insert(0, project_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dulceria.settings')
    django.setup()
    
    # AHORA importar los modelos
    from django.core.management.base import BaseCommand
    from django.core import serializers
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import User
    from dispositivos.models import Proveedor, Producto, PerfilUsuario
    
    print("[OK] Modulos importados correctamente")
    
except ImportError as e:
    print(f"[ERROR] Importando modulos: {e}")
    print("Asegurate de que:")
    print("1. Estas en el directorio correcto (donde esta manage.py)")
    print("2. Tu virtual environment esta activado")
    print("3. Django esta instalado")
    sys.exit(1)

class Command(BaseCommand):
    help = 'Genera archivos fixtures para la aplicacion dispositivos'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando generacion de fixtures...')
        
        # Crear directorio de fixtures si no existe
        fixtures_dir = os.path.join('dispositivos', 'fixtures')
        if not os.path.exists(fixtures_dir):
            os.makedirs(fixtures_dir)
            self.stdout.write(f'[OK] Directorio creado: {fixtures_dir}')
        else:
            self.stdout.write(f'[OK] Directorio ya existe: {fixtures_dir}')

        # Generar datos de prueba
        self.generar_datos_prueba()
        
        # Exportar a fixtures
        self.exportar_fixtures()
        
        self.stdout.write(self.style.SUCCESS('[EXITO] Fixtures generados exitosamente!'))
        self.stdout.write('Archivos creados en: dispositivos/fixtures/')
        self.stdout.write('Usuario admin: admin / admin123')

    def generar_datos_prueba(self):
        """Genera datos de prueba para el sistema"""
        User = get_user_model()
        
        self.stdout.write('Limpiando datos existentes...')
        self.limpiar_datos()
        
        self.stdout.write('Creando usuarios...')
        # Crear superusuario
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@empresa.com',
            password='admin123',
            first_name='Administrador',
            last_name='Principal'
        )

        # Crear usuario normal
        vendedor_user = User.objects.create_user(
            username='vendedor1',
            email='vendedor@empresa.com',
            password='vendedor123',
            first_name='Carlos',
            last_name='Vendedor'
        )

        self.stdout.write('Creando perfiles de usuario...')
        # Crear perfiles
        PerfilUsuario.objects.create(
            user=admin_user,
            email='admin@empresa.com',
            telefono='+56912345678',
            rol='admin'
        )

        PerfilUsuario.objects.create(
            user=vendedor_user,
            email='vendedor@empresa.com',
            telefono='+56987654321',
            rol='cliente'
        )

        self.stdout.write('Creando proveedores...')
        # Crear proveedores
        proveedor1 = Proveedor.objects.create(
            nombre='Proveedor ABC S.A.',
            contacto='Juan Perez',
            telefono='+56911223344',
            email='contacto@proveedorabc.com'
        )

        proveedor2 = Proveedor.objects.create(
            nombre='Distribuidora XYZ Ltda.',
            contacto='Maria Gonzalez',
            telefono='+56955667788',
            email='ventas@xyz.com'
        )

        proveedor3 = Proveedor.objects.create(
            nombre='Dulces Nacionales S.A.',
            contacto='Roberto Silva',
            telefono='+56999887766',
            email='info@dulcesnacionales.cl'
        )

        self.stdout.write('Creando productos...')
        # Crear productos
        Producto.objects.create(
            nombre='Chocolate Amargo 70%',
            precio=3500,
            stock=150,
            proveedor=proveedor1
        )

        Producto.objects.create(
            nombre='Caramelo de Fruta Mix',
            precio=1200,
            stock=300,
            proveedor=proveedor2
        )

        Producto.objects.create(
            nombre='Galletas de Mantequilla',
            precio=2800,
            stock=80,
            proveedor=proveedor1
        )

        Producto.objects.create(
            nombre='Bombones Surtidos',
            precio=4200,
            stock=60,
            proveedor=proveedor3
        )

        Producto.objects.create(
            nombre='Gomitas de Ositos',
            precio=1800,
            stock=200,
            proveedor=proveedor2
        )

    def limpiar_datos(self):
        """Limpia los datos existentes"""
        User = get_user_model()
        PerfilUsuario.objects.all().delete()
        Producto.objects.all().delete()
        Proveedor.objects.all().delete()
        # No eliminar superusuarios existentes
        User.objects.filter(is_superuser=False).delete()

    def exportar_fixtures(self):
        """Exporta los datos a archivos fixtures"""
        
        self.stdout.write('Exportando a archivos JSON...')
        
        # 00_proveedores.json
        proveedores = Proveedor.objects.all()
        with open('dispositivos/fixtures/00_proveedores.json', 'w', encoding='utf-8') as f:
            data = serializers.serialize('json', proveedores, indent=2, ensure_ascii=False)
            f.write(data)
        self.stdout.write('[OK] 00_proveedores.json')

        # 01_usuarios.json  
        User = get_user_model()
        usuarios = User.objects.all()
        with open('dispositivos/fixtures/01_usuarios.json', 'w', encoding='utf-8') as f:
            data = serializers.serialize('json', usuarios, indent=2, ensure_ascii=False)
            f.write(data)
        self.stdout.write('[OK] 01_usuarios.json')

        # 02_perfiles.json
        perfiles = PerfilUsuario.objects.all()
        with open('dispositivos/fixtures/02_perfiles.json', 'w', encoding='utf-8') as f:
            data = serializers.serialize('json', perfiles, indent=2, ensure_ascii=False)
            f.write(data)
        self.stdout.write('[OK] 02_perfiles.json')

        # 03_productos.json
        productos = Producto.objects.all()
        with open('dispositivos/fixtures/03_productos.json', 'w', encoding='utf-8') as f:
            data = serializers.serialize('json', productos, indent=2, ensure_ascii=False)
            f.write(data)
        self.stdout.write('[OK] 03_productos.json')