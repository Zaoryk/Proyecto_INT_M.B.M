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
-- Generation Time: Nov 10, 2025 at 07:02 PM
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
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_module`
--

INSERT INTO `accounts_module` (`id`, `code`, `name`, `icon`, `description`, `order`) VALUES
(1, 'usuarios', 'Usuarios', 'person', 'Módulo de Usuarios', 1),
(2, 'productos', 'Productos', 'inventory_2', 'Módulo de Productos', 2),
(3, 'proveedores', 'Proveedores', 'local_shipping', 'Módulo de Proveedores', 3),
(4, 'producto_proveedor', 'Inventario (Movimientos)', 'swap_horiz', 'Módulo de Inventario (Movimientos)', 4),
(5, 'bodegas', 'Bodegas', 'warehouse', 'Módulo de Bodegas', 5),
(6, 'clientes', 'Clientes', 'people', 'Módulo de Clientes', 6),
(7, 'costos', 'Costos', 'attach_money', 'Módulo de Costos', 7),
(8, 'listar_precios', 'Listar Precios', 'price_check', 'Módulo de Listar Precios', 8),
(9, 'movimiento_inventario', 'Movimiento Inventario', 'swap_horiz', 'Módulo de Movimiento Inventario', 9),
(10, 'orden_compra', 'Orden de Compra', 'shopping_cart', 'Módulo de Orden de Compra', 10),
(11, 'orden_produccion', 'Orden de Producción', 'build', 'Módulo de Orden de Producción', 11),
(12, 'pedidos', 'Pedidos', 'receipt', 'Módulo de Pedidos', 12),
(13, 'categorias', 'Categorías', 'grid', 'Módulo de Categorías', 5);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_passwordresetcode`
--

DROP TABLE IF EXISTS `accounts_passwordresetcode`;
CREATE TABLE IF NOT EXISTS `accounts_passwordresetcode` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_passwordresetcode`
--

INSERT INTO `accounts_passwordresetcode` (`id`, `email`, `code`, `created_at`, `expires_at`, `is_used`) VALUES
(1, 'mechangala@gmail.com', '901156', '2025-11-07 17:54:45.888147', '2025-11-07 18:09:45.886444', 1),
(2, 'mechangala@gmail.com', '367235', '2025-11-07 17:55:15.445767', '2025-11-07 18:10:15.445767', 0);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_role`
--

DROP TABLE IF EXISTS `accounts_role`;
CREATE TABLE IF NOT EXISTS `accounts_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_role`
--

INSERT INTO `accounts_role` (`id`, `description`, `group_id`) VALUES
(1, 'Administrador del sistema con acceso completo', 1),
(2, 'Operador de inventario - Solo gestiona inventario y movimientos', 2),
(3, 'Operador de compras - Solo gestiona proveedores', 3),
(4, 'Operador de ventas - Gestión limitada', 4),
(5, 'Operador de producción - Solo gestiona productos', 5),
(6, 'Analista financiero - Solo visualización de datos', 6);

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
) ENGINE=MyISAM AUTO_INCREMENT=172 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_rolemodulepermission`
--

INSERT INTO `accounts_rolemodulepermission` (`id`, `can_view`, `can_add`, `can_change`, `can_delete`, `module_id`, `role_id`) VALUES
(138, 1, 1, 1, 1, 10, 1),
(137, 1, 1, 1, 1, 9, 1),
(136, 1, 1, 1, 1, 8, 1),
(128, 1, 1, 1, 1, 1, 1),
(135, 1, 1, 1, 1, 7, 1),
(134, 1, 1, 1, 1, 6, 1),
(140, 1, 1, 1, 1, 12, 1),
(133, 1, 1, 1, 1, 13, 1),
(132, 1, 1, 1, 1, 5, 1),
(131, 1, 1, 1, 1, 4, 1),
(130, 1, 1, 1, 1, 3, 1),
(129, 1, 1, 1, 1, 2, 1),
(142, 1, 0, 0, 0, 2, 2),
(143, 1, 0, 0, 0, 3, 2),
(141, 1, 1, 1, 1, 4, 2),
(144, 1, 0, 0, 0, 13, 2),
(145, 1, 0, 0, 0, 5, 2),
(148, 1, 0, 0, 0, 2, 3),
(149, 1, 0, 0, 0, 4, 3),
(147, 1, 1, 1, 1, 3, 3),
(150, 1, 0, 0, 0, 13, 3),
(154, 1, 0, 0, 0, 6, 4),
(156, 1, 0, 0, 0, 8, 4),
(157, 1, 1, 1, 1, 13, 4),
(155, 1, 0, 0, 0, 12, 4),
(158, 1, 1, 1, 1, 5, 4),
(160, 1, 1, 1, 1, 2, 5),
(161, 1, 0, 0, 0, 4, 5),
(163, 1, 0, 0, 0, 13, 5),
(164, 1, 0, 0, 0, 5, 5),
(169, 1, 0, 0, 0, 13, 6),
(170, 1, 0, 0, 0, 5, 6),
(171, 1, 0, 1, 0, 1, 6),
(167, 1, 0, 0, 0, 3, 6),
(166, 1, 0, 0, 0, 2, 6),
(168, 1, 0, 0, 0, 4, 6),
(139, 1, 1, 1, 1, 11, 1),
(146, 1, 0, 1, 0, 1, 2),
(151, 1, 0, 0, 0, 5, 3),
(152, 1, 0, 1, 0, 1, 3),
(153, 1, 0, 0, 0, 2, 4),
(159, 1, 0, 1, 0, 1, 4),
(162, 1, 0, 0, 0, 3, 5),
(165, 1, 0, 1, 0, 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'administrador'),
(2, 'operador_inventario'),
(3, 'operador_compras'),
(4, 'operador_ventas'),
(5, 'operador_produccion'),
(6, 'analista_financiero');

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
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(84, 'Can view Permiso de Módulo', 21, 'view_rolemodulepermission'),
(85, 'Can add Código de Recuperación', 22, 'add_passwordresetcode'),
(86, 'Can change Código de Recuperación', 22, 'change_passwordresetcode'),
(87, 'Can delete Código de Recuperación', 22, 'delete_passwordresetcode'),
(88, 'Can view Código de Recuperación', 22, 'view_passwordresetcode'),
(89, 'Can add categoria', 23, 'add_categoria'),
(90, 'Can change categoria', 23, 'change_categoria'),
(91, 'Can delete categoria', 23, 'delete_categoria'),
(92, 'Can view categoria', 23, 'view_categoria');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$97E4VOahSDPGulgv4IYcQh$kZ6FrM/CIe8DGt34UtBTpIZHyLJ8QTcusxgCUZEaIRs=', '2025-10-27 20:11:53.144084', 1, 'admin', 'Admin', 'Principal', 'admin@dulcerialilis.cl', 1, 1, '2025-10-20 20:54:18.875773'),
(2, 'pbkdf2_sha256$1000000$WYbPZf2XY9LezCWXgCCA4d$/haF+UtrRJdEDohCghZqTsi7BHdCzGNAO/v5av0vMF8=', NULL, 1, 'sf-003x', '', '', '', 1, 1, '2025-10-24 18:38:37.033907'),
(3, 'pbkdf2_sha256$1000000$jtr7I51xZNn0iAhtn2smEn$NPEYxkePcc6STP9epC3ljxwAwN6sT9LMTtMpu/bcioA=', '2025-11-03 20:12:15.170916', 1, 'pedro', '', '', 'pedro@pedro.cl', 1, 1, '2025-11-03 20:09:54.233584'),
(4, 'pbkdf2_sha256$1000000$VFnsyRcqWsLGYiALQum3Xk$4xeoUZS3FBfJGpmtat8KvNwv8mBbkxCb3F57c+BKudc=', NULL, 0, 'jesuswewewwe', 'luciano', 'perez', 'luciano@gmail.com', 0, 1, '2025-11-03 20:11:16.776970'),
(5, 'pbkdf2_sha256$1000000$dYivFWSwamQQAkpoexajhe$IB6r1qY50RLcji8nL8Sx4/5Q/fxRE9RNSJw0BUZRYvQ=', NULL, 0, 'Malboro', 'lamel', 'ano', 'mawi@gmail.com', 0, 0, '2025-11-03 20:13:04.518222'),
(6, 'pbkdf2_sha256$1000000$625iVvTlZ1pqOzA2qjqjd5$3Y8bR8ayufXJqSg9WTRONQJULsRsiMmSlfbwdLF20MY=', NULL, 0, 'porque', 'hola', 'messi', 'holamessi@gmail.com', 0, 1, '2025-11-03 20:13:52.081163'),
(8, 'pbkdf2_sha256$1000000$JYiX73qNIb0Io1WCK67Cih$RuzY5OUE8vTwl9YGWCW1/xGifckMpp3vgs5xdl4B8Bs=', '2025-11-08 15:58:28.262744', 1, 'admintest', '', '', 'admintest@gmail.com', 1, 1, '2025-11-05 19:45:40.647337'),
(9, 'pbkdf2_sha256$1000000$UYkqUTQz88m14p1k9mgBrH$b4EK3tktZa5h3tcWuwe49IbiX6RwodQsMA3abzkLAy4=', NULL, 0, 'admin213123', 'admin', 'admin', 'admin@dulceri312321alilis.cl', 0, 1, '2025-11-05 19:49:48.063883'),
(10, 'pbkdf2_sha256$1000000$aLCY4EmAUWs2aMxsYQYPU4$8NLneO+sAmEVmAQfhjavLlsrZtAiYrIPpWKzD2T2fko=', NULL, 0, 'admin12312312312', 'Admin', 'Principal', 'adm123123in@1231221dulcerialilis.cl', 0, 1, '2025-11-05 20:10:33.762841'),
(11, 'pbkdf2_sha256$1000000$ICRsIaHuMVtFOnUdGLwxKF$ME089bDKkz2acqByC7rtjFKrGYUYWhxT0EVzw1SByUw=', NULL, 0, 'qwewqewq', 'qwew', 'qwewqe', 'eqweewqeqwe@gmail.com', 0, 1, '2025-11-07 16:06:49.984345'),
(15, 'pbkdf2_sha256$1000000$TKkJ2RNXDkzdVt5r4FcmXL$LJCrdFUsTh8aAnfpVvkli+nZmQqcIcAXJnw2ssTwvus=', '2025-11-08 16:02:53.369351', 0, 'Juan', 'Juan', 'Enrique', 'Juan.Enrique@gmail.com', 0, 1, '2025-11-07 16:25:49.518661'),
(16, 'pbkdf2_sha256$1000000$EDoI4M5Esdx76xxDuE7iAg$AetGKXag8jELGrCtVqYYsKXn7icRQNoCpJG54OYYHvg=', NULL, 0, 'Marcos', 'Marcos', 'Changala', 'mechangala@gmail.com', 0, 1, '2025-11-07 17:54:37.637299'),
(17, 'pbkdf2_sha256$1000000$yvZV1QWOXL8AKvQlHDDb4A$4BKfBE6MeXdNmjW3S0f7lMSnliXz52evt54NiemD3n4=', '2025-11-10 16:31:27.946278', 1, 'Administrador', 'Administrador', 'Juan', 'admin@admin.com', 1, 1, '2025-11-08 15:03:24.251757'),
(18, 'pbkdf2_sha256$600000$TEST$TEST', NULL, 0, 'inventario', 'Operador', 'Inventario', 'inventario@dulcerialilis.cl', 0, 1, '2025-11-08 16:02:36.961145'),
(19, 'pbkdf2_sha256$600000$TEST$TEST', NULL, 0, 'ventas', 'Operador', 'Ventas', 'ventas@dulcerialilis.cl', 0, 1, '2025-11-08 16:02:36.969506'),
(20, 'pbkdf2_sha256$600000$TEST$TEST', NULL, 0, 'compras', 'Operador', 'Compras', 'compras@dulcerialilis.cl', 0, 1, '2025-11-08 16:02:36.975569'),
(21, '', NULL, 0, 'awjidawij', 'werw', 'erwer', 'weoijf@gmail.com', 0, 1, '2025-11-08 16:02:37.586250'),
(22, 'pbkdf2_sha256$1000000$6CcSJ4Ez3IredUhmSXKx32$U25HiDQfA6DUZe0wx/Rcw1iSTp7G+2ZZQE1wtWHqobE=', '2025-11-10 13:11:37.228690', 1, 'marmota', 'Marmota', 'Aguilar', 'marmota@marmota.cl', 1, 1, '2025-11-08 21:26:13.153593'),
(23, 'pbkdf2_sha256$1000000$eE6RWzhwoVK0ZYP8YxX6Ez$51xQJmNyRh8BpMSvMV4ztedYzK4YMwjk+y2r4XR8cbc=', '2025-11-10 16:47:01.648584', 0, 'Funciona', 'Fun', 'ciona', 'Funciona@gmail.com', 0, 1, '2025-11-10 15:22:30.254582'),
(24, 'pbkdf2_sha256$1000000$m79iRCjp422dVSuYv6SYlS$vrlUMPFmJsDhL9O0J9QjsHKRDcSr8lwhp0bZD360Q+M=', NULL, 0, 'CreandoPrueba', 'me', 'si', 'CreandoPrueba@gmail.com', 0, 1, '2025-11-10 16:47:28.277934');

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
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(47, 1, 1),
(42, 18, 2),
(43, 19, 4),
(44, 20, 3),
(5, 4, 4),
(6, 21, 3),
(7, 5, 3),
(8, 6, 4),
(9, 9, 4),
(10, 10, 4),
(11, 11, 4),
(15, 15, 4),
(13, 16, 2),
(61, 17, 4),
(54, 22, 1),
(62, 23, 1),
(64, 24, 2);

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
-- Table structure for table `bodega`
--

DROP TABLE IF EXISTS `bodega`;
CREATE TABLE IF NOT EXISTS `bodega` (
  `idBodega` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ubicacion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `capacidad` int DEFAULT '0',
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'activo',
  PRIMARY KEY (`idBodega`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bodega`
--

INSERT INTO `bodega` (`idBodega`, `nombre`, `ubicacion`, `capacidad`, `estado`) VALUES
(1, 'Central Norte #1', 'Av. Independencia 1001', 5222, 'activo'),
(2, 'Alimentaria Sur #2', 'Calle Dulzura 2020', 5444, 'activo'),
(3, 'Dulce Oriente #3', 'Ruta 5 Sur Km 15', 5666, 'inactivo'),
(4, 'ChocoStore #4', 'Costanera 2590', 5888, 'activo'),
(5, 'Galletilandia #5', 'Manuel Montt 765', 6110, 'activo'),
(6, 'Candy Box #6', 'Granaderos 400', 6332, 'inactivo'),
(7, 'Depósito Frutal #7', 'Libertador 844', 6554, 'activo'),
(8, 'Fiesta Express #8', 'Irarrázaval 2341', 6776, 'activo'),
(9, 'Stock Express #9', 'Mall Center Piso 3', 6998, 'inactivo'),
(10, 'Bodega Fantasía #10', 'Camino Real 127', 7220, 'activo'),
(11, 'Central Norte #11', 'Av. Independencia 1001', 7442, 'activo'),
(12, 'Alimentaria Sur #12', 'Calle Dulzura 2020', 7664, 'inactivo'),
(13, 'Dulce Oriente #13', 'Ruta 5 Sur Km 15', 7886, 'activo'),
(14, 'ChocoStore #14', 'Costanera 2590', 8108, 'activo'),
(15, 'Galletilandia #15', 'Manuel Montt 765', 8330, 'inactivo'),
(16, 'Candy Box #16', 'Granaderos 400', 8552, 'activo'),
(17, 'Depósito Frutal #17', 'Libertador 844', 8774, 'activo'),
(18, 'Fiesta Express #18', 'Irarrázaval 2341', 8996, 'inactivo'),
(19, 'Stock Express #19', 'Mall Center Piso 3', 9218, 'activo'),
(20, 'Bodega Fantasía #20', 'Camino Real 127', 9440, 'activo'),
(21, 'Central Norte #21', 'Av. Independencia 1001', 9662, 'inactivo'),
(22, 'Alimentaria Sur #22', 'Calle Dulzura 2020', 9884, 'activo'),
(23, 'Dulce Oriente #23', 'Ruta 5 Sur Km 15', 10106, 'activo'),
(24, 'ChocoStore #24', 'Costanera 2590', 10328, 'inactivo'),
(25, 'Galletilandia #25', 'Manuel Montt 765', 10550, 'activo'),
(26, 'Candy Box #26', 'Granaderos 400', 10772, 'activo'),
(27, 'Depósito Frutal #27', 'Libertador 844', 10994, 'inactivo'),
(28, 'Fiesta Express #28', 'Irarrázaval 2341', 11216, 'activo'),
(29, 'Stock Express #29', 'Mall Center Piso 3', 11438, 'activo'),
(30, 'Bodega Fantasía #30', 'Camino Real 127', 11660, 'inactivo'),
(31, 'Central Norte #31', 'Av. Independencia 1001', 11882, 'activo'),
(32, 'Alimentaria Sur #32', 'Calle Dulzura 2020', 12104, 'activo'),
(33, 'Dulce Oriente #33', 'Ruta 5 Sur Km 15', 12326, 'inactivo'),
(34, 'ChocoStore #34', 'Costanera 2590', 12548, 'activo'),
(35, 'Galletilandia #35', 'Manuel Montt 765', 12770, 'activo'),
(36, 'Candy Box #36', 'Granaderos 400', 12992, 'inactivo'),
(37, 'Depósito Frutal #37', 'Libertador 844', 13214, 'activo'),
(38, 'Fiesta Express #38', 'Irarrázaval 2341', 13436, 'activo'),
(39, 'Stock Express #39', 'Mall Center Piso 3', 13658, 'inactivo'),
(40, 'Bodega Fantasía #40', 'Camino Real 127', 13880, 'activo'),
(41, 'Central Norte #41', 'Av. Independencia 1001', 14102, 'activo'),
(42, 'Alimentaria Sur #42', 'Calle Dulzura 2020', 14324, 'inactivo'),
(43, 'Dulce Oriente #43', 'Ruta 5 Sur Km 15', 14546, 'activo'),
(44, 'ChocoStore #44', 'Costanera 2590', 14768, 'activo'),
(45, 'Galletilandia #45', 'Manuel Montt 765', 14990, 'inactivo'),
(46, 'Candy Box #46', 'Granaderos 400', 15212, 'activo'),
(47, 'Depósito Frutal #47', 'Libertador 844', 15434, 'activo'),
(48, 'Fiesta Express #48', 'Irarrázaval 2341', 15656, 'inactivo'),
(49, 'Stock Express #49', 'Mall Center Piso 3', 15878, 'activo'),
(50, 'Bodega Fantasía #50', 'Camino Real 127', 16100, 'activo'),
(51, 'Central Norte #51', 'Av. Independencia 1001', 16322, 'inactivo'),
(52, 'Alimentaria Sur #52', 'Calle Dulzura 2020', 16544, 'activo'),
(53, 'Dulce Oriente #53', 'Ruta 5 Sur Km 15', 16766, 'activo'),
(54, 'ChocoStore #54', 'Costanera 2590', 16988, 'inactivo'),
(55, 'Galletilandia #55', 'Manuel Montt 765', 17210, 'activo'),
(56, 'Candy Box #56', 'Granaderos 400', 17432, 'activo'),
(57, 'Depósito Frutal #57', 'Libertador 844', 17654, 'inactivo'),
(58, 'Fiesta Express #58', 'Irarrázaval 2341', 17876, 'activo'),
(59, 'Stock Express #59', 'Mall Center Piso 3', 18098, 'activo'),
(60, 'Bodega Fantasía #60', 'Camino Real 127', 18320, 'inactivo'),
(61, 'Central Norte #61', 'Av. Independencia 1001', 18542, 'activo'),
(62, 'Alimentaria Sur #62', 'Calle Dulzura 2020', 18764, 'activo'),
(63, 'Dulce Oriente #63', 'Ruta 5 Sur Km 15', 18986, 'inactivo'),
(64, 'ChocoStore #64', 'Costanera 2590', 19208, 'activo'),
(65, 'Galletilandia #65', 'Manuel Montt 765', 19430, 'activo'),
(66, 'Candy Box #66', 'Granaderos 400', 19652, 'inactivo'),
(67, 'Depósito Frutal #67', 'Libertador 844', 19874, 'activo'),
(68, 'Fiesta Express #68', 'Irarrázaval 2341', 20096, 'activo'),
(69, 'Stock Express #69', 'Mall Center Piso 3', 20318, 'inactivo'),
(70, 'Bodega Fantasía #70', 'Camino Real 127', 20540, 'activo'),
(71, 'Central Norte #71', 'Av. Independencia 1001', 20762, 'activo'),
(72, 'Alimentaria Sur #72', 'Calle Dulzura 2020', 20984, 'inactivo'),
(73, 'Dulce Oriente #73', 'Ruta 5 Sur Km 15', 21206, 'activo'),
(74, 'ChocoStore #74', 'Costanera 2590', 21428, 'activo'),
(75, 'Galletilandia #75', 'Manuel Montt 765', 21650, 'inactivo'),
(76, 'Candy Box #76', 'Granaderos 400', 21872, 'activo'),
(77, 'Depósito Frutal #77', 'Libertador 844', 22094, 'activo'),
(78, 'Fiesta Express #78', 'Irarrázaval 2341', 22316, 'inactivo'),
(79, 'Stock Express #79', 'Mall Center Piso 3', 22538, 'activo'),
(80, 'Bodega Fantasía #80', 'Camino Real 127', 22760, 'activo'),
(81, 'Central Norte #81', 'Av. Independencia 1001', 22982, 'inactivo'),
(82, 'Alimentaria Sur #82', 'Calle Dulzura 2020', 23204, 'activo'),
(83, 'Dulce Oriente #83', 'Ruta 5 Sur Km 15', 23426, 'activo'),
(84, 'ChocoStore #84', 'Costanera 2590', 23648, 'inactivo'),
(85, 'Galletilandia #85', 'Manuel Montt 765', 23870, 'activo'),
(86, 'Candy Box #86', 'Granaderos 400', 24092, 'activo'),
(87, 'Depósito Frutal #87', 'Libertador 844', 24314, 'inactivo'),
(88, 'Fiesta Express #88', 'Irarrázaval 2341', 24536, 'activo'),
(89, 'Stock Express #89', 'Mall Center Piso 3', 24758, 'activo'),
(90, 'Bodega Fantasía #90', 'Camino Real 127', 24980, 'inactivo'),
(91, 'Central Norte #91', 'Av. Independencia 1001', 25202, 'activo'),
(92, 'Alimentaria Sur #92', 'Calle Dulzura 2020', 25424, 'activo'),
(93, 'Dulce Oriente #93', 'Ruta 5 Sur Km 15', 25646, 'inactivo'),
(94, 'ChocoStore #94', 'Costanera 2590', 25868, 'activo'),
(95, 'Galletilandia #95', 'Manuel Montt 765', 26090, 'activo'),
(96, 'Candy Box #96', 'Granaderos 400', 26312, 'inactivo'),
(97, 'Depósito Frutal #97', 'Libertador 844', 26534, 'activo'),
(98, 'Fiesta Express #98', 'Irarrázaval 2341', 26756, 'activo'),
(99, 'Stock Express #99', 'Mall Center Piso 3', 26978, 'inactivo'),
(100, 'Bodega Fantasía #100', 'Camino Real 127', 27200, 'activo'),
(101, 'Bodega Izquierda', 'jeklrjlkrjlkjlktejlk', 222, 'activo');

-- --------------------------------------------------------

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
CREATE TABLE IF NOT EXISTS `categoria` (
  `idCategoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'activo',
  PRIMARY KEY (`idCategoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categoria`
--

INSERT INTO `categoria` (`idCategoria`, `nombre`, `descripcion`, `estado`) VALUES
(1, 'Chocolates', 'Producto a base de cacao', 'activo'),
(2, 'Caramelos', 'Golosinas duras y blandas variadas', 'activo'),
(3, 'Galletas', 'Dulces secos, ideales para café o té', 'activo'),
(4, 'Bombones', 'Pequeños dulces de chocolate y relleno', 'activo'),
(5, 'Gomitas', 'Golosinas masticables de sabores', 'inactivo'),
(6, 'Confites', 'Variedad de grajeas y pastillas', 'activo'),
(7, '231456754321456', '123456u75432456', 'inactivo');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(21, 'accounts', 'rolemodulepermission'),
(22, 'accounts', 'passwordresetcode'),
(23, 'dispositivos', 'categoria');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(22, 'sessions', '0001_initial', '2025-10-20 20:53:53.217146'),
(23, 'accounts', '0002_passwordresetcode', '2025-11-03 20:07:49.218346'),
(24, 'dispositivos', '0004_categoria', '2025-11-09 02:08:21.475382'),
(25, 'dispositivos', '0005_alter_producto_table', '2025-11-10 07:02:31.687752');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('7x9qcp4fj8xfux6zjonnwwyl4ln8g2m3', '.eJxVjEEOgjAQRe_StWk6QDuFpXvOQKadjlQNJBTcGO8uJCx0-9_7760G2tZx2EpahsyqU6Auv1ug-EjTAfhO023WcZ7WJQd9KPqkRfczp-f1dP8CI5VxfxufPGBjalNxtMZYjkit99aLoyqgIAiIWEAUBlNHSgGCtK4JjsU1e_SVS16pqA7t5wu8UTvw:1vCP1q:8mleGr3XUFBCzH9lkopmxD2KiSHavcYiu4MJ0dIKXSo', '2025-10-24 23:08:54.424301'),
('mlyc97f6lldrlh7sgi20rfj4m7cr8fqu', '.eJxVjDsOgzAQBe_iOrK8gH-U6TkDWnu9sZMIJAxpotw9IFEk7Zt58xYjbmset5qWsZDoBYjL7xYwPtJ0ALrjdJtlnKd1KUEeijxplcNM6Xk93b9Axpr3t3LJge1UqxqKWilN0aJ3Tjs22ATLFhiYNVjLBKqNmAIE9qYLhth0e_RValmxir7xny-8Sjvv:1vCfUk:0g-739AwB8ezf-6tIo6iCwXrYxMtJRsuD58O91VoEug', '2025-10-25 16:43:50.201804'),
('4a1l507dkrya1iuk3ss2kgje5xyoww7c', '.eJxVjDsOgzAQBe_iOrK8Bn-gTM8Z0NrrjZ1EIGFIE-XuAYkiad_Mm7cYcVvzuNW0jIVEL0BcfreA8ZGmA9Adp9ss4zytSwnyUORJqxxmSs_r6f4FMta8v5VPHlyrGqUpGqUMRYed98azRR0cO2BgNuAcE6gmYgoQuLNtsMS23aOvUsuKVfTafL68Qjvr:1vD430:Q-GgZhd9vG3L0cVVKUrq987YuNps-jTl3LZ_PCGYtjA', '2025-10-26 18:56:50.274940'),
('sl9bt7chifkykyruk5jee3tp4rdm0e20', '.eJxVjDsOgzAQBe_iOrK8gD9QpucMaO31xk4ikLBJE-XuAYkiad_Mm7eYcKtp2kpcp0xiECAuv5vH8IjzAeiO822RYZnrmr08FHnSIseF4vN6un-BhCXtb-WiA9upVjUUtFKagsXeOe3YYOMtW2Bg1mAtE6g2YPTguTedN8Sm26OvXHLFIgaAzxe8Nzvm:1vDQYH:T8bW9Ntilp1vrLEKU6_wB64JVYku9bwlGjHk27Hjfac', '2025-10-27 18:58:37.595536'),
('ysn2lwfltfuwaqmroxxvixern0nrv5hc', '.eJxVjEEOgjAQRe_StWk6QDuFpXvOQKadjlQNJBTcGO8uJCx0-9_7760G2tZx2EpahsyqU6Auv1ug-EjTAfhO023WcZ7WJQd9KPqkRfczp-f1dP8CI5VxfxufPGBjalNxtMZYjkit99aLoyqgIAiIWEAUBlNHSgGCtK4JjsU1e_SVS16pqA6w-nwB-BY8Hg:1vDU3c:H35Hp2ULDWBMvTpJgXouftyUl_t8BwiETDALw0vP280', '2025-10-27 22:43:12.854867'),
('g2gj1ghe1rqnl6rkqna7nh3wlpplv4ul', '.eJxVjDEPgjAQRv9LZ0PaQsvJaMLs5EzujmtolJLQ4mL870LioOv3vvdeasCtTMOWZR3iqDpVq9PvRsh3SQdA5mVLJVcHlFQiY4lLqvoZ4-O63vZ3wlkuX-GvMmGe9oS3LUggodETkg8N6BoEoGkCgWFyTutzzS0by0wYhNG2qMVZI2Z0sEefMceCWXVevz-xCz9Z:1vG18B:Chtao1mZLF3Y9mvu78IlQi-bSRtR8Yxx5UzBhkedPPM', '2025-11-03 22:26:23.338674'),
('lvq8kax4cjipr9wznmwr68mvo1vx1769', '.eJxVjj0PwiAURf8Ls2le-ajQ0aSzk3PzeNBAtDQp4GL879LEQdd77j25LzZjLWGu2e9zdGxkmp1-M4t09-kASLTVVHJ3QJ9KJCxxS920Ynxc91trJ1z95Tv4swTMoSmcFBZIK9BuMYYWLrUEMpY7Lv1ARgwAaJU1g9LgQLWi4r3AdgLPVpgmfcYcC2Y2yv79AXPXPgs:1vGk3D:PAHBLqj6S-b9rvl6TAMM5lSwIdttFUSdiMPIGRkWmqg', '2025-11-05 22:24:15.249664'),
('oxswakynjj1177ta46ng4k33do5gwlbx', '.eJxVjj0PwiAURf8Ls2le-ajQ0aSzk3PzeNBAtDQp4GL879LEQdd77j25LzZjLWGu2e9zdGxkmp1-M4t09-kASLTVVHJ3QJ9KJCxxS920Ynxc91trJ1z95Tv4swTMoSmcFBZIK9BuMYYWLrUEMpY7Lv1ARgwAaJU1g9LgQLWi4r3AdgLPVpgmfcYcC2Y2iv79AXPUPgo:1vHLEs:XK9uxJ2zb_JYwR9-J1t-peJoHtEgA4EFJnuOQpvGVEI', '2025-11-07 14:06:46.919337'),
('0vhfqbud8tg6ljvkvkl74s04xhohlt0m', '.eJxVjDsLwjAYRf9LZin58qQdBWcn53LzokGbQpO6iP_dFhx0veee82IjtjaNW43rmAMbGGl2-h0d_D2Wg8D7ZSutdgeMpWWPlpfSXWbkx3W97e-COZ6_wl9lQp32hJUpeBGs6xMlGKdJSdKgKHtuSNheCaMB65IGF6QCHBJJw3nkkguzR5-55obKBvH-AGK0Pec:1vHQnh:VOqBR7ZIrmPBtl_ooYFey6Qq8FVnfp7OiAZOa9k1uRo', '2025-11-07 20:03:05.080799'),
('4hy7vjzu90u1a4gf5y7c33n73rcsojjz', '.eJxVjj0PwiAURf8Ls2mefAkdTZydnMnjQVOipUkBF-N_lyYOut5z78l9MYetzq6VuLkU2MgMO_xmHuke8w6QaG25lmGHMddEWNOah8uC6XHdbr2dcYnn7-DPMmOZuyJI4YGMAhMma2ni0kgg63ngMmqyQgOgV95qZSCA6kXFjwL7CTx5Ybv0mUqqWNjI3x82FD3Y:1vHaXh:v5-9wF0df7l-4lnImUf0tg4z_Xp7tlQBLOKAHjfJx2A', '2025-11-08 06:27:13.273632'),
('9d5daajcn3h24be919vd4xz1v0hfkojg', '.eJxVjj0PwiAURf8Ls2n4aHmlo4mzkzN5wCMlWpoUcDH-d9vEQdd77j25L2ax1dm2QptNgU1MADv9hg79nfJB0Pu15Vq6A1KuyWNNa-4uC6bHdbvt7YwLnb-DP8uMZd4VQBI49AF9GCIgIVc0jiF6pYQayWinzGAcl6R1jGCADxik4CB7scPj2jOVVLGwSbw_dS4-JA:1vHlPe:eNNbATUY8uipvnM1T3rAeySo6V77qWVY8I29OTewTQ0', '2025-11-08 18:03:38.415644'),
('2thqzd9qf3l3kt83n0oajbd995kvzq7u', '.eJxdj7FuAyEMht-FOYrgOMiRsVLmTp2RMU4ONYEKc5Waqu9ekDKkHf_vs3_Z38LD1la_MVWfojiKaRK7ZxgA3ykPA4hly433Q1JuCaGlkvenG6Tra33r0xlu9PJY-NOyAq-jPEiUzmBUGt18UHA-z9ZIBXGygaKGuFhNUsMC1jg9LyTRkYIQZbQHp3vpZ-LUgMXRmJ0oNVIdpzGKR_Lhq4MK95I9F0xw7eYDLp7TnboxPYYS6QLsn7AavD_0j_38AkV0Xt0:1vHy6H:fWsEgrMZx6tOm1PMQ-azjugumIFEcIrRQTPpCCIz6ks', '2025-11-09 07:36:29.989353'),
('5l3c57pweblbgz4e1wxp0l9bjziod2tv', '.eJxVjLEOgjAURf-lsyEtLYUymjg7OZPb10dolJLQ4mL8dyFx0PWee85LDNjKNGyZ1yEG0Yu6Fqff0YPunA4ComVLJVcH5FQiocQlVZcZ8XFdb_s7YebzV_irTMjTEfeSpGsoKE3OtArjaGwjFUJtPQeN0FnNUqODbZw2HUtyrOCDDLZ1eo8-Y44FWfTm_QFwZj6S:1vIB7l:dDtYCSRcZxHlnOhikbT99EZ7QKzwyQw9ectvmLSy-K8', '2025-11-09 21:30:53.043430'),
('m452b205ab0g817pq6gtws3ywo0kxtk5', '.eJxtkctuwyAQRf-FdRRh42eWlbruqms0wLhGjSHiYamp-u-FOopi0u09M0eX4ZtwiGHm0aPjWpETqWtyeAwFyE80mYCUNprgjxmiCVpC0NYcXxfQ5zf3nqYNLPhyW9hZZvBzlgsq6dhKVTE5Nn0F09R0La1A1Z1AxUANHUPKYICuHVkzIJUjViAUVV0_siRdtdcBPDnV_YFEH8Fp67l1Cl3u6CUpYy6-Eom3eo_4Ah_c6ysmXLUJaLOmd2V2Fyr8M5Zkc04oZ-CLXfWiE7b7wdJ-cXZFVNZh2feJbHoHV2u4t1LDuZj6x62iDE-XKPLNa-wiHO5o6UtfW5juSeHI-X775xcDfc8n:1vILg3:M6awEKJWHXD8nIKl8JZbsMVhN66IvCep80_6s2k5ZKs', '2025-11-10 08:46:59.972094'),
('u594wqti5nq057je7m9kvuox4qsks8nm', '.eJxdj8EOgjAQRP-lZ0IKBQocTTx78tws7SKNUky3NVHjv0sTDuh13s7k7ZspiGFSkdAra1jPCsmyfTiAvqJLBLReoguUJ4guWA3BLi4_zmBvJ39erx3MeNgKPysT0LROSCwll5UBbepRAgIX2LZm1EIUosWuGURXdwMvsWnGUXaS12DKgsuyKlaY1B6WbABifZWxSBG8XUgt3qBPiqTZf6yG50riZrfHd7gosi9MX9fs8wUUtFpA:1vILwD:XQBCaw4zNGBhYoD5A5L-q0iNM0u4MV8bSNocvYgZOjk', '2025-11-10 09:03:41.657438');

-- --------------------------------------------------------

--
-- Table structure for table `movimientoinventario`
--

DROP TABLE IF EXISTS `movimientoinventario`;
CREATE TABLE IF NOT EXISTS `movimientoinventario` (
  `idMovimientoInventario` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
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
  `ean_upc` varchar(50) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `descripcion` text,
  `categoria` varchar(100) DEFAULT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `uom_compra` varchar(45) DEFAULT NULL,
  `uom_venta` varchar(45) DEFAULT NULL,
  `factor_conversion` int DEFAULT NULL,
  `costo_estandar` decimal(18,6) DEFAULT NULL,
  `costo_promedio` decimal(18,6) DEFAULT NULL,
  `precio_venta` decimal(18,6) DEFAULT NULL,
  `impuesto_iva` int DEFAULT NULL,
  `stock_minimo` int DEFAULT NULL,
  `stock_maximo` int DEFAULT NULL,
  `punto_reorden` int DEFAULT NULL,
  `perishable` int DEFAULT NULL,
  `control_por_lote` tinyint(1) DEFAULT '0',
  `control_por_serie` tinyint(1) DEFAULT '0',
  `lote` int DEFAULT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `ficha_tecnica_url` varchar(255) DEFAULT NULL,
  `stock_actual` int DEFAULT '0',
  `alerta_bajo_stock` varchar(10) DEFAULT 'NO',
  `alerta_por_vencer` varchar(10) DEFAULT 'NO',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idProducto`),
  UNIQUE KEY `sku` (`sku`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `producto`
--

INSERT INTO `producto` (`idProducto`, `sku`, `ean_upc`, `nombre`, `descripcion`, `categoria`, `marca`, `modelo`, `uom_compra`, `uom_venta`, `factor_conversion`, `costo_estandar`, `costo_promedio`, `precio_venta`, `impuesto_iva`, `stock_minimo`, `stock_maximo`, `punto_reorden`, `perishable`, `control_por_lote`, `control_por_serie`, `lote`, `imagen_url`, `ficha_tecnica_url`, `stock_actual`, `alerta_bajo_stock`, `alerta_por_vencer`, `created_at`, `updated_at`) VALUES
(1, 'SKU-CHO-001', NULL, 'Trufas de Avellana', 'Dulce clásico y suave con notas de caramelo natural.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 2, NULL, NULL, NULL, 19, 13, NULL, NULL, 0, 0, 0, 801, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(2, 'SKU-CAR-002', NULL, 'Alfajor Cordobés', 'Receta artesanal inspirada en tradiciones latinoamericanas.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 3, NULL, NULL, NULL, 19, 16, NULL, NULL, 1, 0, 0, 802, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(3, 'SKU-GAL-003', NULL, 'Turrón de Maní', 'Cubierta de chocolate premium y relleno cremoso.', 'Galletas', NULL, NULL, 'caja', 'unidad', 4, NULL, NULL, NULL, 19, 19, NULL, NULL, 0, 0, 0, 803, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(4, 'SKU-BOM-004', NULL, 'Chocolate Rubí 75g', 'Ideal para acompañar el café de la tarde.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 5, NULL, NULL, NULL, 19, 22, NULL, NULL, 1, 0, 0, 804, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(5, 'SKU-GOM-005', NULL, 'Cinta de Caramelo', 'Boquiabierto de sabor frutal intenso y textura masticable.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 6, NULL, NULL, NULL, 19, 25, NULL, NULL, 0, 0, 0, 805, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(6, 'SKU-CON-006', NULL, 'Barra de Cacao 80%', 'Sabor a frutas rojas y glaseado suave.', 'Confites', NULL, NULL, 'kg', 'unidad', 7, NULL, NULL, NULL, 19, 28, NULL, NULL, 1, 0, 0, 806, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(7, 'SKU-CHO-007', NULL, 'Confites Turquesa', 'Mezcla equilibrada de cacao, frutos secos y especias.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 8, NULL, NULL, NULL, 19, 31, NULL, NULL, 0, 0, 0, 807, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(8, 'SKU-CAR-008', NULL, 'Bombones del Bosque', 'Formato pequeño, ideal para compartir o regalar.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 9, NULL, NULL, NULL, 19, 34, NULL, NULL, 1, 0, 0, 808, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(9, 'SKU-GAL-009', NULL, 'Frutilla Glaseada', 'Relleno aireado con aroma de vainilla auténtica.', 'Galletas', NULL, NULL, 'caja', 'unidad', 10, NULL, NULL, NULL, 19, 37, NULL, NULL, 0, 0, 0, 809, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(10, 'SKU-BOM-010', NULL, 'Mentitas Lemon', 'Apto para público infantil con colores vibrantes.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 1, NULL, NULL, NULL, 19, 40, NULL, NULL, 1, 0, 0, 810, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(11, 'SKU-GOM-011', NULL, 'Gomitas Frutales', 'Edición limitada, producción artesanal en lotes pequeños.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 2, NULL, NULL, NULL, 19, 43, NULL, NULL, 0, 0, 0, 811, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(12, 'SKU-CON-012', NULL, 'Galletas de Coco', 'Garantizado sin alérgenos comunes y bajo en sodio.', 'Confites', NULL, NULL, 'kg', 'unidad', 3, NULL, NULL, NULL, 19, 46, NULL, NULL, 1, 0, 0, 812, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(13, 'SKU-CHO-013', NULL, 'Almendrado Gourmet', 'Envasado unitario para máxima frescura.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 4, NULL, NULL, NULL, 19, 49, NULL, NULL, 0, 0, 0, 813, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(14, 'SKU-CAR-014', NULL, 'Chocoteja Limeña', 'Sello de calidad de la Dulcería Lilis.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 5, NULL, NULL, NULL, 19, 52, NULL, NULL, 1, 0, 0, 814, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(15, 'SKU-GAL-015', NULL, 'Bastón de Menta', 'Recubrimiento crujiente y centro blando.', 'Galletas', NULL, NULL, 'caja', 'unidad', 6, NULL, NULL, NULL, 19, 55, NULL, NULL, 0, 0, 0, 815, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(16, 'SKU-BOM-016', NULL, 'Jalea Real Berry', 'Relleno de pasta de maní natural, sin azúcar añadido.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 7, NULL, NULL, NULL, 19, 58, NULL, NULL, 1, 0, 0, 816, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(17, 'SKU-GOM-017', NULL, 'Enrejado de Nuez', 'Decorado a mano, cada pieza es única.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 8, NULL, NULL, NULL, 19, 61, NULL, NULL, 0, 0, 0, 817, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(18, 'SKU-CON-018', NULL, 'Crocante de Maní', 'Perfecto para fiestas y celebraciones temáticas.', 'Confites', NULL, NULL, 'kg', 'unidad', 9, NULL, NULL, NULL, 19, 64, NULL, NULL, 1, 0, 0, 818, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(19, 'SKU-CHO-019', NULL, 'Relleno de Avellana', 'Inspirado en recetas europeas centenarias.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 10, NULL, NULL, NULL, 19, 67, NULL, NULL, 0, 0, 0, 819, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(20, 'SKU-CAR-020', NULL, 'Napoleón Frambuesa', 'Presentación deluxe en caja de regalo.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 1, NULL, NULL, NULL, 19, 70, NULL, NULL, 1, 0, 0, 820, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(21, 'SKU-GAL-021', NULL, 'Marmoleado de Damasco', 'Libre de colorantes artificiales y conservantes.', 'Galletas', NULL, NULL, 'caja', 'unidad', 2, NULL, NULL, NULL, 19, 73, NULL, NULL, 0, 0, 0, 821, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(22, 'SKU-BOM-022', NULL, 'Glaseado de Limón', 'Fusión de sabores cítricos y tropicales.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 3, NULL, NULL, NULL, 19, 76, NULL, NULL, 1, 0, 0, 822, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(23, 'SKU-GOM-023', NULL, 'Tarta Chocolate Negro', 'Textura crocante, con notas acarameladas.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 4, NULL, NULL, NULL, 19, 79, NULL, NULL, 0, 0, 0, 823, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(24, 'SKU-CON-024', NULL, 'Galletón Rock', 'Recomendado para dietas vegetarianas.', 'Confites', NULL, NULL, 'kg', 'unidad', 5, NULL, NULL, NULL, 19, 82, NULL, NULL, 1, 0, 0, 824, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(25, 'SKU-CHO-025', NULL, 'Flan de Cappuccino', 'Formato mini ideal para lunchbox.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 6, NULL, NULL, NULL, 19, 85, NULL, NULL, 0, 0, 0, 825, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(26, 'SKU-CAR-026', NULL, 'Mousse de Mango', 'Fragancia a naranja y canela recién horneada.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 7, NULL, NULL, NULL, 19, 88, NULL, NULL, 1, 0, 0, 826, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(27, 'SKU-GAL-027', NULL, 'Brownie Express', 'Delicioso con trocitos de almendra.', 'Galletas', NULL, NULL, 'caja', 'unidad', 8, NULL, NULL, NULL, 19, 91, NULL, NULL, 0, 0, 0, 827, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(28, 'SKU-BOM-028', NULL, 'Tableta Festival', 'Versión familiar, rendimiento mejorado.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 9, NULL, NULL, NULL, 19, 94, NULL, NULL, 1, 0, 0, 828, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(29, 'SKU-GOM-029', NULL, 'Chocobolas Dulzón', 'Con cobertura de chocolate blanco y relleno de frutas.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 10, NULL, NULL, NULL, 19, 97, NULL, NULL, 0, 0, 0, 829, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(30, 'SKU-CON-030', NULL, 'Azúcar Avainillado', 'Sello vegano, ingredientes 100% vegetales.', 'Confites', NULL, NULL, 'kg', 'unidad', 1, NULL, NULL, NULL, 19, 100, NULL, NULL, 1, 0, 0, 830, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(31, 'SKU-CHO-031', NULL, 'Bizcocho Sorpresa', 'Edición aniversario de Dulcería Lilis.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 2, NULL, NULL, NULL, 19, 103, NULL, NULL, 0, 0, 0, 831, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(32, 'SKU-CAR-032', NULL, 'Tarta de Pistacho', 'Aportando energía con ingredientes naturales.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 3, NULL, NULL, NULL, 19, 106, NULL, NULL, 1, 0, 0, 832, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(33, 'SKU-GAL-033', NULL, 'Alfajor Marplatense', 'Enriquecido con calcio y vitaminas.', 'Galletas', NULL, NULL, 'caja', 'unidad', 4, NULL, NULL, NULL, 19, 109, NULL, NULL, 0, 0, 0, 833, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(34, 'SKU-BOM-034', NULL, 'Bombón Cítrico', 'Receta exclusiva para la línea premium.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 5, NULL, NULL, NULL, 19, 12, NULL, NULL, 1, 0, 0, 834, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(35, 'SKU-GOM-035', NULL, 'Pomelo Drops', 'Libre de gluten y lactosa.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 6, NULL, NULL, NULL, 19, 15, NULL, NULL, 0, 0, 0, 835, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(36, 'SKU-CON-036', NULL, 'Cereza Semiamarga', 'Inspirado en dulces franceses clásicos.', 'Confites', NULL, NULL, 'kg', 'unidad', 7, NULL, NULL, NULL, 19, 18, NULL, NULL, 1, 0, 0, 836, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(37, 'SKU-CHO-037', NULL, 'Caramelo Naranja', 'Recubierto de glaseado espeso artesanal.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 8, NULL, NULL, NULL, 19, 21, NULL, NULL, 0, 0, 0, 837, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(38, 'SKU-CAR-038', NULL, 'Trufa de Frutos Rojos', 'Mejor opción en relación calidad/precio.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 9, NULL, NULL, NULL, 19, 24, NULL, NULL, 1, 0, 0, 838, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(39, 'SKU-GAL-039', NULL, 'Nocciola Tableta', 'Sabor tradicional con giro innovador.', 'Galletas', NULL, NULL, 'caja', 'unidad', 10, NULL, NULL, NULL, 19, 27, NULL, NULL, 0, 0, 0, 839, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(40, 'SKU-BOM-040', NULL, 'Brownie de Caramelo', 'Delicia irresistible para toda la familia.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 1, NULL, NULL, NULL, 19, 30, NULL, NULL, 1, 0, 0, 840, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(41, 'SKU-GOM-041', NULL, 'Trufas de Avellana', 'Fórmula especial para quienes buscan alternativas saludables.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 2, NULL, NULL, NULL, 19, 33, NULL, NULL, 0, 0, 0, 841, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(42, 'SKU-CON-042', NULL, 'Alfajor Cordobés', 'Bajo en azúcar, apto para diabéticos.', 'Confites', NULL, NULL, 'kg', 'unidad', 3, NULL, NULL, NULL, 19, 36, NULL, NULL, 1, 0, 0, 842, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(43, 'SKU-CHO-043', NULL, 'Turrón de Maní', 'Con semillas crocantes para extra textura.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 4, NULL, NULL, NULL, 19, 39, NULL, NULL, 0, 0, 0, 843, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(44, 'SKU-CAR-044', NULL, 'Chocolate Rubí 75g', 'Base de almendras tostadas.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 5, NULL, NULL, NULL, 19, 42, NULL, NULL, 1, 0, 0, 844, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(45, 'SKU-GAL-045', NULL, 'Cinta de Caramelo', 'Capa doble de chocolate intenso.', 'Galletas', NULL, NULL, 'caja', 'unidad', 6, NULL, NULL, NULL, 19, 45, NULL, NULL, 0, 0, 0, 845, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(46, 'SKU-BOM-046', NULL, 'Barra de Cacao 80%', 'Toques cítricos de naranja y limón.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 7, NULL, NULL, NULL, 19, 48, NULL, NULL, 1, 0, 0, 846, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(47, 'SKU-GOM-047', NULL, 'Confites Turquesa', 'Sabor a miel natural y frutos secos.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 8, NULL, NULL, NULL, 19, 51, NULL, NULL, 0, 0, 0, 847, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(48, 'SKU-CON-048', NULL, 'Bombones del Bosque', 'Tierno y suave, ideal para niños y adultos.', 'Confites', NULL, NULL, 'kg', 'unidad', 9, NULL, NULL, NULL, 19, 54, NULL, NULL, 1, 0, 0, 848, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(49, 'SKU-CHO-049', NULL, 'Frutilla Glaseada', 'Sin conservantes, consumo responsable garantizado.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 10, NULL, NULL, NULL, 19, 57, NULL, NULL, 0, 0, 0, 849, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(50, 'SKU-CAR-050', NULL, 'Mentitas Lemon', 'Embalaje eco-friendly y biodegradable.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 1, NULL, NULL, NULL, 19, 60, NULL, NULL, 1, 0, 0, 850, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(51, 'SKU-GAL-051', NULL, 'Gomitas Frutales', 'Notas a canela y frutas deshidratadas.', 'Galletas', NULL, NULL, 'caja', 'unidad', 2, NULL, NULL, NULL, 19, 63, NULL, NULL, 0, 0, 0, 851, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(52, 'SKU-BOM-052', NULL, 'Galletas de Coco', 'Receta transmitida por generaciones.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 3, NULL, NULL, NULL, 19, 66, NULL, NULL, 1, 0, 0, 852, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(53, 'SKU-GOM-053', NULL, 'Almendrado Gourmet', 'Light, con menos calorías.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 4, NULL, NULL, NULL, 19, 69, NULL, NULL, 0, 0, 0, 853, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(54, 'SKU-CON-054', NULL, 'Chocoteja Limeña', 'Sabor a frutos del bosque.', 'Confites', NULL, NULL, 'kg', 'unidad', 5, NULL, NULL, NULL, 19, 72, NULL, NULL, 1, 0, 0, 854, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(55, 'SKU-CHO-055', NULL, 'Bastón de Menta', 'Ideal para celebraciones y eventos.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 6, NULL, NULL, NULL, 19, 75, NULL, NULL, 0, 0, 0, 855, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(56, 'SKU-CAR-056', NULL, 'Jalea Real Berry', 'Bañado en chocolate negro premium.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 7, NULL, NULL, NULL, 19, 78, NULL, NULL, 1, 0, 0, 856, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(57, 'SKU-GAL-057', NULL, 'Enrejado de Nuez', 'Aroma a vainilla bourbon.', 'Galletas', NULL, NULL, 'caja', 'unidad', 8, NULL, NULL, NULL, 19, 81, NULL, NULL, 0, 0, 0, 857, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(58, 'SKU-BOM-058', NULL, 'Crocante de Maní', 'Decoraciones coloridas de azúcar glasé.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 9, NULL, NULL, NULL, 19, 84, NULL, NULL, 1, 0, 0, 858, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(59, 'SKU-GOM-059', NULL, 'Relleno de Avellana', 'Galleta crujiente, relleno cremoso.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 10, NULL, NULL, NULL, 19, 87, NULL, NULL, 0, 0, 0, 859, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(60, 'SKU-CON-060', NULL, 'Napoleón Frambuesa', 'Corazón líquido de caramelo.', 'Confites', NULL, NULL, 'kg', 'unidad', 1, NULL, NULL, NULL, 19, 90, NULL, NULL, 1, 0, 0, 860, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(61, 'SKU-CHO-061', NULL, 'Marmoleado de Damasco', 'Mini porciones para picoteo.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 2, NULL, NULL, NULL, 19, 93, NULL, NULL, 0, 0, 0, 861, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(62, 'SKU-CAR-062', NULL, 'Glaseado de Limón', 'Textura aireada y esponjosa.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 3, NULL, NULL, NULL, 19, 96, NULL, NULL, 1, 0, 0, 862, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(63, 'SKU-GAL-063', NULL, 'Tarta Chocolate Negro', 'Intenso sabor a cacao.', 'Galletas', NULL, NULL, 'caja', 'unidad', 4, NULL, NULL, NULL, 19, 99, NULL, NULL, 0, 0, 0, 863, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(64, 'SKU-BOM-064', NULL, 'Galletón Rock', 'Impregnado con licor suave (sin alcohol).', 'Bombones', NULL, NULL, 'kg', 'bolsa', 5, NULL, NULL, NULL, 19, 102, NULL, NULL, 1, 0, 0, 864, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(65, 'SKU-GOM-065', NULL, 'Flan de Cappuccino', 'Receta exclusiva, solo venta en Lilis.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 6, NULL, NULL, NULL, 19, 105, NULL, NULL, 0, 0, 0, 865, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(66, 'SKU-CON-066', NULL, 'Mousse de Mango', 'Tapa de chocolate ruby.', 'Confites', NULL, NULL, 'kg', 'unidad', 7, NULL, NULL, NULL, 19, 108, NULL, NULL, 1, 0, 0, 866, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(67, 'SKU-CHO-067', NULL, 'Brownie Express', 'Fusión novedosa de ingredientes autóctonos.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 8, NULL, NULL, NULL, 19, 11, NULL, NULL, 0, 0, 0, 867, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(68, 'SKU-CAR-068', NULL, 'Tableta Festival', 'Snack ideal para media mañana.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 9, NULL, NULL, NULL, 19, 14, NULL, NULL, 1, 0, 0, 868, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(69, 'SKU-GAL-069', NULL, 'Chocobolas Dulzón', 'Arrullo de caramelo con centro de fruta.', 'Galletas', NULL, NULL, 'caja', 'unidad', 10, NULL, NULL, NULL, 19, 17, NULL, NULL, 0, 0, 0, 869, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(70, 'SKU-BOM-070', NULL, 'Azúcar Avainillado', 'Chispeante para explotar en tu boca.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 1, NULL, NULL, NULL, 19, 20, NULL, NULL, 1, 0, 0, 870, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(71, 'SKU-GOM-071', NULL, 'Bizcocho Sorpresa', 'Apto para veganos y celíacos.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 2, NULL, NULL, NULL, 19, 23, NULL, NULL, 0, 0, 0, 871, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(72, 'SKU-CON-072', NULL, 'Tarta de Pistacho', 'Sabor suave a coco natural.', 'Confites', NULL, NULL, 'kg', 'unidad', 3, NULL, NULL, NULL, 19, 26, NULL, NULL, 1, 0, 0, 872, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(73, 'SKU-CHO-073', NULL, 'Alfajor Marplatense', 'Croquetas dulces elaboradas a mano.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 4, NULL, NULL, NULL, 19, 29, NULL, NULL, 0, 0, 0, 873, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(74, 'SKU-CAR-074', NULL, 'Bombón Cítrico', 'Receta ganadora de premios regionales.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 5, NULL, NULL, NULL, 19, 32, NULL, NULL, 1, 0, 0, 874, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(75, 'SKU-GAL-075', NULL, 'Pomelo Drops', 'Relleno de dulce de leche tradicional.', 'Galletas', NULL, NULL, 'caja', 'unidad', 6, NULL, NULL, NULL, 19, 35, NULL, NULL, 0, 0, 0, 875, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(76, 'SKU-BOM-076', NULL, 'Cereza Semiamarga', 'Sorpresa de frutos secos picados.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 7, NULL, NULL, NULL, 19, 38, NULL, NULL, 1, 0, 0, 876, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(77, 'SKU-GOM-077', NULL, 'Caramelo Naranja', 'Miniaturas surtidas con sabores variados.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 8, NULL, NULL, NULL, 19, 41, NULL, NULL, 0, 0, 0, 877, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(78, 'SKU-CON-078', NULL, 'Trufa de Frutos Rojos', 'Barra energética y nutritiva.', 'Confites', NULL, NULL, 'kg', 'unidad', 9, NULL, NULL, NULL, 19, 44, NULL, NULL, 1, 0, 0, 878, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(79, 'SKU-CHO-079', NULL, 'Nocciola Tableta', 'Cubierta de menta para frescura extra.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 10, NULL, NULL, NULL, 19, 47, NULL, NULL, 0, 0, 0, 879, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(80, 'SKU-CAR-080', NULL, 'Brownie de Caramelo', 'Gomitas rellenas con jugo real de fruta.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 1, NULL, NULL, NULL, 19, 50, NULL, NULL, 1, 0, 0, 880, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(81, 'SKU-GAL-081', NULL, 'Trufas de Avellana', 'Dulce edición primavera.', 'Galletas', NULL, NULL, 'caja', 'unidad', 2, NULL, NULL, NULL, 19, 53, NULL, NULL, 0, 0, 0, 881, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(82, 'SKU-BOM-082', NULL, 'Alfajor Cordobés', 'Esencia cítrica con final acidito.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 3, NULL, NULL, NULL, 19, 56, NULL, NULL, 1, 0, 0, 882, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(83, 'SKU-GOM-083', NULL, 'Turrón de Maní', 'Dulce texturizado con semillas de chía.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 4, NULL, NULL, NULL, 19, 59, NULL, NULL, 0, 0, 0, 883, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(84, 'SKU-CON-084', NULL, 'Chocolate Rubí 75g', 'Recubrimiento doble: chocolate y glaseado.', 'Confites', NULL, NULL, 'kg', 'unidad', 5, NULL, NULL, NULL, 19, 62, NULL, NULL, 1, 0, 0, 884, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(85, 'SKU-CHO-085', NULL, 'Cinta de Caramelo', 'Variedad gourmet, edición limitada.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 6, NULL, NULL, NULL, 19, 65, NULL, NULL, 0, 0, 0, 885, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(86, 'SKU-CAR-086', NULL, 'Barra de Cacao 80%', 'Inspirado en golosinas clásicas europeas.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 7, NULL, NULL, NULL, 19, 68, NULL, NULL, 1, 0, 0, 886, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(87, 'SKU-GAL-087', NULL, 'Confites Turquesa', 'Perfecto para combos y packs familiares.', 'Galletas', NULL, NULL, 'caja', 'unidad', 8, NULL, NULL, NULL, 19, 71, NULL, NULL, 0, 0, 0, 887, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(88, 'SKU-BOM-088', NULL, 'Bombones del Bosque', 'Regalo ideal para sorprender.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 9, NULL, NULL, NULL, 19, 74, NULL, NULL, 1, 0, 0, 888, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(89, 'SKU-GOM-089', NULL, 'Frutilla Glaseada', 'Mini-tarta de frutas confitadas.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 10, NULL, NULL, NULL, 19, 77, NULL, NULL, 0, 0, 0, 889, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(90, 'SKU-CON-090', NULL, 'Mentitas Lemon', 'Múltiples capas de sabores dulces.', 'Confites', NULL, NULL, 'kg', 'unidad', 1, NULL, NULL, NULL, 19, 80, NULL, NULL, 1, 0, 0, 890, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(91, 'SKU-CHO-091', NULL, 'Gomitas Frutales', 'Homenaje a recetas históricas chilenas.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 2, NULL, NULL, NULL, 19, 83, NULL, NULL, 0, 0, 0, 891, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(92, 'SKU-CAR-092', NULL, 'Galletas de Coco', 'Incluído en la caja degustación temporada.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 3, NULL, NULL, NULL, 19, 86, NULL, NULL, 1, 0, 0, 892, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(93, 'SKU-GAL-093', NULL, 'Almendrado Gourmet', 'Snack sin sellos, apto para escolar.', 'Galletas', NULL, NULL, 'caja', 'unidad', 4, NULL, NULL, NULL, 19, 89, NULL, NULL, 0, 0, 0, 893, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(94, 'SKU-BOM-094', NULL, 'Chocoteja Limeña', 'Receta secreta de la abuela de Lili’s.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 5, NULL, NULL, NULL, 19, 92, NULL, NULL, 1, 0, 0, 894, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(95, 'SKU-GOM-095', NULL, 'Bastón de Menta', 'Edición especial Día del Niño.', 'Gomitas', NULL, NULL, 'caja', 'bolsa', 6, NULL, NULL, NULL, 19, 95, NULL, NULL, 0, 0, 0, 895, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(96, 'SKU-CON-096', NULL, 'Jalea Real Berry', 'Mix tropical para verano.', 'Confites', NULL, NULL, 'kg', 'unidad', 7, NULL, NULL, NULL, 19, 98, NULL, NULL, 1, 0, 0, 896, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(97, 'SKU-CHO-097', NULL, 'Enrejado de Nuez', 'Sin azúcar añadida y bajo en grasa.', 'Chocolates', NULL, NULL, 'caja', 'bolsa', 8, NULL, NULL, NULL, 19, 101, NULL, NULL, 0, 0, 0, 897, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(98, 'SKU-CAR-098', NULL, 'Crocante de Maní', 'Decorado con trozos de fruta confitada.', 'Caramelos', NULL, NULL, 'kg', 'bolsa', 9, NULL, NULL, NULL, 19, 104, NULL, NULL, 1, 0, 0, 898, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(99, 'SKU-GAL-099', NULL, 'Relleno de Avellana', 'Sello nacional de calidad.', 'Galletas', NULL, NULL, 'caja', 'unidad', 10, NULL, NULL, NULL, 19, 107, NULL, NULL, 0, 0, 0, 899, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(100, 'SKU-BOM-100', NULL, 'Napoleón Frambuesa', 'Golosina vibrante, presentación arcoíris.', 'Bombones', NULL, NULL, 'kg', 'bolsa', 1, NULL, NULL, NULL, 19, 10, NULL, NULL, 1, 0, 0, 900, NULL, NULL, 0, 'NO', 'NO', NULL, NULL),
(101, 'q2w345678', NULL, 'swerdtfgyutrdser', 'caca mojon', 'Caramelos', 'caca', 'mojon', 'LT', 'UN', 1, NULL, NULL, NULL, 19, 3, 2345, 5, 1, 1, 0, NULL, NULL, NULL, 7, 'SI', 'SI', '2025-11-10 15:25:55', '2025-11-10 15:25:55'),
(102, '1324567654321', NULL, '12345643213456', 'wertyrewtyutretyutretyutretyretyretyretyretyewrtertyretyretyuret', 'Chocolates', '234532134', '5324532134', 'KG', 'BL', 1, NULL, NULL, NULL, 19, 3, 8, 1234543245, 1, 1, 1, NULL, NULL, NULL, 8, 'SI', 'NO', '2025-11-10 15:43:15', '2025-11-10 15:43:15');

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
  `lead_time_dias` int NOT NULL DEFAULT '7',
  `preferente` tinyint(1) NOT NULL DEFAULT '0',
  `Producto_idProducto` int NOT NULL,
  `Proveedor_idProveedor` int NOT NULL,
  `Bodega_idBodega` int DEFAULT NULL,
  `manejo_lotes` tinyint(1) DEFAULT '0',
  `manejo_series` tinyint(1) DEFAULT '0',
  `perecible` tinyint(1) DEFAULT '0',
  `lote` varchar(50) DEFAULT NULL,
  `serie` varchar(50) DEFAULT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `doc_referencia` varchar(100) DEFAULT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `observaciones` text,
  PRIMARY KEY (`idProducto_Proveedor`),
  KEY `fk_Producto_Proveedor_Producto1_idx` (`Producto_idProducto`),
  KEY `fk_Producto_Proveedor_Proveedor1_idx` (`Proveedor_idProveedor`),
  KEY `fk_producto_proveedor_bodega` (`Bodega_idBodega`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `producto_proveedor`
--

INSERT INTO `producto_proveedor` (`idProducto_Proveedor`, `tipo_movimiento`, `cantidad`, `fecha_movimiento`, `lead_time_dias`, `preferente`, `Producto_idProducto`, `Proveedor_idProveedor`, `Bodega_idBodega`, `manejo_lotes`, `manejo_series`, `perecible`, `lote`, `serie`, `fecha_vencimiento`, `doc_referencia`, `motivo`, `observaciones`) VALUES
(1, 'entrada', 87, '2025-01-02 10:00:00', 7, 0, 1, 4, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(2, 'entrada', 94, '2025-01-03 10:00:00', 7, 0, 2, 7, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(3, 'entrada', 101, '2025-01-04 10:00:00', 7, 0, 3, 10, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(4, 'entrada', 108, '2025-01-05 10:00:00', 7, 0, 4, 13, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(5, 'entrada', 115, '2025-01-06 10:00:00', 7, 0, 5, 16, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(6, 'entrada', 122, '2025-01-07 10:00:00', 7, 0, 6, 19, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(7, 'entrada', 129, '2025-01-08 10:00:00', 7, 0, 7, 22, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(8, 'entrada', 136, '2025-01-09 10:00:00', 7, 0, 8, 25, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(9, 'entrada', 143, '2025-01-10 10:00:00', 7, 0, 9, 28, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(10, 'entrada', 150, '2025-01-11 10:00:00', 7, 0, 10, 31, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(11, 'entrada', 157, '2025-01-12 10:00:00', 7, 0, 11, 34, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(12, 'entrada', 164, '2025-01-13 10:00:00', 7, 0, 12, 37, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(13, 'entrada', 171, '2025-01-14 10:00:00', 7, 0, 13, 40, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(14, 'entrada', 178, '2025-01-15 10:00:00', 7, 0, 14, 43, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(15, 'entrada', 185, '2025-01-16 10:00:00', 7, 0, 15, 46, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(16, 'entrada', 192, '2025-01-17 10:00:00', 7, 0, 16, 49, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(17, 'entrada', 199, '2025-01-18 10:00:00', 7, 0, 17, 52, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(18, 'entrada', 206, '2025-01-19 10:00:00', 7, 0, 18, 55, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(19, 'entrada', 213, '2025-01-20 10:00:00', 7, 0, 19, 58, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(20, 'entrada', 220, '2025-01-21 10:00:00', 7, 0, 20, 61, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(21, 'entrada', 227, '2025-01-22 10:00:00', 7, 0, 21, 64, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(22, 'entrada', 234, '2025-01-23 10:00:00', 7, 0, 22, 67, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(23, 'entrada', 241, '2025-01-24 10:00:00', 7, 0, 23, 70, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(24, 'entrada', 248, '2025-01-25 10:00:00', 7, 0, 24, 73, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(25, 'entrada', 255, '2025-01-26 10:00:00', 7, 0, 25, 76, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(26, 'entrada', 262, '2025-01-27 10:00:00', 7, 0, 26, 79, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(27, 'entrada', 269, '2025-01-28 10:00:00', 7, 0, 27, 82, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(28, 'entrada', 276, '2025-01-29 10:00:00', 7, 0, 28, 85, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(29, 'entrada', 283, '2025-01-30 10:00:00', 7, 0, 29, 88, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(30, 'entrada', 290, '2025-01-31 10:00:00', 7, 0, 30, 91, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(31, 'entrada', 297, '2025-02-01 10:00:00', 7, 0, 31, 94, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(32, 'entrada', 304, '2025-02-02 10:00:00', 7, 0, 32, 97, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(33, 'entrada', 311, '2025-02-03 10:00:00', 7, 0, 33, 100, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(34, 'entrada', 318, '2025-02-04 10:00:00', 7, 0, 34, 3, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(35, 'entrada', 325, '2025-02-05 10:00:00', 7, 0, 35, 6, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(36, 'entrada', 332, '2025-02-06 10:00:00', 7, 0, 36, 9, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(37, 'entrada', 339, '2025-02-07 10:00:00', 7, 0, 37, 12, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(38, 'entrada', 346, '2025-02-08 10:00:00', 7, 0, 38, 15, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(39, 'entrada', 353, '2025-02-09 10:00:00', 7, 0, 39, 18, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(40, 'entrada', 360, '2025-02-10 10:00:00', 7, 0, 40, 21, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(41, 'entrada', 367, '2025-02-11 10:00:00', 7, 0, 41, 24, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(42, 'entrada', 374, '2025-02-12 10:00:00', 7, 0, 42, 27, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(43, 'entrada', 381, '2025-02-13 10:00:00', 7, 0, 43, 30, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(44, 'entrada', 388, '2025-02-14 10:00:00', 7, 0, 44, 33, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(45, 'entrada', 395, '2025-02-15 10:00:00', 7, 0, 45, 36, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(46, 'entrada', 402, '2025-02-16 10:00:00', 7, 0, 46, 39, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(47, 'entrada', 409, '2025-02-17 10:00:00', 7, 0, 47, 42, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(48, 'entrada', 416, '2025-02-18 10:00:00', 7, 0, 48, 45, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(49, 'entrada', 423, '2025-02-19 10:00:00', 7, 0, 49, 48, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(50, 'entrada', 430, '2025-02-20 10:00:00', 7, 0, 50, 51, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(51, 'entrada', 437, '2025-02-21 10:00:00', 7, 0, 51, 54, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(52, 'entrada', 444, '2025-02-22 10:00:00', 7, 0, 52, 57, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(53, 'entrada', 451, '2025-02-23 10:00:00', 7, 0, 53, 60, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(54, 'entrada', 458, '2025-02-24 10:00:00', 7, 0, 54, 63, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(55, 'entrada', 465, '2025-02-25 10:00:00', 7, 0, 55, 66, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(56, 'entrada', 472, '2025-02-26 10:00:00', 7, 0, 56, 69, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(57, 'entrada', 479, '2025-02-27 10:00:00', 7, 0, 57, 72, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(58, 'entrada', 486, '2025-02-28 10:00:00', 7, 0, 58, 75, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(59, 'entrada', 493, '2025-03-01 10:00:00', 7, 0, 59, 78, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(60, 'entrada', 500, '2025-03-02 10:00:00', 7, 0, 60, 81, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(61, 'entrada', 507, '2025-03-03 10:00:00', 7, 0, 61, 84, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(62, 'entrada', 514, '2025-03-04 10:00:00', 7, 0, 62, 87, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(63, 'entrada', 521, '2025-03-05 10:00:00', 7, 0, 63, 90, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(64, 'entrada', 528, '2025-03-06 10:00:00', 7, 0, 64, 93, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(65, 'entrada', 535, '2025-03-07 10:00:00', 7, 0, 65, 96, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(66, 'entrada', 542, '2025-03-08 10:00:00', 7, 0, 66, 99, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(67, 'entrada', 549, '2025-03-09 10:00:00', 7, 0, 67, 2, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(68, 'entrada', 556, '2025-03-10 10:00:00', 7, 0, 68, 5, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(69, 'entrada', 563, '2025-03-11 10:00:00', 7, 0, 69, 8, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(70, 'entrada', 570, '2025-03-12 10:00:00', 7, 0, 70, 11, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(71, 'entrada', 577, '2025-03-13 10:00:00', 7, 0, 71, 14, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(72, 'entrada', 584, '2025-03-14 10:00:00', 7, 0, 72, 17, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(73, 'entrada', 591, '2025-03-15 10:00:00', 7, 0, 73, 20, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(74, 'entrada', 598, '2025-03-16 10:00:00', 7, 0, 74, 23, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(75, 'entrada', 605, '2025-03-17 10:00:00', 7, 0, 75, 26, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(76, 'entrada', 612, '2025-03-18 10:00:00', 7, 0, 76, 29, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(77, 'entrada', 619, '2025-03-19 10:00:00', 7, 0, 77, 32, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(78, 'entrada', 626, '2025-03-20 10:00:00', 7, 0, 78, 35, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(79, 'entrada', 633, '2025-03-21 10:00:00', 7, 0, 79, 38, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(80, 'entrada', 640, '2025-03-22 10:00:00', 7, 0, 80, 41, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(81, 'entrada', 647, '2025-03-23 10:00:00', 7, 0, 81, 44, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(82, 'entrada', 654, '2025-03-24 10:00:00', 7, 0, 82, 47, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(83, 'entrada', 661, '2025-03-25 10:00:00', 7, 0, 83, 50, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(84, 'entrada', 668, '2025-03-26 10:00:00', 7, 0, 84, 53, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(85, 'entrada', 675, '2025-03-27 10:00:00', 7, 0, 85, 56, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(86, 'entrada', 682, '2025-03-28 10:00:00', 7, 0, 86, 59, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(87, 'entrada', 689, '2025-03-29 10:00:00', 7, 0, 87, 62, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(88, 'entrada', 696, '2025-03-30 10:00:00', 7, 0, 88, 65, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(89, 'entrada', 703, '2025-03-31 10:00:00', 7, 0, 89, 68, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(90, 'entrada', 710, '2025-04-01 10:00:00', 7, 0, 90, 71, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(91, 'entrada', 717, '2025-04-02 10:00:00', 7, 0, 91, 74, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(92, 'entrada', 724, '2025-04-03 10:00:00', 7, 0, 92, 77, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(93, 'entrada', 731, '2025-04-04 10:00:00', 7, 0, 93, 80, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(94, 'entrada', 738, '2025-04-05 10:00:00', 7, 0, 94, 83, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(95, 'entrada', 745, '2025-04-06 10:00:00', 7, 0, 95, 86, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(96, 'entrada', 752, '2025-04-07 10:00:00', 7, 0, 96, 89, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(97, 'entrada', 759, '2025-04-08 10:00:00', 7, 0, 97, 92, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(98, 'entrada', 766, '2025-04-09 10:00:00', 7, 0, 98, 95, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(99, 'entrada', 773, '2025-04-10 10:00:00', 7, 0, 99, 98, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL),
(100, 'entrada', 780, '2025-04-11 10:00:00', 7, 0, 100, 1, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
CREATE TABLE IF NOT EXISTS `proveedor` (
  `idProveedor` int NOT NULL AUTO_INCREMENT,
  `rut_nif` varchar(20) NOT NULL,
  `razon_social` varchar(255) NOT NULL,
  `nombre_fantasia` varchar(255) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `pais` varchar(64) NOT NULL DEFAULT 'Chile',
  `condiciones_pago` varchar(45) NOT NULL,
  `moneda` varchar(8) NOT NULL DEFAULT 'CLP',
  `estado` enum('Activo','Inactivo','Bloqueado') NOT NULL DEFAULT 'Activo',
  `Usuario_idUsuario` int NOT NULL,
  PRIMARY KEY (`idProveedor`),
  UNIQUE KEY `rut_nif` (`rut_nif`),
  KEY `fk_Proveedor_Usuario1_idx` (`Usuario_idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `proveedor`
--

INSERT INTO `proveedor` (`idProveedor`, `rut_nif`, `razon_social`, `nombre_fantasia`, `email`, `pais`, `condiciones_pago`, `moneda`, `estado`, `Usuario_idUsuario`) VALUES
(1, '76.001.101-1', 'Comercial CacaoMix S.A.', 'CacaoMix 1', 'contacto1@CacaoMix.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(2, '76.002.102-2', 'Distribuidora Sweetland S.A.', 'Sweetland 2', 'contacto2@Sweetland.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(3, '76.003.103-3', 'Central FrutiKing S.A.', 'FrutiKing 3', 'contacto3@FrutiKing.cl', 'Colombia', '15 días', 'CLP', 'Inactivo', 4),
(4, '76.004.104-4', 'Mayorista DeliNet S.A.', 'DeliNet 4', 'contacto4@DeliNet.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(5, '76.005.105-5', 'Emporio Merken S.A.', 'Merken 5', 'contacto5@Merken.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(6, '76.006.106-6', 'Proveedoría Chocolito S.A.', 'Chocolito 6', 'contacto6@Chocolito.cl', 'Perú', '30 días', 'CLP', 'Inactivo', 4),
(7, '76.007.107-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 7', 'contacto7@CandyHouse.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(8, '76.008.108-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 8', 'contacto8@Mansión Dulce.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(9, '76.009.109-9', 'Importadora SnacksLab S.A.', 'SnacksLab 9', 'contacto9@SnacksLab.cl', 'Argentina', '15 días', 'CLP', 'Inactivo', 4),
(10, '76.010.110-0', 'Exportadora Dulsur S.A.', 'Dulsur 10', 'contacto10@Dulsur.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(11, '76.011.111-1', 'Comercial CacaoMix S.A.', 'CacaoMix 11', 'contacto11@CacaoMix.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(12, '76.012.112-2', 'Distribuidora Sweetland S.A.', 'Sweetland 12', 'contacto12@Sweetland.cl', 'Uruguay', '30 días', 'CLP', 'Inactivo', 4),
(13, '76.013.113-3', 'Central FrutiKing S.A.', 'FrutiKing 13', 'contacto13@FrutiKing.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(14, '76.014.114-4', 'Mayorista DeliNet S.A.', 'DeliNet 14', 'contacto14@DeliNet.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(15, '76.015.115-5', 'Emporio Merken S.A.', 'Merken 15', 'contacto15@Merken.cl', 'Brasil', '15 días', 'CLP', 'Inactivo', 4),
(16, '76.016.116-6', 'Proveedoría Chocolito S.A.', 'Chocolito 16', 'contacto16@Chocolito.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(17, '76.017.117-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 17', 'contacto17@CandyHouse.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(18, '76.018.118-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 18', 'contacto18@Mansión Dulce.cl', 'México', '30 días', 'CLP', 'Inactivo', 4),
(19, '76.019.119-9', 'Importadora SnacksLab S.A.', 'SnacksLab 19', 'contacto19@SnacksLab.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(20, '76.020.120-0', 'Exportadora Dulsur S.A.', 'Dulsur 20', 'contacto20@Dulsur.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(21, '76.021.121-1', 'Comercial CacaoMix S.A.', 'CacaoMix 21', 'contacto21@CacaoMix.cl', 'Paraguay', '15 días', 'CLP', 'Inactivo', 4),
(22, '76.022.122-2', 'Distribuidora Sweetland S.A.', 'Sweetland 22', 'contacto22@Sweetland.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(23, '76.023.123-3', 'Central FrutiKing S.A.', 'FrutiKing 23', 'contacto23@FrutiKing.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(24, '76.024.124-4', 'Mayorista DeliNet S.A.', 'DeliNet 24', 'contacto24@DeliNet.cl', 'Chile', '30 días', 'CLP', 'Inactivo', 4),
(25, '76.025.125-5', 'Emporio Merken S.A.', 'Merken 25', 'contacto25@Merken.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(26, '76.026.126-6', 'Proveedoría Chocolito S.A.', 'Chocolito 26', 'contacto26@Chocolito.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(27, '76.027.127-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 27', 'contacto27@CandyHouse.cl', 'Colombia', '15 días', 'CLP', 'Inactivo', 4),
(28, '76.028.128-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 28', 'contacto28@Mansión Dulce.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(29, '76.029.129-9', 'Importadora SnacksLab S.A.', 'SnacksLab 29', 'contacto29@SnacksLab.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(30, '76.030.130-0', 'Exportadora Dulsur S.A.', 'Dulsur 30', 'contacto30@Dulsur.cl', 'Perú', '30 días', 'CLP', 'Inactivo', 4),
(31, '76.031.131-1', 'Comercial CacaoMix S.A.', 'CacaoMix 31', 'contacto31@CacaoMix.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(32, '76.032.132-2', 'Distribuidora Sweetland S.A.', 'Sweetland 32', 'contacto32@Sweetland.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(33, '76.033.133-3', 'Central FrutiKing S.A.', 'FrutiKing 33', 'contacto33@FrutiKing.cl', 'Argentina', '15 días', 'CLP', 'Inactivo', 4),
(34, '76.034.134-4', 'Mayorista DeliNet S.A.', 'DeliNet 34', 'contacto34@DeliNet.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(35, '76.035.135-5', 'Emporio Merken S.A.', 'Merken 35', 'contacto35@Merken.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(36, '76.036.136-6', 'Proveedoría Chocolito S.A.', 'Chocolito 36', 'contacto36@Chocolito.cl', 'Uruguay', '30 días', 'CLP', 'Inactivo', 4),
(37, '76.037.137-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 37', 'contacto37@CandyHouse.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(38, '76.038.138-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 38', 'contacto38@Mansión Dulce.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(39, '76.039.139-9', 'Importadora SnacksLab S.A.', 'SnacksLab 39', 'contacto39@SnacksLab.cl', 'Brasil', '15 días', 'CLP', 'Inactivo', 4),
(40, '76.040.140-0', 'Exportadora Dulsur S.A.', 'Dulsur 40', 'contacto40@Dulsur.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(41, '76.041.141-1', 'Comercial CacaoMix S.A.', 'CacaoMix 41', 'contacto41@CacaoMix.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(42, '76.042.142-2', 'Distribuidora Sweetland S.A.', 'Sweetland 42', 'contacto42@Sweetland.cl', 'México', '30 días', 'CLP', 'Inactivo', 4),
(43, '76.043.143-3', 'Central FrutiKing S.A.', 'FrutiKing 43', 'contacto43@FrutiKing.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(44, '76.044.144-4', 'Mayorista DeliNet S.A.', 'DeliNet 44', 'contacto44@DeliNet.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(45, '76.045.145-5', 'Emporio Merken S.A.', 'Merken 45', 'contacto45@Merken.cl', 'Paraguay', '15 días', 'CLP', 'Inactivo', 4),
(46, '76.046.146-6', 'Proveedoría Chocolito S.A.', 'Chocolito 46', 'contacto46@Chocolito.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(47, '76.047.147-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 47', 'contacto47@CandyHouse.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(48, '76.048.148-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 48', 'contacto48@Mansión Dulce.cl', 'Chile', '30 días', 'CLP', 'Inactivo', 4),
(49, '76.049.149-9', 'Importadora SnacksLab S.A.', 'SnacksLab 49', 'contacto49@SnacksLab.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(50, '76.050.150-0', 'Exportadora Dulsur S.A.', 'Dulsur 50', 'contacto50@Dulsur.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(51, '76.051.151-1', 'Comercial CacaoMix S.A.', 'CacaoMix 51', 'contacto51@CacaoMix.cl', 'Colombia', '15 días', 'CLP', 'Inactivo', 4),
(52, '76.052.152-2', 'Distribuidora Sweetland S.A.', 'Sweetland 52', 'contacto52@Sweetland.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(53, '76.053.153-3', 'Central FrutiKing S.A.', 'FrutiKing 53', 'contacto53@FrutiKing.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(54, '76.054.154-4', 'Mayorista DeliNet S.A.', 'DeliNet 54', 'contacto54@DeliNet.cl', 'Perú', '30 días', 'CLP', 'Inactivo', 4),
(55, '76.055.155-5', 'Emporio Merken S.A.', 'Merken 55', 'contacto55@Merken.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(56, '76.056.156-6', 'Proveedoría Chocolito S.A.', 'Chocolito 56', 'contacto56@Chocolito.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(57, '76.057.157-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 57', 'contacto57@CandyHouse.cl', 'Argentina', '15 días', 'CLP', 'Inactivo', 4),
(58, '76.058.158-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 58', 'contacto58@Mansión Dulce.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(59, '76.059.159-9', 'Importadora SnacksLab S.A.', 'SnacksLab 59', 'contacto59@SnacksLab.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(60, '76.060.160-0', 'Exportadora Dulsur S.A.', 'Dulsur 60', 'contacto60@Dulsur.cl', 'Uruguay', '30 días', 'CLP', 'Inactivo', 4),
(61, '76.061.161-1', 'Comercial CacaoMix S.A.', 'CacaoMix 61', 'contacto61@CacaoMix.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(62, '76.062.162-2', 'Distribuidora Sweetland S.A.', 'Sweetland 62', 'contacto62@Sweetland.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(63, '76.063.163-3', 'Central FrutiKing S.A.', 'FrutiKing 63', 'contacto63@FrutiKing.cl', 'Brasil', '15 días', 'CLP', 'Inactivo', 4),
(64, '76.064.164-4', 'Mayorista DeliNet S.A.', 'DeliNet 64', 'contacto64@DeliNet.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(65, '76.065.165-5', 'Emporio Merken S.A.', 'Merken 65', 'contacto65@Merken.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(66, '76.066.166-6', 'Proveedoría Chocolito S.A.', 'Chocolito 66', 'contacto66@Chocolito.cl', 'México', '30 días', 'CLP', 'Inactivo', 4),
(67, '76.067.167-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 67', 'contacto67@CandyHouse.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(68, '76.068.168-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 68', 'contacto68@Mansión Dulce.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(69, '76.069.169-9', 'Importadora SnacksLab S.A.', 'SnacksLab 69', 'contacto69@SnacksLab.cl', 'Paraguay', '15 días', 'CLP', 'Inactivo', 4),
(70, '76.070.170-0', 'Exportadora Dulsur S.A.', 'Dulsur 70', 'contacto70@Dulsur.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(71, '76.071.171-1', 'Comercial CacaoMix S.A.', 'CacaoMix 71', 'contacto71@CacaoMix.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(72, '76.072.172-2', 'Distribuidora Sweetland S.A.', 'Sweetland 72', 'contacto72@Sweetland.cl', 'Chile', '30 días', 'CLP', 'Inactivo', 4),
(73, '76.073.173-3', 'Central FrutiKing S.A.', 'FrutiKing 73', 'contacto73@FrutiKing.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(74, '76.074.174-4', 'Mayorista DeliNet S.A.', 'DeliNet 74', 'contacto74@DeliNet.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(75, '76.075.175-5', 'Emporio Merken S.A.', 'Merken 75', 'contacto75@Merken.cl', 'Colombia', '15 días', 'CLP', 'Inactivo', 4),
(76, '76.076.176-6', 'Proveedoría Chocolito S.A.', 'Chocolito 76', 'contacto76@Chocolito.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(77, '76.077.177-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 77', 'contacto77@CandyHouse.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(78, '76.078.178-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 78', 'contacto78@Mansión Dulce.cl', 'Perú', '30 días', 'CLP', 'Inactivo', 4),
(79, '76.079.179-9', 'Importadora SnacksLab S.A.', 'SnacksLab 79', 'contacto79@SnacksLab.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(80, '76.080.180-0', 'Exportadora Dulsur S.A.', 'Dulsur 80', 'contacto80@Dulsur.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(81, '76.081.181-1', 'Comercial CacaoMix S.A.', 'CacaoMix 81', 'contacto81@CacaoMix.cl', 'Argentina', '15 días', 'CLP', 'Inactivo', 4),
(82, '76.082.182-2', 'Distribuidora Sweetland S.A.', 'Sweetland 82', 'contacto82@Sweetland.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(83, '76.083.183-3', 'Central FrutiKing S.A.', 'FrutiKing 83', 'contacto83@FrutiKing.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(84, '76.084.184-4', 'Mayorista DeliNet S.A.', 'DeliNet 84', 'contacto84@DeliNet.cl', 'Uruguay', '30 días', 'CLP', 'Inactivo', 4),
(85, '76.085.185-5', 'Emporio Merken S.A.', 'Merken 85', 'contacto85@Merken.cl', 'Paraguay', '15 días', 'CLP', 'Activo', 4),
(86, '76.086.186-6', 'Proveedoría Chocolito S.A.', 'Chocolito 86', 'contacto86@Chocolito.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(87, '76.087.187-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 87', 'contacto87@CandyHouse.cl', 'Brasil', '15 días', 'CLP', 'Inactivo', 4),
(88, '76.088.188-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 88', 'contacto88@Mansión Dulce.cl', 'Chile', '30 días', 'CLP', 'Activo', 4),
(89, '76.089.189-9', 'Importadora SnacksLab S.A.', 'SnacksLab 89', 'contacto89@SnacksLab.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(90, '76.090.190-0', 'Exportadora Dulsur S.A.', 'Dulsur 90', 'contacto90@Dulsur.cl', 'México', '30 días', 'CLP', 'Inactivo', 4),
(91, '76.091.191-1', 'Comercial CacaoMix S.A.', 'CacaoMix 91', 'contacto91@CacaoMix.cl', 'Colombia', '15 días', 'CLP', 'Activo', 4),
(92, '76.092.192-2', 'Distribuidora Sweetland S.A.', 'Sweetland 92', 'contacto92@Sweetland.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4),
(93, '76.093.193-3', 'Central FrutiKing S.A.', 'FrutiKing 93', 'contacto93@FrutiKing.cl', 'Paraguay', '15 días', 'CLP', 'Inactivo', 4),
(94, '76.094.194-4', 'Mayorista DeliNet S.A.', 'DeliNet 94', 'contacto94@DeliNet.cl', 'Perú', '30 días', 'CLP', 'Activo', 4),
(95, '76.095.195-5', 'Emporio Merken S.A.', 'Merken 95', 'contacto95@Merken.cl', 'Brasil', '15 días', 'CLP', 'Activo', 4),
(96, '76.096.196-6', 'Proveedoría Chocolito S.A.', 'Chocolito 96', 'contacto96@Chocolito.cl', 'Chile', '30 días', 'CLP', 'Inactivo', 4),
(97, '76.097.197-7', 'Bebestible CandyHouse S.A.', 'CandyHouse 97', 'contacto97@CandyHouse.cl', 'Argentina', '15 días', 'CLP', 'Activo', 4),
(98, '76.098.198-8', 'Fábrica Mansión Dulce S.A.', 'Mansión Dulce 98', 'contacto98@Mansión Dulce.cl', 'México', '30 días', 'CLP', 'Activo', 4),
(99, '76.099.199-9', 'Importadora SnacksLab S.A.', 'SnacksLab 99', 'contacto99@SnacksLab.cl', 'Colombia', '15 días', 'CLP', 'Inactivo', 4),
(100, '76.100.200-0', 'Exportadora Dulsur S.A.', 'Dulsur 100', 'contacto100@Dulsur.cl', 'Uruguay', '30 días', 'CLP', 'Activo', 4);

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
  `avatar` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `username`, `email`, `nombre`, `apellido`, `rol`, `estado`, `mfa_habilitado`, `password`, `avatar`) VALUES
(1, 'admin', 'admin@dulcerialilis.cl', 'Admin', 'Principal', 'administrador', 'activo', 'deshabilitado', 'Admin#123', ''),
(2, 'inventario', 'inventario@dulcerialilis.cl', 'Tomás', 'Gallardo', 'operador_inventario', 'activo', 'deshabilitado', 'Inventario#001', ''),
(3, 'ventas', 'ventas@dulcerialilis.cl', 'Andrea', 'Sánchez', 'operador_ventas', 'activo', 'deshabilitado', 'Ventas#001', ''),
(4, 'compras', 'compras@dulcerialilis.cl', 'Martín', 'Lagos', 'operador_compras', 'activo', 'deshabilitado', 'Compras#001', ''),
(5, 'marmota', 'marmota@marmota.cl', 'Marmota', 'Aguilar', 'Administrador', 'activo', 'deshabilitado', NULL, 'avatars/Screenshot_1_oce6tgV.png'),
(6, 'Administrador', 'admin@admin.com', 'Administrador', 'Juan', 'operador_ventas', 'activo', 'deshabilitado', NULL, ''),
(7, 'Funciona', 'Funciona@gmail.com', 'Fun', 'ciona', 'administrador', 'activo', 'deshabilitado', 'pbkdf2_sha256$1000000$eE6RWzhwoVK0ZYP8YxX6Ez$51xQJmNyRh8BpMSvMV4ztedYzK4YMwjk+y2r4XR8cbc=', ''),
(8, 'CreandoPrueba', 'CreandoPrueba@gmail.com', 'me', 'si', 'operador_inventario', 'activo', 'deshabilitado', 'pbkdf2_sha256$1000000$m79iRCjp422dVSuYv6SYlS$vrlUMPFmJsDhL9O0J9QjsHKRDcSr8lwhp0bZD360Q+M=', '');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `producto_proveedor`
--
ALTER TABLE `producto_proveedor`
  ADD CONSTRAINT `fk_producto_proveedor_bodega` FOREIGN KEY (`Bodega_idBodega`) REFERENCES `bodega` (`idBodega`) ON DELETE SET NULL ON UPDATE CASCADE,
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
