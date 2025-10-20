from datetime import date, datetime
from django.core.management.base import BaseCommand
from dispositivos.models import (
    Usuario, Producto, Proveedor, ProductoProveedor
)

class Command(BaseCommand):
    help = 'Crea datos de prueba directamente en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de prueba...')
        
        try:
            # 1. Usuarios (primero porque otros modelos dependen de ellos)
            self.stdout.write('Creando usuarios')
            usuario_admin, created = Usuario.objects.get_or_create(
                idUsuario=1,
                defaults={
                    'username': 'admin',
                    'email': 'admin@dulcerialilis.cl',
                    'nombre': 'Admin',
                    'apellido': 'Principal',
                    'rol': 'administrador',
                    'estado': 'activo',
                    'mfa_habilitado': 'deshabilitado',
                    'password': 'pbkdf2_sha256$600000$TEST$TEST'
                }
            )
            
            usuario_inventario, created = Usuario.objects.get_or_create(
                idUsuario=2,
                defaults={
                    'username': 'inventario',
                    'email': 'inventario@dulcerialilis.cl',
                    'nombre': 'Operador',
                    'apellido': 'Inventario',
                    'rol': 'operador_inventario',
                    'estado': 'activo',
                    'mfa_habilitado': 'deshabilitado',
                    'password': 'pbkdf2_sha256$600000$TEST$TEST'
                }
            )
            
            usuario_ventas, created = Usuario.objects.get_or_create(
                idUsuario=3,
                defaults={
                    'username': 'ventas',
                    'email': 'ventas@dulcerialilis.cl',
                    'nombre': 'Operador',
                    'apellido': 'Ventas',
                    'rol': 'operador_ventas',
                    'estado': 'activo',
                    'mfa_habilitado': 'deshabilitado',
                    'password': 'pbkdf2_sha256$600000$TEST$TEST'
                }
            )

            usuario_compras, created = Usuario.objects.get_or_create(
                idUsuario=4,
                defaults={
                    'username': 'compras',
                    'email': 'compras@dulcerialilis.cl',
                    'nombre': 'Operador',
                    'apellido': 'Compras',
                    'rol': 'operador_compras',
                    'estado': 'activo',
                    'mfa_habilitado': 'deshabilitado',
                    'password': 'pbkdf2_sha256$600000$TEST$TEST'
                }
            )

            # 2. Productos
            self.stdout.write('Creando productos')
            producto1, created = Producto.objects.get_or_create(
                idProducto=1,
                defaults={
                    'sku': 'SKU-CHOC-001',
                    'nombre': 'Chocolate Amargo 100g',
                    'categoria': 'Chocolates',
                    'uom_compra': 'kg',
                    'uom_venta': 'unidad',
                    'factor_conversion': 10,
                    'impuesto_iva': 19,
                    'stock_minimo': 20,
                    'perishable': 1,
                    'lote': 1001
                }
            )
            
            producto2, created = Producto.objects.get_or_create(
                idProducto=2,
                defaults={
                    'sku': 'SKU-CAR-001',
                    'nombre': 'Caramelo Frutal 500g',
                    'categoria': 'Caramelos',
                    'uom_compra': 'kg',
                    'uom_venta': 'bolsa',
                    'factor_conversion': 2,
                    'impuesto_iva': 19,
                    'stock_minimo': 30,
                    'perishable': 1,
                    'lote': 1002
                }
            )
            
            producto3, created = Producto.objects.get_or_create(
                idProducto=3,
                defaults={
                    'sku': 'SKU-GAL-001',
                    'nombre': 'Galletas Vainilla 200g',
                    'categoria': 'Galletas',
                    'uom_compra': 'caja',
                    'uom_venta': 'paquete',
                    'factor_conversion': 1,
                    'impuesto_iva': 19,
                    'stock_minimo': 15,
                    'perishable': 1,
                    'lote': 1003
                }
            )

            # 3. Proveedores
            self.stdout.write('Creando proveedores')
            proveedor1, created = Proveedor.objects.get_or_create(
                idProveedor=1,
                defaults={
                    'rut_nif': '76.123.456-7',
                    'razon_social': 'Proveedor Andino S.A.',
                    'nombre_fantasia': 'Andino Distribuciones',
                    'email': 'contacto@andino.cl',
                    'pais': 'Chile',
                    'condiciones_pago': '30 días',
                    'moneda': 'CLP',
                    'estado': 'activo',
                    'usuario': usuario_compras
                }
            )
            
            proveedor2, created = Proveedor.objects.get_or_create(
                idProveedor=2,
                defaults={
                    'rut_nif': '76.765.432-1',
                    'razon_social': 'Electro Patagon SpA',
                    'nombre_fantasia': 'ElectroPatagon',
                    'email': 'ventas@electropatagon.cl',
                    'pais': 'Chile',
                    'condiciones_pago': '15 días',
                    'moneda': 'CLP',
                    'estado': 'activo',
                    'usuario': usuario_compras
                }
            )

            proveedor3, created = Proveedor.objects.get_or_create(
                idProveedor=3,
                defaults={
                    'rut_nif': '76.987.654-3',
                    'razon_social': 'Dulces del Norte Ltda.',
                    'nombre_fantasia': 'Dulces Norte',
                    'email': 'info@dulcesnorte.cl',
                    'pais': 'Chile',
                    'condiciones_pago': '30 días',
                    'moneda': 'CLP',
                    'estado': 'activo',
                    'usuario': usuario_compras
                }
            )

            # 4. ProductoProveedor (Relaciones)
            self.stdout.write('Creando relaciones producto-proveedor')
            producto_proveedor1, created = ProductoProveedor.objects.get_or_create(
                idProducto_Proveedor=1,
                defaults={
                    'tipo_movimiento': 'entrada',
                    'cantidad': 1000,
                    'fecha_movimiento': datetime(2025, 1, 10, 10, 0, 0),
                    'producto': producto1,
                    'proveedor': proveedor1
                }
            )

            producto_proveedor2, created = ProductoProveedor.objects.get_or_create(
                idProducto_Proveedor=2,
                defaults={
                    'tipo_movimiento': 'entrada',
                    'cantidad': 500,
                    'fecha_movimiento': datetime(2025, 1, 12, 14, 30, 0),
                    'producto': producto2,
                    'proveedor': proveedor2
                }
            )

            producto_proveedor3, created = ProductoProveedor.objects.get_or_create(
                idProducto_Proveedor=3,
                defaults={
                    'tipo_movimiento': 'entrada',
                    'cantidad': 750,
                    'fecha_movimiento': datetime(2025, 1, 15, 9, 15, 0),
                    'producto': producto3,
                    'proveedor': proveedor3
                }
            )
            
            # Resumen
            self.stdout.write(
                self.style.SUCCESS('\n DATOS CARGADOS EXITOSAMENTE')
            )
            self.stdout.write("=" * 60)
            self.stdout.write(f'Usuarios: {Usuario.objects.count()}')
            self.stdout.write(f'Productos: {Producto.objects.count()}')
            self.stdout.write(f'Proveedores: {Proveedor.objects.count()}')
            self.stdout.write(f'Relaciones Producto-Proveedor: {ProductoProveedor.objects.count()}')
            self.stdout.write("=" * 60)
            self.stdout.write(self.style.SUCCESS('Todos los datos han sido cargados correctamente'))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar datos: {e}')
            )
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))