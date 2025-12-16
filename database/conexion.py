"""
Módulo de conexión a la base de datos SQLite
Maneja todas las operaciones de conexión y consultas
"""
import sqlite3
import os
from typing import Optional, List, Tuple, Any

class DatabaseConnection:
    """Maneja las conexiones a la base de datos SQLite"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Asegura que el archivo de BD exista"""
        if not os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            conn.close()
    
    def conectar(self) -> Optional[sqlite3.Connection]:
        """
        Crea una conexión a la base de datos
        Returns: Conexión a SQLite o None si hay error
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None
    
    def ejecutar(self, query: str, params: Tuple = ()) -> bool:
        """
        Ejecuta una consulta que modifica datos (INSERT, UPDATE, DELETE)
        Returns: True si se ejecutó exitosamente, False en caso contrario
        """
        conn = self.conectar()
        if conn is None:
            return False
        try:
            conn.execute(query, params)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar query: {e}")
            return False
        finally:
            conn.close()
    
    def ejecutar_muchos(self, query: str, params_list: List[Tuple]) -> bool:
        """
        Ejecuta múltiples consultas de una sola vez
        Returns: True si se ejecutaron exitosamente
        """
        conn = self.conectar()
        if conn is None:
            return False
        try:
            conn.executemany(query, params_list)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar queries múltiples: {e}")
            return False
        finally:
            conn.close()
    
    def consultar_uno(self, query: str, params: Tuple = ()) -> Optional[Tuple]:
        """
        Ejecuta una consulta y retorna una fila
        Returns: Una tupla con los datos o None
        """
        conn = self.conectar()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error en consulta: {e}")
            return None
        finally:
            conn.close()
    
    def consultar_todos(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """
        Ejecuta una consulta y retorna todas las filas
        Returns: Lista de tuplas con los datos
        """
        conn = self.conectar()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en consulta: {e}")
            return []
        finally:
            conn.close()
    
    def get_last_row_id(self) -> Optional[int]:
        """Obtiene el ID de la última fila insertada"""
        conn = self.conectar()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
