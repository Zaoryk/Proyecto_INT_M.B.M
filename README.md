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
## ES NECESARIO CREAR UN SUPERUSUARIO ANTES DE CORRER EL SERVIDOR
- Crear super usuario

```python
python manage.py createsuperuser
```

- Migrar y abrir servidor

#### ES IMPORTANTE CORRER INIT_ROLES PARA ASIGNAR ROLES A LOS USUARIOS NUEVOS.
```python
python manage.py makemigrations
python manage.py migrate

# Inicializar y crear los roles con sus usuarios
python manage.py init_roles

# Correr el servidor
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

### BASE DE DATOS PARA COPIAR A WAMPSERVER

```bash
-- LIMPIAR Y RECREAR esquema completo (RECOMENDADO si no necesitas conservar datos)
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS; SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=0; SET FOREIGN_KEY_CHECKS=0;

DROP DATABASE IF EXISTS `mydb`;
CREATE DATABASE `mydb` DEFAULT CHARACTER SET utf8;
USE `mydb`;

-- Cliente
CREATE TABLE `Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100),
  `tipo` VARCHAR(50),
  PRIMARY KEY (`idCliente`)
) ENGINE=InnoDB;

-- ListarPrecios (referencia a Cliente)
CREATE TABLE `ListarPrecios` (
  `idListarPrecios` INT NOT NULL AUTO_INCREMENT,
  `Canal` VARCHAR(50),
  `Temporada` VARCHAR(45),
  `Valor` INT,
  `Cliente_idCliente` INT NOT NULL,
  PRIMARY KEY (`idListarPrecios`),
  INDEX `idx_ListarPrecios_Cliente` (`Cliente_idCliente`),
  CONSTRAINT `fk_ListarPrecios_Cliente` FOREIGN KEY (`Cliente_idCliente`) REFERENCES `Cliente`(`idCliente`)
) ENGINE=InnoDB;

-- Usuario (id como PK Ãºnica)
CREATE TABLE `Usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100),
  `rol` VARCHAR(50),
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(120),
  `ListarPrecios_idListarPrecios` INT,
  PRIMARY KEY (`id`),
  INDEX `idx_Usuario_ListarPrecios` (`ListarPrecios_idListarPrecios`),
  CONSTRAINT `fk_Usuario_ListarPrecios` FOREIGN KEY (`ListarPrecios_idListarPrecios`) REFERENCES `ListarPrecios`(`idListarPrecios`)
) ENGINE=InnoDB;

-- Producto
CREATE TABLE `Producto` (
  `idProducto` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(120),
  `lote` VARCHAR(50),
  `fecha_vencimiento` DATE,
  `precio` INT,
  `stock` INT,
  PRIMARY KEY (`idProducto`),
  UNIQUE KEY `lote_UNIQUE` (`lote`)
) ENGINE=InnoDB;

-- OrdenProduccion (referencias a Usuario.id y Producto.idProducto)
CREATE TABLE `OrdenProduccion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fechaInicio` DATE,
  `fechaFin` DATE,
  `estado` VARCHAR(45),
  `Usuario_id` INT NOT NULL,
  `Producto_idProducto` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_OrdenUsuario` (`Usuario_id`),
  INDEX `idx_OrdenProducto` (`Producto_idProducto`),
  CONSTRAINT `fk_OrdenProduccion_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `Usuario`(`id`),
  CONSTRAINT `fk_OrdenProduccion_Producto` FOREIGN KEY (`Producto_idProducto`) REFERENCES `Producto`(`idProducto`)
) ENGINE=InnoDB;

-- Proveedor
CREATE TABLE `Proveedor` (
  `id_Proveedor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(130),
  `contacto` VARCHAR(200),
  `email` VARCHAR(120),
  PRIMARY KEY (`id_Proveedor`)
) ENGINE=InnoDB;

-- OrdendeCompra
CREATE TABLE `OrdendeCompra` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE,
  `estado` VARCHAR(45),
  `monto_total` INT,
  `proveedor_id_proveedor` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_ordendeCompra_proveedor` (`proveedor_id_proveedor`),
  CONSTRAINT `fk_ordendeCompra_proveedor` FOREIGN KEY (`proveedor_id_proveedor`) REFERENCES `Proveedor`(`id_Proveedor`)
) ENGINE=InnoDB;

-- Bodega
CREATE TABLE `Bodega` (
  `idBodega` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(120),
  `ubicacion` VARCHAR(100),
  PRIMARY KEY (`idBodega`)
) ENGINE=InnoDB;

-- MovimientoInventario
CREATE TABLE `MovimientoInventario` (
  `idMovimientoInventario` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45),
  `fecha` DATE,
  `cantidad` VARCHAR(45),
  `Bodega_idBodega` INT NOT NULL,
  `Producto_idProducto` INT NOT NULL,
  PRIMARY KEY (`idMovimientoInventario`),
  INDEX `idx_Mov_Bodega` (`Bodega_idBodega`),
  INDEX `idx_Mov_Producto` (`Producto_idProducto`),
  CONSTRAINT `fk_MovimientoInventario_Bodega` FOREIGN KEY (`Bodega_idBodega`) REFERENCES `Bodega`(`idBodega`),
  CONSTRAINT `fk_MovimientoInventario_Producto` FOREIGN KEY (`Producto_idProducto`) REFERENCES `Producto`(`idProducto`)
) ENGINE=InnoDB;

-- Costo
CREATE TABLE `Costo` (
  `idCosto` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45),
  `monto` INT,
  `Producto_idProducto` INT NOT NULL,
  PRIMARY KEY (`idCosto`),
  INDEX `idx_Costo_Producto` (`Producto_idProducto`),
  CONSTRAINT `fk_Costo_Producto` FOREIGN KEY (`Producto_idProducto`) REFERENCES `Producto`(`idProducto`)
) ENGINE=InnoDB;

-- Pedido
CREATE TABLE `Pedido` (
  `idPedido` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE,
  `monto_total` INT,
  `Usuario_id` INT NOT NULL,
  `Cliente_idCliente` INT NOT NULL,
  `OrdendeCompra_id` INT,
  PRIMARY KEY (`idPedido`),
  INDEX `idx_Pedido_Usuario` (`Usuario_id`),
  INDEX `idx_Pedido_Cliente` (`Cliente_idCliente`),
  INDEX `idx_Pedido_OrdendeCompra` (`OrdendeCompra_id`),
  CONSTRAINT `fk_Pedido_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `Usuario`(`id`),
  CONSTRAINT `fk_Pedido_Cliente` FOREIGN KEY (`Cliente_idCliente`) REFERENCES `Cliente`(`idCliente`),
  CONSTRAINT `fk_Pedido_OrdendeCompra` FOREIGN KEY (`OrdendeCompra_id`) REFERENCES `OrdendeCompra`(`id`)
) ENGINE=InnoDB;

-- RecetaDetalle (solo FK a Producto; si necesitas FK a Receta, crea tabla Receta antes)
CREATE TABLE `RecetaDetalle` (
  `Receta_idReceta` INT NOT NULL,
  `Producto_idProducto` INT NOT NULL,
  `Producto_Bodega_idBodega` INT NOT NULL,
  INDEX `idx_Receta_Producto` (`Producto_idProducto`, `Producto_Bodega_idBodega`),
  INDEX `idx_Receta` (`Receta_idReceta`),
  CONSTRAINT `fk_RecetaDetalle_Producto` FOREIGN KEY (`Producto_idProducto`) REFERENCES `Producto`(`idProducto`)
) ENGINE=InnoDB;

-- RESTAURAR flags
SET FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
```
