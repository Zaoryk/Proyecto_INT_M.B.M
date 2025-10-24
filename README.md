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

#### ES IMPORTANTE CORRER INIT_ROLES PARA ASIGNAR ROLES A LOS USUARIOS NUEVOS.
```python
python manage.py makemigrations
python manage.py migrate

# ES NECESARIO CREAR UN SUPERUSUARIO ANTES DE CORRER EL SERVIDOR

python manage.py createsuperuser

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
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 24, 2025 at 09:06 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mydb`
--
CREATE DATABASE IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `mydb`;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_module`
--

DROP TABLE IF EXISTS `accounts_module`;
CREATE TABLE IF NOT EXISTS `accounts_module` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `icon` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_role`
--

DROP TABLE IF EXISTS `accounts_role`;
CREATE TABLE IF NOT EXISTS `accounts_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_rolemodulepermission`
--

DROP TABLE IF EXISTS `accounts_rolemodulepermission`;
CREATE TABLE IF NOT EXISTS `accounts_rolemodulepermission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `can_view` tinyint(1) NOT NULL,
  `can_add` tinyint(1) NOT NULL,
  `can_change` tinyint(1) NOT NULL,
  `can_delete` tinyint(1) NOT NULL,
  `module_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_rolemodulepermission_role_id_module_id_6954e96f_uniq` (`role_id`,`module_id`),
  KEY `accounts_rolemodulepermission_module_id_9f97b920` (`module_id`),
  KEY `accounts_rolemodulepermission_role_id_41b3edbd` (`role_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add bodega', 7, 'add_bodega'),
(26, 'Can change bodega', 7, 'change_bodega'),
(27, 'Can delete bodega', 7, 'delete_bodega'),
(28, 'Can view bodega', 7, 'view_bodega'),
(29, 'Can add costo', 8, 'add_costo'),
(30, 'Can change costo', 8, 'change_costo'),
(31, 'Can delete costo', 8, 'delete_costo'),
(32, 'Can view costo', 8, 'view_costo'),
(33, 'Can add movimiento inventario', 9, 'add_movimientoinventario'),
(34, 'Can change movimiento inventario', 9, 'change_movimientoinventario'),
(35, 'Can delete movimiento inventario', 9, 'delete_movimientoinventario'),
(36, 'Can view movimiento inventario', 9, 'view_movimientoinventario'),
(37, 'Can add orden de compra', 10, 'add_ordendecompra'),
(38, 'Can change orden de compra', 10, 'change_ordendecompra'),
(39, 'Can delete orden de compra', 10, 'delete_ordendecompra'),
(40, 'Can view orden de compra', 10, 'view_ordendecompra'),
(41, 'Can add orden produccion', 11, 'add_ordenproduccion'),
(42, 'Can change orden produccion', 11, 'change_ordenproduccion'),
(43, 'Can delete orden produccion', 11, 'delete_ordenproduccion'),
(44, 'Can view orden produccion', 11, 'view_ordenproduccion'),
(45, 'Can add producto', 12, 'add_producto'),
(46, 'Can change producto', 12, 'change_producto'),
(47, 'Can delete producto', 12, 'delete_producto'),
(48, 'Can view producto', 12, 'view_producto'),
(49, 'Can add proveedor', 13, 'add_proveedor'),
(50, 'Can change proveedor', 13, 'change_proveedor'),
(51, 'Can delete proveedor', 13, 'delete_proveedor'),
(52, 'Can view proveedor', 13, 'view_proveedor'),
(53, 'Can add usuario', 14, 'add_usuario'),
(54, 'Can change usuario', 14, 'change_usuario'),
(55, 'Can delete usuario', 14, 'delete_usuario'),
(56, 'Can view usuario', 14, 'view_usuario'),
(57, 'Can add cliente', 15, 'add_cliente'),
(58, 'Can change cliente', 15, 'change_cliente'),
(59, 'Can delete cliente', 15, 'delete_cliente'),
(60, 'Can view cliente', 15, 'view_cliente'),
(61, 'Can add listar precios', 16, 'add_listarprecios'),
(62, 'Can change listar precios', 16, 'change_listarprecios'),
(63, 'Can delete listar precios', 16, 'delete_listarprecios'),
(64, 'Can view listar precios', 16, 'view_listarprecios'),
(65, 'Can add pedido', 17, 'add_pedido'),
(66, 'Can change pedido', 17, 'change_pedido'),
(67, 'Can delete pedido', 17, 'delete_pedido'),
(68, 'Can view pedido', 17, 'view_pedido'),
(69, 'Can add producto proveedor', 18, 'add_productoproveedor'),
(70, 'Can change producto proveedor', 18, 'change_productoproveedor'),
(71, 'Can delete producto proveedor', 18, 'delete_productoproveedor'),
(72, 'Can view producto proveedor', 18, 'view_productoproveedor'),
(73, 'Can add Módulo', 19, 'add_module'),
(74, 'Can change Módulo', 19, 'change_module'),
(75, 'Can delete Módulo', 19, 'delete_module'),
(76, 'Can view Módulo', 19, 'view_module'),
(77, 'Can add Rol', 20, 'add_role'),
(78, 'Can change Rol', 20, 'change_role'),
(79, 'Can delete Rol', 20, 'delete_role'),
(80, 'Can view Rol', 20, 'view_role'),
(81, 'Can add Permiso de Módulo', 21, 'add_rolemodulepermission'),
(82, 'Can change Permiso de Módulo', 21, 'change_rolemodulepermission'),
(83, 'Can delete Permiso de Módulo', 21, 'delete_rolemodulepermission'),
(84, 'Can view Permiso de Módulo', 21, 'view_rolemodulepermission');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$pQnGXSkXTIBiZXLaehV9rK$xdQP1z+nn7I2gLdpFAuiCkVoYLe9Qp7ygDzYJnVp4Bo=', '2025-10-24 18:38:55.557574', 1, 'admin', '', '', 'admin@admin.cl', 1, 1, '2025-10-20 20:54:18.875773'),
(2, 'pbkdf2_sha256$1000000$WYbPZf2XY9LezCWXgCCA4d$/haF+UtrRJdEDohCghZqTsi7BHdCzGNAO/v5av0vMF8=', NULL, 1, 'sf-003x', '', '', '', 1, 1, '2025-10-24 18:38:37.033907');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'dispositivos', 'bodega'),
(8, 'dispositivos', 'costo'),
(9, 'dispositivos', 'movimientoinventario'),
(10, 'dispositivos', 'ordendecompra'),
(11, 'dispositivos', 'ordenproduccion'),
(12, 'dispositivos', 'producto'),
(13, 'dispositivos', 'proveedor'),
(14, 'dispositivos', 'usuario'),
(15, 'dispositivos', 'cliente'),
(16, 'dispositivos', 'listarprecios'),
(17, 'dispositivos', 'pedido'),
(18, 'dispositivos', 'productoproveedor'),
(19, 'accounts', 'module'),
(20, 'accounts', 'role'),
(21, 'accounts', 'rolemodulepermission');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-10-20 20:53:52.466057'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-10-20 20:53:52.499495'),
(3, 'auth', '0001_initial', '2025-10-20 20:53:52.793223'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-10-20 20:53:52.812705'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-10-20 20:53:52.833202'),
(6, 'auth', '0004_alter_user_username_opts', '2025-10-20 20:53:52.837943'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-10-20 20:53:52.855696'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-10-20 20:53:52.856618'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-10-20 20:53:52.862866'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-10-20 20:53:52.882831'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-10-20 20:53:52.899953'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-10-20 20:53:52.920190'),
(13, 'auth', '0011_update_proxy_permissions', '2025-10-20 20:53:52.925539'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-10-20 20:53:52.943101'),
(15, 'accounts', '0001_initial', '2025-10-20 20:53:53.056120'),
(16, 'admin', '0001_initial', '2025-10-20 20:53:53.165136'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-10-20 20:53:53.171018'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-10-20 20:53:53.175638'),
(19, 'dispositivos', '0001_initial', '2025-10-20 20:53:53.182467'),
(20, 'dispositivos', '0002_cliente_listarprecios_pedido_delete_pedidodeventa_and_more', '2025-10-20 20:53:53.190866'),
(21, 'dispositivos', '0003_productoproveedor_alter_producto_table_and_more', '2025-10-20 20:53:53.198125'),
(22, 'sessions', '0001_initial', '2025-10-20 20:53:53.217146');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('7x9qcp4fj8xfux6zjonnwwyl4ln8g2m3', '.eJxVjEEOgjAQRe_StWk62HYKS_eegUw7HakaSCi4Md5dSFjo9r_331v1tC5Dv9Y894VVp0CdfrdI6ZHHHfCdxtuk0zQuc4l6V_RBq75OnJ-Xw_0LDFSH7W1CDoDWnE3DyRnjOCG1IbggnpqIgiAg4gBRGMw5UY4QpfU2ehZvt-ir1LJQVR3azxe8Tzvv:1vCOz1:V7quUJyciDvA_Gkl1USlxVjku7pHkUbV_5aj-_edK00', '2025-10-24 23:05:59.047127');

-- --------------------------------------------------------

--
-- Table structure for table `movimientoinventario`
--

DROP TABLE IF EXISTS `movimientoinventario`;
CREATE TABLE IF NOT EXISTS `movimientoinventario` (
  `idMovimientoInventario` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `cantidad` int UNSIGNED NOT NULL,
  `Bodega_idBodega` int DEFAULT NULL,
  `Producto_idProducto` int NOT NULL,
  PRIMARY KEY (`idMovimientoInventario`),
  UNIQUE KEY `idMovimientoInventario` (`idMovimientoInventario`,`Bodega_idBodega`,`Producto_idProducto`),
  KEY `Bodega_idBodega` (`Bodega_idBodega`),
  KEY `Producto_idProducto` (`Producto_idProducto`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
CREATE TABLE IF NOT EXISTS `producto` (
  `idProducto` int NOT NULL AUTO_INCREMENT,
  `sku` varchar(50) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `uom_compra` varchar(45) DEFAULT NULL,
  `uom_venta` varchar(45) DEFAULT NULL,
  `factor_conversion` int DEFAULT NULL,
  `impuesto_iva` int DEFAULT NULL,
  `stock_minimo` int DEFAULT NULL,
  `perishable` int DEFAULT NULL,
  `lote` int DEFAULT NULL,
  PRIMARY KEY (`idProducto`),
  UNIQUE KEY `sku` (`sku`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `producto_proveedor`
--

DROP TABLE IF EXISTS `producto_proveedor`;
CREATE TABLE IF NOT EXISTS `producto_proveedor` (
  `idProducto_Proveedor` int NOT NULL AUTO_INCREMENT,
  `tipo_movimiento` varchar(100) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `fecha_movimiento` datetime DEFAULT NULL,
  `Producto_idProducto` int NOT NULL,
  `Proveedor_idProveedor` int NOT NULL,
  PRIMARY KEY (`idProducto_Proveedor`),
  KEY `fk_Producto_Proveedor_Producto1_idx` (`Producto_idProducto`),
  KEY `fk_Producto_Proveedor_Proveedor1_idx` (`Proveedor_idProveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
CREATE TABLE IF NOT EXISTS `proveedor` (
  `idProveedor` int NOT NULL AUTO_INCREMENT,
  `rut_nif` varchar(20) DEFAULT NULL,
  `razon_social` varchar(255) DEFAULT NULL,
  `nombre_fantasia` varchar(255) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `pais` varchar(45) DEFAULT NULL,
  `condiciones_pago` varchar(45) DEFAULT NULL,
  `moneda` varchar(45) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `Usuario_idUsuario` int NOT NULL,
  PRIMARY KEY (`idProveedor`),
  KEY `fk_Proveedor_Usuario1_idx` (`Usuario_idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `rol` varchar(50) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `mfa_habilitado` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `username`, `email`, `nombre`, `apellido`, `rol`, `estado`, `mfa_habilitado`, `password`) VALUES
(5, 'jesus', 'luciano@gmail.com', 'luciano', 'perez', 'operador_ventas', 'activo', 'habilitado', NULL),
(6, 'jesuswewewwe', 'luciano@gmail.com', 'luciano', 'perez', 'operador_ventas', 'activo', 'habilitado', NULL),
(8, 'awjidawij', 'weoijf@gmail.com', 'werw', 'erwer', 'operador_compras', 'activo', 'habilitado', NULL);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `producto_proveedor`
--
ALTER TABLE `producto_proveedor`
  ADD CONSTRAINT `fk_Producto_Proveedor_Producto1` FOREIGN KEY (`Producto_idProducto`) REFERENCES `producto` (`idProducto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Producto_Proveedor_Proveedor1` FOREIGN KEY (`Proveedor_idProveedor`) REFERENCES `proveedor` (`idProveedor`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `proveedor`
--
ALTER TABLE `proveedor`
  ADD CONSTRAINT `fk_Proveedor_Usuario1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

```
