"""
Módulo de Alumno/Prestatario - Contiene la lógica de negocio para alumnos
"""
from database.conexion import DatabaseConnection
from typing import List, Tuple, Optional

class AlumnoModel:
    """Maneja todas las operaciones relacionadas con Alumnos/Prestatarios"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def crear_alumno(self, rut: str, nombre: str, curso: str = "") -> bool:
        """
        Crea un nuevo alumno en la BD
        Returns: True si se creó exitosamente
        """
        query = "INSERT INTO Prestatarios (RUT, Nombre, Curso) VALUES (?, ?, ?)"
        return self.db.ejecutar(query, (rut, nombre, curso))
    
    def obtener_alumno_por_rut(self, rut: str) -> Optional[Tuple]:
        """Obtiene un alumno por RUT (con búsqueda flexible sin puntos/guiones)"""
        rut_limpio = rut.replace(".", "").replace("-", "")
        query = """
            SELECT ID_Prestatario, Nombre FROM Prestatarios 
            WHERE REPLACE(REPLACE(RUT, '.', ''), '-', '') = ?
        """
        return self.db.consultar_uno(query, (rut_limpio,))
    
    def obtener_alumno_por_id(self, id_prestatario: int) -> Optional[Tuple]:
        """Obtiene un alumno por su ID"""
        query = "SELECT ID_Prestatario, RUT, Nombre, Curso FROM Prestatarios WHERE ID_Prestatario = ?"
        return self.db.consultar_uno(query, (id_prestatario,))
    
    def buscar_alumnos(self, termino: str = "") -> List[Tuple]:
        """
        Busca alumnos por término. Si está vacío, muestra solo los con préstamos activos
        Returns: Lista de tuplas con datos de alumnos
        """
        if termino:
            termino_limpio = termino.replace(".", "").replace("-", "")
            lk_limpio = f"%{termino_limpio}%"
            lk_normal = f"%{termino}%"
            query = """
                SELECT p.ID_Prestatario, p.RUT, p.Nombre, p.Curso,
                       (SELECT COUNT(*) FROM Transacciones t 
                        WHERE t.ID_Prestatario=p.ID_Prestatario AND t.Estado='Prestado') as Activos
                FROM Prestatarios p
                WHERE
                    (REPLACE(REPLACE(p.RUT, '.', ''), '-', '') LIKE ?) OR
                    (p.Nombre LIKE ?) OR
                    (p.Curso LIKE ?)
                ORDER BY p.Nombre
            """
            return self.db.consultar_todos(query, (lk_limpio, lk_normal, lk_normal))
        else:
            query = """
                SELECT p.ID_Prestatario, p.RUT, p.Nombre, p.Curso,
                       (SELECT COUNT(*) FROM Transacciones t 
                        WHERE t.ID_Prestatario=p.ID_Prestatario AND t.Estado='Prestado') as Activos
                FROM Prestatarios p
                WHERE (SELECT COUNT(*) FROM Transacciones t 
                       WHERE t.ID_Prestatario=p.ID_Prestatario AND t.Estado='Prestado') > 0
                ORDER BY p.Nombre
            """
            return self.db.consultar_todos(query)
    
    def actualizar_alumno(self, id_prestatario: int, rut: str, nombre: str, curso: str = "") -> bool:
        """Actualiza los datos de un alumno"""
        query = "UPDATE Prestatarios SET RUT=?, Nombre=?, Curso=? WHERE ID_Prestatario=?"
        return self.db.ejecutar(query, (rut, nombre, curso, id_prestatario))
    
    def eliminar_alumno(self, id_prestatario: int) -> bool:
        """Elimina un alumno de la BD"""
        query = "DELETE FROM Prestatarios WHERE ID_Prestatario=?"
        return self.db.ejecutar(query, (id_prestatario,))    
    def obtener_total_alumnos(self) -> int:
        """Obtiene el total de alumnos registrados"""
        query = "SELECT COUNT(*) FROM Prestatarios"
        result = self.db.consultar_uno(query)
        return result[0] if result else 0    
    def tiene_prestamos_activos(self, id_prestatario: int) -> bool:
        """Verifica si un alumno tiene préstamos activos"""
        query = "SELECT 1 FROM Transacciones WHERE ID_Prestatario=? AND Estado='Prestado'"
        return self.db.consultar_uno(query, (id_prestatario,)) is not None
    
    def obtener_libros_en_poder(self, id_prestatario: int) -> List[Tuple]:
        """Obtiene los libros que un alumno tiene en préstamo activo"""
        query = """
            SELECT l.ISBN, l.Título, l.Autor, t.Fecha_Entrega 
            FROM Transacciones t 
            JOIN Libros l ON t.ID_Libro = l.ID_Libro 
            WHERE t.ID_Prestatario = ? AND t.Estado = 'Prestado'
            ORDER BY t.Fecha_Entrega
        """
        return self.db.consultar_todos(query, (id_prestatario,))
    
    def obtener_todos(self) -> List[Tuple]:
        """Obtiene todos los alumnos"""
        query = "SELECT ID_Prestatario, RUT, Nombre, Curso FROM Prestatarios ORDER BY Nombre"
        return self.db.consultar_todos(query)
