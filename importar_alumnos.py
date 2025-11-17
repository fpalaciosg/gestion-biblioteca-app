import pandas as pd
import sqlite3
import os

# --- CONFIGURACIÓN ---
RUTA_EXCEL = "alumnos.xlsx" 

# 2. El nombre de tu base de datos
DATABASE_NAME = "inventario.db"

def importar_datos():
    print(f"Iniciando importación desde '{RUTA_EXCEL}'...")

    # 1. Verificar que el Excel exista
    if not os.path.exists(RUTA_EXCEL):
        print(f"Error: No se encontró el archivo '{RUTA_EXCEL}' en la carpeta.")
        print("Asegúrate de que el archivo esté en la misma carpeta que este script.")
        return

    # 2. Leer el Excel usando Pandas
    try:
        df = pd.read_excel(RUTA_EXCEL, dtype=str)
        df = df.fillna("")
        columnas_necesarias = ['RUT', 'Nombre', 'Curso']
        if not all(col in df.columns for col in columnas_necesarias):
            print("Error: El archivo de Excel NO tiene las columnas correctas.")
            print(f"Asegúrate de que las cabeceras sean: {columnas_necesarias}")
            return
            
        print(f"Se encontraron {len(df)} alumnos en el Excel.")

    except Exception as e:
        print(f"Error leyendo el archivo de Excel: {e}")
        return

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        registros_importados = 0
        registros_omitidos = 0

        for index, fila in df.iterrows():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO Prestatarios (RUT, Nombre, Curso) 
                    VALUES (?, ?, ?)
                """, (fila['RUT'], fila['Nombre'], fila['Curso']))
                
                if cursor.rowcount > 0:
                    registros_importados += 1
                else:
                    registros_omitidos += 1
                    
            except sqlite3.Error as e:
                print(f"Error insertando fila {index}: {e}")

        conn.commit()
        conn.close()

        print("\n--- ¡Importación Completa! ---")
        print(f"✅ Alumnos nuevos importados: {registros_importados}")
        print(f"🚫 Alumnos omitidos (RUT duplicado): {registros_omitidos}")

    except Exception as e:
        print(f"Error conectando o insertando en la base de datos: {e}")


# --- Punto de entrada ---
if __name__ == "__main__":
    importar_datos()