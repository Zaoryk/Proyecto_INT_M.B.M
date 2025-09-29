# dulceria/management/commands/cargardatos_prueba.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dispositivos.models import *

class Command(BaseCommand):
    help = 'Carga datos de prueba para el sistema'

    def handle(self, *args, **options):
        Usuario = get_user_model()
        
        self.stdout.write('Cargando datos de prueba...')

        # Limpiar datos existentes (en el orden correcto por dependencias)
        Factura.objects.all().delete()
        ListaPrecios.objects.all().delete()
        DetalleOrdenCompra.objects.all().delete()
        OrdenCompra.objects.all().delete()
        DetalleSolicitudCompra.objects.all().delete()
        SolicitudCompra.objects.all().delete()
        DetallePedidoVenta.objects.all().delete()
        PedidoVenta.objects.all().delete()
        OrdenProduccion.objects.all().delete()
        Inventario.objects.all().delete()
        RecetaProducto.objects.all().delete()
        Receta.objects.all().delete()
        Producto.objects.all().delete()
        Bodega.objects.all().delete()
        Cliente.objects.all().delete()
        Proveedor.objects.all().delete()
        
        # No eliminar todos los usuarios, solo los que no son superusers
        Usuario.objects.filter(is_superuser=False).delete()

        # Crear usuarios solo si no existen
        if not Usuario.objects.filter(username='admin').exists():
            usuario1 = Usuario.objects.create_user(
                username='admin',
                password='admin123',
                nombre='Administrador Principal',
                rut='12345678-9',
                permisos='superusuario',
                email='admin@empresa.com',
                is_staff=True,
                is_superuser=True
            )
        else:
            usuario1 = Usuario.objects.get(username='admin')

        if not Usuario.objects.filter(username='vendedor1').exists():
            vendedor1 = Usuario.objects.create_user(
                username='vendedor1',
                password='vendedor123',
                nombre='Carlos Vendedor',
                rut='98765432-1',
                permisos='vendedor',
                email='vendedor@empresa.com'
            )
        else:
            vendedor1 = Usuario.objects.get(username='vendedor1')

        if not Usuario.objects.filter(username='comprador1').exists():
            comprador1 = Usuario.objects.create_user(
                username='comprador1',
                password='comprador123',
                nombre='Ana Compradora',
                rut='45678901-2',
                permisos='comprador',
                email='comprador@empresa.com'
            )
        else:
            comprador1 = Usuario.objects.get(username='comprador1')

        # Crear proveedores
        proveedor1 = Proveedor.objects.create(
            nombre='Proveedor ABC S.A.',
            contacto='contacto@proveedorabc.com',
            condiciones='Pago a 30 días'
        )

        proveedor2 = Proveedor.objects.create(
            nombre='Distribuidora XYZ Ltda.',
            contacto='ventas@xyz.com',
            condiciones='Pago contado 5% descuento'
        )

        # Crear productos
        producto1 = Producto.objects.create(
            nombre='Chocolate Amargo',
            base='100g',
            fecha_elaboracion='2024-01-15',
            precio=2500,
            stock=500
        )

        producto2 = Producto.objects.create(
            nombre='Caramelo de Fruta',
            base='50g',
            fecha_elaboracion='2024-01-20',
            precio=800,
            stock=1000
        )

        producto3 = Producto.objects.create(
            nombre='Galletas de Mantequilla',
            base='200g',
            fecha_elaboracion='2024-01-18',
            precio=1800,
            stock=300
        )

        # Crear recetas
        receta1 = Receta.objects.create(
            version='1.0',
            manejo_necesario=18.5
        )

        receta2 = Receta.objects.create(
            version='2.1',
            manejo_necesario=22.0
        )

        # Relacionar recetas con productos
        RecetaProducto.objects.create(
            receta=receta1,
            producto=producto1,
            cantidad=100
        )

        RecetaProducto.objects.create(
            receta=receta2,
            producto=producto2,
            cantidad=200
        )

        # Crear clientes
        cliente1 = Cliente.objects.create(
            nombre='Tienda Dulces S.A.',
            condiciones='Pago a 30 días',
            desde=2022
        )

        cliente2 = Cliente.objects.create(
            nombre='Super Dulcería',
            condiciones='Pago contado',
            desde=2023
        )

        # Crear bodegas
        bodega1 = Bodega.objects.create(
            nombre='Bodega Principal',
            ubicacion='Local Central'
        )

        bodega2 = Bodega.objects.create(
            nombre='Bodega Secundaria',
            ubicacion='Almacén Norte'
        )

        # Crear inventario
        Inventario.objects.create(
            lote='LOTE-CHOCO-001',
            fecha='2024-01-25',
            cantidad=200,
            producto=producto1,
            bodega=bodega1
        )

        Inventario.objects.create(
            lote='LOTE-CARAM-001',
            fecha='2024-01-26',
            cantidad=500,
            producto=producto2,
            bodega=bodega1
        )

        # Crear órdenes de producción
        orden_prod1 = OrdenProduccion.objects.create(
            fecha_inicio='2024-01-27',
            fecha_limite='2024-02-10',
            estado='en_proceso',
            receta=receta1
        )

        # Crear pedidos de venta
        pedido_venta1 = PedidoVenta.objects.create(
            fecha='2024-01-26',
            estado='confirmado',
            monto_total=8300,
            vendedor=vendedor1,
            cliente=cliente1
        )

        # Crear detalles del pedido de venta
        DetallePedidoVenta.objects.create(
            pedido_venta=pedido_venta1,
            producto=producto1,
            cantidad=2,
            precio_unitario=2500
        )

        DetallePedidoVenta.objects.create(
            pedido_venta=pedido_venta1,
            producto=producto2,
            cantidad=4,
            precio_unitario=800
        )

        # Crear factura
        Factura.objects.create(
            fecha='2024-01-26',
            total=8300,
            pedido_venta=pedido_venta1
        )

        # Crear lista de precios
        ListaPrecios.objects.create(
            nombre='Lista Clientes Frecuentes',
            temporada='Enero 2024',
            valor=2300,
            cliente=cliente1,
            producto=producto1
        )

        self.stdout.write(
            self.style.SUCCESS('¡Datos de prueba cargados exitosamente!')
        )
        self.stdout.write('Superusuario: admin / admin123')
        self.stdout.write('Vendedor: vendedor1 / vendedor123')
        self.stdout.write('Comprador: comprador1 / comprador123')