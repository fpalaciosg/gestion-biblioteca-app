# 📚 Sistema de Gestión de Biblioteca (CRA)

Este es un software de escritorio desarrollado en Python con CustomTkinter y SQLite, diseñado para gestionar el inventario de libros, préstamos y alumnos de la biblioteca CRA de una escuela.

## 🌟 Mejoras de Calidad y Robustez

Esta versión incluye mejoras clave de rendimiento y experiencia de usuario:

* **Optimización de Rendimiento:** La búsqueda ahora utiliza una **Vista Inteligente**. Al presionar "Buscar" con el campo vacío, solo se muestran los ítems con préstamos activos, lo cual asegura que el programa sea instantáneo incluso con miles de registros.
* **CRUD Completo:** Implementación de la edición de datos para Libros y Alumnos.
* **Búsqueda Flexible:** Los campos de RUT en Préstamos y Búsqueda ahora ignoran puntos y guiones, lo que facilita la vida del usuario.
* **UX:** Implementación de placeholders (texto de ejemplo) y diseño moderno en la pestaña de Préstamos.

## 🚀 Características Principales

* **Gestión de Inventario:** Permite agregar, editar y eliminar libros de la base de datos.
* **Control de Préstamos:** Registro de salida y devolución de libros.
* **Base de Datos Local:** Utiliza **SQLite** para un almacenamiento ligero y eficiente sin necesidad de servidores complejos.
* **Interfaz Intuitiva:** Diseñada pensando en la facilidad de uso para el personal bibliotecario.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Base de Datos:** SQLite
* **Entorno de Desarrollo:** Visual Studio Code
* **Control de Versiones:** Git & GitHub

## 📋 Requisitos Previos

Para ejecutar este sistema, necesitas tener instalado:
* Python 3.x

## 🚀 Puesta en Marcha (Importación de Alumnos)

Este proyecto incluye un script de ayuda llamado `importar_alumnos.py`. Su única función es leer un archivo de Excel y cargar masivamente a todos los alumnos en la base de datos, para no tener que registrarlos uno por uno.

**Importante:** Este script está diseñado para ejecutarse **una sola vez** al configurar el programa por primera vez.

### Requisitos

1.  Tener Python instalado.
2.  Tener el archivo de Excel con los datos de los alumnos.

### 📖 Instrucciones Paso a Paso

1.  **Instalar Librerías:**
    Antes de ejecutar cualquier script, necesitas instalar las dependencias. Abre una terminal en la carpeta del proyecto y ejecuta:
    ```bash
    pip install pandas openpyxl customtkinter
    ```

2.  **Preparar el Archivo de Excel:**
    * Toma tu lista de alumnos y asegúrate de que el archivo tenga **exactamente** estas tres columnas: `RUT`, `Nombre`, `Curso`.
    * El orden de las columnas no importa, pero los nombres de las cabeceras deben ser exactos.
    * Guarda este archivo en la **misma carpeta** del proyecto con el nombre: `alumnos.xlsx`.

3.  **Ejecutar el Script de Importación:**
    En la misma terminal, ejecuta **solo** el script de importación (NO el programa principal):
    ```bash
    python importar_alumnos.py
    ```
    * La terminal te mostrará un resumen de cuántos alumnos se importaron y cuántos se omitieron (porque el RUT ya existía).

4.  **¡Listo!**
    * El script habrá poblado el archivo `inventario.db` (que se crea automáticamente si no existe).
    * Ahora puedes borrar o mover tu archivo `alumnos.xlsx` por seguridad.

5.  **Ejecutar el Programa Principal:**
    Ahora sí, ejecuta el sistema de inventario:
    ```bash
    python sistema_biblioteca.py
    ```
    * Ve a la pestaña "Alumnos" y presiona "Buscar" (con el campo vacío) para ver los alumnos con préstamos, o busca por nombre para ver a todos los que importaste.

## 📸 Galería

### 🤝 Control de Préstamos
![Vista del sistema de préstamos](img/Prestamos.png)


### 📚 Catálogo de Libros
![Vista del inventario de libros](img/Libros.png)

### 👥 Gestión de Alumnos
![Vista del módulo/ventana de alumnos](img/Alumnos.png)

## 🔧 Instalación y Uso

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/fpalaciosg/gestion-biblioteca-app.git](https://github.com/fpalaciosg/gestion-biblioteca-app.git)
    ```
2.  Navega a la carpeta del proyecto:
    ```bash
    cd gestion-biblioteca-app
    ```
3.  Ejecuta el programa principal:
    ```bash
    python sistema_biblioteca.py
    ```

---
Desarrollado por **Francisco J. Palacios González** - *Estudiante de Analista Programador*