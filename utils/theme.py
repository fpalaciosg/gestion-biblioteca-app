"""
Tema y Paleta de Colores - Dark Mode Moderno
"""

class Colors:
    """Paleta de colores Dark Mode - Elegante y Profesional"""
    
    # === COLORES PRIMARIOS ===
    PRIMARY = "#2E7D9A"          # Azul cyan profesional
    PRIMARY_LIGHT = "#3B9BB8"    # Variante más clara
    PRIMARY_DARK = "#1F5569"     # Variante más oscura
    
    # === COLORES SECUNDARIOS ===
    SECONDARY = "#E8A75D"        # Naranja cálido
    SECONDARY_LIGHT = "#F5B041"  # Variante clara
    SECONDARY_DARK = "#D68910"   # Variante oscura
    
    # === COLORES DE ESTADO ===
    SUCCESS = "#2ECC71"          # Verde éxito
    SUCCESS_LIGHT = "#58D68D"    # Verde más claro
    WARNING = "#F39C12"          # Naranja advertencia
    DANGER = "#E74C3C"           # Rojo peligro
    INFO = "#3498DB"             # Azul información
    
    # === COLORES DE FONDO (DARK MODE) ===
    BG_DARK = "#1E1E2E"          # Fondo principal oscuro
    BG_SECONDARY = "#2A2A3E"     # Tarjetas/contenedores
    BG_TERTIARY = "#363654"      # Fondo de inputs
    BG_LIGHT = "#424263"         # Hover state
    
    # === COLORES DE TEXTO (DARK MODE) ===
    TEXT_PRIMARY = "#F8F8F2"     # Texto principal (casi blanco)
    TEXT_SECONDARY = "#A8A8B8"   # Texto secundario (gris claro)
    TEXT_TERTIARY = "#6E6E7E"    # Texto terciario (gris medio)
    TEXT_INVERSE = "#1E1E2E"     # Texto inverso (oscuro sobre claro)
    
    # === BORDES ===
    BORDER_LIGHT = "#3A3A4E"     # Borde sutil
    BORDER_DARK = "#4A4A5E"      # Borde medio
    BORDER_ACCENT = "#2E7D9A"    # Borde acentuado
    
    # === ESPECIALES ===
    ACCENT = "#E8A75D"           # Naranja acento
    OVERLAY = "rgba(0,0,0,0.3)"  # Overlay oscuro


class Styles:
    """Estilos y constantes de UI - Light Mode Educativo"""
    
    # Bordes redondeados (según especificación)
    CORNER_RADIUS = 15           # Para CTkFrame (tarjetas, dashboard)
    CORNER_RADIUS_SMALL = 8      # Para CTkButton y CTkEntry
    CORNER_RADIUS_LARGE = 20     # Para contenedores grandes
    CORNER_RADIUS_BUTTON = 8     # Botones (explícito)
    
    # Padding y spacing
    PADDING_XS = 6
    PADDING_SM = 10
    PADDING_MD = 15
    PADDING_LG = 20
    PADDING_XL = 25
    PADDING_XXL = 30
    
    # Tamaños de fuente (tipografía limpia)
    FONT_SIZE_SM = 11
    FONT_SIZE_MD = 12
    FONT_SIZE_LG = 14
    FONT_SIZE_XL = 16
    FONT_SIZE_XXL = 20
    
    # Fuentes (Roboto para diseño educativo)
    FONT_REGULAR = ("Roboto", 12)
    FONT_BOLD = ("Roboto", 12, "bold")
    FONT_BUTTON = ("Roboto Medium", 14)
    FONT_TITLE = ("Roboto", 20, "bold")
    FONT_HEADER = ("Roboto Medium", 16, "bold")
    FONT_MONO = ("Consolas", 11)
    
    # Alturas de botones
    BUTTON_HEIGHT_SM = 32
    BUTTON_HEIGHT_MD = 40
    BUTTON_HEIGHT_LG = 48
    
    # Anchos de borde
    BORDER_WIDTH_THIN = 1
    BORDER_WIDTH_MEDIUM = 2
    BORDER_WIDTH_THICK = 3


class ThemeConfig:
    """Configuración centralizada del tema"""
    
    @staticmethod
    def get_tab_color(tab_name: str) -> str:
        """Retorna el color primario para una pestaña"""
        tab_colors = {
            "Préstamos": Colors.SECONDARY,
            "Libros": Colors.PRIMARY,
            "Alumnos": Colors.INFO,
        }
        return tab_colors.get(tab_name, Colors.PRIMARY)
    
    @staticmethod
    def get_action_color(action: str) -> str:
        """Retorna el color para un tipo de acción"""
        action_colors = {
            "create": Colors.SECONDARY,
            "edit": Colors.PRIMARY,
            "delete": Colors.DANGER,
            "info": Colors.INFO,
            "success": Colors.SUCCESS,
            "warning": Colors.WARNING,
        }
        return action_colors.get(action, Colors.PRIMARY)
