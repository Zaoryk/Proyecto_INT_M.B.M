import os
import sys
import django
import MySQLdb
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Migra la base de datos de SQLite a MySQL'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando migración a MySQL...')
        
        # Paso 1: Hacer backup de SQLite
        self.hacer_backup_sqlite()
        
        # Paso 2: Crear tablas en MySQL
        self.crear_esquema_mysql()
        
        # Paso 3: Exportar datos de SQLite
        self.exportar_datos_sqlite()
        
        # Paso 4: Importar datos a MySQL
        self.importar_datos_mysql()
        
        self.stdout.write(self.style.SUCCESS('Migración completada exitosamente!'))

    def hacer_backup_sqlite(self):
        """Crea un backup de la base de datos SQLite"""
        import shutil
        import datetime
        
        backup_file = f"db_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
        shutil.copy2('db.sqlite3', backup_file)
        self.stdout.write(f'[OK] Backup creado: {backup_file}')

    def crear_esquema_mysql(self):
        """Crea el esquema en MySQL basado en tu diagrama"""
        try:
            # Conectar a MySQL
            conn = MySQLdb.connect(
                host='localhost',
                user='tu_usuario',
                password='tu_password',
                database='dulceria_db'
            )
            cursor = conn.cursor()
            
            # Ejecutar el script SQL de tu diagrama
            sql_script = self.obtener_script_mysql()
            cursor.execute(sql_script)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            self.stdout.write('[OK] Esquema MySQL creado')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creando esquema MySQL: {e}'))

    def obtener_script_mysql(self):
        """Retorna el script SQL de tu diagrama adaptado para MySQL"""
        return """
SET FOREIGN_KEY_CHECKS=0;

-- Table structure for auth_user (usuarios de Django)
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL UNIQUE,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for dispositivos_proveedor
CREATE TABLE IF NOT EXISTS `dispositivos_proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `contacto` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for dispositivos_producto
CREATE TABLE IF NOT EXISTS `dispositivos_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `lote` varchar(50) UNIQUE,
  `proveedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`proveedor_id`) REFERENCES `dispositivos_proveedor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for dispositivos_perfilusuario
CREATE TABLE IF NOT EXISTS `dispositivos_perfilusuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(200),
  `telefono` varchar(20),
  `rol` varchar(50) NOT NULL,
  `user_id` int NOT NULL UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS=1;
"""

    def exportar_datos_sqlite(self):
        """Exporta datos de SQLite a archivos JSON"""
        self.stdout.write('Exportando datos de SQLite...')
        os.system('python manage.py dumpdata --indent=2 > datos_exportados.json')
        self.stdout.write('[OK] Datos exportados a datos_exportados.json')

    def importar_datos_mysql(self):
        """Importa datos a MySQL"""
        self.stdout.write('Importando datos a MySQL...')
        os.system('python manage.py loaddata datos_exportados.json')
        self.stdout.write('[OK] Datos importados a MySQL')