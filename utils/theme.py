"""
Tema y Paleta de Colores - Define la identidad visual de la aplicación
Sistema de Colores Moderno y Cohesivo
"""

class Colors:
    """Paleta de colores para la aplicación"""
    
    # === COLORES PRIMARIOS ===
    PRIMARY = "#2E7D9A"          # Azul moderno y elegante
    PRIMARY_LIGHT = "#3B9DC4"    # Variante clara
    PRIMARY_DARK = "#1E5A75"     # Variante oscura
    
    # === COLORES SECUNDARIOS ===
    SECONDARY = "#00C9A7"        # Verde/Teal vibrante
    SECONDARY_LIGHT = "#1FD9B8"  # Variante clara
    SECONDARY_DARK = "#009B87"   # Variante oscura
    
    # === COLORES DE ESTADO ===
    SUCCESS = "#06A77D"          # Verde éxito
    WARNING = "#F77F00"          # Naranja alerta
    DANGER = "#D62828"           # Rojo error
    INFO = "#2E7D9A"             # Azul información
    
    # === COLORES DE FONDO ===
    BG_DARK = "#1E1E2E"          # Fondo principal oscuro
    BG_SECONDARY = "#2A2A3E"     # Fondo secundario
    BG_TERTIARY = "#323244"      # Fondo terciario
    BG_LIGHT = "#44475A"         # Fondo claro (hover)
    
    # === COLORES DE TEXTO ===
    TEXT_PRIMARY = "#F8F8F2"     # Texto principal blanco
    TEXT_SECONDARY = "#D5D5D5"   # Texto secundario gris claro
    TEXT_TERTIARY = "#A8A8A8"    # Texto terciario gris oscuro
    TEXT_INVERSE = "#1E1E2E"     # Texto inverso (sobre fondos claros)
    
    # === BORDES ===
    BORDER_LIGHT = "#44475A"     # Borde claro
    BORDER_DARK = "#2A2A3E"      # Borde oscuro
    BORDER_ACCENT = "#2E7D9A"    # Borde acentuado
    
    # === ESPECIALES ===
    ACCENT = "#00D9FF"           # Cyan acentuado
    OVERLAY = "rgba(0,0,0,0.5)"  # Overlay oscuro


class Styles:
    """Estilos y constantes de UI"""
    
    # Bordes redondeados
    CORNER_RADIUS = 12
    CORNER_RADIUS_SMALL = 8
    CORNER_RADIUS_LARGE = 16
    
    # Padding y spacing
    PADDING_XS = 4
    PADDING_SM = 8
    PADDING_MD = 12
    PADDING_LG = 16
    PADDING_XL = 20
    
    # Tamaños de fuente
    FONT_SIZE_SM = 11
    FONT_SIZE_MD = 13
    FONT_SIZE_LG = 16
    FONT_SIZE_XL = 18
    FONT_SIZE_XXL = 22
    
    # Fuentes
    FONT_REGULAR = ("Segoe UI", FONT_SIZE_MD)
    FONT_BOLD = ("Segoe UI", FONT_SIZE_MD, "bold")
    FONT_TITLE = ("Segoe UI", FONT_SIZE_XL, "bold")
    FONT_HEADER = ("Segoe UI", FONT_SIZE_LG, "bold")
    FONT_MONO = ("Consolas", FONT_SIZE_SM)
    
    # Alturas de botones
    BUTTON_HEIGHT_SM = 32
    BUTTON_HEIGHT_MD = 40
    BUTTON_HEIGHT_LG = 48


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
