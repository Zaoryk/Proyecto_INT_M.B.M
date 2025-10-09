"""
Comando para inicializar el sistema de roles y permisos de Dulcería Lilis.

Uso:
    python manage.py seed_roles

Este comando crea:
- Módulos del sistema (Inventarios, Compras, Producción, Ventas, Costos)
- Roles del sistema con sus permisos correspondientes
- Matriz de permisos según los requerimientos del ERP

Roles creados:
1. Administrador: Acceso completo a todos los módulos
2. Operador de Compras: Gestión de compras y proveedores
3. Operador de Inventario: Control de inventarios y bodegas
4. Operador de Producción: Gestión de órdenes de producción
5. Operador de Ventas: Gestión de clientes, pedidos y ventas
6. Analista Financiero: Consulta de costos y análisis financiero
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Module, Role, RoleModulePermission


class Command(BaseCommand):
    help = 'Inicializa módulos, roles y permisos para Dulcería Lilis'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🍬 Iniciando configuración de roles - Dulcería Lilis...'))
        
        # 1. Crear Módulos
        self.stdout.write('\n📦 Creando módulos del sistema...')
        modules_data = [
            {'code': 'inventarios', 'name': 'Inventarios', 'icon': '📦', 'order': 1, 
             'description': 'Gestión de inventarios, stock, ubicaciones y trazabilidad'},
            {'code': 'compras', 'name': 'Compras y Proveedores', 'icon': '🛒', 'order': 2,
             'description': 'Gestión de solicitudes, órdenes de compra y proveedores'},
            {'code': 'produccion', 'name': 'Producción', 'icon': '🏭', 'order': 3,
             'description': 'Gestión de órdenes de producción, recetas y mermas'},
            {'code': 'ventas', 'name': 'Ventas y Clientes', 'icon': '💰', 'order': 4,
             'description': 'Gestión de clientes, cotizaciones, pedidos y facturación'},
            {'code': 'costos', 'name': 'Costos y Finanzas', 'icon': '📊', 'order': 5,
             'description': 'Control de costos, listas de precios y reportes financieros'},
        ]
        
        modules = {}
        for module_data in modules_data:
            module, created = Module.objects.get_or_create(
                code=module_data['code'],
                defaults={
                    'name': module_data['name'],
                    'icon': module_data['icon'],
                    'order': module_data['order'],
                    'description': module_data['description']
                }
            )
            modules[module_data['code']] = module
            status = '✅ Creado' if created else '♻️  Ya existe'
            self.stdout.write(f"  {status}: {module.name}")
        
        # 2. Crear Roles (vinculados a Groups de Django)
        self.stdout.write('\n👥 Creando roles del sistema...')
        roles_data = [
            {
                'name': 'Administrador',
                'description': 'Acceso completo a todos los módulos del sistema. Configura usuarios, permisos y parámetros.'
            },
            {
                'name': 'Operador de Compras',
                'description': 'Gestiona solicitudes, órdenes de compra, recepción de insumos y proveedores.'
            },
            {
                'name': 'Operador de Inventario',
                'description': 'Controla existencias, ubicaciones, trazabilidad de lotes y movimientos de inventario.'
            },
            {
                'name': 'Operador de Producción',
                'description': 'Crea órdenes de producción, registra consumos, mermas y producción final.'
            },
            {
                'name': 'Operador de Ventas',
                'description': 'Gestiona clientes, cotizaciones, pedidos, despachos y facturación.'
            },
            {
                'name': 'Analista Financiero',
                'description': 'Controla costos, listas de precios, márgenes y genera reportes financieros.'
            }
        ]
        
        roles = {}
        for role_data in roles_data:
            # Crear o obtener el Group de Django
            group, group_created = Group.objects.get_or_create(name=role_data['name'])
            
            # Crear o obtener el Role vinculado al Group
            role, role_created = Role.objects.get_or_create(
                group=group,
                defaults={'description': role_data['description']}
            )
            
            roles[role_data['name']] = role
            status = '✅ Creado' if role_created else '♻️  Ya existe'
            self.stdout.write(f"  {status}: {role.group.name}")
        
        # 3. Asignar permisos según matriz de roles
        self.stdout.write('\n🔐 Configurando matriz de permisos...')
        
        # Matriz de permisos: {rol: {modulo: (view, add, change, delete)}}
        permissions_matrix = {
            'Administrador': {
                'inventarios': (True, True, True, True),
                'compras': (True, True, True, True),
                'produccion': (True, True, True, True),
                'ventas': (True, True, True, True),
                'costos': (True, True, True, True),
            },
            'Operador de Compras': {
                'inventarios': (True, False, False, False),  # Solo consulta
                'compras': (True, True, True, False),  # No puede eliminar
                'produccion': (False, False, False, False),  # Sin acceso
                'ventas': (False, False, False, False),  # Sin acceso
                'costos': (True, False, False, False),  # Solo consulta
            },
            'Operador de Inventario': {
                'inventarios': (True, True, True, False),  # No puede eliminar
                'compras': (True, False, False, False),  # Solo consulta
                'produccion': (True, False, False, False),  # Solo consulta
                'ventas': (True, False, False, False),  # Solo consulta
                'costos': (True, False, False, False),  # Solo consulta
            },
            'Operador de Producción': {
                'inventarios': (True, False, True, False),  # Consulta y actualiza consumos
                'compras': (True, False, False, False),  # Solo consulta
                'produccion': (True, True, True, False),  # No puede eliminar
                'ventas': (False, False, False, False),  # Sin acceso
                'costos': (True, False, False, False),  # Solo consulta
            },
            'Operador de Ventas': {
                'inventarios': (True, False, False, False),  # Solo consulta
                'compras': (False, False, False, False),  # Sin acceso
                'produccion': (False, False, False, False),  # Sin acceso
                'ventas': (True, True, True, False),  # No puede eliminar
                'costos': (True, False, False, False),  # Solo consulta precios
            },
            'Analista Financiero': {
                'inventarios': (True, False, False, False),  # Solo consulta
                'compras': (True, False, False, False),  # Solo consulta
                'produccion': (True, False, False, False),  # Solo consulta
                'ventas': (True, False, False, False),  # Solo consulta
                'costos': (True, True, True, False),  # Gestiona precios, no elimina
            },
        }
        
        for role_name, module_perms in permissions_matrix.items():
            role = roles[role_name]
            self.stdout.write(f"\n  📋 Configurando permisos para: {role_name}")
            
            for module_code, perms in module_perms.items():
                module = modules[module_code]
                can_view, can_add, can_change, can_delete = perms
                
                # Crear o actualizar permiso
                perm, created = RoleModulePermission.objects.update_or_create(
                    role=role,
                    module=module,
                    defaults={
                        'can_view': can_view,
                        'can_add': can_add,
                        'can_change': can_change,
                        'can_delete': can_delete
                    }
                )
                
                # Mostrar permisos asignados
                perms_list = []
                if can_view: perms_list.append('Ver')
                if can_add: perms_list.append('Agregar')
                if can_change: perms_list.append('Modificar')
                if can_delete: perms_list.append('Eliminar')
                
                perms_str = ', '.join(perms_list) if perms_list else 'Sin acceso'
                self.stdout.write(f"    • {module.name}: {perms_str}")
        
        # Resumen final
        self.stdout.write(self.style.SUCCESS(f'\n✅ Configuración completada exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'   Módulos creados: {Module.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Roles creados: {Role.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Permisos configurados: {RoleModulePermission.objects.count()}'))
        self.stdout.write(self.style.WARNING(f'\n💡 Próximos pasos:'))
        self.stdout.write(f'   1. Crear usuarios: python manage.py createsuperuser')
        self.stdout.write(f'   2. Asignar roles en el Admin: /admin/auth/user/')
        self.stdout.write(f'   3. Los usuarios deben tener is_staff=True para acceder al admin')
