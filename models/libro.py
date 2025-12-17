"""
Módulo de Libro - Contiene la lógica de negocio para libros
"""
from database.conexion import DatabaseConnection
from typing import List, Tuple, Optional, Dict
from datetime import datetime

class LibroModel:
    """Maneja todas las operaciones relacionadas con Libros"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def crear_libro(self, isbn: str, titulo: str, autor: str, editorial: str = "", 
                   anio: int = None, categoria: str = "", ejemplares: int = 1) -> bool:
        """
        Crea un nuevo libro en la BD
        Returns: True si se creó exitosamente
        """
        query = """
            INSERT INTO Libros (ISBN, Título, Autor, Editorial, Año_Publicacion, 
                              Categoría, Total_Ejemplares, Disponibles, Fecha_Ingreso_Donacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        fecha = datetime.now().strftime("%Y-%m-%d")
        return self.db.ejecutar(query, (isbn, titulo, autor, editorial, anio, 
                                       categoria, ejemplares, ejemplares, fecha))
    
    def obtener_libro_por_isbn(self, isbn: str) -> Optional[Tuple]:
        """Obtiene un libro por su ISBN"""
        query = "SELECT * FROM Libros WHERE ISBN = ?"
        return self.db.consultar_uno(query, (isbn,))
    
    def obtener_libro_por_id(self, id_libro: int) -> Optional[Tuple]:
        """Obtiene un libro por su ID"""
        query = "SELECT * FROM Libros WHERE ID_Libro = ?"
        return self.db.consultar_uno(query, (id_libro,))
    
    def obtener_libro_por_titulo_o_isbn(self, termino: str) -> Optional[Tuple]:
        """Busca un libro por título o ISBN exacto/similar"""
        query = """
            SELECT ID_Libro, Título, Disponibles FROM Libros 
            WHERE (ISBN = ? OR Título LIKE ?) AND Disponibles > 0
            LIMIT 1
        """
        lk = f"%{termino}%"
        return self.db.consultar_uno(query, (termino, lk))
    
    def buscar_libros(self, termino: str = "") -> List[Tuple]:
        """
        Busca libros por término. Si está vacío, muestra solo los con préstamos activos
        Returns: Lista de tuplas con datos de libros
        """
        if termino:
            query = """
                SELECT ID_Libro, ISBN, Título, Autor, Editorial, Año_Publicacion, 
                       Categoría, Total_Ejemplares, Disponibles
                FROM Libros 
                WHERE Título LIKE ? OR Autor LIKE ? OR ISBN LIKE ?
                ORDER BY Título
            """
            lk = f"%{termino}%"
            return self.db.consultar_todos(query, (lk, lk, lk))
        else:
            query = """
                SELECT ID_Libro, ISBN, Título, Autor, Editorial, Año_Publicacion, 
                       Categoría, Total_Ejemplares, Disponibles
                FROM Libros
                WHERE Disponibles < Total_Ejemplares
                ORDER BY Título
            """
            return self.db.consultar_todos(query)
    
    def actualizar_libro(self, id_libro: int, isbn: str, titulo: str, autor: str,
                        editorial: str = "", anio: int = None, categoria: str = "") -> bool:
        """Actualiza los datos de un libro"""
        query = """
            UPDATE Libros 
            SET ISBN=?, Título=?, Autor=?, Editorial=?, Año_Publicacion=?, Categoría=?
            WHERE ID_Libro=?
        """
        return self.db.ejecutar(query, (isbn, titulo, autor, editorial, anio, categoria, id_libro))
    
    def sumar_ejemplares(self, isbn: str, cantidad: int) -> bool:
        """Suma ejemplares a un libro existente"""
        query = """
            UPDATE Libros 
            SET Total_Ejemplares=Total_Ejemplares+?, Disponibles=Disponibles+?
            WHERE ISBN=?
        """
        return self.db.ejecutar(query, (cantidad, cantidad, isbn))
    
    def restar_disponibles(self, id_libro: int, cantidad: int = 1) -> bool:
        """Reduce los ejemplares disponibles (préstamo)"""
        query = "UPDATE Libros SET Disponibles = Disponibles - ? WHERE ID_Libro = ?"
        return self.db.ejecutar(query, (cantidad, id_libro))
    
    def sumar_disponibles(self, id_libro: int, cantidad: int = 1) -> bool:
        """Aumenta los ejemplares disponibles (devolución)"""
        query = "UPDATE Libros SET Disponibles = Disponibles + ? WHERE ID_Libro = ?"
        return self.db.ejecutar(query, (cantidad, id_libro))
    
    def eliminar_libro(self, id_libro: int) -> bool:
        """Elimina un libro de la BD"""
        query = "DELETE FROM Libros WHERE ID_Libro = ?"
        return self.db.ejecutar(query, (id_libro,))
    
    def tiene_prestamos_activos(self, id_libro: int) -> bool:
        """Verifica si un libro tiene préstamos activos"""
        query = "SELECT 1 FROM Transacciones WHERE ID_Libro=? AND Estado='Prestado'"
        return self.db.consultar_uno(query, (id_libro,)) is not None
    
    def obtener_todos(self) -> List[Tuple]:
        """Obtiene todos los libros"""
        query = """
            SELECT ID_Libro, ISBN, Título, Autor, Editorial, Año_Publicacion, 
                   Categoría, Total_Ejemplares, Disponibles
            FROM Libros
            ORDER BY Título
        """
        return self.db.consultar_todos(query)
    
    def obtener_estadisticas(self) -> Dict[str, int]:
        """Obtiene estadísticas generales de libros"""
        stats = {
            'total_libros': 0,
            'total_ejemplares': 0,
            'disponibles': 0,
            'prestados': 0
        }
        
        query = "SELECT COUNT(*), SUM(Total_Ejemplares), SUM(Disponibles) FROM Libros"
        result = self.db.consultar_uno(query)
        
        if result:
            stats['total_libros'] = result[0] or 0
            stats['total_ejemplares'] = result[1] or 0
            stats['disponibles'] = result[2] or 0
            stats['prestados'] = stats['total_ejemplares'] - stats['disponibles']
        
        return stats
