"""
Ventana Principal - Orquesta todas las pestañas y componentes de la aplicación
"""
import customtkinter
from ui.tabs.prestamos_tab import PrestamosTab
from ui.tabs.libros_tab import LibrosTab
from ui.tabs.alumnos_tab import AlumnosTab
from models.libro import LibroModel
from models.alumno import AlumnoModel
from models.transaccion import TransaccionModel


class MainWindow(customtkinter.CTk):
    """Ventana principal de la aplicación"""
    
    def __init__(self, db_connection, db_models):
        super().__init__()
        self.title("Sistema de Inventario CRA")
        self.geometry("1200x700")
        
        # Inicializar modelos
        self.db = db_connection
        self.libro_model = LibroModel(self.db)
        self.alumno_model = AlumnoModel(self.db)
        self.transaccion_model = TransaccionModel(self.db)
        
        # Crear tablas si no existen
        db_models.inicializar_db()
        
        # Construir UI
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz principal"""
        # Crear TabView
        self.tab_view = customtkinter.CTkTabview(self, width=980)
        self.tab_view.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Pestaña 1: Préstamos
        self.tab_view.add("Préstamos")
        tab_prestamos = self.tab_view.tab("Préstamos")
        self.prestamos_tab = PrestamosTab(tab_prestamos, self.libro_model, self.alumno_model, self.transaccion_model)
        
        # Pestaña 2: Libros
        self.tab_view.add("Libros")
        tab_libros = self.tab_view.tab("Libros")
        self.libros_tab = LibrosTab(tab_libros, self.libro_model)
        
        # Pestaña 3: Alumnos
        self.tab_view.add("Alumnos")
        tab_alumnos = self.tab_view.tab("Alumnos")
        self.alumnos_tab = AlumnosTab(tab_alumnos, self.alumno_model)
