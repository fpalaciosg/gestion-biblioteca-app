"""
Import Excel - Funciones para importar alumnos desde archivos Excel
"""
import os
from typing import Tuple
import pandas as pd
from database.conexion import DatabaseConnection


def importar_alumnos_desde_excel(archivo_path: str, db_connection: DatabaseConnection) -> Tuple[int, int]:
    """
    Importa alumnos desde un archivo Excel
    
    Args:
        archivo_path: Ruta al archivo .xlsx
        db_connection: Conexión a la base de datos
    
    Returns:
        Tupla (registros_importados, registros_omitidos)
    """
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo_path):
        raise FileNotFoundError(f"No se encontró el archivo '{archivo_path}'")
    
    # Leer Excel
    try:
        df = pd.read_excel(archivo_path, dtype=str)
        df = df.fillna("")
    except Exception as e:
        raise Exception(f"Error leyendo el archivo de Excel: {e}")
    
    # Verificar columnas
    columnas_necesarias = ['RUT', 'Nombre', 'Curso']
    if not all(col in df.columns for col in columnas_necesarias):
        raise Exception(f"El archivo debe tener las columnas: {columnas_necesarias}")
    
    # Importar registros
    registros_importados = 0
    registros_omitidos = 0
    
    query = "INSERT OR IGNORE INTO Prestatarios (RUT, Nombre, Curso) VALUES (?, ?, ?)"
    
    for index, row in df.iterrows():
        try:
            db_connection.ejecutar(
                query,
                (row['RUT'], row['Nombre'], row['Curso'])
            )
            registros_importados += 1
        except Exception as e:
            print(f"Error importando fila {index}: {e}")
            registros_omitidos += 1
    
    return registros_importados, registros_omitidos
