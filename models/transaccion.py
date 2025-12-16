"""
Módulo de Transacción - Contiene la lógica de negocio para préstamos y devoluciones
"""
from database.conexion import DatabaseConnection
from typing import List, Tuple, Optional
from datetime import datetime

class TransaccionModel:
    """Maneja todas las operaciones relacionadas con Préstamos y Devoluciones"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def crear_prestamo(self, id_libro: int, id_prestatario: int) -> bool:
        """
        Registra un nuevo préstamo
        Returns: True si se creó exitosamente
        """
        fecha_entrega = datetime.now().strftime("%Y-%m-%d")
        query = """
            INSERT INTO Transacciones (ID_Libro, ID_Prestatario, Fecha_Entrega, Estado)
            VALUES (?, ?, ?, 'Prestado')
        """
        return self.db.ejecutar(query, (id_libro, id_prestatario, fecha_entrega))
    
    def existe_prestamo_duplicado(self, id_libro: int, id_prestatario: int) -> bool:
        """Verifica si ya existe un préstamo activo del mismo libro al mismo alumno"""
        query = """
            SELECT 1 FROM Transacciones 
            WHERE ID_Libro = ? AND ID_Prestatario = ? AND Estado = 'Prestado'
        """
        return self.db.consultar_uno(query, (id_libro, id_prestatario)) is not None
    
    def obtener_prestamo_activo(self, id_libro: int) -> Optional[Tuple]:
        """Obtiene el préstamo activo de un libro (si existe)"""
        query = """
            SELECT ID_Transaccion FROM Transacciones 
            WHERE ID_Libro = ? AND Estado = 'Prestado' 
            LIMIT 1
        """
        return self.db.consultar_uno(query, (id_libro,))
    
    def registrar_devolucion(self, id_transaccion: int) -> bool:
        """
        Registra la devolución de un libro
        Returns: True si se registró exitosamente
        """
        fecha_devolucion = datetime.now().strftime("%Y-%m-%d")
        query = """
            UPDATE Transacciones 
            SET Estado = 'Devuelto', Fecha_Devolucion_Real = ? 
            WHERE ID_Transaccion = ?
        """
        return self.db.ejecutar(query, (fecha_devolucion, id_transaccion))
    
    def obtener_todas_transacciones(self, id_prestatario: int = None) -> List[Tuple]:
        """
        Obtiene todas las transacciones, opcionalmente filtradas por prestatario
        Returns: Lista de tuplas con datos de transacciones
        """
        if id_prestatario:
            query = """
                SELECT t.ID_Transaccion, t.ID_Libro, t.ID_Prestatario, 
                       t.Fecha_Entrega, t.Fecha_Devolucion_Real, t.Estado
                FROM Transacciones t
                WHERE t.ID_Prestatario = ?
                ORDER BY t.Fecha_Entrega DESC
            """
            return self.db.consultar_todos(query, (id_prestatario,))
        else:
            query = """
                SELECT ID_Transaccion, ID_Libro, ID_Prestatario, 
                       Fecha_Entrega, Fecha_Devolucion_Real, Estado
                FROM Transacciones
                ORDER BY Fecha_Entrega DESC
            """
            return self.db.consultar_todos(query)
    
    def obtener_prestamo_por_libro(self, id_libro: int) -> Optional[Tuple]:
        """Obtiene el préstamo activo de un libro"""
        query = """
            SELECT ID_Transaccion, ID_Prestatario 
            FROM Transacciones 
            WHERE ID_Libro = ? AND Estado = 'Prestado'
        """
        return self.db.consultar_uno(query, (id_libro,))
