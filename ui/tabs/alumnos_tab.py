"""
Pestaña de Alumnos - Interfaz para gestionar los alumnos/prestatarios
"""
import customtkinter
from tkinter import messagebox
from models.alumno import AlumnoModel
from ui.dialogs.dialogs import AlumnoDialog
from utils.theme import Colors, Styles


class AlumnosTab:
    """Construye y gestiona la pestaña de Alumnos"""
    
    def __init__(self, parent_tab, alumno_model: AlumnoModel, main_window=None):
        self.parent = parent_tab
        self.alumno_model = alumno_model
        self.main_window = main_window
        self.win_e_alumno = None
        self.win_n_alumno = None
        self.win_detalle = None
        self.editing_id = None
        self.parent.configure(fg_color=Colors.BG_DARK)
        
        self._build_ui()
        self.buscar_alumnos()  # Cargar inicial
    
    def _build_ui(self):
        """Construye la interfaz de la pestaña"""
        # --- BARRA DE BÚSQUEDA ---
        fa = customtkinter.CTkFrame(self.parent, fg_color=Colors.BG_SECONDARY,
                                   corner_radius=Styles.CORNER_RADIUS_LARGE,
                                   border_width=Styles.BORDER_WIDTH_THIN,
                                   border_color=Colors.BORDER_LIGHT)
        fa.pack(fill="x", padx=Styles.PADDING_LG, pady=Styles.PADDING_LG)
        
        customtkinter.CTkLabel(fa, text="🔍 Buscar:", text_color=Colors.TEXT_PRIMARY,
                              font=Styles.FONT_BOLD).pack(side="left", padx=Styles.PADDING_LG)
        self.entry_bus_a = customtkinter.CTkEntry(fa, placeholder_text="Buscar por nombre, apellidos o RUT...",
                                                  fg_color=Colors.BG_TERTIARY,
                                                  border_color=Colors.BORDER_ACCENT,
                                                  border_width=Styles.BORDER_WIDTH_MEDIUM,
                                                  text_color=Colors.TEXT_PRIMARY,
                                                  placeholder_text_color=Colors.TEXT_TERTIARY,
                                                  height=Styles.BUTTON_HEIGHT_MD,
                                                  corner_radius=Styles.CORNER_RADIUS_BUTTON)
        self.entry_bus_a.pack(side="left", fill="x", expand=True, padx=Styles.PADDING_MD)
        self.entry_bus_a.bind("<Return>", lambda e: self.buscar_alumnos())
        
        customtkinter.CTkButton(fa, text="🔎 Buscar", width=110, fg_color=Colors.INFO,
                               hover_color="#4291B5", text_color=Colors.TEXT_INVERSE,
                               height=Styles.BUTTON_HEIGHT_MD,
                               corner_radius=Styles.CORNER_RADIUS_BUTTON,
                               font=Styles.FONT_BOLD,
                               command=self.buscar_alumnos).pack(side="left", padx=Styles.PADDING_SM)
        customtkinter.CTkButton(fa, text="➕ Nuevo Alumno", fg_color=Colors.SECONDARY,
                               hover_color=Colors.SECONDARY_LIGHT, text_color=Colors.TEXT_INVERSE,
                               height=Styles.BUTTON_HEIGHT_MD,
                               corner_radius=Styles.CORNER_RADIUS_BUTTON,
                               font=Styles.FONT_BOLD,
                               command=self.abrir_nuevo_alumno).pack(side="right", padx=Styles.PADDING_LG)
        
        # --- CABECERA ---
        ha = customtkinter.CTkFrame(self.parent, height=40, fg_color=Colors.INFO,
                                   corner_radius=Styles.CORNER_RADIUS_SMALL)
        ha.pack(fill="x", padx=Styles.PADDING_LG, pady=(0, Styles.PADDING_SM))
        ha.pack_propagate(False)
        ha.grid_columnconfigure(0, weight=2)  # RUT
        ha.grid_columnconfigure(1, weight=4)  # NOMBRE
        ha.grid_columnconfigure(2, weight=2)  # CURSO
        ha.grid_columnconfigure(3, weight=2)  # EN PODER
        ha.grid_columnconfigure(4, weight=2)  # ACCIONES
        
        customtkinter.CTkLabel(ha, text="RUT", anchor="w", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=0, padx=Styles.PADDING_MD, sticky="w")
        customtkinter.CTkLabel(ha, text="NOMBRE", anchor="w", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=1, padx=Styles.PADDING_MD, sticky="w")
        customtkinter.CTkLabel(ha, text="CURSO", anchor="w", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=2, padx=Styles.PADDING_MD, sticky="w")
        customtkinter.CTkLabel(ha, text="EN PODER", anchor="center", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=3, padx=Styles.PADDING_MD, sticky="ew")
        customtkinter.CTkLabel(ha, text="ACCIONES", anchor="center", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=4, padx=Styles.PADDING_MD, sticky="e")
        
        # --- ÁREA SCROLLABLE ---
        self.scroll_alumnos = customtkinter.CTkScrollableFrame(self.parent, fg_color=Colors.BG_DARK)
        self.scroll_alumnos.pack(fill="both", expand=True, padx=Styles.PADDING_LG, pady=(0, Styles.PADDING_LG))
        self.scroll_alumnos.grid_columnconfigure(0, weight=2)  # RUT
        self.scroll_alumnos.grid_columnconfigure(1, weight=4)  # NOMBRE
        self.scroll_alumnos.grid_columnconfigure(2, weight=2)  # CURSO
        self.scroll_alumnos.grid_columnconfigure(3, weight=2)  # EN PODER
        self.scroll_alumnos.grid_columnconfigure(4, weight=2)  # ACCIONES
    
    def buscar_alumnos(self):
        """Busca alumnos según el término ingresado"""
        for w in self.scroll_alumnos.winfo_children():
            w.destroy()
        
        term = self.entry_bus_a.get()
        rows = self.alumno_model.buscar_alumnos(term)
        
        if not rows:
            msg = "👤 No se encontraron coincidencias." if term else "👤 No hay alumnos con préstamos activos."
            customtkinter.CTkLabel(self.scroll_alumnos, text=msg, text_color=Colors.TEXT_SECONDARY,
                                  font=Styles.FONT_REGULAR).pack(pady=Styles.PADDING_XL)
            return
        
        for idx, r in enumerate(rows):
            pid, rut, nom, cur, act = r
            nom_trunc = (nom[:25] + '...') if len(nom) > 25 else nom

            # Columna 0: RUT
            customtkinter.CTkLabel(self.scroll_alumnos, text=str(rut), anchor="w",
                                  text_color=Colors.TEXT_PRIMARY, font=Styles.FONT_REGULAR).grid(
                row=idx, column=0, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="w"
            )
            # Columna 1: NOMBRE
            customtkinter.CTkLabel(self.scroll_alumnos, text=nom_trunc, anchor="w",
                                  text_color=Colors.TEXT_PRIMARY, font=Styles.FONT_REGULAR).grid(
                row=idx, column=1, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="w"
            )
            # Columna 2: CURSO
            customtkinter.CTkLabel(self.scroll_alumnos, text=str(cur) if cur else "-", anchor="w",
                                  text_color=Colors.TEXT_SECONDARY, font=Styles.FONT_REGULAR).grid(
                row=idx, column=2, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="w"
            )

            # Columna 3: EN PODER (botón)
            col_btn = Colors.WARNING if act > 0 else Colors.TEXT_TERTIARY
            customtkinter.CTkButton(
                self.scroll_alumnos,
                text=f"📚 {act}",
                fg_color=col_btn,
                hover_color="#D9A820" if act > 0 else Colors.TEXT_TERTIARY,
                text_color=Colors.TEXT_INVERSE,
                corner_radius=Styles.CORNER_RADIUS_BUTTON,
                height=32,
                font=("Segoe UI", 11, "bold"),
                command=lambda p=pid, n=nom: self.ver_libros_alumno(p, n)
            ).grid(row=idx, column=3, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="ew")

            # Columna 4: ACCIONES (contenedor con botones Editar y X)
            acciones = customtkinter.CTkFrame(self.scroll_alumnos, fg_color="transparent")
            acciones.grid(row=idx, column=4, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="e")

            datos_edit = (rut, nom, cur)
            customtkinter.CTkButton(
                acciones,
                text="✏️ Editar",
                width=90,
                fg_color=Colors.INFO,
                hover_color="#4291B5",
                text_color=Colors.TEXT_INVERSE,
                corner_radius=Styles.CORNER_RADIUS_BUTTON,
                height=32,
                font=("Segoe UI", 11, "bold"),
                command=lambda p=pid, d=datos_edit: self.abrir_editar_alumno(p, d)
            ).pack(side="left", padx=Styles.PADDING_XS)
            customtkinter.CTkButton(
                acciones,
                text="🗑️",
                width=40,
                fg_color=Colors.DANGER,
                hover_color="#B02020",
                text_color=Colors.TEXT_INVERSE,
                corner_radius=Styles.CORNER_RADIUS_BUTTON,
                height=32,
                command=lambda p=pid, n=nom: self.eliminar_alumno(p, n)
            ).pack(side="left", padx=Styles.PADDING_XS)
    
    def abrir_nuevo_alumno(self):
        """Abre el diálogo para crear un nuevo alumno"""
        if not self.win_n_alumno or not self.win_n_alumno.winfo_exists():
            self.win_n_alumno = AlumnoDialog(self.parent, self._guardar_alumno)
        else:
            self.win_n_alumno.focus()
    
    def abrir_editar_alumno(self, id_prestatario: int, datos: tuple):
        """Abre el diálogo para editar un alumno"""
        self.editing_id = id_prestatario
        if not self.win_e_alumno or not self.win_e_alumno.winfo_exists():
            self.win_e_alumno = AlumnoDialog(self.parent, self._guardar_alumno, datos)
        else:
            self.win_e_alumno.focus()
    
    def _guardar_alumno(self):
        """Guarda un alumno nuevo o edita uno existente"""
        try:
            if self.editing_id:
                messagebox.showinfo("✅ Éxito", "Alumno actualizado.")
                self.editing_id = None
            else:
                messagebox.showinfo("✅ Éxito", "Alumno creado.")
            
            self.buscar_alumnos()
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
    
    def eliminar_alumno(self, id_prestatario: int, nombre: str):
        """Elimina un alumno de la base de datos"""
        try:
            if self.alumno_model.tiene_prestamos_activos(id_prestatario):
                return messagebox.showerror("❌ Error", f"{nombre} tiene libros sin devolver.")
            
            if messagebox.askyesno("🗑️ Borrar", f"¿Eliminar a {nombre}?"):
                self.alumno_model.eliminar_alumno(id_prestatario)
                self.buscar_alumnos()
                
                # Actualizar dashboard
                if self.main_window:
                    self.main_window.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
    
    def ver_libros_alumno(self, id_prestatario: int, nombre_alumno: str):
        """Muestra los libros que un alumno tiene en poder"""
        if not self.win_detalle or not self.win_detalle.winfo_exists():
            self.win_detalle = DetalleLibrosWindow(self.parent, id_prestatario, nombre_alumno, self.alumno_model)
        else:
            self.win_detalle.focus()


class DetalleLibrosWindow(customtkinter.CTkToplevel):
    """Ventana que muestra los libros en poder de un alumno"""
    
    def __init__(self, master, id_prestatario: int, nombre_alumno: str, alumno_model: AlumnoModel):
        super().__init__(master)
        self.title(f"📚 Libros en poder de: {nombre_alumno}")
        self.geometry("700x450")
        self.transient(master)
        
        # Configurar fondo con tema
        self.configure(fg_color=Colors.BG_DARK)
        
        # Título
        titulo = customtkinter.CTkLabel(
            self,
            text=f"📚 Libros en poder de {nombre_alumno}",
            text_color=Colors.TEXT_PRIMARY,
            font=Styles.FONT_HEADER
        )
        titulo.pack(pady=Styles.PADDING_LG, padx=Styles.PADDING_LG)
        
        # Textbox con tema
        self.textbox = customtkinter.CTkTextbox(
            self,
            font=Styles.FONT_MONO,
            fg_color=Colors.BG_SECONDARY,
            text_color=Colors.TEXT_PRIMARY,
            border_color=Colors.BORDER_ACCENT,
            border_width=1
        )
        self.textbox.pack(fill="both", expand=True, padx=Styles.PADDING_LG, pady=(0, Styles.PADDING_LG))
        
        self._cargar_libros(id_prestatario, alumno_model)
    
    def _cargar_libros(self, id_prestatario: int, alumno_model: AlumnoModel):
        """Carga y muestra los libros del alumno"""
        rows = alumno_model.obtener_libros_en_poder(id_prestatario)
        
        if not rows:
            self.textbox.insert("1.0", "Este alumno no tiene libros pendientes.")
        else:
            header = f"{'ISBN':<15} | {'TÍTULO':<40} | {'FECHA PRESTAMO':<15}\n" + ("-"*75) + "\n"
            self.textbox.insert("1.0", header)
            for r in rows:
                isbn, titulo, autor, fecha = r
                titulo_trunc = (titulo[:37]+'..') if len(titulo)>40 else titulo
                self.textbox.insert("end", f"{isbn:<15} | {titulo_trunc:<40} | {fecha:<15}\n")
        
        self.textbox.configure(state="disabled")
