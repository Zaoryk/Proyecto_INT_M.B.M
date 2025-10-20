from datetime import date, datetime
from django.core.management.base import BaseCommand
from dispositivos.models import (
    Usuario, Producto, Proveedor, ProductoProveedor, Bodega, Cliente, 
    Costo, ListarPrecios, MovimientoInventario, OrdenDeCompra, 
    OrdenProduccion, Pedido
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

            # 5. Bodegas
            self.stdout.write('Creando bodegas')
            bodega_central, created = Bodega.objects.get_or_create(
                idbodega=1,
                defaults={'nombre': 'BOD-CENTRAL', 'ubicacion': 'La Serena'}
            )
            
            bodega_sur, created = Bodega.objects.get_or_create(
                idbodega=2,
                defaults={'nombre': 'BOD-SUR', 'ubicacion': 'Ovalle'}
            )
            
            # 6. Clientes
            self.stdout.write('Creando clientes')
            cliente1, created = Cliente.objects.get_or_create(
                idcliente=1,
                defaults={'nombre': 'Supermercado Lider', 'tipo': 'Minorista'}
            )
            
            cliente2, created = Cliente.objects.get_or_create(
                idcliente=2,
                defaults={'nombre': 'Feria La Serena', 'tipo': 'Mayorista'}
            )

            cliente3, created = Cliente.objects.get_or_create(
                idcliente=3,
                defaults={'nombre': 'Distribuidora Coquimbo', 'tipo': 'Mayorista'}
            )
            
            # 7. ListarPrecios
            self.stdout.write('Creando listas de precios')
            listar_precio1, created = ListarPrecios.objects.get_or_create(
                idlistarprecios=1,
                defaults={
                    'canal': 'Minorista',
                    'temporada': 'Normal',
                    'valor': 1500,
                    'cliente': cliente1
                }
            )
            
            listar_precio2, created = ListarPrecios.objects.get_or_create(
                idlistarprecios=2,
                defaults={
                    'canal': 'Mayorista',
                    'temporada': 'Promoción',
                    'valor': 1300,
                    'cliente': cliente2
                }
            )

            listar_precio3, created = ListarPrecios.objects.get_or_create(
                idlistarprecios=3,
                defaults={
                    'canal': 'Mayorista',
                    'temporada': 'Normal',
                    'valor': 1400,
                    'cliente': cliente3
                }
            )
            
            # 8. Costos
            self.stdout.write('Creando costos')
            costo1, created = Costo.objects.get_or_create(
                idcosto=1,
                defaults={
                    'tipo': 'Producción',
                    'monto': 800,
                    'producto': producto1
                }
            )
            
            costo2, created = Costo.objects.get_or_create(
                idcosto=2,
                defaults={
                    'tipo': 'Embalaje',
                    'monto': 150,
                    'producto': producto1
                }
            )
            
            costo3, created = Costo.objects.get_or_create(
                idcosto=3,
                defaults={
                    'tipo': 'Producción',
                    'monto': 400,
                    'producto': producto2
                }
            )

            costo4, created = Costo.objects.get_or_create(
                idcosto=4,
                defaults={
                    'tipo': 'Logística',
                    'monto': 200,
                    'producto': producto3
                }
            )
            
            # 9. Movimientos de Inventario
            self.stdout.write('Creando movimientos de inventario')
            movimiento1, created = MovimientoInventario.objects.get_or_create(
                idmovimiento=1,
                defaults={
                    'tipo': 'Ingreso',
                    'fecha': date(2025, 1, 15),
                    'cantidad': 100,
                    'bodega': bodega_central,
                    'producto': producto1
                }
            )
            
            movimiento2, created = MovimientoInventario.objects.get_or_create(
                idmovimiento=2,
                defaults={
                    'tipo': 'Salida',
                    'fecha': date(2025, 1, 20),
                    'cantidad': 50,
                    'bodega': bodega_central,
                    'producto': producto1
                }
            )
            
            movimiento3, created = MovimientoInventario.objects.get_or_create(
                idmovimiento=3,
                defaults={
                    'tipo': 'Ingreso',
                    'fecha': date(2025, 1, 10),
                    'cantidad': 150,
                    'bodega': bodega_central,
                    'producto': producto2
                }
            )

            movimiento4, created = MovimientoInventario.objects.get_or_create(
                idmovimiento=4,
                defaults={
                    'tipo': 'Ingreso',
                    'fecha': date(2025, 1, 8),
                    'cantidad': 80,
                    'bodega': bodega_sur,
                    'producto': producto3
                }
            )
            
            # 10. Órdenes de Compra
            self.stdout.write('Creando órdenes de compra')
            orden_compra1, created = OrdenDeCompra.objects.get_or_create(
                id=1,
                defaults={
                    'fecha': date(2025, 1, 5),
                    'estado': 'cerrada',
                    'monto_total': 150000,
                    'proveedor': proveedor1
                }
            )
            
            orden_compra2, created = OrdenDeCompra.objects.get_or_create(
                id=2,
                defaults={
                    'fecha': date(2025, 1, 18),
                    'estado': 'en_proceso',
                    'monto_total': 80000,
                    'proveedor': proveedor2
                }
            )

            orden_compra3, created = OrdenDeCompra.objects.get_or_create(
                id=3,
                defaults={
                    'fecha': date(2025, 1, 22),
                    'estado': 'no_iniciado',
                    'monto_total': 120000,
                    'proveedor': proveedor3
                }
            )
            
            # 11. Órdenes de Producción
            self.stdout.write('Creando órdenes de producción')
            orden_prod1, created = OrdenProduccion.objects.get_or_create(
                id=1,
                defaults={
                    'fechainicio': date(2025, 1, 1),
                    'fechafin': date(2025, 1, 10),
                    'estado': 'Completada',
                    'usuario': usuario_inventario,
                    'producto': producto1
                }
            )
            
            orden_prod2, created = OrdenProduccion.objects.get_or_create(
                id=2,
                defaults={
                    'fechainicio': date(2025, 1, 15),
                    'fechafin': date(2025, 1, 25),
                    'estado': 'En Proceso',
                    'usuario': usuario_inventario,
                    'producto': producto3
                }
            )

            orden_prod3, created = OrdenProduccion.objects.get_or_create(
                id=3,
                defaults={
                    'fechainicio': date(2025, 1, 20),
                    'fechafin': date(2025, 2, 5),
                    'estado': 'Planificada',
                    'usuario': usuario_inventario,
                    'producto': producto2
                }
            )
            
            # 12. Pedidos
            self.stdout.write('Creando pedidos')
            pedido1, created = Pedido.objects.get_or_create(
                idpedido=1,
                defaults={
                    'fecha': date(2025, 1, 12),
                    'monto_total': 45000,
                    'usuario': usuario_ventas,
                    'cliente': cliente1,
                    'ordendecompra': orden_compra1
                }
            )
            
            pedido2, created = Pedido.objects.get_or_create(
                idpedido=2,
                defaults={
                    'fecha': date(2025, 1, 19),
                    'monto_total': 32000,
                    'usuario': usuario_ventas,
                    'cliente': cliente2,
                    'ordendecompra': orden_compra2
                }
            )

            pedido3, created = Pedido.objects.get_or_create(
                idpedido=3,
                defaults={
                    'fecha': date(2025, 1, 24),
                    'monto_total': 28000,
                    'usuario': usuario_ventas,
                    'cliente': cliente3,
                    'ordendecompra': orden_compra3
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
            self.stdout.write(f'Bodegas: {Bodega.objects.count()}')
            self.stdout.write(f'Clientes: {Cliente.objects.count()}')
            self.stdout.write(f'ListarPrecios: {ListarPrecios.objects.count()}')
            self.stdout.write(f'Costos: {Costo.objects.count()}')
            self.stdout.write(f'Movimientos: {MovimientoInventario.objects.count()}')
            self.stdout.write(f'Órdenes Compra: {OrdenDeCompra.objects.count()}')
            self.stdout.write(f'Órdenes Producción: {OrdenProduccion.objects.count()}')
            self.stdout.write(f'Pedidos: {Pedido.objects.count()}')
            self.stdout.write("=" * 60)
            self.stdout.write(self.style.SUCCESS('Todos los datos han sido cargados correctamente'))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar datos: {e}')
            )
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))