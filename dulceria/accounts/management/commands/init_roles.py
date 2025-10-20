from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Module, Role, RoleModulePermission

class Command(BaseCommand):
    help = 'Inicializa los módulos y roles del sistema'

    def handle(self, *args, **options):
        # Módulos actualizados incluyendo las nuevas tablas
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
            ('producto_proveedor', 'Relación Producto-Proveedor', 'link', 12),
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

        # Roles del sistema
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

                # Asignar permisos según el rol
                if group_name == 'administrador':
                    # Acceso completo a todos los módulos
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
                    inventario_modules = [
                        'bodegas', 
                        'productos', 
                        'movimiento_inventario',
                        'producto_proveedor'  # Nuevo módulo para gestión de inventario
                    ]
                    for module_code in inventario_modules:
                        try:
                            module = Module.objects.get(code=module_code)
                            RoleModulePermission.objects.create(
                                role=role,
                                module=module,
                                can_view=True,
                                can_add=True,
                                can_change=True,
                                can_delete=False  # No puede eliminar registros
                            )
                        except Module.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Módulo no encontrado: {module_code}'))
                
                elif group_name == 'operador_compras':
                    compras_modules = [
                        'proveedores', 
                        'orden_compra',
                        'producto_proveedor'  # Nuevo módulo para relación con proveedores
                    ]
                    for module_code in compras_modules:
                        try:
                            module = Module.objects.get(code=module_code)
                            RoleModulePermission.objects.create(
                                role=role,
                                module=module,
                                can_view=True,
                                can_add=True,
                                can_change=True,
                                can_delete=False
                            )
                        except Module.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Módulo no encontrado: {module_code}'))
                
                elif group_name == 'operador_ventas':
                    ventas_modules = [
                        'clientes', 
                        'pedidos', 
                        'listar_precios',
                        'productos'  # Puede ver productos para ventas
                    ]
                    for module_code in ventas_modules:
                        try:
                            module = Module.objects.get(code=module_code)
                            # Permisos específicos para ventas
                            can_delete = module_code in ['clientes']  # Solo puede eliminar clientes
                            can_add = module_code != 'productos'  # No puede agregar productos
                            can_change = module_code != 'productos'  # No puede modificar productos
                            
                            RoleModulePermission.objects.create(
                                role=role,
                                module=module,
                                can_view=True,
                                can_add=can_add,
                                can_change=can_change,
                                can_delete=can_delete
                            )
                        except Module.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Módulo no encontrado: {module_code}'))
                
                elif group_name == 'operador_produccion':
                    produccion_modules = [
                        'orden_produccion', 
                        'productos',
                        'movimiento_inventario'  # Para registrar movimientos de producción
                    ]
                    for module_code in produccion_modules:
                        try:
                            module = Module.objects.get(code=module_code)
                            # Permisos específicos para producción
                            can_delete = module_code == 'orden_produccion'  # Solo puede eliminar órdenes de producción
                            can_add_products = module_code == 'productos'  # No puede agregar productos
                            
                            RoleModulePermission.objects.create(
                                role=role,
                                module=module,
                                can_view=True,
                                can_add=module_code != 'productos',  # No puede agregar productos
                                can_change=True,
                                can_delete=can_delete
                            )
                        except Module.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Módulo no encontrado: {module_code}'))
                
                elif group_name == 'analista_financiero':
                    finanzas_modules = [
                        'costos', 
                        'listar_precios',
                        'productos',  # Para análisis de costos por producto
                        'proveedores'  # Para análisis de costos por proveedor
                    ]
                    for module_code in finanzas_modules:
                        try:
                            module = Module.objects.get(code=module_code)
                            # Analista financiero solo puede ver y modificar, no agregar/eliminar
                            RoleModulePermission.objects.create(
                                role=role,
                                module=module,
                                can_view=True,
                                can_add=False,    # No puede agregar nuevos registros
                                can_change=True,  # Puede modificar costos y precios
                                can_delete=False  # No puede eliminar registros
                            )
                        except Module.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Módulo no encontrado: {module_code}'))

        # Actualizar permisos para roles existentes (en caso de que se ejecute nuevamente)
        self.actualizar_permisos_existentes()

        self.stdout.write(self.style.SUCCESS('Sistema de roles inicializado exitosamente!'))

    def actualizar_permisos_existentes(self):
        """Actualiza permisos para roles existentes con nuevos módulos"""
        
        # Módulo nuevo que necesita ser agregado a roles existentes
        nuevo_modulo_codigo = 'producto_proveedor'
        
        try:
            nuevo_modulo = Module.objects.get(code=nuevo_modulo_codigo)
            
            # Roles que deberían tener acceso al nuevo módulo
            roles_con_acceso = [
                'operador_inventario',
                'operador_compras',
                'administrador'
            ]
            
            for role_name in roles_con_acceso:
                try:
                    group = Group.objects.get(name=role_name)
                    role = Role.objects.get(group=group)
                    
                    # Verificar si ya existe el permiso
                    if not RoleModulePermission.objects.filter(role=role, module=nuevo_modulo).exists():
                        # Asignar permisos según el rol
                        if role_name == 'administrador':
                            RoleModulePermission.objects.create(
                                role=role,
                                module=nuevo_modulo,
                                can_view=True,
                                can_add=True,
                                can_change=True,
                                can_delete=True
                            )
                        else:
                            RoleModulePermission.objects.create(
                                role=role,
                                module=nuevo_modulo,
                                can_view=True,
                                can_add=True,
                                can_change=True,
                                can_delete=False
                            )
                        self.stdout.write(self.style.SUCCESS(f'Permiso agregado para {role_name} en {nuevo_modulo_codigo}'))
                        
                except (Group.DoesNotExist, Role.DoesNotExist):
                    self.stdout.write(self.style.WARNING(f'Rol no encontrado: {role_name}'))
                    
        except Module.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'Módulo nuevo no encontrado: {nuevo_modulo_codigo}'))