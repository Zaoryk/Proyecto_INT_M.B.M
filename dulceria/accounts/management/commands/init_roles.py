from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Module, Role, RoleModulePermission

class Command(BaseCommand):
    help = 'Inicializa los módulos y roles del sistema con permisos específicos'

    def handle(self, *args, **options):
        # Módulos actualizados incluyendo las nuevas tablas
        MODULOS_SISTEMA = [
            ('usuarios', 'Usuarios', 'person', 1),
            ('productos', 'Productos', 'inventory_2', 2),
            ('proveedores', 'Proveedores', 'local_shipping', 3),
            ('producto_proveedor', 'Inventario (Movimientos)', 'swap_horiz', 4),
            ('bodegas', 'Bodegas', 'warehouse', 5),
            ('clientes', 'Clientes', 'people', 6),
            ('costos', 'Costos', 'attach_money', 7),
            ('listar_precios', 'Listar Precios', 'price_check', 8),
            ('movimiento_inventario', 'Movimiento Inventario', 'swap_horiz', 9),
            ('orden_compra', 'Orden de Compra', 'shopping_cart', 10),
            ('orden_produccion', 'Orden de Producción', 'build', 11),
            ('pedidos', 'Pedidos', 'receipt', 12),
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
            ('operador_inventario', 'Operador de inventario - Solo gestiona inventario y movimientos'),
            ('operador_compras', 'Operador de compras - Solo gestiona proveedores'),
            ('operador_ventas', 'Operador de ventas - Gestión limitada'),
            ('operador_produccion', 'Operador de producción - Solo gestiona productos'),
            ('analista_financiero', 'Analista financiero - Solo visualización de datos'),
        ]

        for group_name, description in ROLES_SISTEMA:
            group, created = Group.objects.get_or_create(name=group_name)
            role, role_created = Role.objects.get_or_create(
                group=group,
                defaults={'description': description}
            )

            # Limpiar permisos existentes para reconfigurar
            if not role_created:
                RoleModulePermission.objects.filter(role=role).delete()
                self.stdout.write(self.style.WARNING(f'Limpiando permisos de: {group_name}'))

            self.stdout.write(self.style.SUCCESS(f'Configurando rol: {group_name}'))


            # Asignar permisos según el rol
            # ==========================================
            # ADMINISTRADOR - ACCESO TOTAL
            # ==========================================
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
            
            # ==============================================
            # OPERADOR DE INVENTARIO - SOLO CRUD INVENTARIO
            # ==============================================
            elif group_name == 'operador_inventario':
                permisos = {
                    'producto_proveedor': {'view': True, 'add': True, 'change': True, 'delete': True},
                    'productos': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'proveedores': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'bodegas': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'usuarios': {'view': True, 'add': False, 'change': True, 'delete': False},  # Solo editar su perfil
                }
                self._aplicar_permisos(role, permisos)

            # ==========================================
            # OPERADOR DE COMPRAS - SOLO CRUD PROVEEDOR
            # ==========================================
            elif group_name == 'operador_compras':
                permisos = {
                    'proveedores': {'view': True, 'add': True, 'change': True, 'delete': True},
                    'productos': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'producto_proveedor': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'usuarios': {'view': True, 'add': False, 'change': True, 'delete': False},  # Solo editar su perfil
                }
                self._aplicar_permisos(role, permisos)

            # ========================================
            # OPERADOR DE VENTAS - SOLO VISUALIZACION
            # ========================================
            elif group_name == 'operador_ventas':
                permisos = {
                    'productos': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'clientes': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'pedidos': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'listar_precios': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'usuarios': {'view': True, 'add': False, 'change': True, 'delete': False},  # Solo editar su perfil
                }
                self._aplicar_permisos(role, permisos)

            # ============================================
            # OPERADOR DE PRODUCCION - SOLO CRUD PRODUCTO
            # ============================================
            elif group_name == 'operador_produccion':
                permisos = {
                    'productos': {'view': True, 'add': True, 'change': True, 'delete': True},
                    'producto_proveedor': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'proveedores': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'usuarios': {'view': True, 'add': False, 'change': True, 'delete': False},  # Solo editar su perfil
                }
                self._aplicar_permisos(role, permisos)

            # =========================================
            # ANALISTA FINANCIERO - SOLO VISUALIZACION
            # =========================================
            elif group_name == 'analista_financiero':
                permisos = {
                    'usuarios': {'view': True, 'add': False, 'change': True, 'delete': False},
                    'productos': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'proveedores': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'producto_proveedor': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'costos': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'listar_precios': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'clientes': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'pedidos': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'orden_compra': {'view': True, 'add': False, 'change': False, 'delete': False},
                    'movimiento_inventario': {'view': True, 'add': False, 'change': False, 'delete': False},
                }
                self._aplicar_permisos(role, permisos)


        self.stdout.write(self.style.SUCCESS('Sistema de roles inicializado exitosamente!'))

    def _aplicar_permisos(self, role, permisos_dict):
            """
            Aplica permisos específicos para un rol
            permisos_dict: {'module_code': {'view': bool, 'add': bool, 'change': bool, 'delete': bool}}
            """
            for module_code, perms in permisos_dict.items():
                try:
                    module = Module.objects.get(code=module_code)
                    RoleModulePermission.objects.create(
                        role=role,
                        module=module,
                        can_view=perms.get('view', False),
                        can_add=perms.get('add', False),
                        can_change=perms.get('change', False),
                        can_delete=perms.get('delete', False)
                    )
                    actions = []
                    if perms.get('view'): actions.append('Ver')
                    if perms.get('add'): actions.append('Crear')
                    if perms.get('change'): actions.append('Editar')
                    if perms.get('delete'): actions.append('Eliminar')
                    self.stdout.write(f'  → {module.name}: {", ".join(actions) if actions else "Sin permisos"}')
                except Module.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Módulo no encontrado: {module_code}'))