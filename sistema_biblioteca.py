import sqlite3
import customtkinter
from tkinter import messagebox
from datetime import datetime

# --- Configuración de Apariencia ---
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

DATABASE_NAME = "inventario.db"

# --- Funciones de Base de Datos ---
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

# --- Ventanas Emergentes ---

class VentanaNuevoLibro(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Registrar Nuevo Libro")
        self.geometry("500x550")
        self.transient(master) 
        self.grab_set()
        self.lift()
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1) 
        
        campos = ["Título:", "Autor:", "ISBN:", "Editorial:", "Año Publicación:", "Categoría:", "Nº Ejemplares (a sumar):"]
        self.entries = {}
        for i, label_text in enumerate(campos):
            lbl = customtkinter.CTkLabel(self.frame, text=label_text)
            lbl.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = customtkinter.CTkEntry(self.frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.entries[label_text] = entry
            
        self.boton_guardar = customtkinter.CTkButton(self.frame, text="Guardar Libro", command=self.guardar_nuevo_libro)
        self.boton_guardar.grid(row=7, column=0, columnspan=2, pady=20)

    def guardar_nuevo_libro(self):
        titulo = self.entries["Título:"].get()
        autor = self.entries["Autor:"].get()
        isbn = self.entries["ISBN:"].get()
        editorial = self.entries["Editorial:"].get()
        anio = self.entries["Año Publicación:"].get()
        categoria = self.entries["Categoría:"].get()
        ejemplares_str = self.entries["Nº Ejemplares (a sumar):"].get()
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        if not isbn:
             messagebox.showerror("Error", "El campo 'ISBN' es obligatorio.", parent=self)
             return
        try:
            ejemplares = int(ejemplares_str)
            if ejemplares <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El campo 'Nº Ejemplares' debe ser un número positivo.", parent=self)
            return

        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_Libro FROM Libros WHERE ISBN = ?", (isbn,))
            existe = cursor.fetchone()
            if existe:
                if messagebox.askyesno("Libro Existente", f"El ISBN '{isbn}' ya existe. ¿Sumar {ejemplares} copias?", parent=self):
                    cursor.execute("UPDATE Libros SET Total_Ejemplares = Total_Ejemplares + ?, Disponibles = Disponibles + ? WHERE ISBN = ?", (ejemplares, ejemplares, isbn))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Stock actualizado.", parent=self)
                    self.destroy()
            else:
                if not titulo or not autor:
                    messagebox.showerror("Error", "Para libros nuevos, Título y Autor son obligatorios.", parent=self)
                    return
                cursor.execute("INSERT INTO Libros (ISBN, Título, Autor, Editorial, Año_Publicacion, Categoría, Total_Ejemplares, Disponibles, Fecha_Ingreso_Donacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                               (isbn, titulo, autor, editorial, anio, categoria, ejemplares, ejemplares, fecha_actual))
                conn.commit()
                messagebox.showinfo("Éxito", "Libro registrado.", parent=self)
                self.destroy()
        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror("Error DB", str(e), parent=self)
        finally:
            conn.close()

class VentanaNuevoPrestatario(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Registrar Alumno")
        self.geometry("400x250")
        self.transient(master) 
        self.grab_set()
        self.lift()
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1) 
        
        self.lbl_rut = customtkinter.CTkLabel(self.frame, text="RUT:")
        self.lbl_rut.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_rut = customtkinter.CTkEntry(self.frame)
        self.entry_rut.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        self.lbl_nom = customtkinter.CTkLabel(self.frame, text="Nombre:")
        self.lbl_nom.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_nom = customtkinter.CTkEntry(self.frame)
        self.entry_nom.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        self.lbl_curso = customtkinter.CTkLabel(self.frame, text="Curso:")
        self.lbl_curso.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_curso = customtkinter.CTkEntry(self.frame)
        self.entry_curso.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        self.btn = customtkinter.CTkButton(self.frame, text="Guardar", command=self.guardar)
        self.btn.grid(row=3, column=0, columnspan=2, pady=20)

    def guardar(self):
        rut, nom, curso = self.entry_rut.get(), self.entry_nom.get(), self.entry_curso.get()
        if not rut or not nom:
            messagebox.showerror("Error", "RUT y Nombre obligatorios.", parent=self)
            return
        conn = conectar_db()
        try:
            conn.execute("INSERT INTO Prestatarios (RUT, Nombre, Curso) VALUES (?, ?, ?)", (rut, nom, curso))
            conn.commit()
            messagebox.showinfo("Éxito", "Alumno registrado.", parent=self)
            self.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El RUT ya existe.", parent=self)
        finally:
            conn.close()

class VentanaEliminarPrestatario(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Eliminar Alumno")
        self.geometry("400x200")
        self.transient(master) 
        self.grab_set()
        self.lift()
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1) 
        
        customtkinter.CTkLabel(self.frame, text="RUT a Eliminar:").grid(row=0, column=0, padx=10)
        self.entry_rut = customtkinter.CTkEntry(self.frame)
        self.entry_rut.grid(row=0, column=1, sticky="ew", padx=10)
        
        customtkinter.CTkButton(self.frame, text="Eliminar", fg_color="red", command=self.eliminar).grid(row=1, column=0, columnspan=2, pady=20)

    def eliminar(self):
        rut = self.entry_rut.get()
        if not rut: return
        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_Prestatario, Nombre FROM Prestatarios WHERE RUT = ?", (rut,))
            res = cursor.fetchone()
            if not res:
                messagebox.showerror("Error", "Alumno no encontrado.", parent=self)
                return
            pid, nom = res
            
            cursor.execute("SELECT 1 FROM Transacciones WHERE ID_Prestatario = ? AND Estado = 'Prestado'", (pid,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El alumno tiene libros prestados sin devolver.", parent=self)
                return
                
            if messagebox.askyesno("Confirmar", f"¿Eliminar a {nom}? Se borrará su historial."):
                cursor.execute("DELETE FROM Prestatarios WHERE ID_Prestatario = ?", (pid,))
                conn.commit()
                messagebox.showinfo("Éxito", "Alumno eliminado.", parent=self)
                self.destroy()
        finally:
            conn.close()

# --- (NUEVO) VENTANA DETALLE DE LIBROS ---
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
        conn = conectar_db()
        c = conn.cursor()
        try:
            # Buscamos libros PRESTADOS por este alumno
            query = """
                SELECT l.ISBN, l.Título, l.Autor, t.Fecha_Entrega
                FROM Transacciones t
                JOIN Libros l ON t.ID_Libro = l.ID_Libro
                WHERE t.ID_Prestatario = ? AND t.Estado = 'Prestado'
            """
            c.execute(query, (pid,))
            rows = c.fetchall()
            
            if not rows:
                self.textbox.insert("1.0", "Este alumno no tiene libros pendientes de devolución.")
            else:
                header = f"{'ISBN':<15} | {'TÍTULO':<35} | {'FECHA PRÉSTAMO'}\n" + ("-"*75) + "\n"
                self.textbox.insert("1.0", header)
                for r in rows:
                    isbn, tit, aut, fecha = r
                    tit = (tit[:32] + '..') if len(tit)>35 else tit
                    self.textbox.insert("end", f"{isbn:<15} | {tit:<35} | {fecha}\n")
            self.textbox.configure(state="disabled")
        finally:
            conn.close()

# --- APP PRINCIPAL ---

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventario CRA")
        self.geometry("1100x650")
        inicializar_db()

        self.tab_view = customtkinter.CTkTabview(self, width=980)
        self.tab_view.pack(pady=10, padx=10, fill="both", expand=True) 

        # ===================================================
        # PESTAÑA 1: PRÉSTAMOS
        # ===================================================
        self.tab_view.add("Préstamos")
        tab_prestamos = self.tab_view.tab("Préstamos")
        tab_prestamos.grid_columnconfigure(0, weight=1)
        tab_prestamos.grid_columnconfigure(1, weight=1)
        tab_prestamos.grid_rowconfigure(0, weight=1)

        frame_p = customtkinter.CTkFrame(tab_prestamos, corner_radius=10)
        frame_p.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_p.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(frame_p, text="Realizar Préstamo", font=("Roboto", 16, "bold")).grid(row=0, columnspan=2, pady=10)
        customtkinter.CTkLabel(frame_p, text="RUT Alumno:").grid(row=1, column=0, sticky="w", padx=10)
        self.entry_p_rut = customtkinter.CTkEntry(frame_p)
        self.entry_p_rut.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        customtkinter.CTkLabel(frame_p, text="ISBN/Título:").grid(row=2, column=0, sticky="w", padx=10)
        self.entry_p_isbn = customtkinter.CTkEntry(frame_p)
        self.entry_p_isbn.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        customtkinter.CTkButton(frame_p, text="Confirmar Préstamo", command=self.realizar_prestamo).grid(row=3, columnspan=2, pady=20)

        frame_d = customtkinter.CTkFrame(tab_prestamos, corner_radius=10)
        frame_d.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame_d.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(frame_d, text="Registrar Devolución", font=("Roboto", 16, "bold")).grid(row=0, columnspan=2, pady=10)
        customtkinter.CTkLabel(frame_d, text="ISBN/Título:").grid(row=1, column=0, sticky="w", padx=10)
        self.entry_d_isbn = customtkinter.CTkEntry(frame_d)
        self.entry_d_isbn.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        customtkinter.CTkButton(frame_d, text="Confirmar Devolución", fg_color="green", command=self.realizar_devolucion).grid(row=2, columnspan=2, pady=20)

        # ===================================================
        # PESTAÑA 2: LIBROS
        # ===================================================
        self.tab_view.add("Libros")
        tab_libros = self.tab_view.tab("Libros")
        
        frame_top_l = customtkinter.CTkFrame(tab_libros)
        frame_top_l.pack(fill="x", padx=10, pady=10)
        
        customtkinter.CTkLabel(frame_top_l, text="Buscar:").pack(side="left", padx=5)
        self.entry_bus_l = customtkinter.CTkEntry(frame_top_l)
        self.entry_bus_l.pack(side="left", fill="x", expand=True, padx=5)
        
        customtkinter.CTkButton(frame_top_l, text="Buscar", width=80, command=self.buscar_libros).pack(side="left", padx=5)
        customtkinter.CTkButton(frame_top_l, text="Eliminar (ISBN)", fg_color="red", width=100, command=self.eliminar_libro).pack(side="left", padx=5)
        customtkinter.CTkButton(frame_top_l, text="Nuevo / Stock", fg_color="green", command=self.abrir_nuevo_libro).pack(side="right", padx=5)
        
        self.txt_libros = customtkinter.CTkTextbox(tab_libros, state="disabled", font=("Consolas", 12))
        self.txt_libros.pack(fill="both", expand=True, padx=10, pady=5)

        # ===================================================
        # PESTAÑA 3: ALUMNOS (REDDISEÑADA PARA INTERACTIVIDAD)
        # ===================================================
        self.tab_view.add("Alumnos")
        tab_alumnos = self.tab_view.tab("Alumnos")
        
        frame_top_a = customtkinter.CTkFrame(tab_alumnos)
        frame_top_a.pack(fill="x", padx=10, pady=10)
        
        customtkinter.CTkLabel(frame_top_a, text="Buscar Alumno (RUT/Nombre):").pack(side="left", padx=5)
        self.entry_bus_a = customtkinter.CTkEntry(frame_top_a)
        self.entry_bus_a.pack(side="left", fill="x", expand=True, padx=5)
        
        customtkinter.CTkButton(frame_top_a, text="Buscar", width=80, command=self.buscar_alumnos).pack(side="left", padx=5)
        customtkinter.CTkButton(frame_top_a, text="Eliminar Alumno", fg_color="red", width=120, command=self.abrir_eliminar_alumno).pack(side="left", padx=5)
        customtkinter.CTkButton(frame_top_a, text="Nuevo Alumno", fg_color="green", command=self.abrir_nuevo_alumno).pack(side="right", padx=5)
        
        # --- CAMBIO IMPORTANTE: Usamos ScrollableFrame en vez de Textbox para poder poner botones ---
        # Cabecera manual (Frame fijo)
        self.header_frame = customtkinter.CTkFrame(tab_alumnos, height=30, fg_color="gray40")
        self.header_frame.pack(fill="x", padx=10)
        customtkinter.CTkLabel(self.header_frame, text="RUT", width=100, anchor="w").pack(side="left", padx=10)
        customtkinter.CTkLabel(self.header_frame, text="NOMBRE", width=250, anchor="w").pack(side="left", padx=10)
        customtkinter.CTkLabel(self.header_frame, text="CURSO", width=100, anchor="w").pack(side="left", padx=10)
        customtkinter.CTkLabel(self.header_frame, text="LIBROS (Clic para ver)", width=150, anchor="center").pack(side="left", padx=10)

        # Area desplazable para las filas
        self.scroll_alumnos = customtkinter.CTkScrollableFrame(tab_alumnos)
        self.scroll_alumnos.pack(fill="both", expand=True, padx=10, pady=5)

        self.win_n_libro = None
        self.win_n_alumno = None
        self.win_e_alumno = None
        self.win_detalle = None # Para la nueva ventana de detalle

    # --- Lógica de Ventanas ---
    def abrir_nuevo_libro(self):
        if not self.win_n_libro or not self.win_n_libro.winfo_exists(): self.win_n_libro = VentanaNuevoLibro(self)
        else: self.win_n_libro.focus()
    def abrir_nuevo_alumno(self):
        if not self.win_n_alumno or not self.win_n_alumno.winfo_exists(): self.win_n_alumno = VentanaNuevoPrestatario(self)
        else: self.win_n_alumno.focus()
    def abrir_eliminar_alumno(self):
        if not self.win_e_alumno or not self.win_e_alumno.winfo_exists(): self.win_e_alumno = VentanaEliminarPrestatario(self)
        else: self.win_e_alumno.focus()
    
    # NUEVO: Abre la ventana de detalle
    def ver_libros_alumno(self, id_prest, nombre):
        if not self.win_detalle or not self.win_detalle.winfo_exists(): 
            self.win_detalle = VentanaDetalleLibros(self, id_prest, nombre)
        else: 
            self.win_detalle.focus()

    # --- Lógica Libros ---
    def buscar_libros(self):
        term = self.entry_bus_l.get()
        conn = conectar_db()
        c = conn.cursor()
        q = "SELECT ISBN, Título, Autor, Disponibles, Total_Ejemplares FROM Libros"
        p = ()
        if term:
            q += " WHERE Título LIKE ? OR Autor LIKE ? OR ISBN LIKE ?"
            lk = f"%{term}%"
            p = (lk, lk, lk)
        q += " ORDER BY Título"
        c.execute(q, p)
        rows = c.fetchall()
        conn.close()
        
        self.txt_libros.configure(state="normal")
        self.txt_libros.delete("1.0", "end")
        header = f"{'ISBN':<15} | {'TÍTULO':<40} | {'AUTOR':<30} | {'DISP/TOT'}\n" + ("-"*100) + "\n"
        self.txt_libros.insert("1.0", header)
        for r in rows:
            isbn, tit, aut, dis, tot = r
            isbn = isbn if isbn else "N/A"
            tit = (tit[:37] + '..') if len(tit)>40 else tit
            aut = (aut[:27] + '..') if len(aut)>30 else aut
            self.txt_libros.insert("end", f"{isbn:<15} | {tit:<40} | {aut:<30} | {dis:>3}/{tot:<3}\n")
        self.txt_libros.configure(state="disabled")

    def eliminar_libro(self):
        isbn = self.entry_bus_l.get()
        if not isbn:
            messagebox.showerror("Error", "Ingrese ISBN en el buscador para eliminar.")
            return
        conn = conectar_db()
        c = conn.cursor()
        try:
            c.execute("SELECT ID_Libro, Título FROM Libros WHERE ISBN = ?", (isbn,))
            res = c.fetchone()
            if not res:
                messagebox.showerror("Error", "Libro no encontrado.")
                return
            lid, tit = res
            c.execute("SELECT 1 FROM Transacciones WHERE ID_Libro = ? AND Estado = 'Prestado'", (lid,))
            if c.fetchone():
                messagebox.showerror("Error", "El libro tiene préstamos activos.")
                return
            if messagebox.askyesno("Confirmar", f"¿Eliminar '{tit}' y su historial?"):
                c.execute("DELETE FROM Libros WHERE ID_Libro = ?", (lid,))
                conn.commit()
                messagebox.showinfo("Éxito", "Libro eliminado.")
                self.buscar_libros()
        finally:
            conn.close()

    # --- Lógica Alumnos (RE-HECHA PARA BOTONES) ---
    def buscar_alumnos(self):
        # Limpiar el scrollable frame antes de poner nuevos resultados
        for widget in self.scroll_alumnos.winfo_children():
            widget.destroy()

        term = self.entry_bus_a.get()
        conn = conectar_db()
        c = conn.cursor()
        
        # Necesitamos el ID_Prestatario para saber qué buscar cuando hagan clic
        query = """
            SELECT 
                p.ID_Prestatario,
                p.RUT, 
                p.Nombre, 
                p.Curso,
                (SELECT COUNT(*) FROM Transacciones t 
                 WHERE t.ID_Prestatario = p.ID_Prestatario AND t.Estado = 'Prestado') as Activos
            FROM Prestatarios p
        """
        params = ()
        
        if term:
            query += " WHERE p.RUT LIKE ? OR p.Nombre LIKE ? OR p.Curso LIKE ?"
            like_term = f"%{term}%"
            params = (like_term, like_term, like_term)
            
        query += " ORDER BY p.Nombre"
        
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            customtkinter.CTkLabel(self.scroll_alumnos, text="No se encontraron alumnos.").pack(pady=20)
            return

        # Generar una "Fila" por cada alumno
        for row in rows:
            pid, rut, nombre, curso, activos = row
            
            # Fila contenedor
            fila = customtkinter.CTkFrame(self.scroll_alumnos, fg_color="transparent")
            fila.pack(fill="x", pady=2)
            
            # Datos
            customtkinter.CTkLabel(fila, text=rut, width=100, anchor="w").pack(side="left", padx=10)
            customtkinter.CTkLabel(fila, text=nombre, width=250, anchor="w").pack(side="left", padx=10)
            customtkinter.CTkLabel(fila, text=curso if curso else "-", width=100, anchor="w").pack(side="left", padx=10)
            
            # EL BOTÓN MAGICO
            # Usamos un color diferente si tiene libros (Rojo/Naranja) o si está limpio (Verde/Gris)
            color_btn = "orange" if activos > 0 else "gray"
            
            # Usamos lambda pid=pid, nombre=nombre para "congelar" el valor actual del ciclo
            btn = customtkinter.CTkButton(fila, text=f"{activos} Libros", width=120, fg_color=color_btn,
                                          command=lambda p=pid, n=nombre: self.ver_libros_alumno(p, n))
            btn.pack(side="left", padx=10)


    # --- Lógica Préstamos ---
    def realizar_prestamo(self):
        rut, item = self.entry_p_rut.get(), self.entry_p_isbn.get()
        if not rut or not item: return
        conn = conectar_db()
        c = conn.cursor()
        try:
            c.execute("SELECT ID_Prestatario, Nombre FROM Prestatarios WHERE RUT = ?", (rut,))
            res_a = c.fetchone()
            if not res_a: 
                messagebox.showerror("Error", "Alumno no encontrado.")
                return
            pid, pnom = res_a
            
            lk = f"%{item}%"
            c.execute("SELECT ID_Libro, Título, Disponibles FROM Libros WHERE (ISBN = ? OR Título LIKE ?) AND Disponibles > 0", (item, lk))
            res_l = c.fetchone()
            if not res_l:
                messagebox.showerror("Error", "Libro no disponible o no encontrado.")
                return
            lid, ltit, ldisp = res_l
            
            c.execute("SELECT 1 FROM Transacciones WHERE ID_Libro = ? AND ID_Prestatario = ? AND Estado = 'Prestado'", (lid, pid))
            if c.fetchone():
                messagebox.showerror("Error", "Préstamo duplicado.")
                return
                
            c.execute("UPDATE Libros SET Disponibles = Disponibles - 1 WHERE ID_Libro = ?", (lid,))
            c.execute("INSERT INTO Transacciones (ID_Libro, ID_Prestatario, Fecha_Entrega, Estado) VALUES (?, ?, ?, 'Prestado')", 
                      (lid, pid, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            messagebox.showinfo("Éxito", f"Préstamo: {ltit} -> {pnom}")
            self.entry_p_rut.delete(0, "end")
            self.entry_p_isbn.delete(0, "end")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def realizar_devolucion(self):
        item = self.entry_d_isbn.get()
        if not item: return
        conn = conectar_db()
        c = conn.cursor()
        try:
            lk = f"%{item}%"
            c.execute("SELECT ID_Libro, Título FROM Libros WHERE ISBN = ? OR Título LIKE ?", (item, lk))
            res = c.fetchone()
            if not res: return
            lid, ltit = res
            
            c.execute("SELECT ID_Transaccion FROM Transacciones WHERE ID_Libro = ? AND Estado = 'Prestado' LIMIT 1", (lid,))
            res_t = c.fetchone()
            if not res_t:
                messagebox.showerror("Error", "No hay préstamo activo para este libro.")
                return
            tid = res_t[0]
            
            c.execute("UPDATE Transacciones SET Estado = 'Devuelto', Fecha_Devolucion_Real = ? WHERE ID_Transaccion = ?", 
                      (datetime.now().strftime("%Y-%m-%d"), tid))
            c.execute("UPDATE Libros SET Disponibles = Disponibles + 1 WHERE ID_Libro = ?", (lid,))
            conn.commit()
            messagebox.showinfo("Éxito", f"Devuelto: {ltit}")
            self.entry_d_isbn.delete(0, "end")
        finally:
            conn.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()