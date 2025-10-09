from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Module, Role, RoleModulePermission

class Command(BaseCommand):
    help = 'Inicializa los módulos y roles del sistema'

    def handle(self, *args, **options):
        MODULOS_SISTEMA = [
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
        for code, name, icon, order in MODULOS_SISTEMA:
            module, created = Module.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'icon': icon,
                    'order': order,
                    'description': f'Módulo de {name}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Módulo creado: {name}'))

        ROLES_SISTEMA = [
            ('administrador', 'Administrador del sistema con acceso completo'),
            ('operador_inventario', 'Operador de inventario - Gestión de bodegas, productos y movimientos'),
            ('operador_compras', 'Operador de compras - Gestión de proveedores y órdenes de compra'),
            ('operador_ventas', 'Operador de ventas - Gestión de clientes y pedidos'),
            ('operador_produccion', 'Operador de producción - Gestión de órdenes de producción'),
            ('analista_financiero', 'Analista financiero - Gestión de costos y precios'),
        ]
        for group_name, description in ROLES_SISTEMA:
            group, created = Group.objects.get_or_create(name=group_name)
            role, role_created = Role.objects.get_or_create(
                group=group,
                defaults={'description': description}
            )

            if role_created:
                self.stdout.write(self.style.SUCCESS(f'Rol creado: {group_name}'))

                if group_name == 'administrador':
                    for module in Module.objects.all():
                        RoleModulePermission.objects.create(
                            role=role,
                            module=module,
                            can_view=True,
                            can_add=True,
                            can_change=True,
                            can_delete=True
                        )
                
                elif group_name == 'operador_inventario':
                    inventario_modules = ['bodegas', 'productos', 'movimiento_inventario']
                    for module_code in inventario_modules:
                        module = Module.objects.get(code=module_code)
                        RoleModulePermission.objects.create(
                            role=role,
                            module=module,
                            can_view=True,
                            can_add=True,
                            can_change=True,
                            can_delete=False 
                        )
                
                elif group_name == 'operador_compras':
                    compras_modules = ['proveedores', 'orden_compra']
                    for module_code in compras_modules:
                        module = Module.objects.get(code=module_code)
                        RoleModulePermission.objects.create(
                            role=role,
                            module=module,
                            can_view=True,
                            can_add=True,
                            can_change=True,
                            can_delete=False
                        )
                
                elif group_name == 'operador_ventas':
                    ventas_modules = ['clientes', 'pedidos', 'listar_precios']
                    for module_code in ventas_modules:
                        module = Module.objects.get(code=module_code)
                        RoleModulePermission.objects.create(
                            role=role,
                            module=module,
                            can_view=True,
                            can_add=True,
                            can_change=True,
                            can_delete=False
                        )
                
                elif group_name == 'operador_produccion':
                    produccion_modules = ['orden_produccion', 'productos']
                    for module_code in produccion_modules:
                        module = Module.objects.get(code=module_code)
                        RoleModulePermission.objects.create(
                            role=role,
                            module=module,
                            can_view=True,
                            can_add=True,
                            can_change=True,
                            can_delete=False
                        )
                
                elif group_name == 'analista_financiero':
                    finanzas_modules = ['costos', 'listar_precios']
                    for module_code in finanzas_modules:
                        module = Module.objects.get(code=module_code)
                        RoleModulePermission.objects.create(
                            role=role,
                            module=module,
                            can_view=True,
                            can_add=True,
                            can_change=True,
                            can_delete=False
                        )

        self.stdout.write(self.style.SUCCESS('Sistema de roles inicializado exitosamente!'))