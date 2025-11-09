import json
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Genera fixtures creativos para la dulcería Lilis'

    def handle(self, *args, **options):
        fixtures = []

        # 1. Usuarios base (puedes agregar los que quieras)
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
                    "password": "Admin#123"
                }
            },
            {
                "model": "dispositivos.usuario",
                "pk": 2,
                "fields": {
                    "username": "inventario",
                    "email": "inventario@dulcerialilis.cl",
                    "nombre": "Tomás",
                    "apellido": "Gallardo",
                    "rol": "operador_inventario",
                    "estado": "activo",
                    "mfa_habilitado": "deshabilitado",
                    "password": "Inventario#001"
                }
            },
            {
                "model": "dispositivos.usuario",
                "pk": 3,
                "fields": {
                    "username": "ventas",
                    "email": "ventas@dulcerialilis.cl",
                    "nombre": "Andrea",
                    "apellido": "Sánchez",
                    "rol": "operador_ventas",
                    "estado": "activo",
                    "mfa_habilitado": "deshabilitado",
                    "password": "Ventas#001"
                }
            },
            {
                "model": "dispositivos.usuario",
                "pk": 4,
                "fields": {
                    "username": "compras",
                    "email": "compras@dulcerialilis.cl",
                    "nombre": "Martín",
                    "apellido": "Lagos",
                    "rol": "operador_compras",
                    "estado": "activo",
                    "mfa_habilitado": "deshabilitado",
                    "password": "Compras#001"
                }
            }
        ]
        fixtures.extend(usuarios)

                # 5. Categorías (6 creativas)
        categorias_lista = [
            {"nombre": "Chocolates", "descripcion": "Producto a base de cacao", "estado": "activo"},
            {"nombre": "Caramelos", "descripcion": "Golosinas duras y blandas variadas", "estado": "activo"},
            {"nombre": "Galletas", "descripcion": "Dulces secos, ideales para café o té", "estado": "activo"},
            {"nombre": "Bombones", "descripcion": "Pequeños dulces de chocolate y relleno", "estado": "activo"},
            {"nombre": "Gomitas", "descripcion": "Golosinas masticables de sabores", "estado": "inactivo"},
            {"nombre": "Confites", "descripcion": "Variedad de grajeas y pastillas", "estado": "activo"},
        ]
        categorias_fixture = []
        for i, cat in enumerate(categorias_lista, start=1):
            categorias_fixture.append({
                "model": "dispositivos.categoria",
                "pk": i,
                "fields": cat
            })
        fixtures.extend(categorias_fixture)

        # 6. Bodegas (10 creativas)
        nombres_bodegas = [
            "Central Norte", "Alimentaria Sur", "Dulce Oriente", "ChocoStore", "Galletilandia",
            "Candy Box", "Depósito Frutal", "Fiesta Express", "Stock Express", "Bodega Fantasía"
        ]
        ubicaciones = [
            "Av. Independencia 1001", "Calle Dulzura 2020", "Ruta 5 Sur Km 15", "Costanera 2590",
            "Manuel Montt 765", "Granaderos 400", "Libertador 844", "Irarrázaval 2341", "Mall Center Piso 3", "Camino Real 127"
        ]
        bodegas_fixture = []
        for i in range(1, 11):
            bodega = {
                "model": "dispositivos.bodega",
                "pk": i,
                "fields": {
                    "nombre": nombres_bodegas[(i-1) % len(nombres_bodegas)],
                    "ubicacion": ubicaciones[(i-1) % len(ubicaciones)],
                    "capacidad": 5000 + (i * 222),
                    "estado": "activo" if i % 3 != 0 else "inactivo"
                }
            }
            bodegas_fixture.append(bodega)
        fixtures.extend(bodegas_fixture)


        # Listas para variedad creativa
        nombres_productos = [
            "Trufas de Avellana", "Alfajor Cordobés", "Turrón de Maní", "Chocolate Rubí 75g", "Cinta de Caramelo",
            "Barra de Cacao 80%", "Confites Turquesa", "Bombones del Bosque", "Frutilla Glaseada", "Mentitas Lemon",
            "Gomitas Frutales", "Galletas de Coco", "Almendrado Gourmet", "Chocoteja Limeña", "Bastón de Menta",
            "Jalea Real Berry", "Enrejado de Nuez", "Crocante de Maní", "Relleno de Avellana", "Napoleón Frambuesa",
            "Marmoleado de Damasco", "Glaseado de Limón", "Tarta Chocolate Negro", "Galletón Rock", "Flan de Cappuccino",
            "Mousse de Mango", "Brownie Express", "Tableta Festival", "Chocobolas Dulzón", "Azúcar Avainillado",
            "Bizcocho Sorpresa", "Tarta de Pistacho", "Alfajor Marplatense", "Bombón Cítrico", "Pomelo Drops",
            "Cereza Semiamarga", "Caramelo Naranja", "Trufa de Frutos Rojos", "Nocciola Tableta", "Brownie de Caramelo"
        ]
        categorias = ["Chocolates", "Caramelos", "Galletas", "Bombones", "Gomitas", "Confites"]
        paises = ["Chile", "Argentina", "México", "Colombia", "Uruguay", "Paraguay", "Perú", "Brasil"]

        # 2. 40 Productos
        productos = []
        for i in range(1, 41):
            nombre = nombres_productos[(i-1) % len(nombres_productos)]
            categoria = categorias[(i-1) % len(categorias)]
            prod = {
                "model": "dispositivos.producto",
                "pk": i,
                "fields": {
                    "sku": f"SKU-{categoria[:3].upper()}-{str(i).zfill(3)}",
                    "nombre": nombre,
                    "categoria": categoria,
                    "uom_compra": "kg" if i % 2 == 0 else "caja",
                    "uom_venta": "unidad" if i % 3 == 0 else "bolsa",
                    "factor_conversion": (i % 10) + 1,
                    "impuesto_iva": 19,
                    "stock_minimo": (i * 3) % 100 + 10,
                    "perishable": 1 if i % 2 == 0 else 0,
                    "lote": 800 + i,
                }
            }
            productos.append(prod)
        fixtures.extend(productos)

        # 3. 40 Proveedores creativos
        nombres_proveedores = [
            "Exportadora", "Comercial", "Distribuidora", "Central", "Mayorista", "Emporio", "Proveedoría", "Bebestible",
            "Fábrica", "Importadora"
        ]
        fantasia_extras = [
            "Dulsur", "CacaoMix", "Sweetland", "FrutiKing", "DeliNet", "Merken", "Chocolito", "CandyHouse", "Mansión Dulce", "SnacksLab"
        ]
        proveedores = []
        for i in range(1, 41):
            razon_social = f"{nombres_proveedores[i % len(nombres_proveedores)]} {fantasia_extras[i % len(fantasia_extras)]} S.A."
            fantasia = f"{fantasia_extras[i % len(fantasia_extras)]} {i}"
            proveedor = {
                "model": "dispositivos.proveedor",
                "pk": i,
                "fields": {
                    "rut_nif": f"76.{i:03d}.{(100+i):03d}-{i%10}",
                    "razon_social": razon_social,
                    "nombre_fantasia": fantasia,
                    "email": f"contacto{i}@{fantasia_extras[i%len(fantasia_extras)]}.cl",
                    "pais": paises[i % len(paises)],
                    "condiciones_pago": "30 días" if i % 2 == 0 else "15 días",
                    "moneda": "CLP",
                    "estado": "activo" if i % 3 != 0 else "inactivo",
                    "usuario": 4
                }
            }
            proveedores.append(proveedor)
        fixtures.extend(proveedores)

        # 4. 40 Relaciones producto-proveedor (1 a 1, puedes fácilmente hacer combinaciones diferentes)
        producto_proveedor = []
        base_fecha = datetime(2025, 1, 1, 10, 0, 0)
        for i in range(1, 41):
            mov = {
                "model": "dispositivos.productoproveedor",
                "pk": i,
                "fields": {
                    "tipo_movimiento": "entrada",
                    "cantidad": 80 + i * 7,
                    "fecha_movimiento": (base_fecha + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "producto": i,
                    "proveedor": ((i * 3) % 40) + 1  # Distribuye relaciones entre proveedores
                }
            }
            producto_proveedor.append(mov)
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
