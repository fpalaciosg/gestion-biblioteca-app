"""
Módulo de inicialización de modelos/tablas de base de datos
Define la estructura de las tablas SQLite
"""
from .conexion import DatabaseConnection
from typing import Optional

class DatabaseModels:
    """Maneja la inicialización y creación de tablas en la base de datos"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def inicializar_db(self) -> bool:
        """
        Crea todas las tablas necesarias si no existen
        Returns: True si se inicializó correctamente
        """
        try:
            self._crear_tabla_libros()
            self._crear_tabla_prestatarios()
            self._crear_tabla_transacciones()
            return True
        except Exception as e:
            print(f"Error al inicializar BD: {e}")
            return False
    
    def _crear_tabla_libros(self) -> bool:
        """Crea la tabla de Libros"""
        query = """
            CREATE TABLE IF NOT EXISTS Libros (
                ID_Libro INTEGER PRIMARY KEY AUTOINCREMENT,
                ISBN TEXT UNIQUE, 
                Título TEXT NOT NULL, 
                Autor TEXT NOT NULL,
                Editorial TEXT, 
                Año_Publicacion INTEGER, 
                Categoría TEXT,
                Total_Ejemplares INTEGER NOT NULL, 
                Disponibles INTEGER NOT NULL,
                Fecha_Ingreso_Donacion TEXT
            );
        """
        return self.db.ejecutar(query)
    
    def _crear_tabla_prestatarios(self) -> bool:
        """Crea la tabla de Prestatarios (Alumnos)"""
        query = """
            CREATE TABLE IF NOT EXISTS Prestatarios (
                ID_Prestatario INTEGER PRIMARY KEY AUTOINCREMENT,
                RUT TEXT UNIQUE NOT NULL,
                Nombre TEXT NOT NULL,
                Curso TEXT
            );
        """
        return self.db.ejecutar(query)
    
    def _crear_tabla_transacciones(self) -> bool:
        """Crea la tabla de Transacciones (Préstamos/Devoluciones)"""
        query = """
            CREATE TABLE IF NOT EXISTS Transacciones (
                ID_Transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Libro INTEGER NOT NULL, 
                ID_Prestatario INTEGER NOT NULL,
                Fecha_Entrega TEXT NOT NULL, 
                Fecha_Devolucion_Estimada TEXT,
                Fecha_Devolucion_Real TEXT NULL, 
                Estado TEXT NOT NULL,
                FOREIGN KEY (ID_Libro) REFERENCES Libros(ID_Libro) ON DELETE CASCADE,
                FOREIGN KEY (ID_Prestatario) REFERENCES Prestatarios(ID_Prestatario) ON DELETE CASCADE
            );
        """
        return self.db.ejecutar(query)
    
    def drop_all_tables(self) -> bool:
        """
        Elimina todas las tablas (útil para testing)
        Returns: True si se eliminaron correctamente
        """
        try:
            self.db.ejecutar("DROP TABLE IF EXISTS Transacciones")
            self.db.ejecutar("DROP TABLE IF EXISTS Libros")
            self.db.ejecutar("DROP TABLE IF EXISTS Prestatarios")
            return True
        except Exception as e:
            print(f"Error al eliminar tablas: {e}")
            return False
