import sqlite3
import customtkinter
from tkinter import messagebox
from datetime import datetime

# --- Configuración de Apariencia ---
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

DATABASE_NAME = "inventario.db"

# --- Funciones de Base de Datos (IGUAL) ---
def conectar_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def inicializar_db():
    conn = conectar_db()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Libros (
            ID_Libro INTEGER PRIMARY KEY AUTOINCREMENT,
            ISBN TEXT UNIQUE, Título TEXT NOT NULL, Autor TEXT NOT NULL,
            Editorial TEXT, Año_Publicacion INTEGER, Categoría TEXT,
            Total_Ejemplares INTEGER NOT NULL, Disponibles INTEGER NOT NULL,
            Fecha_Ingreso_Donacion TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prestatarios (
            ID_Prestatario INTEGER PRIMARY KEY AUTOINCREMENT,
            RUT TEXT UNIQUE NOT NULL,
            Nombre TEXT NOT NULL,
            Curso TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transacciones (
            ID_Transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Libro INTEGER NOT NULL, ID_Prestatario INTEGER NOT NULL,
            Fecha_Entrega TEXT NOT NULL, Fecha_Devolucion_Estimada TEXT,
            Fecha_Devolucion_Real TEXT NULL, Estado TEXT NOT NULL,
            FOREIGN KEY (ID_Libro) REFERENCES Libros(ID_Libro) ON DELETE CASCADE,
            FOREIGN KEY (ID_Prestatario) REFERENCES Prestatarios(ID_Prestatario) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()

# --- VENTANAS EMERGENTES (IGUAL) ---
# (Clases VentanaNuevoLibro, VentanaEditarLibro, VentanaNuevoPrestatario,
# VentanaEditarPrestatario y VentanaDetalleLibros son idénticas a la V18)

class VentanaNuevoLibro(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Registrar Nuevo Libro / Stock")
        self.geometry("500x550")
        self.transient(master); self.grab_set(); self.lift()
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1) 
        campos = ["Título:", "Autor:", "ISBN:", "Editorial:", "Año Publicación:", "Categoría:", "Nº Ejemplares (a sumar):"]
        self.entries = {}
        for i, label_text in enumerate(campos):
            customtkinter.CTkLabel(self.frame, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = customtkinter.CTkEntry(self.frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.entries[label_text] = entry
        customtkinter.CTkButton(self.frame, text="Guardar", command=self.guardar).grid(row=8, column=0, columnspan=2, pady=20)

    def guardar(self):
        datos = {k: v.get() for k, v in self.entries.items()}
        isbn = datos["ISBN:"]
        if not isbn: return messagebox.showerror("Error", "ISBN obligatorio.", parent=self)
        try:
            ejemplares = int(datos["Nº Ejemplares (a sumar):"])
            if ejemplares <= 0: raise ValueError
        except: return messagebox.showerror("Error", "Ejemplares debe ser número positivo.", parent=self)
        conn = conectar_db(); c = conn.cursor()
        try:
            c.execute("SELECT ID_Libro FROM Libros WHERE ISBN = ?", (isbn,))
            if c.fetchone():
                if messagebox.askyesno("Stock", f"ISBN existente. ¿Sumar {ejemplares} copias?", parent=self):
                    c.execute("UPDATE Libros SET Total_Ejemplares=Total_Ejemplares+?, Disponibles=Disponibles+? WHERE ISBN=?", (ejemplares, ejemplares, isbn))
                    conn.commit(); messagebox.showinfo("Ok", "Stock sumado.", parent=self); self.destroy()
            else:
                if not datos["Título:"] or not datos["Autor:"]: return messagebox.showerror("Error", "Título y Autor obligatorios.", parent=self)
                c.execute("INSERT INTO Libros (ISBN, Título, Autor, Editorial, Año_Publicacion, Categoría, Total_Ejemplares, Disponibles, Fecha_Ingreso_Donacion) VALUES (?,?,?,?,?,?,?,?,?)",
                          (isbn, datos["Título:"], datos["Autor:"], datos["Editorial:"], datos["Año Publicación:"], datos["Categoría:"], ejemplares, ejemplares, datetime.now().strftime("%Y-%m-%d")))
                conn.commit(); messagebox.showinfo("Ok", "Libro creado.", parent=self); self.destroy()
        except Exception as e: messagebox.showerror("Error", str(e), parent=self)
        finally: conn.close()

class VentanaEditarLibro(customtkinter.CTkToplevel):
    def __init__(self, master, id_libro, datos_actuales, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Editar Datos del Libro")
        self.geometry("500x500")
        self.transient(master); self.grab_set()
        self.id_libro = id_libro
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1)
        self.campos = ["ISBN", "Título", "Autor", "Editorial", "Año_Publicacion", "Categoría"]
        self.entries = {}
        for i, campo in enumerate(self.campos):
            customtkinter.CTkLabel(self.frame, text=campo + ":").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = customtkinter.CTkEntry(self.frame); entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            entry.insert(0, str(datos_actuales[i])); self.entries[campo] = entry
        customtkinter.CTkButton(self.frame, text="Guardar Cambios", command=self.guardar_cambios).grid(row=6, column=0, columnspan=2, pady=20)

    def guardar_cambios(self):
        nuevos_datos = [self.entries[c].get() for c in self.campos]
        if not nuevos_datos[0] or not nuevos_datos[1]: return messagebox.showerror("Error", "ISBN y Título obligatorios.", parent=self)
        conn = conectar_db()
        try:
            conn.execute("UPDATE Libros SET ISBN=?, Título=?, Autor=?, Editorial=?, Año_Publicacion=?, Categoría=? WHERE ID_Libro=?", (*nuevos_datos, self.id_libro))
            conn.commit(); messagebox.showinfo("Éxito", "Actualizado.", parent=self); self.destroy()
        except: messagebox.showerror("Error", "Error al actualizar (quizás ISBN duplicado).", parent=self)
        finally: conn.close()

class VentanaNuevoPrestatario(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Registrar Alumno")
        self.geometry("400x250")
        self.transient(master); self.grab_set(); self.lift()
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1) 
        self.lbl_rut = customtkinter.CTkLabel(self.frame, text="RUT:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_rut = customtkinter.CTkEntry(self.frame, placeholder_text="12.345.678-9"); self.entry_rut.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        self.lbl_nom = customtkinter.CTkLabel(self.frame, text="Nombre:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_nom = customtkinter.CTkEntry(self.frame, placeholder_text="Francisco Palacios González"); self.entry_nom.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        self.lbl_curso = customtkinter.CTkLabel(self.frame, text="Curso:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_curso = customtkinter.CTkEntry(self.frame, placeholder_text="2°B"); self.entry_curso.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        customtkinter.CTkButton(self.frame, text="Guardar", command=self.guardar).grid(row=3, column=0, columnspan=2, pady=20)

    def guardar(self):
        rut, nom, curso = self.entry_rut.get(), self.entry_nom.get(), self.entry_curso.get()
        if not rut or not nom: return messagebox.showerror("Error", "RUT y Nombre obligatorios.", parent=self)
        conn = conectar_db()
        try:
            conn.execute("INSERT INTO Prestatarios (RUT, Nombre, Curso) VALUES (?, ?, ?)", (rut, nom, curso))
            conn.commit(); messagebox.showinfo("Éxito", "Alumno registrado.", parent=self); self.destroy()
        except: messagebox.showerror("Error", "RUT ya existe.", parent=self)
        finally: conn.close()

class VentanaEditarPrestatario(customtkinter.CTkToplevel):
    def __init__(self, master, id_prestatario, datos_actuales, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Editar Alumno")
        self.geometry("400x250")
        self.transient(master); self.grab_set()
        self.id_prestatario = id_prestatario
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(self.frame, text="RUT:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_rut = customtkinter.CTkEntry(self.frame); self.entry_rut.grid(row=0, column=1, sticky="ew", padx=10, pady=5); self.entry_rut.insert(0, datos_actuales[0])
        customtkinter.CTkLabel(self.frame, text="Nombre:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_nom = customtkinter.CTkEntry(self.frame); self.entry_nom.grid(row=1, column=1, sticky="ew", padx=10, pady=5); self.entry_nom.insert(0, datos_actuales[1])
        customtkinter.CTkLabel(self.frame, text="Curso:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_curso = customtkinter.CTkEntry(self.frame); self.entry_curso.grid(row=2, column=1, sticky="ew", padx=10, pady=5); self.entry_curso.insert(0, datos_actuales[2])
        customtkinter.CTkButton(self.frame, text="Guardar Cambios", command=self.guardar).grid(row=3, column=0, columnspan=2, pady=20)

    def guardar(self):
        rut, nom, curso = self.entry_rut.get(), self.entry_nom.get(), self.entry_curso.get()
        if not rut or not nom: return messagebox.showerror("Error", "Datos obligatorios.", parent=self)
        conn = conectar_db()
        try:
            conn.execute("UPDATE Prestatarios SET RUT=?, Nombre=?, Curso=? WHERE ID_Prestatario=?", (rut, nom, curso, self.id_prestatario))
            conn.commit(); messagebox.showinfo("Éxito", "Actualizado.", parent=self); self.destroy()
        except: messagebox.showerror("Error", "Error al actualizar.", parent=self)
        finally: conn.close()

class VentanaDetalleLibros(customtkinter.CTkToplevel):
    def __init__(self, master, id_prestatario, nombre_alumno, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title(f"Libros en poder de: {nombre_alumno}")
        self.geometry("600x400")
        self.transient(master)
        self.textbox = customtkinter.CTkTextbox(self, font=("Consolas", 12))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.cargar_libros(id_prestatario)
        
    def cargar_libros(self, pid):
        conn = conectar_db(); c = conn.cursor()
        try:
            c.execute("SELECT l.ISBN, l.Título, l.Autor, t.Fecha_Entrega FROM Transacciones t JOIN Libros l ON t.ID_Libro = l.ID_Libro WHERE t.ID_Prestatario = ? AND t.Estado = 'Prestado'", (pid,))
            rows = c.fetchall()
            if not rows: self.textbox.insert("1.0", "Este alumno no tiene libros pendientes.")
            else:
                self.textbox.insert("1.0", f"{'ISBN':<15} | {'TÍTULO':<35} | {'FECHA'}\n" + ("-"*70) + "\n")
                for r in rows: self.textbox.insert("end", f"{r[0]:<15} | {(r[1][:32]+'..') if len(r[1])>35 else r[1]:<35} | {r[3]}\n")
            self.textbox.configure(state="disabled")
        finally: conn.close()

# --- APP PRINCIPAL ---

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventario CRA")
        self.geometry("1200x700")
        inicializar_db()
        self.tab_view = customtkinter.CTkTabview(self, width=980)
        self.tab_view.pack(pady=10, padx=10, fill="both", expand=True) 

        # PESTAÑA 1: PRÉSTAMOS (Sin cambios)
        self.tab_view.add("Préstamos")
        tab_p = self.tab_view.tab("Préstamos")
        tab_p.grid_columnconfigure(0, weight=10); tab_p.grid_columnconfigure(1, weight=1); tab_p.grid_columnconfigure(2, weight=10)
        tab_p.grid_rowconfigure(0, weight=1)
        fp = customtkinter.CTkFrame(tab_p, corner_radius=15, border_width=2, border_color="#3B8ED0"); fp.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        fp.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(fp, text="📤 REALIZAR PRÉSTAMO", font=("Arial", 18, "bold"), text_color="#3B8ED0").grid(row=0, columnspan=2, pady=(20, 10))
        customtkinter.CTkLabel(fp, text="RUT Alumno:").grid(row=2, column=0, sticky="w", padx=20)
        self.entry_p_rut = customtkinter.CTkEntry(fp, placeholder_text="Ej: 12345678-9"); self.entry_p_rut.grid(row=2, column=1, sticky="ew", padx=20, pady=10)
        customtkinter.CTkLabel(fp, text="ISBN/Título:").grid(row=3, column=0, sticky="w", padx=20)
        self.entry_p_isbn = customtkinter.CTkEntry(fp, placeholder_text="Escanee o escriba..."); self.entry_p_isbn.grid(row=3, column=1, sticky="ew", padx=20, pady=10)
        customtkinter.CTkButton(fp, text="CONFIRMAR PRÉSTAMO", fg_color="#3B8ED0", height=40, command=self.realizar_prestamo).grid(row=4, columnspan=2, pady=30, padx=20, sticky="ew")
        customtkinter.CTkFrame(tab_p, width=2, fg_color="gray40").grid(row=0, column=1, sticky="ns", pady=40)
        fd = customtkinter.CTkFrame(tab_p, corner_radius=15, border_width=2, border_color="#2CC985"); fd.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
        fd.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(fd, text="📥 REGISTRAR DEVOLUCIÓN", font=("Arial", 18, "bold"), text_color="#2CC985").grid(row=0, columnspan=2, pady=(20, 10))
        customtkinter.CTkLabel(fd, text="ISBN/Título:").grid(row=2, column=0, sticky="w", padx=20)
        self.entry_d_isbn = customtkinter.CTkEntry(fd, placeholder_text="Libro a devolver..."); self.entry_d_isbn.grid(row=2, column=1, sticky="ew", padx=20, pady=10)
        customtkinter.CTkButton(fd, text="CONFIRMAR DEVOLUCIÓN", fg_color="#2CC985", height=40, command=self.realizar_devolucion).grid(row=4, columnspan=2, pady=30, padx=20, sticky="ew")

        # ===================================================
        # PESTAÑA 2: LIBROS (MODIFICADA CON GRID)
        # ===================================================
        self.tab_view.add("Libros")
        tab_l = self.tab_view.tab("Libros")
        fl = customtkinter.CTkFrame(tab_l); fl.pack(fill="x", padx=10, pady=10)
        customtkinter.CTkLabel(fl, text="Buscar:").pack(side="left", padx=5)
        self.entry_bus_l = customtkinter.CTkEntry(fl, placeholder_text="Nombre del libro"); self.entry_bus_l.pack(side="left", fill="x", expand=True, padx=5)
        customtkinter.CTkButton(fl, text="Buscar", width=80, command=self.buscar_libros).pack(side="left", padx=5)
        customtkinter.CTkButton(fl, text="Nuevo / Stock", fg_color="green", command=self.abrir_nuevo_libro).pack(side="right", padx=5)
        
        # --- Cabecera Tabla Libros (Ahora con GRID) ---
        hl = customtkinter.CTkFrame(tab_l, height=30, fg_color="gray40"); hl.pack(fill="x", padx=10)
        hl.grid_columnconfigure(0, weight=2) # ISBN
        hl.grid_columnconfigure(1, weight=5) # TÍTULO (Más espacio)
        hl.grid_columnconfigure(2, weight=4) # AUTOR
        hl.grid_columnconfigure(3, weight=1) # DISP/TOT
        hl.grid_columnconfigure(4, weight=2) # ACCIONES
        
        customtkinter.CTkLabel(hl, text="ISBN", anchor="w").grid(row=0, column=0, padx=5, sticky="w")
        customtkinter.CTkLabel(hl, text="TÍTULO", anchor="w").grid(row=0, column=1, padx=5, sticky="w")
        customtkinter.CTkLabel(hl, text="AUTOR", anchor="w").grid(row=0, column=2, padx=5, sticky="w")
        customtkinter.CTkLabel(hl, text="DISP/TOT", anchor="center").grid(row=0, column=3, padx=5, sticky="ew")
        customtkinter.CTkLabel(hl, text="ACCIONES", anchor="center").grid(row=0, column=4, padx=10, sticky="e")

        self.scroll_libros = customtkinter.CTkScrollableFrame(tab_l); self.scroll_libros.pack(fill="both", expand=True, padx=10, pady=5)

        # ===================================================
        # PESTAÑA 3: ALUMNOS (MODIFICADA CON GRID)
        # ===================================================
        self.tab_view.add("Alumnos")
        tab_a = self.tab_view.tab("Alumnos"); fa = customtkinter.CTkFrame(tab_a); fa.pack(fill="x", padx=10, pady=10)
        customtkinter.CTkLabel(fa, text="Buscar:").pack(side="left", padx=5)
        self.entry_bus_a = customtkinter.CTkEntry(fa, placeholder_text="Buscar por nombre, apellidos o RUT"); self.entry_bus_a.pack(side="left", fill="x", expand=True, padx=5)
        customtkinter.CTkButton(fa, text="Buscar", width=80, command=self.buscar_alumnos).pack(side="left", padx=5)
        customtkinter.CTkButton(fa, text="Nuevo Alumno", fg_color="green", command=self.abrir_nuevo_alumno).pack(side="right", padx=5)
        
        # --- Cabecera Tabla Alumnos (Ahora con GRID) ---
        ha = customtkinter.CTkFrame(tab_a, height=30, fg_color="gray40"); ha.pack(fill="x", padx=10)
        ha.grid_columnconfigure(0, weight=2) # RUT
        ha.grid_columnconfigure(1, weight=4) # NOMBRE (Más espacio)
        ha.grid_columnconfigure(2, weight=2) # CURSO
        ha.grid_columnconfigure(3, weight=2) # EN PODER
        ha.grid_columnconfigure(4, weight=2) # ACCIONES
        
        customtkinter.CTkLabel(ha, text="RUT", anchor="w").grid(row=0, column=0, padx=5, sticky="w")
        customtkinter.CTkLabel(ha, text="NOMBRE", anchor="w").grid(row=0, column=1, padx=5, sticky="w")
        customtkinter.CTkLabel(ha, text="CURSO", anchor="w").grid(row=0, column=2, padx=5, sticky="w")
        customtkinter.CTkLabel(ha, text="EN PODER", anchor="center").grid(row=0, column=3, padx=5, sticky="ew")
        customtkinter.CTkLabel(ha, text="ACCIONES", anchor="center").grid(row=0, column=4, padx=10, sticky="e")

        self.scroll_alumnos = customtkinter.CTkScrollableFrame(tab_a); self.scroll_alumnos.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.win_n_libro=None; self.win_e_libro=None; self.win_n_alumno=None; self.win_e_alumno=None; self.win_detalle=None

    # --- VENTANAS ---
    def abrir_nuevo_libro(self):
        if not self.win_n_libro or not self.win_n_libro.winfo_exists(): self.win_n_libro = VentanaNuevoLibro(self)
        else: self.win_n_libro.focus()
    def abrir_nuevo_alumno(self):
        if not self.win_n_alumno or not self.win_n_alumno.winfo_exists(): self.win_n_alumno = VentanaNuevoPrestatario(self)
        else: self.win_n_alumno.focus()
    def abrir_editar_libro(self, id_libro, datos):
        if not self.win_e_libro or not self.win_e_libro.winfo_exists(): self.win_e_libro = VentanaEditarLibro(self, id_libro, datos)
        else: self.win_e_libro.focus()
    def abrir_editar_alumno(self, id_prest, datos):
        if not self.win_e_alumno or not self.win_e_alumno.winfo_exists(): self.win_e_alumno = VentanaEditarPrestatario(self, id_prest, datos)
        else: self.win_e_alumno.focus()
    def ver_libros_alumno(self, pid, nom):
        if not self.win_detalle or not self.win_detalle.winfo_exists(): self.win_detalle = VentanaDetalleLibros(self, pid, nom)
        else: self.win_detalle.focus()

    # --- LOGICA LIBROS (MODIFICADA CON GRID) ---
    def buscar_libros(self):
        for w in self.scroll_libros.winfo_children(): w.destroy()
        term = self.entry_bus_l.get(); conn = conectar_db(); c = conn.cursor()
        q = "SELECT ID_Libro, ISBN, Título, Autor, Editorial, Año_Publicacion, Categoría, Total_Ejemplares, Disponibles FROM Libros"
        p = ()
        if term: q += " WHERE Título LIKE ? OR Autor LIKE ? OR ISBN LIKE ?"; lk = f"%{term}%"; p = (lk, lk, lk)
        else: q += " WHERE Disponibles < Total_Ejemplares"
        q += " ORDER BY Título"; c.execute(q, p); rows = c.fetchall(); conn.close()
        
        if not rows:
            msg = "No se encontraron coincidencias." if term else "No hay libros con préstamos activos."
            customtkinter.CTkLabel(self.scroll_libros, text=msg).pack(pady=10); return

        for r in rows:
            lid, isbn, tit, aut, edit, anio, cat, tot, disp = r
            
            # Fila
            row_f = customtkinter.CTkFrame(self.scroll_libros, fg_color="transparent"); row_f.pack(fill="x", pady=2)
            # Definir columnas (mismos pesos que la cabecera)
            row_f.grid_columnconfigure(0, weight=2) # ISBN
            row_f.grid_columnconfigure(1, weight=5) # TÍTULO
            row_f.grid_columnconfigure(2, weight=4) # AUTOR
            row_f.grid_columnconfigure(3, weight=1) # DISP/TOT
            row_f.grid_columnconfigure(4, weight=2) # ACCIONES
            
            # Truncar texto largo para que quepa bien
            tit_trunc = (tit[:35] + '...') if len(tit) > 35 else tit
            aut_trunc = (aut[:25] + '...') if len(aut) > 25 else aut

            # Añadir widgets al grid
            customtkinter.CTkLabel(row_f, text=str(isbn), anchor="w").grid(row=0, column=0, padx=5, sticky="w")
            customtkinter.CTkLabel(row_f, text=tit_trunc, anchor="w").grid(row=0, column=1, padx=5, sticky="w")
            customtkinter.CTkLabel(row_f, text=aut_trunc, anchor="w").grid(row=0, column=2, padx=5, sticky="w")
            customtkinter.CTkLabel(row_f, text=f"{disp}/{tot}", anchor="center").grid(row=0, column=3, padx=5, sticky="ew")

            # Frame para acciones, alineado a la derecha de la celda de acciones
            frame_acciones = customtkinter.CTkFrame(row_f, fg_color="transparent")
            frame_acciones.grid(row=0, column=4, padx=10, sticky="e")
            
            datos_para_editar = (isbn, tit, aut, edit, anio, cat)
            customtkinter.CTkButton(frame_acciones, text="Editar", width=60, fg_color="blue", command=lambda i=lid, d=datos_para_editar: self.abrir_editar_libro(i, d)).pack(side="left", padx=2)
            customtkinter.CTkButton(frame_acciones, text="X", width=30, fg_color="red", command=lambda i=lid, t=tit: self.eliminar_libro_id(i, t)).pack(side="left", padx=2)

    def eliminar_libro_id(self, lid, titulo):
        conn = conectar_db(); c = conn.cursor()
        try:
            c.execute("SELECT 1 FROM Transacciones WHERE ID_Libro=? AND Estado='Prestado'", (lid,))
            if c.fetchone(): return messagebox.showerror("Error", f"'{titulo}' tiene préstamos activos.")
            if messagebox.askyesno("Borrar", f"¿Eliminar '{titulo}'?"): c.execute("DELETE FROM Libros WHERE ID_Libro=?", (lid,)); conn.commit(); self.buscar_libros()
        finally: conn.close()

    # --- LOGICA ALUMNOS (MODIFICADA CON GRID) ---
    def buscar_alumnos(self):
        for w in self.scroll_alumnos.winfo_children(): w.destroy()
        term = self.entry_bus_a.get(); conn = conectar_db(); c = conn.cursor()
        q = """SELECT p.ID_Prestatario, p.RUT, p.Nombre, p.Curso,
               (SELECT COUNT(*) FROM Transacciones t WHERE t.ID_Prestatario=p.ID_Prestatario AND t.Estado='Prestado') as Activos
               FROM Prestatarios p"""
        p = ()
        if term: 
            term_limpio = term.replace(".", "").replace("-", "")
            lk_limpio = f"%{term_limpio}%"
            lk_normal = f"%{term}%"
            q += """
                WHERE
                    (REPLACE(REPLACE(p.RUT, '.', ''), '-', '') LIKE ?) OR
                    (p.Nombre LIKE ?) OR
                    (p.Curso LIKE ?)

            """
            p = (lk_limpio, lk_normal, lk_normal)
        else: q += " WHERE (SELECT COUNT(*) FROM Transacciones t WHERE t.ID_Prestatario=p.ID_Prestatario AND t.Estado='Prestado') > 0"
        q += " ORDER BY p.Nombre"; c.execute(q, p); rows = c.fetchall(); conn.close()

        if not rows:
            msg = "No se encontraron coincidencias." if term else "No hay alumnos con préstamos activos."
            customtkinter.CTkLabel(self.scroll_alumnos, text=msg).pack(pady=10); return

        for r in rows:
            pid, rut, nom, cur, act = r
            
            # --- NUEVO CÓDIGO: Truncar nombre ---
            nom_trunc = (nom[:25] + '...') if len(nom) > 25 else nom
            # --- FIN NUEVO CÓDIGO ---

            # Fila
            row_f = customtkinter.CTkFrame(self.scroll_alumnos, fg_color="transparent"); row_f.pack(fill="x", pady=2)
            # Definir columnas (mismos pesos que la cabecera)
            row_f.grid_columnconfigure(0, weight=2) # RUT
            row_f.grid_columnconfigure(1, weight=4) # NOMBRE
            row_f.grid_columnconfigure(2, weight=2) # CURSO
            row_f.grid_columnconfigure(3, weight=2) # EN PODER
            row_f.grid_columnconfigure(4, weight=2) # ACCIONES
            
            customtkinter.CTkLabel(row_f, text=str(rut), anchor="w").grid(row=0, column=0, padx=5, sticky="w")
            # --- MODIFICADO: Usar el nombre truncado ---
            customtkinter.CTkLabel(row_f, text=nom_trunc, anchor="w").grid(row=0, column=1, padx=5, sticky="w")
            # --- FIN MODIFICADO ---
            customtkinter.CTkLabel(row_f, text=str(cur) if cur else "-", anchor="w").grid(row=0, column=2, padx=5, sticky="w")
            
            col_btn = "orange" if act > 0 else "gray"
            customtkinter.CTkButton(row_f, text=f"{act} Libros", width=100, fg_color=col_btn, command=lambda p=pid, n=nom: self.ver_libros_alumno(p, n)).grid(row=0, column=3, padx=5, sticky="ew")
            
            # Frame para acciones, alineado a la derecha
            frame_acciones = customtkinter.CTkFrame(row_f, fg_color="transparent")
            frame_acciones.grid(row=0, column=4, padx=10, sticky="e")
            
            datos_edit = (rut, nom, cur)
            customtkinter.CTkButton(frame_acciones, text="Editar", width=60, fg_color="blue", command=lambda p=pid, d=datos_edit: self.abrir_editar_alumno(p, d)).pack(side="left", padx=2)
            customtkinter.CTkButton(frame_acciones, text="X", width=30, fg_color="red", command=lambda p=pid, n=nom: self.eliminar_alumno_id(p, n)).pack(side="left", padx=2)
            
    def eliminar_alumno_id(self, pid, nombre):
        conn = conectar_db(); c = conn.cursor()
        try:
            c.execute("SELECT 1 FROM Transacciones WHERE ID_Prestatario=? AND Estado='Prestado'", (pid,))
            if c.fetchone(): return messagebox.showerror("Error", f"{nombre} tiene libros sin devolver.")
            if messagebox.askyesno("Borrar", f"¿Eliminar a {nombre}?"): c.execute("DELETE FROM Prestatarios WHERE ID_Prestatario=?", (pid,)); conn.commit(); self.buscar_alumnos()
        finally: conn.close()

    # --- LOGICA PRESTAMOS (SIN CAMBIOS, CÓDIGO EXPANDIDO) ---
    def realizar_prestamo(self):
        rut = self.entry_p_rut.get(); item = self.entry_p_isbn.get()
        if not rut or not item: return messagebox.showerror("Error", "Datos incompletos.")
        conn = conectar_db(); c = conn.cursor()
        try:
            rut_limpio = rut.replace(".", "").replace("-", "")
            c.execute("SELECT ID_Prestatario, Nombre FROM Prestatarios WHERE REPLACE(REPLACE(RUT, '.', ''), '-', '') = ?", (rut_limpio,)); res_a = c.fetchone()
            if not res_a: return messagebox.showerror("Error", "Alumno no encontrado.")
            pid, pnom = res_a
            lk = f"%{item}%"
            c.execute("SELECT ID_Libro, Título, Disponibles FROM Libros WHERE (ISBN = ? OR Título LIKE ?) AND Disponibles > 0", (item, lk)); res_l = c.fetchone()
            if not res_l: return messagebox.showerror("Error", "Libro no disponible.")
            lid, ltit, _ = res_l
            c.execute("SELECT 1 FROM Transacciones WHERE ID_Libro = ? AND ID_Prestatario = ? AND Estado = 'Prestado'", (lid, pid))
            if c.fetchone(): return messagebox.showerror("Error", "Préstamo duplicado.")
            c.execute("UPDATE Libros SET Disponibles = Disponibles - 1 WHERE ID_Libro = ?", (lid,))
            c.execute("INSERT INTO Transacciones (ID_Libro, ID_Prestatario, Fecha_Entrega, Estado) VALUES (?, ?, ?, 'Prestado')", (lid, pid, datetime.now().strftime("%Y-%m-%d")))
            conn.commit(); messagebox.showinfo("Éxito", f"Préstamo: {ltit} -> {pnom}"); self.entry_p_rut.delete(0, "end"); self.entry_p_isbn.delete(0, "end")
        except Exception as e: conn.rollback(); messagebox.showerror("Error", str(e))
        finally: conn.close()

    def realizar_devolucion(self):
        item = self.entry_d_isbn.get()
        if not item: return messagebox.showerror("Error", "Ingrese ISBN o Título.")
        conn = conectar_db(); c = conn.cursor()
        try:
            lk = f"%{item}%"; c.execute("SELECT ID_Libro, Título FROM Libros WHERE ISBN = ? OR Título LIKE ?", (item, lk)); res = c.fetchone()
            if not res: return messagebox.showerror("Error", "Libro no encontrado.")
            lid, ltit = res
            c.execute("SELECT ID_Transaccion FROM Transacciones WHERE ID_Libro = ? AND Estado = 'Prestado' LIMIT 1", (lid,)); res_t = c.fetchone()
            if not res_t: return messagebox.showerror("Error", "No hay préstamo activo.")
            tid = res_t[0]
            c.execute("UPDATE Transacciones SET Estado = 'Devuelto', Fecha_Devolucion_Real = ? WHERE ID_Transaccion = ?", (datetime.now().strftime("%Y-%m-%d"), tid))
            c.execute("UPDATE Libros SET Disponibles = Disponibles + 1 WHERE ID_Libro = ?", (lid,))
            conn.commit(); messagebox.showinfo("Éxito", f"Devuelto: {ltit}"); self.entry_d_isbn.delete(0, "end")
        finally: conn.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()