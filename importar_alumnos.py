import pandas as pd
import sqlite3
import os

# --- CONFIGURACIÓN ---
# 1. El nombre de tu archivo de Excel (ponlo en la misma carpeta)
RUTA_EXCEL = "alumnos.xlsx" 

# 2. El nombre de tu base de datos
DATABASE_NAME = "inventario.db"
# ---------------------

def importar_datos():
    print(f"Iniciando importación desde '{RUTA_EXCEL}'...")

    # 1. Verificar que el Excel exista
    if not os.path.exists(RUTA_EXCEL):
        print(f"Error: No se encontró el archivo '{RUTA_EXCEL}' en la carpeta.")
        print("Asegúrate de que el archivo esté en la misma carpeta que este script.")
        return

    # 2. Leer el Excel usando Pandas
    try:
        # Leemos el archivo, especificando que los datos son de tipo 'str' (texto)
        # para que no se coman los ceros del RUT o el guion.
        df = pd.read_excel(RUTA_EXCEL, dtype=str)
        
        # Llenar valores vacíos (NaN) con un string vacío
        df = df.fillna("")

        # 3. Verificar columnas necesarias
        columnas_necesarias = ['RUT', 'Nombre', 'Curso']
        if not all(col in df.columns for col in columnas_necesarias):
            print("Error: El archivo de Excel NO tiene las columnas correctas.")
            print(f"Asegúrate de que las cabeceras sean: {columnas_necesarias}")
            return
            
        print(f"Se encontraron {len(df)} alumnos en el Excel.")

    except Exception as e:
        print(f"Error leyendo el archivo de Excel: {e}")
        return

    # 4. Conectar a la Base de Datos SQLite
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        registros_importados = 0
        registros_omitidos = 0

        # 5. Insertar los datos (fila por fila)
        for index, fila in df.iterrows():
            try:
                # INSERT OR IGNORE:
                # Intenta insertar. Si falla (ej: RUT duplicado), simplemente lo ignora
                # y sigue con la siguiente fila, sin detener el script.
                cursor.execute("""
                    INSERT OR IGNORE INTO Prestatarios (RUT, Nombre, Curso) 
                    VALUES (?, ?, ?)
                """, (fila['RUT'], fila['Nombre'], fila['Curso']))
                
                # 'rowcount' nos dice si la inserción fue exitosa (1) o ignorada (0)
                if cursor.rowcount > 0:
                    registros_importados += 1
                else:
                    registros_omitidos += 1
                    
            except sqlite3.Error as e:
                print(f"Error insertando fila {index}: {e}")

        # 6. Guardar cambios (Commit)
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