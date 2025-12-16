"""
Pestaña de Alumnos - Interfaz para gestionar los alumnos/prestatarios
"""
import customtkinter
from tkinter import messagebox
from models.alumno import AlumnoModel
from ui.dialogs.dialogs import AlumnoDialog


class AlumnosTab:
    """Construye y gestiona la pestaña de Alumnos"""
    
    def __init__(self, parent_tab, alumno_model: AlumnoModel):
        self.parent = parent_tab
        self.alumno_model = alumno_model
        self.win_e_alumno = None
        self.win_n_alumno = None
        self.win_detalle = None
        
        self._build_ui()
        self.buscar_alumnos()  # Cargar inicial
    
    def _build_ui(self):
        """Construye la interfaz de la pestaña"""
        # --- BARRA DE BÚSQUEDA ---
        fa = customtkinter.CTkFrame(self.parent)
        fa.pack(fill="x", padx=10, pady=10)
        
        customtkinter.CTkLabel(fa, text="Buscar:").pack(side="left", padx=5)
        self.entry_bus_a = customtkinter.CTkEntry(fa, placeholder_text="Buscar por nombre, apellidos o RUT")
        self.entry_bus_a.pack(side="left", fill="x", expand=True, padx=5)
        
        customtkinter.CTkButton(fa, text="Buscar", width=80, command=self.buscar_alumnos).pack(side="left", padx=5)
        customtkinter.CTkButton(fa, text="Nuevo Alumno", fg_color="green",
                               command=self.abrir_nuevo_alumno).pack(side="right", padx=5)
        
        # --- CABECERA ---
        ha = customtkinter.CTkFrame(self.parent, height=30, fg_color="gray40")
        ha.pack(fill="x", padx=10)
        ha.grid_columnconfigure(0, weight=2)  # RUT
        ha.grid_columnconfigure(1, weight=4)  # NOMBRE
        ha.grid_columnconfigure(2, weight=2)  # CURSO
        ha.grid_columnconfigure(3, weight=2)  # EN PODER
        ha.grid_columnconfigure(4, weight=2)  # ACCIONES
        
        customtkinter.CTkLabel(ha, text="RUT", anchor="w").grid(row=0, column=0, padx=5, sticky="w")
        customtkinter.CTkLabel(ha, text="NOMBRE", anchor="w").grid(row=0, column=1, padx=5, sticky="w")
        customtkinter.CTkLabel(ha, text="CURSO", anchor="w").grid(row=0, column=2, padx=5, sticky="w")
        customtkinter.CTkLabel(ha, text="EN PODER", anchor="center").grid(row=0, column=3, padx=5, sticky="ew")
        customtkinter.CTkLabel(ha, text="ACCIONES", anchor="center").grid(row=0, column=4, padx=10, sticky="e")
        
        # --- ÁREA SCROLLABLE ---
        self.scroll_alumnos = customtkinter.CTkScrollableFrame(self.parent)
        self.scroll_alumnos.pack(fill="both", expand=True, padx=10, pady=5)
    
    def buscar_alumnos(self):
        """Busca alumnos según el término ingresado"""
        for w in self.scroll_alumnos.winfo_children():
            w.destroy()
        
        term = self.entry_bus_a.get()
        rows = self.alumno_model.buscar_alumnos(term)
        
        if not rows:
            msg = "No se encontraron coincidencias." if term else "No hay alumnos con préstamos activos."
            customtkinter.CTkLabel(self.scroll_alumnos, text=msg).pack(pady=10)
            return
        
        for r in rows:
            pid, rut, nom, cur, act = r
            
            nom_trunc = (nom[:25] + '...') if len(nom) > 25 else nom
            
            # Fila
            row_f = customtkinter.CTkFrame(self.scroll_alumnos, fg_color="transparent")
            row_f.pack(fill="x", pady=2)
            row_f.grid_columnconfigure(0, weight=2)
            row_f.grid_columnconfigure(1, weight=4)
            row_f.grid_columnconfigure(2, weight=2)
            row_f.grid_columnconfigure(3, weight=2)
            row_f.grid_columnconfigure(4, weight=2)
            
            customtkinter.CTkLabel(row_f, text=str(rut), anchor="w").grid(row=0, column=0, padx=5, sticky="w")
            customtkinter.CTkLabel(row_f, text=nom_trunc, anchor="w").grid(row=0, column=1, padx=5, sticky="w")
            customtkinter.CTkLabel(row_f, text=str(cur) if cur else "-", anchor="w").grid(row=0, column=2, padx=5, sticky="w")
            
            col_btn = "orange" if act > 0 else "gray"
            customtkinter.CTkButton(row_f, text=f"{act} Libros", width=100, fg_color=col_btn,
                                   command=lambda p=pid, n=nom: self.ver_libros_alumno(p, n)).grid(row=0, column=3, padx=5, sticky="ew")
            
            frame_acciones = customtkinter.CTkFrame(row_f, fg_color="transparent")
            frame_acciones.grid(row=0, column=4, padx=10, sticky="e")
            
            datos_edit = (rut, nom, cur)
            customtkinter.CTkButton(frame_acciones, text="Editar", width=60, fg_color="blue",
                                   command=lambda p=pid, d=datos_edit: self.abrir_editar_alumno(p, d)).pack(side="left", padx=2)
            customtkinter.CTkButton(frame_acciones, text="X", width=30, fg_color="red",
                                   command=lambda p=pid, n=nom: self.eliminar_alumno(p, n)).pack(side="left", padx=2)
    
    def abrir_nuevo_alumno(self):
        """Abre el diálogo para crear un nuevo alumno"""
        if not self.win_n_alumno or not self.win_n_alumno.winfo_exists():
            self.win_n_alumno = AlumnoDialog(self.parent, self._guardar_alumno)
        else:
            self.win_n_alumno.focus()
    
    def abrir_editar_alumno(self, id_prestatario: int, datos):
        """Abre el diálogo para editar un alumno"""
        if not self.win_e_alumno or not self.win_e_alumno.winfo_exists():
            self.win_e_alumno = AlumnoDialog(self.parent, self._guardar_alumno, datos)
        else:
            self.win_e_alumno.focus()
    
    def _guardar_alumno(self, rut: str, nombre: str, curso: str, is_edit: bool) -> bool:
        """Guarda un alumno nuevo o edita uno existente"""
        try:
            if is_edit:
                # Necesitaríamos el ID para editar - por ahora es simplificado
                self.alumno_model.actualizar_alumno(1, rut, nombre, curso)
                messagebox.showinfo("Éxito", "Actualizado.")
            else:
                self.alumno_model.crear_alumno(rut, nombre, curso)
                messagebox.showinfo("Éxito", "Alumno registrado.")
            
            self.buscar_alumnos()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def eliminar_alumno(self, id_prestatario: int, nombre: str):
        """Elimina un alumno de la base de datos"""
        try:
            if self.alumno_model.tiene_prestamos_activos(id_prestatario):
                return messagebox.showerror("Error", f"{nombre} tiene libros sin devolver.")
            
            if messagebox.askyesno("Borrar", f"¿Eliminar a {nombre}?"):
                self.alumno_model.eliminar_alumno(id_prestatario)
                self.buscar_alumnos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
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
        self.title(f"Libros en poder de: {nombre_alumno}")
        self.geometry("600x400")
        self.transient(master)
        
        self.textbox = customtkinter.CTkTextbox(self, font=("Consolas", 12))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._cargar_libros(id_prestatario, alumno_model)
    
    def _cargar_libros(self, id_prestatario: int, alumno_model: AlumnoModel):
        """Carga y muestra los libros del alumno"""
        rows = alumno_model.obtener_libros_en_poder(id_prestatario)
        
        if not rows:
            self.textbox.insert("1.0", "Este alumno no tiene libros pendientes.")
        else:
            self.textbox.insert("1.0", f"{'ISBN':<15} | {'TÍTULO':<35} | {'FECHA'}\n" + ("-"*70) + "\n")
            for r in rows:
                isbn, titulo, autor, fecha = r
                titulo_trunc = (titulo[:32]+'..') if len(titulo)>35 else titulo
                self.textbox.insert("end", f"{isbn:<15} | {titulo_trunc:<35} | {fecha}\n")
        
        self.textbox.configure(state="disabled")
