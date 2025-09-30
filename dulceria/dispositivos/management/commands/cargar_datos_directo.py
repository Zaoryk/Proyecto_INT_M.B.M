# dispositivos/management/commands/cargar_datos_directo.py
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
from dispositivos.models import (
    ListarPrecios, Usuario, Producto, OrdenProduccion, Proveedor, 
    OrdendeCompra, Bodega, MovimientoInventario, Costo, Cliente, Pedido
)

class Command(BaseCommand):
    help = 'Carga datos directamente en la base de datos con nuevo esquema'

    def handle(self, *args, **options):
        print("=== CARGANDO DATOS CON NUEVO ESQUEMA MYSQL ===")
        
        print("Limpiando datos existentes...")
        self.limpiar_datos()
        
        print("Creando datos...")
        
        # Crear en orden de dependencias
        clientes = self.crear_clientes()
        listas_precios = self.crear_listas_precios(clientes)
        usuarios = self.crear_usuarios(listas_precios)
        proveedores = self.crear_proveedores()
        productos = self.crear_productos()
        bodegas = self.crear_bodegas()
        ordenes_compra = self.crear_ordenes_compra(proveedores)
        
        # Crear datos que dependen de los anteriores
        self.crear_ordenes_produccion(usuarios, productos)
        self.crear_pedidos(usuarios, clientes, ordenes_compra)
        self.crear_movimientos_inventario(bodegas, productos)
        self.crear_costos(productos)
        
        print("¡Datos cargados exitosamente!")
        print("=== USUARIOS DISPONIBLES ===")
        print("Administrador: admin123")
        print("Vendedor: vendedor123") 

    def limpiar_datos(self):
        """Limpia los datos existentes en orden inverso de dependencias"""
        Pedido.objects.all().delete()
        OrdenProduccion.objects.all().delete()
        MovimientoInventario.objects.all().delete()
        Costo.objects.all().delete()
        OrdendeCompra.objects.all().delete()
        Producto.objects.all().delete()
        Bodega.objects.all().delete()
        Proveedor.objects.all().delete()
        Usuario.objects.all().delete()
        ListarPrecios.objects.all().delete()
        Cliente.objects.all().delete()

    def crear_clientes(self):
        """Crea clientes"""
        print("--- Creando clientes ---")
        
        clientes_data = [
            {'nombre': 'Supermercado Central', 'tipo': 'mayorista'},
            {'nombre': 'Tienda Dulce Sabor', 'tipo': 'minorista'},
            {'nombre': 'Distribuidora Norte', 'tipo': 'mayorista'},
        ]
        
        clientes_creados = []
        for data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            status = "creado" if created else "ya existía"
            print(f"✓ Cliente {cliente.nombre} ({status})")
            clientes_creados.append(cliente)
            
        return clientes_creados

    def crear_listas_precios(self, clientes):
        """Crea listas de precios"""
        print("--- Creando listas de precios ---")
        
        listas_data = [
            {'canal': 'Mayorista', 'temporada': 'Verano 2025', 'valor': 2800, 'cliente_idcliente': clientes[0].idcliente},
            {'canal': 'Minorista', 'temporada': 'Verano 2025', 'valor': 3200, 'cliente_idcliente': clientes[1].idcliente},
            {'canal': 'Mayorista', 'temporada': 'Verano 2025', 'valor': 2700, 'cliente_idcliente': clientes[2].idcliente},
        ]
        
        listas_creadas = []
        for data in listas_data:
            lista, created = ListarPrecios.objects.get_or_create(
                canal=data['canal'],
                temporada=data['temporada'],
                cliente_idcliente=data['cliente_idcliente'],
                defaults=data
            )
            status = "creada" if created else "ya existía"
            print(f"✓ Lista precio {lista.canal} - {lista.temporada} ({status})")
            listas_creadas.append(lista)
            
        return listas_creadas

    def crear_usuarios(self, listas_precios):
        """Crea usuarios"""
        print("--- Creando usuarios ---")
        
        usuarios_data = [
            {
                'nombre': 'Administrador Principal',
                'rol': 'admin',
                'password': 'admin123',
                'email': 'admin@empresa.com',
                'listarprecios_idlistarprecios': listas_precios[0].idlistarprecios,
                'listarprecios_cliente_idcliente': listas_precios[0].cliente_idcliente
            },
            {
                'nombre': 'Carlos Vendedor',
                'rol': 'vendedor',
                'password': 'vendedor123',
                'email': 'vendedor@empresa.com',
                'listarprecios_idlistarprecios': listas_precios[1].idlistarprecios,
                'listarprecios_cliente_idcliente': listas_precios[1].cliente_idcliente
            },
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
            {'nombre': 'Proveedor ABC S.A.', 'contacto': 'Juan Pérez', 'email': 'contacto@proveedorabc.com'},
            {'nombre': 'Distribuidora XYZ Ltda.', 'contacto': 'María González', 'email': 'ventas@xyz.com'},
            {'nombre': 'Dulces Nacionales S.A.', 'contacto': 'Roberto Silva', 'email': 'info@dulcesnacionales.cl'},
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

    def crear_productos(self):
        """Crea productos"""
        print("--- Creando productos ---")
        
        fecha_vencimiento = datetime.now() + timedelta(days=365)
        
        productos_data = [
            {
                'nombre': 'Chocolate Amargo 70%',
                'lote': 'LOTE-CHOCO-001',
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 3500,
                'stock': 150
            },
            {
                'nombre': 'Caramelo de Fruta Mix',
                'lote': 'LOTE-CARAM-001',
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 1200,
                'stock': 300
            },
            {
                'nombre': 'Gomitas de Ositos',
                'lote': 'LOTE-GOMI-001',
                'fecha_vencimiento': fecha_vencimiento,
                'precio': 1800,
                'stock': 200
            },
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
            {'nombre': 'Bodega Principal', 'ubicacion': 'Local Central'},
            {'nombre': 'Bodega Secundaria', 'ubicacion': 'Almacén Norte'},
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

    def crear_ordenes_compra(self, proveedores):
        """Crea órdenes de compra"""
        print("--- Creando órdenes de compra ---")
        
        ordenes_data = [
            {
                'fecha': datetime.now().date(),
                'estado': 'pendiente',
                'monto_total': 150000,
                'proveedor': proveedores[0]
            },
            {
                'fecha': datetime.now().date(),
                'estado': 'completada',
                'monto_total': 200000,
                'proveedor': proveedores[1]
            },
        ]
        
        ordenes_creadas = []
        for data in ordenes_data:
            orden, created = OrdendeCompra.objects.get_or_create(
                fecha=data['fecha'],
                proveedor=data['proveedor'],
                defaults=data
            )
            status = "creada" if created else "ya existía"
            print(f"✓ Orden compra {orden.id} - ${orden.monto_total} ({status})")
            ordenes_creadas.append(orden)
            
        return ordenes_creadas

    def crear_ordenes_produccion(self, usuarios, productos):
        """Crea órdenes de producción"""
        print("--- Creando órdenes de producción ---")
        
        orden_data = {
            'fechainicio': datetime.now().date(),
            'fechafin': datetime.now().date() + timedelta(days=14),
            'estado': 'en_proceso',
            'usuario': usuarios[0],
            'producto': productos[0]
        }
        
        try:
            orden, created = OrdenProduccion.objects.get_or_create(
                fechainicio=orden_data['fechainicio'],
                producto=orden_data['producto'],
                defaults=orden_data
            )
            if created:
                print(f"✓ Orden producción: {orden.producto.nombre}")
        except Exception as e:
            print(f"⚠ Error en orden producción: {e}")

    def crear_pedidos(self, usuarios, clientes, ordenes_compra):
        """Crea pedidos"""
        print("--- Creando pedidos ---")
        
        pedido_data = {
            'fecha': datetime.now().date(),
            'monto_total': 14600,
            'usuario': usuarios[1],
            'cliente': clientes[0],
            'ordendecompra': ordenes_compra[0]
        }
        
        try:
            pedido, created = Pedido.objects.get_or_create(
                fecha=pedido_data['fecha'],
                usuario=pedido_data['usuario'],
                cliente=pedido_data['cliente'],
                defaults=pedido_data
            )
            if created:
                print(f"✓ Pedido creado - Cliente: {pedido.cliente.nombre} - Total: ${pedido.monto_total}")
        except Exception as e:
            print(f"⚠ Error creando pedido: {e}")

    def crear_movimientos_inventario(self, bodegas, productos):
        """Crea movimientos de inventario"""
        print("--- Creando movimientos de inventario ---")
        
        for producto in productos:
            movimiento_data = {
                'tipo': 'entrada',
                'fecha': datetime.now().date(),
                'cantidad': str(producto.stock),
                'bodega': bodegas[0],
                'producto': producto
            }
            
            try:
                movimiento, created = MovimientoInventario.objects.get_or_create(
                    producto=movimiento_data['producto'],
                    bodega=movimiento_data['bodega'],
                    defaults=movimiento_data
                )
                if created:
                    print(f"✓ Movimiento: {producto.nombre} - {movimiento.cantidad} unidades")
            except Exception as e:
                print(f"⚠ Error en movimiento inventario: {e}")

    def crear_costos(self, productos):
        """Crea costos asociados a productos"""
        print("--- Creando costos ---")
        
        for producto in productos:
            costo_data = {
                'tipo': 'produccion',
                'monto': producto.precio * 60 // 100,  # 60% del precio como costo
                'producto': producto
            }
            
            try:
                costo, created = Costo.objects.get_or_create(
                    producto=costo_data['producto'],
                    tipo=costo_data['tipo'],
                    defaults=costo_data
                )
                if created:
                    print(f"✓ Costo: {producto.nombre} - ${costo.monto}")
            except Exception as e:
                print(f"⚠ Error en costo: {e}")