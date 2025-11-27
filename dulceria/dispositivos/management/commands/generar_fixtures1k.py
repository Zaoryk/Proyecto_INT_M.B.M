import json
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Genera fixtures para la dulcería Lilis: N productos, N proveedores, N movimientos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--size',
            type=int,
            default=5000,
            help='Cantidad por tipo: productos, proveedores y movimientos (ej: 5000, 10000)',
        )

    def handle(self, *args, **options):
        size = options['size']
        fixtures = []

        # ---- 1. Usuarios base (4) ----
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

        # ---- 2. Categorías fijas ----
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

        # ---- 3. Bodegas fijas (puedes subir a size si quieres) ----
        nombres_bodegas = [
            "Central Norte", "Alimentaria Sur", "Dulce Oriente", "ChocoStore", "Galletilandia",
            "Candy Box", "Depósito Frutal", "Fiesta Express", "Stock Express", "Bodega Fantasía"
        ]
        ubicaciones = [
            "Av. Independencia 1001", "Calle Dulzura 2020", "Ruta 5 Sur Km 15", "Costanera 2590",
            "Manuel Montt 765", "Granaderos 400", "Libertador 844", "Irarrázaval 2341",
            "Mall Center Piso 3", "Camino Real 127"
        ]
        bodegas_fixture = []
        n_bodegas = 100  # fijo, pero puedes usar size si quieres 1:1
        for i in range(1, n_bodegas + 1):
            bodega = {
                "model": "dispositivos.bodega",
                "pk": i,
                "fields": {
                    "nombre": f"{nombres_bodegas[(i-1) % len(nombres_bodegas)]} #{i}",
                    "ubicacion": ubicaciones[(i-1) % len(ubicaciones)],
                    "capacidad": 5000 + (i * 222),
                    "estado": "activo" if i % 3 != 0 else "inactivo"
                }
            }
            bodegas_fixture.append(bodega)
        fixtures.extend(bodegas_fixture)

        # ---- 4. Listas comunes para variedad ----
        nombres_productos = [
            "Trufas de Avellana", "Alfajor Cordobés", "Turrón de Maní", "Chocolate Rubí 75g",
            "Cinta de Caramelo", "Barra de Cacao 80%", "Confites Turquesa", "Bombones del Bosque",
            "Frutilla Glaseada", "Mentitas Lemon", "Gomitas Frutales", "Galletas de Coco",
            "Almendrado Gourmet", "Chocoteja Limeña", "Bastón de Menta", "Jalea Real Berry",
            "Enrejado de Nuez", "Crocante de Maní", "Relleno de Avellana", "Napoleón Frambuesa",
            "Marmoleado de Damasco", "Glaseado de Limón", "Tarta Chocolate Negro", "Galletón Rock",
            "Flan de Cappuccino", "Mousse de Mango", "Brownie Express", "Tableta Festival",
            "Chocobolas Dulzón", "Azúcar Avainillado", "Bizcocho Sorpresa", "Tarta de Pistacho",
            "Alfajor Marplatense", "Bombón Cítrico", "Pomelo Drops", "Cereza Semiamarga",
            "Caramelo Naranja", "Trufa de Frutos Rojos", "Nocciola Tableta", "Brownie de Caramelo"
        ]
        categorias = ["Chocolates", "Caramelos", "Galletas", "Bombones", "Gomitas", "Confites"]
        paises = ["Chile", "Argentina", "México", "Colombia", "Uruguay", "Paraguay", "Perú", "Brasil"]

        descripciones = [
            "Dulce clásico y suave con notas de caramelo natural.",
            "Receta artesanal inspirada en tradiciones latinoamericanas.",
            "Cubierta de chocolate premium y relleno cremoso.",
            "Ideal para acompañar el café de la tarde.",
            "Boquiabierto de sabor frutal intenso y textura masticable.",
            "Sabor a frutas rojas y glaseado suave.",
            "Mezcla equilibrada de cacao, frutos secos y especias.",
            "Formato pequeño, ideal para compartir o regalar.",
            "Relleno aireado con aroma de vainilla auténtica.",
            "Apto para público infantil con colores vibrantes.",
            "Edición limitada, producción artesanal en lotes pequeños.",
            "Garantizado sin alérgenos comunes y bajo en sodio.",
            "Envasado unitario para máxima frescura.",
            "Sello de calidad de la Dulcería Lilis.",
            "Recubrimiento crujiente y centro blando.",
            "Relleno de pasta de maní natural, sin azúcar añadido.",
            "Decorado a mano, cada pieza es única.",
            "Perfecto para fiestas y celebraciones temáticas.",
            "Inspirado en recetas europeas centenarias.",
            "Presentación deluxe en caja de regalo.",
            "Libre de colorantes artificiales y conservantes.",
            "Fusión de sabores cítricos y tropicales.",
            "Textura crocante, con notas acarameladas.",
            "Recomendado para dietas vegetarianas.",
            "Formato mini ideal para lunchbox.",
            "Fragancia a naranja y canela recién horneada.",
            "Delicioso con trocitos de almendra.",
            "Versión familiar, rendimiento mejorado.",
            "Con cobertura de chocolate blanco y relleno de frutas.",
            "Sello vegano, ingredientes 100% vegetales.",
            "Edición aniversario de Dulcería Lilis.",
            "Aportando energía con ingredientes naturales.",
            "Enriquecido con calcio y vitaminas.",
            "Receta exclusiva para la línea premium.",
            "Libre de gluten y lactosa.",
            "Inspirado en dulces franceses clásicos.",
            "Recubierto de glaseado espeso artesanal.",
            "Mejor opción en relación calidad/precio.",
            "Sabor tradicional con giro innovador.",
            "Delicia irresistible para toda la familia.",
            "Fórmula especial para quienes buscan alternativas saludables.",
            "Bajo en azúcar, apto para diabéticos.",
            "Con semillas crocantes para extra textura.",
            "Base de almendras tostadas.",
            "Capa doble de chocolate intenso.",
            "Toques cítricos de naranja y limón.",
            "Sabor a miel natural y frutos secos.",
            "Tierno y suave, ideal para niños y adultos.",
            "Sin conservantes, consumo responsable garantizado.",
            "Embalaje eco-friendly y biodegradable.",
            "Notas a canela y frutas deshidratadas.",
            "Receta transmitida por generaciones.",
            "Light, con menos calorías.",
            "Sabor a frutos del bosque.",
            "Ideal para celebraciones y eventos.",
            "Bañado en chocolate negro premium.",
            "Aroma a vainilla bourbon.",
            "Decoraciones coloridas de azúcar glasé.",
            "Galleta crujiente, relleno cremoso.",
            "Corazón líquido de caramelo.",
            "Mini porciones para picoteo.",
            "Textura aireada y esponjosa.",
            "Intenso sabor a cacao.",
            "Impregnado con licor suave (sin alcohol).",
            "Receta exclusiva, solo venta en Lilis.",
            "Tapa de chocolate ruby.",
            "Fusión novedosa de ingredientes autóctonos.",
            "Snack ideal para media mañana.",
            "Arrullo de caramelo con centro de fruta.",
            "Chispeante para explotar en tu boca.",
            "Apto para veganos y celíacos.",
            "Sabor suave a coco natural.",
            "Croquetas dulces elaboradas a mano.",
            "Receta ganadora de premios regionales.",
            "Relleno de dulce de leche tradicional.",
            "Sorpresa de frutos secos picados.",
            "Miniaturas surtidas con sabores variados.",
            "Barra energética y nutritiva.",
            "Cubierta de menta para frescura extra.",
            "Gomitas rellenas con jugo real de fruta.",
            "Dulce edición primavera.",
            "Esencia cítrica con final acidito.",
            "Dulce texturizado con semillas de chía.",
            "Recubrimiento doble: chocolate y glaseado.",
            "Variedad gourmet, edición limitada.",
            "Inspirado en golosinas clásicas europeas.",
            "Perfecto para combos y packs familiares.",
            "Regalo ideal para sorprender.",
            "Mini-tarta de frutas confitadas.",
            "Múltiples capas de sabores dulces.",
            "Homenaje a recetas históricas chilenas.",
            "Incluído en la caja degustación temporada.",
            "Snack sin sellos, apto para escolar.",
            "Receta secreta de la abuela de Lili’s.",
            "Edición especial Día del Niño.",
            "Mix tropical para verano.",
            "Sin azúcar añadida y bajo en grasa.",
            "Decorado con trozos de fruta confitada.",
            "Sello nacional de calidad.",
            "Golosina vibrante, presentación arcoíris.",
            "Fusión de chocolate y frutos rojos.",
            "Galleta integral con chips de chocolate negro.",
            "Bombón de edición limitada aniversario 2025."
        ]

        # ---- 5. Productos: size ----
        productos = []
        for i in range(1, size + 1):
            nombre = nombres_productos[(i-1) % len(nombres_productos)]
            categoria = categorias[(i-1) % len(categorias)]
            prod = {
                "model": "dispositivos.producto",
                "pk": i,
                "fields": {
                    "sku": f"SKU-{categoria[:3].upper()}-{str(i).zfill(5)}",
                    "nombre": nombre,
                    "categoria": categoria,
                    "uom_compra": "kg" if i % 2 == 0 else "caja",
                    "uom_venta": "unidad" if i % 3 == 0 else "bolsa",
                    "factor_conversion": (i % 10) + 1,
                    "impuesto_iva": 19,
                    "stock_minimo": (i * 3) % 100 + 10,
                    "perishable": 1 if i % 2 == 0 else 0,
                    "lote": 800 + i,
                    "descripcion": descripciones[(i-1) % len(descripciones)]
                }
            }
            productos.append(prod)
        fixtures.extend(productos)

        # ---- 6. Proveedores: size ----
        nombres_proveedores = [
            "Exportadora", "Comercial", "Distribuidora", "Central", "Mayorista",
            "Emporio", "Proveedoría", "Bebestible", "Fábrica", "Importadora"
        ]
        fantasia_extras = [
            "Dulsur", "CacaoMix", "Sweetland", "FrutiKing", "DeliNet",
            "Merken", "Chocolito", "CandyHouse", "Mansión Dulce", "SnacksLab"
        ]
        proveedores = []
        for i in range(1, size + 1):
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

        # ---- 7. Movimientos: size ----
        producto_proveedor = []
        base_fecha = datetime(2025, 1, 1, 10, 0, 0)
        for pk_mov in range(1, size + 1):
            # producto y proveedor rotando dentro del rango size
            prod_id = ((pk_mov - 1) % size) + 1
            prov_id = ((pk_mov * 7) % size) + 1  # salto 7 para mezclar
            tipo = "entrada" if pk_mov % 3 != 0 else "salida"
            mov = {
                "model": "dispositivos.productoproveedor",
                "pk": pk_mov,
                "fields": {
                    "tipo_movimiento": tipo,
                    "cantidad": 50 + (pk_mov % 50),
                    "fecha_movimiento": (base_fecha + timedelta(minutes=pk_mov)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "producto": prod_id,
                    "proveedor": prov_id
                }
            }
            producto_proveedor.append(mov)
        fixtures.extend(producto_proveedor)

        # ---- Guardar ----
        filename = f'fixtures_dulceria_{size}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, indent=2, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(
            f'Fixtures generados: {len(fixtures)} registros en {filename}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Usuarios: {len(usuarios)}, Categorías: {len(categorias_fixture)}, '
            f'Bodegas: {len(bodegas_fixture)}, Productos: {len(productos)}, '
            f'Proveedores: {len(proveedores)}, Movimientos: {len(producto_proveedor)}'
        ))
