# Guía de Importación de Alumnos

## 📥 Importar desde Excel

### Requisitos previos
Instalar la librería pandas:
```bash
pip install pandas openpyxl
```

### Formato del archivo Excel

Tu archivo Excel debe tener **exactamente** estas 3 columnas (en cualquier orden):
- **RUT**: RUT del alumno (puede ser con o sin puntos/guión)
- **NOMBRE**: Nombre completo del alumno
- **CURSO**: Curso al que pertenece

**Ejemplo:**

| RUT | NOMBRE | CURSO |
|-----|--------|-------|
| 12345678-9 | Juan Pérez García | 1° Medio A |
| 98765432-1 | María González López | 2° Medio B |
| 11223344-5 | Pedro Martínez Silva | 3° Medio C |

### Pasos para importar

1. Ve a la pestaña **👥 Alumnos**
2. Haz clic en el botón **📥 Importar**
3. Selecciona tu archivo Excel (.xlsx o .xls)
4. El sistema validará las columnas y mostrará un resumen de la importación

**Nota:** Los RUTs duplicados serán omitidos automáticamente.

---

## 📥 Importar desde SQLite

### Formato de la base de datos

Tu base de datos SQLite debe tener **al menos una tabla** con estas columnas:
- **RUT**
- **NOMBRE**
- **CURSO**

La tabla puede tener otros campos adicionales, pero estos 3 son obligatorios.

### Pasos para importar

1. Ve a la pestaña **👥 Alumnos**
2. Haz clic en el botón **📥 Importar**
3. Selecciona tu archivo de base de datos (.db, .sqlite o .sqlite3)
4. El sistema buscará automáticamente la tabla con las columnas correctas
5. Se importarán todos los registros válidos

**Nota:** Los RUTs duplicados serán omitidos automáticamente.

---

## ✅ Resultado de la importación

Al finalizar, verás un mensaje con:
- ✓ Alumnos importados correctamente
- Duplicados omitidos
- Errores en filas inválidas (si las hay)

Los nuevos alumnos aparecerán inmediatamente en la lista y el dashboard se actualizará automáticamente.

---

## 📝 Archivo de plantilla

Incluimos un archivo `plantilla_alumnos.csv` que puedes usar como referencia para crear tu propio archivo Excel.

---

## ⚠️ Solución de problemas

### Error: "Librería no disponible"
Si aparece este error al importar Excel, instala pandas:
```bash
pip install pandas openpyxl
```

### Error: "Columnas faltantes"
Verifica que tu archivo tenga exactamente las columnas: **RUT**, **NOMBRE** y **CURSO** (en mayúsculas o minúsculas, no importa).

### Error: "Estructura inválida" (SQLite)
Tu base de datos SQLite no tiene ninguna tabla con las columnas requeridas. Verifica que al menos una tabla contenga RUT, NOMBRE y CURSO.
