"""
Configuración global de la aplicación
"""
import os
import sys
from pathlib import Path
from .theme import Colors, Styles

# Configuración de apariencia
APPEARANCE_MODE = "dark"  # dark, light, system
COLOR_THEME = "blue"  # CustomTkinter theme (fallback)

# Rutas
if getattr(sys, 'frozen', False):
    APPLICATION_PATH = os.path.dirname(sys.executable)
else:
    APPLICATION_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(APPLICATION_PATH, "inventario.db")
EXCEL_IMPORT_PATH = os.path.join(APPLICATION_PATH, "alumnos.xlsx")

# Nombres de tablas
TABLE_LIBROS = "Libros"
TABLE_PRESTATARIOS = "Prestatarios"
TABLE_TRANSACCIONES = "Transacciones"

# Configuración de UI
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Sistema de Inventario CRA"
