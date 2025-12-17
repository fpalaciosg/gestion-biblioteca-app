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
        """Configura la apariencia de la aplicación - Light Mode"""
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        # Se aplicará color por elemento en lugar de tema global
    
    def _build_ui(self):
        """Construye la interfaz principal"""
        # Frame principal con padding
        main_frame = customtkinter.CTkFrame(self, fg_color=Colors.BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # === HEADER ===
        self._build_header(main_frame)
        
        # === DASHBOARD DE ESTADÍSTICAS ===
        self._build_dashboard(main_frame)
        
        # === SEPARADOR ===
        sep = customtkinter.CTkFrame(main_frame, height=2, fg_color=Colors.BORDER_LIGHT)
        sep.pack(fill="x", padx=0, pady=0)
        
        # === CONTENIDO (TABS) ===
        content_frame = customtkinter.CTkFrame(main_frame, fg_color=Colors.BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=Styles.PADDING_LG, pady=Styles.PADDING_LG)
        
        # Crear TabView
        self.tab_view = customtkinter.CTkTabview(
            content_frame, 
            fg_color=Colors.BG_SECONDARY,
            segmented_button_fg_color=Colors.BG_TERTIARY,
            segmented_button_selected_color=Colors.PRIMARY,
            segmented_button_selected_hover_color=Colors.PRIMARY_LIGHT,
            segmented_button_unselected_color=Colors.BG_TERTIARY,
            segmented_button_unselected_hover_color=Colors.BG_LIGHT,
            text_color=Colors.TEXT_PRIMARY,
            text_color_disabled=Colors.TEXT_SECONDARY,
            corner_radius=Styles.CORNER_RADIUS,
            border_width=Styles.BORDER_WIDTH_THIN,
            border_color=Colors.BORDER_LIGHT
        )
        self.tab_view.pack(pady=0, padx=0, fill="both", expand=True)
        
        # Pestaña 1: Préstamos
        self.tab_view.add("📤 Préstamos")
        tab_prestamos = self.tab_view.tab("📤 Préstamos")
        tab_prestamos.configure(fg_color=Colors.BG_SECONDARY)
        self.prestamos_tab = PrestamosTab(tab_prestamos, self.libro_model, self.alumno_model, self.transaccion_model, self)
        
        # Pestaña 2: Libros
        self.tab_view.add("📚 Libros")
        tab_libros = self.tab_view.tab("📚 Libros")
        tab_libros.configure(fg_color=Colors.BG_SECONDARY)
        self.libros_tab = LibrosTab(tab_libros, self.libro_model, self)
        
        # Pestaña 3: Alumnos
        self.tab_view.add("👥 Alumnos")
        tab_alumnos = self.tab_view.tab("👥 Alumnos")
        tab_alumnos.configure(fg_color=Colors.BG_SECONDARY)
        self.alumnos_tab = AlumnosTab(tab_alumnos, self.alumno_model, self)
    
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
                                       text_color=Colors.TEXT_INVERSE,
                                       font=Styles.FONT_TITLE)
        title.pack(side="left", padx=0)
        
        # Subtítulo
        subtitle = customtkinter.CTkLabel(content, text="Centro de Recursos de Aprendizaje",
                                         text_color=Colors.SECONDARY,
                                         font=Styles.FONT_REGULAR)
        subtitle.pack(side="left", padx=Styles.PADDING_LG)
    
    def _build_dashboard(self, parent):
        """Construye el dashboard de estadísticas"""
        dashboard = customtkinter.CTkFrame(parent, fg_color=Colors.BG_DARK, 
                                          corner_radius=0, height=160)
        dashboard.pack(fill="x", padx=0, pady=0)
        dashboard.pack_propagate(False)
        
        # Contenedor de tarjetas
        cards_container = customtkinter.CTkFrame(dashboard, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=Styles.PADDING_XL, pady=Styles.PADDING_LG)
        
        # Obtener estadísticas
        libro_stats = self.libro_model.obtener_estadisticas()
        total_alumnos = self.alumno_model.obtener_total_alumnos()
        prestamos_activos = self.transaccion_model.obtener_total_prestamos_activos()
        
        # Tarjeta 1: Total de Libros
        self._create_stat_card(
            cards_container,
            icon="📚",
            value=str(libro_stats['total_libros']),
            label="Libros Únicos",
            color=Colors.INFO
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 2: Ejemplares Totales
        self._create_stat_card(
            cards_container,
            icon="📖",
            value=str(libro_stats['total_ejemplares']),
            label="Total de Libros",
            color=Colors.SECONDARY
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 3: Disponibles
        self._create_stat_card(
            cards_container,
            icon="✅",
            value=str(libro_stats['disponibles']),
            label="Libros Disponibles",
            color=Colors.SUCCESS
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 4: Prestados
        self._create_stat_card(
            cards_container,
            icon="📤",
            value=str(libro_stats['prestados']),
            label="Libros Prestados",
            color=Colors.WARNING
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 5: Alumnos
        self._create_stat_card(
            cards_container,
            icon="👥",
            value=str(total_alumnos),
            label="Cantidad de Alumnos",
            color=Colors.PRIMARY
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Guardar referencia al dashboard para actualizarlo
        self.dashboard_frame = dashboard
    
    def _create_stat_card(self, parent, icon: str, value: str, label: str, color: str):
        """Crea una tarjeta de estadística - Light Mode"""
        card = customtkinter.CTkFrame(parent, fg_color=Colors.BG_SECONDARY, 
                                     corner_radius=Styles.CORNER_RADIUS,
                                     border_width=Styles.BORDER_WIDTH_THIN,
                                     border_color=Colors.BORDER_LIGHT)
        
        # Frame superior para icono + etiqueta
        top_frame = customtkinter.CTkFrame(card, fg_color="transparent")
        top_frame.pack(pady=(Styles.PADDING_LG, Styles.PADDING_XS), padx=Styles.PADDING_MD)
        
        # Icono (pequeño, al lado del título)
        icon_label = customtkinter.CTkLabel(
            top_frame,
            text=icon,
            font=("Segoe UI", 22),
            text_color=color
        )
        icon_label.pack(side="left", padx=(0, Styles.PADDING_SM))
        
        # Etiqueta (nombre descriptivo)
        label_label = customtkinter.CTkLabel(
            top_frame,
            text=label.upper(),
            font=("Roboto", 10, "bold"),
            text_color=Colors.TEXT_SECONDARY
        )
        label_label.pack(side="left")
        
        # Valor (grande y destacado)
        value_label = customtkinter.CTkLabel(
            card,
            text=value,
            font=("Roboto", 42, "bold"),
            text_color=color
        )
        value_label.pack(pady=(0, Styles.PADDING_LG))
        
        return card
    
    def refresh_dashboard(self):
        """Actualiza las estadísticas del dashboard"""
        # Destruir dashboard existente
        if hasattr(self, 'dashboard_frame'):
            self.dashboard_frame.destroy()
        
        # Encontrar el main_frame
        main_frame = self.winfo_children()[0]
        
        # Reconstruir dashboard
        dashboard = customtkinter.CTkFrame(main_frame, fg_color=Colors.BG_DARK, 
                                          corner_radius=0, height=160)
        # Insertar después del header (posición 1)
        dashboard.pack(fill="x", padx=0, pady=0, after=main_frame.winfo_children()[0])
        dashboard.pack_propagate(False)
        
        # Contenedor de tarjetas
        cards_container = customtkinter.CTkFrame(dashboard, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=Styles.PADDING_XL, pady=Styles.PADDING_LG)
        
        # Obtener estadísticas actualizadas
        libro_stats = self.libro_model.obtener_estadisticas()
        total_alumnos = self.alumno_model.obtener_total_alumnos()
        prestamos_activos = self.transaccion_model.obtener_total_prestamos_activos()
        
        # Tarjeta 1: Total de Libros
        self._create_stat_card(
            cards_container,
            icon="📚",
            value=str(libro_stats['total_libros']),
            label="Libros Únicos",
            color=Colors.INFO
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 2: Ejemplares Totales
        self._create_stat_card(
            cards_container,
            icon="📖",
            value=str(libro_stats['total_ejemplares']),
            label="Total de Libros",
            color=Colors.SECONDARY
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 3: Disponibles
        self._create_stat_card(
            cards_container,
            icon="✅",
            value=str(libro_stats['disponibles']),
            label="Libros Disponibles",
            color=Colors.SUCCESS
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 4: Prestados
        self._create_stat_card(
            cards_container,
            icon="📤",
            value=str(libro_stats['prestados']),
            label="Libros Prestados",
            color=Colors.WARNING
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Tarjeta 5: Alumnos
        self._create_stat_card(
            cards_container,
            icon="👥",
            value=str(total_alumnos),
            label="Cantidad de Alumnos",
            color=Colors.PRIMARY
        ).pack(side="left", fill="both", expand=True, padx=Styles.PADDING_SM)
        
        # Guardar referencia al dashboard
        self.dashboard_frame = dashboard

