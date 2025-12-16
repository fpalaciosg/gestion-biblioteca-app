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
    Asegúrate de que el archivo `alumnos.xlsx` esté en la carpeta y luego ejecuta:
    ```bash
    python importar_alumnos.py
    ```
    * El script leerá automáticamente el archivo llamado `alumnos.xlsx`.

4.  **¡Listo!**
    * El script habrá poblado el archivo `inventario.db`.
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

## � Estructura del Proyecto (v2.0 - Refactorizada)

```
ProyectoCRA/
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias
├── importar_alumnos.py       # Script para importación desde Excel
├── sistema_biblioteca.py     # [LEGACY] Código anterior sin refactorizar
├── inventario.db             # Base de datos SQLite
├── README.md
├── img/                       # Screenshots
│
├── database/                  # Capa de Datos
│   ├── conexion.py           # Conexiones a BD
│   └── modelos.py            # Esquema de tablas
│
├── models/                    # Capa de Lógica (Modelos)
│   ├── libro.py              # Operaciones con Libros
│   ├── alumno.py             # Operaciones con Alumnos
│   └── transaccion.py        # Operaciones con Préstamos
│
├── ui/                        # Capa de Presentación
│   ├── main_window.py        # Ventana principal
│   ├── tabs/                 # Pestañas
│   │   ├── prestamos_tab.py
│   │   ├── libros_tab.py
│   │   └── alumnos_tab.py
│   └── dialogs/              # Diálogos emergentes
│       └── dialogs.py
│
└── utils/                     # Utilidades
    ├── config.py             # Configuración global
    ├── validators.py         # Validación de datos
    └── import_excel.py       # Importación desde Excel
```

## 🏗️ Arquitectura MVC (Model-View-Controller)

La aplicación ha sido refactorizada siguiendo el patrón **MVC**, separando responsabilidades:

- **Models** (`models/`): Contiene la lógica de negocio (CRUD, consultas)
- **Views** (`ui/`): Interfaz gráfica (ventanas, diálogos, pestañas)
- **Controller** (`main.py`): Orquestador que conecta modelos con vistas
- **Database** (`database/`): Capa de persistencia de datos

**Beneficios:**
✅ Código más mantenible y escalable  
✅ Fácil agregar nuevas funcionalidades  
✅ Posibilidad de hacer tests unitarios  
✅ Separación clara de responsabilidades

## 🔧 Instalación y Uso

1.  Clona el repositorio:
    ```bash
    git clone https://github.com/fpalaciosg/gestion-biblioteca-app.git
    cd gestion-biblioteca-app
    ```

2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3.  Ejecuta el programa principal:
    ```bash
    python main.py
    ```

---
Desarrollado por **Francisco J. Palacios González** - *Estudiante de Analista Programador*