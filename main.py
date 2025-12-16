"""
Sistema de Inventario CRA - Punto de Entrada
Aplicación de gestión de biblioteca para escuelas
"""
import customtkinter
from database.conexion import DatabaseConnection
from database.modelos import DatabaseModels
from ui.main_window import MainWindow
from utils.config import (
    DATABASE_PATH, APPEARANCE_MODE, COLOR_THEME, WINDOW_TITLE
)


def main():
    """Función principal que inicia la aplicación"""
    
    # Configurar apariencia
    customtkinter.set_appearance_mode(APPEARANCE_MODE)
    customtkinter.set_default_color_theme(COLOR_THEME)
    
    # Inicializar base de datos
    db_connection = DatabaseConnection(DATABASE_PATH)
    db_models = DatabaseModels(db_connection)
    
    # Crear ventana principal
    app = MainWindow(db_connection, db_models)
    
    # Ejecutar
    app.mainloop()


if __name__ == "__main__":
    main()
