"""
Ventana Principal - Orquestador de todas las pestañas y componentes
"""
import customtkinter
from ui.tabs.prestamos_tab import PrestamosTab
from ui.tabs.libros_tab import LibrosTab
from ui.tabs.alumnos_tab import AlumnosTab
from models.libro import LibroModel
from models.alumno import AlumnoModel
from models.transaccion import TransaccionModel
from utils.theme import Colors, Styles, ThemeConfig


class MainWindow(customtkinter.CTk):
    """Ventana principal de la aplicación"""
    
    def __init__(self, db_connection, db_models):
        super().__init__()
        self.title("📚 Sistema de Inventario CRA")
        self.geometry("1200x750")
        self._set_appearance()
        
        # Inicializar modelos
        self.db = db_connection
        self.libro_model = LibroModel(self.db)
        self.alumno_model = AlumnoModel(self.db)
        self.transaccion_model = TransaccionModel(self.db)
        
        # Crear tablas si no existen
        db_models.inicializar_db()
        
        # Construir UI
        self._build_ui()
    
    def _set_appearance(self):
        """Configura la apariencia de la aplicación"""
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        
        # Aplicar colores personalizados (nota: CustomTkinter tiene limitaciones)
        # Se aplicará color por elemento en lugar de tema global
    
    def _build_ui(self):
        """Construye la interfaz principal"""
        # Frame principal con padding
        main_frame = customtkinter.CTkFrame(self, fg_color=Colors.BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # === HEADER ===
        self._build_header(main_frame)
        
        # === SEPARADOR ===
        sep = customtkinter.CTkFrame(main_frame, height=2, fg_color=Colors.BORDER_LIGHT)
        sep.pack(fill="x", padx=0, pady=0)
        
        # === CONTENIDO (TABS) ===
        content_frame = customtkinter.CTkFrame(main_frame, fg_color=Colors.BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=Styles.PADDING_LG, pady=Styles.PADDING_LG)
        
        # Crear TabView
        self.tab_view = customtkinter.CTkTabview(content_frame, fg_color=Colors.BG_SECONDARY,
                                                  segmented_button_fg_color=Colors.BG_TERTIARY,
                                                  segmented_button_selected_color=Colors.PRIMARY,
                                                  segmented_button_selected_hover_color=Colors.PRIMARY_LIGHT,
                                                  text_color=Colors.TEXT_PRIMARY)
        self.tab_view.pack(pady=0, padx=0, fill="both", expand=True)
        
        # Pestaña 1: Préstamos
        self.tab_view.add("📤 Préstamos")
        tab_prestamos = self.tab_view.tab("📤 Préstamos")
        tab_prestamos.configure(fg_color=Colors.BG_DARK)
        self.prestamos_tab = PrestamosTab(tab_prestamos, self.libro_model, self.alumno_model, self.transaccion_model)
        
        # Pestaña 2: Libros
        self.tab_view.add("📚 Libros")
        tab_libros = self.tab_view.tab("📚 Libros")
        tab_libros.configure(fg_color=Colors.BG_DARK)
        self.libros_tab = LibrosTab(tab_libros, self.libro_model)
        
        # Pestaña 3: Alumnos
        self.tab_view.add("👥 Alumnos")
        tab_alumnos = self.tab_view.tab("👥 Alumnos")
        tab_alumnos.configure(fg_color=Colors.BG_DARK)
        self.alumnos_tab = AlumnosTab(tab_alumnos, self.alumno_model)
    
    def _build_header(self, parent):
        """Construye el encabezado de la ventana"""
        header = customtkinter.CTkFrame(parent, fg_color=Colors.PRIMARY, 
                                       corner_radius=0, height=70)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Contenido del header
        content = customtkinter.CTkFrame(header, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=Styles.PADDING_XL, pady=Styles.PADDING_LG)
        
        # Título
        title = customtkinter.CTkLabel(content, text="📚 Sistema de Gestión de Biblioteca (CRA)",
                                       text_color=Colors.TEXT_PRIMARY,
                                       font=("Segoe UI", 20, "bold"))
        title.pack(side="left", padx=0)
        
        # Subtítulo
        subtitle = customtkinter.CTkLabel(content, text="Centro de Recursos de Aprendizaje",
                                         text_color=Colors.ACCENT,
                                         font=("Segoe UI", 12))
        subtitle.pack(side="left", padx=Styles.PADDING_LG)

