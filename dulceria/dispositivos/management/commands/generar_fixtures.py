import json
from datetime import date, datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Genera fixtures para la dulcería Lilis'

    def handle(self, *args, **options):
        fixtures = []
        
        # 1. Usuarios (primero por dependencias)
        usuarios = [
            {
                "model": "dispositivos.usuario", 
                "pk": 1, 
                "fields": {
                    "username": "admin",
                    "email": "admin@dulcerialilis.cl",
                    "nombre": "Admin",
                    "apellido": "Principal",
                    "rol": "administrador",
                    "estado": "activo",
                    "mfa_habilitado": "deshabilitado",
                    "password": "pbkdf2_sha256$600000$TEST$TEST"
                }
            },
            {
                "model": "dispositivos.usuario", 
                "pk": 2, 
                "fields": {
                    "username": "inventario",
                    "email": "inventario@dulcerialilis.cl",
                    "nombre": "Operador",
                    "apellido": "Inventario",
                    "rol": "operador_inventario",
                    "estado": "activo",
                    "mfa_habilitado": "deshabilitado",
                    "password": "pbkdf2_sha256$600000$TEST$TEST"
                }
            },
            {
                "model": "dispositivos.usuario", 
                "pk": 3, 
                "fields": {
                    "username": "ventas",
                    "email": "ventas@dulcerialilis.cl",
                    "nombre": "Operador",
                    "apellido": "Ventas",
                    "rol": "operador_ventas",
                    "estado": "activo",
                    "mfa_habilitado": "deshabilitado",
                    "password": "pbkdf2_sha256$600000$TEST$TEST"
                }
            },
            {
                "model": "dispositivos.usuario", 
                "pk": 4, 
                "fields": {
                    "username": "compras",
                    "email": "compras@dulcerialilis.cl",
                    "nombre": "Operador",
                    "apellido": "Compras",
                    "rol": "operador_compras",
                    "estado": "activo",
                    "mfa_habilitado": "deshabilitado",
                    "password": "pbkdf2_sha256$600000$TEST$TEST"
                }
            }
        ]
        fixtures.extend(usuarios)
        
        # 2. Productos
        productos = [
            {
                "model": "dispositivos.producto", 
                "pk": 1, 
                "fields": {
                    "sku": "SKU-CHOC-001",
                    "nombre": "Chocolate Amargo 100g",
                    "categoria": "Chocolates",
                    "uom_compra": "kg",
                    "uom_venta": "unidad",
                    "factor_conversion": 10,
                    "impuesto_iva": 19,
                    "stock_minimo": 20,
                    "perishable": 1,
                    "lote": 1001
                }
            },
            {
                "model": "dispositivos.producto", 
                "pk": 2, 
                "fields": {
                    "sku": "SKU-CAR-001",
                    "nombre": "Caramelo Frutal 500g",
                    "categoria": "Caramelos",
                    "uom_compra": "kg",
                    "uom_venta": "bolsa",
                    "factor_conversion": 2,
                    "impuesto_iva": 19,
                    "stock_minimo": 30,
                    "perishable": 1,
                    "lote": 1002
                }
            },
            {
                "model": "dispositivos.producto", 
                "pk": 3, 
                "fields": {
                    "sku": "SKU-GAL-001",
                    "nombre": "Galletas Vainilla 200g",
                    "categoria": "Galletas",
                    "uom_compra": "caja",
                    "uom_venta": "paquete",
                    "factor_conversion": 1,
                    "impuesto_iva": 19,
                    "stock_minimo": 15,
                    "perishable": 1,
                    "lote": 1003
                }
            }
        ]
        fixtures.extend(productos)
        
        # 3. Proveedores
        proveedores = [
            {
                "model": "dispositivos.proveedor", 
                "pk": 1, 
                "fields": {
                    "rut_nif": "76.123.456-7",
                    "razon_social": "Proveedor Andino S.A.",
                    "nombre_fantasia": "Andino Distribuciones",
                    "email": "contacto@andino.cl",
                    "pais": "Chile",
                    "condiciones_pago": "30 días",
                    "moneda": "CLP",
                    "estado": "activo",
                    "usuario": 4  # usuario_compras
                }
            },
            {
                "model": "dispositivos.proveedor", 
                "pk": 2, 
                "fields": {
                    "rut_nif": "76.765.432-1",
                    "razon_social": "Electro Patagon SpA",
                    "nombre_fantasia": "ElectroPatagon",
                    "email": "ventas@electropatagon.cl",
                    "pais": "Chile",
                    "condiciones_pago": "15 días",
                    "moneda": "CLP",
                    "estado": "activo",
                    "usuario": 4  # usuario_compras
                }
            },
            {
                "model": "dispositivos.proveedor", 
                "pk": 3, 
                "fields": {
                    "rut_nif": "76.987.654-3",
                    "razon_social": "Dulces del Norte Ltda.",
                    "nombre_fantasia": "Dulces Norte",
                    "email": "info@dulcesnorte.cl",
                    "pais": "Chile",
                    "condiciones_pago": "30 días",
                    "moneda": "CLP",
                    "estado": "activo",
                    "usuario": 4  # usuario_compras
                }
            }
        ]
        fixtures.extend(proveedores)
        
        # 4. ProductoProveedor (Relaciones)
        producto_proveedor = [
            {
                "model": "dispositivos.productoproveedor", 
                "pk": 1, 
                "fields": {
                    "tipo_movimiento": "entrada",
                    "cantidad": 1000,
                    "fecha_movimiento": "2025-01-10T10:00:00Z",
                    "producto": 1,
                    "proveedor": 1
                }
            },
            {
                "model": "dispositivos.productoproveedor", 
                "pk": 2, 
                "fields": {
                    "tipo_movimiento": "entrada",
                    "cantidad": 500,
                    "fecha_movimiento": "2025-01-12T14:30:00Z",
                    "producto": 2,
                    "proveedor": 2
                }
            },
            {
                "model": "dispositivos.productoproveedor", 
                "pk": 3, 
                "fields": {
                    "tipo_movimiento": "entrada",
                    "cantidad": 750,
                    "fecha_movimiento": "2025-01-15T09:15:00Z",
                    "producto": 3,
                    "proveedor": 3
                }
            }
        ]
        fixtures.extend(producto_proveedor)
        
        # 5. Bodegas
        bodegas = [
            {
                "model": "dispositivos.bodega", 
                "pk": 1, 
                "fields": {
                    "nombre": "BOD-CENTRAL", 
                    "ubicacion": "La Serena"
                }
            },
            {
                "model": "dispositivos.bodega", 
                "pk": 2, 
                "fields": {
                    "nombre": "BOD-SUR", 
                    "ubicacion": "Ovalle"
                }
            },
        ]
        fixtures.extend(bodegas)
        
        # 6. Clientes
        clientes = [
            {
                "model": "dispositivos.cliente", 
                "pk": 1, 
                "fields": {
                    "nombre": "Supermercado Lider", 
                    "tipo": "Minorista"
                }
            },
            {
                "model": "dispositivos.cliente", 
                "pk": 2, 
                "fields": {
                    "nombre": "Feria La Serena", 
                    "tipo": "Mayorista"
                }
            },
            {
                "model": "dispositivos.cliente", 
                "pk": 3, 
                "fields": {
                    "nombre": "Distribuidora Coquimbo", 
                    "tipo": "Mayorista"
                }
            },
        ]
        fixtures.extend(clientes)
        
        # 7. ListarPrecios
        listar_precios = [
            {
                "model": "dispositivos.listarprecios", 
                "pk": 1, 
                "fields": {
                    "canal": "Minorista", 
                    "temporada": "Normal", 
                    "valor": 1500, 
                    "cliente": 1
                }
            },
            {
                "model": "dispositivos.listarprecios", 
                "pk": 2, 
                "fields": {
                    "canal": "Mayorista", 
                    "temporada": "Promoción", 
                    "valor": 1300, 
                    "cliente": 2
                }
            },
            {
                "model": "dispositivos.listarprecios", 
                "pk": 3, 
                "fields": {
                    "canal": "Mayorista", 
                    "temporada": "Normal", 
                    "valor": 1400, 
                    "cliente": 3
                }
            },
        ]
        fixtures.extend(listar_precios)
        
        # 8. Costos
        costos = [
            {
                "model": "dispositivos.costo", 
                "pk": 1, 
                "fields": {
                    "tipo": "Producción", 
                    "monto": 800, 
                    "producto": 1
                }
            },
            {
                "model": "dispositivos.costo", 
                "pk": 2, 
                "fields": {
                    "tipo": "Embalaje", 
                    "monto": 150, 
                    "producto": 1
                }
            },
            {
                "model": "dispositivos.costo", 
                "pk": 3, 
                "fields": {
                    "tipo": "Producción", 
                    "monto": 400, 
                    "producto": 2
                }
            },
            {
                "model": "dispositivos.costo", 
                "pk": 4, 
                "fields": {
                    "tipo": "Logística", 
                    "monto": 200, 
                    "producto": 3
                }
            },
        ]
        fixtures.extend(costos)
        
        # 9. MovimientosInventario
        movimientos = [
            {
                "model": "dispositivos.movimientoinventario", 
                "pk": 1, 
                "fields": {
                    "tipo": "Ingreso", 
                    "fecha": "2025-01-15", 
                    "cantidad": 100, 
                    "bodega": 1, 
                    "producto": 1
                }
            },
            {
                "model": "dispositivos.movimientoinventario", 
                "pk": 2, 
                "fields": {
                    "tipo": "Salida", 
                    "fecha": "2025-01-20", 
                    "cantidad": 50, 
                    "bodega": 1, 
                    "producto": 1
                }
            },
            {
                "model": "dispositivos.movimientoinventario", 
                "pk": 3, 
                "fields": {
                    "tipo": "Ingreso", 
                    "fecha": "2025-01-10", 
                    "cantidad": 150, 
                    "bodega": 1, 
                    "producto": 2
                }
            },
            {
                "model": "dispositivos.movimientoinventario", 
                "pk": 4, 
                "fields": {
                    "tipo": "Ingreso", 
                    "fecha": "2025-01-08", 
                    "cantidad": 80, 
                    "bodega": 2, 
                    "producto": 3
                }
            },
        ]
        fixtures.extend(movimientos)
        
        # 10. OrdenesDeCompra
        ordenes_compra = [
            {
                "model": "dispositivos.ordendecompra", 
                "pk": 1, 
                "fields": {
                    "fecha": "2025-01-05", 
                    "estado": "cerrada", 
                    "monto_total": 150000, 
                    "proveedor": 1
                }
            },
            {
                "model": "dispositivos.ordendecompra", 
                "pk": 2, 
                "fields": {
                    "fecha": "2025-01-18", 
                    "estado": "en_proceso", 
                    "monto_total": 80000, 
                    "proveedor": 2
                }
            },
            {
                "model": "dispositivos.ordendecompra", 
                "pk": 3, 
                "fields": {
                    "fecha": "2025-01-22", 
                    "estado": "no_iniciado", 
                    "monto_total": 120000, 
                    "proveedor": 3
                }
            },
        ]
        fixtures.extend(ordenes_compra)
        
        # 11. OrdenesProduccion
        ordenes_produccion = [
            {
                "model": "dispositivos.ordenproduccion", 
                "pk": 1, 
                "fields": {
                    "fechainicio": "2025-01-01", 
                    "fechafin": "2025-01-10", 
                    "estado": "Completada", 
                    "usuario": 2, 
                    "producto": 1
                }
            },
            {
                "model": "dispositivos.ordenproduccion", 
                "pk": 2, 
                "fields": {
                    "fechainicio": "2025-01-15", 
                    "fechafin": "2025-01-25", 
                    "estado": "En Proceso", 
                    "usuario": 2, 
                    "producto": 3
                }
            },
            {
                "model": "dispositivos.ordenproduccion", 
                "pk": 3, 
                "fields": {
                    "fechainicio": "2025-01-20", 
                    "fechafin": "2025-02-05", 
                    "estado": "Planificada", 
                    "usuario": 2, 
                    "producto": 2
                }
            },
        ]
        fixtures.extend(ordenes_produccion)
        
        # 12. Pedidos
        pedidos = [
            {
                "model": "dispositivos.pedido", 
                "pk": 1, 
                "fields": {
                    "fecha": "2025-01-12", 
                    "monto_total": 45000, 
                    "usuario": 3, 
                    "cliente": 1, 
                    "ordendecompra": 1
                }
            },
            {
                "model": "dispositivos.pedido", 
                "pk": 2, 
                "fields": {
                    "fecha": "2025-01-19", 
                    "monto_total": 32000, 
                    "usuario": 3, 
                    "cliente": 2, 
                    "ordendecompra": 2
                }
            },
            {
                "model": "dispositivos.pedido", 
                "pk": 3, 
                "fields": {
                    "fecha": "2025-01-24", 
                    "monto_total": 28000, 
                    "usuario": 3, 
                    "cliente": 3, 
                    "ordendecompra": 3
                }
            },
        ]
        fixtures.extend(pedidos)
        
        # Guardar fixtures
        with open('fixtures_dulceria.json', 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'Fixtures generados: {len(fixtures)} registros en fixtures_dulceria.json')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Desglose: {len(usuarios)} usuarios, {len(productos)} productos, {len(proveedores)} proveedores, etc.')
        )