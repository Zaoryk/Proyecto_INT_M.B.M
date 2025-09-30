# Sistema de Gestión Dulceria Lili's

![Django](https://img.shields.io/badge/Django-5.2.5-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)

Sistema de gestión integral desarrollado en Django para la administración completa de una dulcería. Control de inventario, ventas, producción, compras y gestión de proveedores.

# Caracteristicas Principales

| Módulo | Descripción |
|--------|-------------|
| **Inventario** | Control completo de stock y bodegas |
| **Ventas** | Administración de pedidos de venta |
| **Producción** | Órdenes de producción y recetas |
| **Compras** | Solicitudes de compra y órdenes a proveedores |
| **Proveedores** | Gestión de proveedores y condiciones |
| **Costos** | Seguimiento de costos por producto |
| **Usuarios** | Sistema de roles y permisos |

### Tecnologias Utilizadas
- **Backend**: Django 5.2.5
- **Base de Datos**: MySQL
- **Frontend**: Django Templates + Admin interface
- **Python**: 3.13+

### Prerequisitos
- Python 3.8+
- Django 4.2+
- MySQL Server (Como WampServer)
- Git

### Instalación
- Clonar el repositorio

```bash
git clone https://github.com/Zaoryk/Proyecto_INT_M.B.M.git
cd Proyecto_INT_M.B.M/dulceria
```

- Migrar y abrir servidor
```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Acceder a: http://127.0.0.1:8000/admin/

- Si es necesario crear datos de ejemplo:
#### ES OBLIGATORIO TENER EL SERVIDOR CORRIENDO ANTES DE EJECUTAR ESTOS COMANDOS.
```python
# Opcion 1: Cargar datos directamente
python manage.py cargar_datos_directo

# Opcion 2: Generar y cargar fixtures
python manage.py generar_fixtures
python manage.py cargar_fixtures
```

### Usuarios de Prueba Creados:

- **Administrador**: ```admin``` / ```admin123```
- **Vendedor**: ```vendedor1``` / ```vendedor123```
- **Comprador**: ```comprador1``` / ```comprador123```
