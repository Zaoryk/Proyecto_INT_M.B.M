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
        
        # Guardar fixtures
        with open('fixtures_dulceria.json', 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'Fixtures generados: {len(fixtures)} registros en fixtures_dulceria.json')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Desglose: {len(usuarios)} usuarios, {len(productos)} productos, {len(proveedores)} proveedores, {len(producto_proveedor)} relaciones producto-proveedor')
        )