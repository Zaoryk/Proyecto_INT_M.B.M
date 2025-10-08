from datetime import date
from django.core.management.base import BaseCommand
from dispositivos.models import (
    Bodega, Cliente, Producto, Costo, ListarPrecios, 
    MovimientoInventario, Proveedor, OrdenDeCompra, 
    Usuario, OrdenProduccion, Pedido
)

class Command(BaseCommand):
    help = 'Crea datos de prueba directamente en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de prueba...')
        
        try:
            # 1. Bodegas
            self.stdout.write('Creando bodegas')
            bodega_central, created = Bodega.objects.get_or_create(
                idbodega=1,
                defaults={'nombre': 'BOD-CENTRAL', 'ubicacion': 'La Serena'}
            )
            
            bodega_sur, created = Bodega.objects.get_or_create(
                idbodega=2,
                defaults={'nombre': 'BOD-SUR', 'ubicacion': 'Ovalle'}
            )
            
            # 2. Clientes
            self.stdout.write('Creando clientes')
            cliente1, created = Cliente.objects.get_or_create(
                idcliente=1,
                defaults={'nombre': 'Supermercado Lider', 'tipo': 'Minorista'}
            )
            
            cliente2, created = Cliente.objects.get_or_create(
                idcliente=2,
                defaults={'nombre': 'Feria La Serena', 'tipo': 'Mayorista'}
            )
            
            # 3. Proveedores
            self.stdout.write('Creando proveedores')
            proveedor1, created = Proveedor.objects.get_or_create(
                id_proveedor=1,
                defaults={
                    'nombre': 'Proveedor Andino S.A.', 
                    'contacto': 'Juan Pérez', 
                    'email': 'contacto@andino.cl'
                }
            )
            
            proveedor2, created = Proveedor.objects.get_or_create(
                id_proveedor=2,
                defaults={
                    'nombre': 'Electro Patagon SpA', 
                    'contacto': 'María González', 
                    'email': 'ventas@electropatagon.cl'
                }
            )
            
            # 4. Productos
            self.stdout.write('Creando productos')
            producto1, created = Producto.objects.get_or_create(
                idproducto=1,
                defaults={
                    'nombre': 'Chocolate Amargo 100g',
                    'lote': 'LOTE-CHOC-001',
                    'fecha_vencimiento': date(2025, 12, 31),
                    'precio': 1500,
                    'stock': 50
                }
            )
            
            producto2, created = Producto.objects.get_or_create(
                idproducto=2,
                defaults={
                    'nombre': 'Caramelo Frutal 500g',
                    'lote': 'LOTE-CAR-001',
                    'fecha_vencimiento': date(2025, 10, 15),
                    'precio': 800,
                    'stock': 100
                }
            )
            
            producto3, created = Producto.objects.get_or_create(
                idproducto=3,
                defaults={
                    'nombre': 'Galletas Vainilla 200g',
                    'lote': 'LOTE-GAL-001',
                    'fecha_vencimiento': date(2025, 11, 20),
                    'precio': 1200,
                    'stock': 75
                }
            )
            
            # 5. ListarPrecios
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
            
            # 6. Usuarios
            self.stdout.write('Creando usuarios')
            usuario_admin, created = Usuario.objects.get_or_create(
                id=1,
                defaults={
                    'nombre': 'Admin Principal',
                    'rol': 'administrador',
                    'password': 'pbkdf2_sha256$600000$TEST$TEST',
                    'email': 'admin@dulcerialilis.cl'
                }
            )
            
            usuario_inventario, created = Usuario.objects.get_or_create(
                id=2,
                defaults={
                    'nombre': 'Operador Inventario',
                    'rol': 'operador_inventario',
                    'password': 'pbkdf2_sha256$600000$TEST$TEST',
                    'email': 'inventario@dulcerialilis.cl'
                }
            )
            
            usuario_ventas, created = Usuario.objects.get_or_create(
                id=3,
                defaults={
                    'nombre': 'Operador Ventas',
                    'rol': 'operador_ventas',
                    'password': 'pbkdf2_sha256$600000$TEST$TEST',
                    'email': 'ventas@dulcerialilis.cl'
                }
            )
            
            # 7. Costos
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
            
            # 8. Movimientos de Inventario
            self.stdout.write('Creando movimientos de inventario')
            movimiento1, created = MovimientoInventario.objects.get_or_create(
                idmovimiento=1,
                defaults={
                    'tipo': 'Ingreso',
                    'fecha': date(2025, 1, 15),
                    'cantidad': '100',
                    'bodega': bodega_central,
                    'producto': producto1
                }
            )
            
            movimiento2, created = MovimientoInventario.objects.get_or_create(
                idmovimiento=2,
                defaults={
                    'tipo': 'Salida',
                    'fecha': date(2025, 1, 20),
                    'cantidad': '50',
                    'bodega': bodega_central,
                    'producto': producto1
                }
            )
            
            movimiento3, created = MovimientoInventario.objects.get_or_create(
                idmovimiento=3,
                defaults={
                    'tipo': 'Ingreso',
                    'fecha': date(2025, 1, 10),
                    'cantidad': '150',
                    'bodega': bodega_central,
                    'producto': producto2
                }
            )
            
            # 9. Órdenes de Compra
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
            
            # 10. Órdenes de Producción
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
            
            # 11. Pedidos
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
            
            # Resumen
            self.stdout.write(
                self.style.SUCCESS('\n DATOS CARGADOS')
            )
            self.stdout.write("=" * 50)
            self.stdout.write(f'Bodegas: {Bodega.objects.count()}')
            self.stdout.write(f'Clientes: {Cliente.objects.count()}')
            self.stdout.write(f'Productos: {Producto.objects.count()}')
            self.stdout.write(f'Proveedores: {Proveedor.objects.count()}')
            self.stdout.write(f'Usuarios: {Usuario.objects.count()}')
            self.stdout.write(f'ListarPrecios: {ListarPrecios.objects.count()}')
            self.stdout.write(f'Costos: {Costo.objects.count()}')
            self.stdout.write(f'Movimientos: {MovimientoInventario.objects.count()}')
            self.stdout.write(f'Órdenes Compra: {OrdenDeCompra.objects.count()}')
            self.stdout.write(f'Órdenes Producción: {OrdenProduccion.objects.count()}')
            self.stdout.write(f'Pedidos: {Pedido.objects.count()}')
            self.stdout.write("=" * 50)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar datos: {e}')
            )
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))