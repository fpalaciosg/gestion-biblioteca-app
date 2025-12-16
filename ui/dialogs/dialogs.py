"""
Módulo de Dialogs - Ventanas emergentes para crear/editar datos
"""
import customtkinter
from tkinter import messagebox
from typing import Optional, Callable
from utils.theme import Colors, Styles


class LibroDialog(customtkinter.CTkToplevel):
    """Diálogo para crear o editar un libro"""
    
    def __init__(self, master, on_save: Callable, datos_actuales: Optional[tuple] = None):
        super().__init__(master)
        self.title("📖 Registrar Nuevo Libro" if not datos_actuales else "✏️ Editar Libro")
        self.geometry("550x600")
        self.transient(master)
        self.grab_set()
        self.lift()
        
        # Aplicar tema
        self.configure(fg_color=Colors.BG_DARK)
        
        self.on_save = on_save
        self.datos_actuales = datos_actuales
        self.is_edit = datos_actuales is not None
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz del diálogo"""
        # Marco principal
        self.frame = customtkinter.CTkFrame(self, fg_color=Colors.BG_DARK)
        self.frame.pack(pady=Styles.PADDING_LG, padx=Styles.PADDING_LG, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1)
        
        if self.is_edit:
            campos = ["ISBN", "Título", "Autor", "Editorial", "Año_Publicacion", "Categoría"]
        else:
            campos = ["Título:", "Autor:", "ISBN:", "Editorial:", "Año Publicación:", 
                     "Categoría:", "Nº Ejemplares:"]
        
        self.entries = {}
        for i, label_text in enumerate(campos):
            # Etiqueta
            lbl = customtkinter.CTkLabel(
                self.frame,
                text=label_text,
                text_color=Colors.TEXT_PRIMARY,
                font=Styles.FONT_REGULAR
            )
            lbl.grid(row=i, column=0, sticky="w", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
            
            # Entry
            entry = customtkinter.CTkEntry(
                self.frame,
                fg_color=Colors.BG_TERTIARY,
                border_color=Colors.BORDER_ACCENT,
                text_color=Colors.TEXT_PRIMARY,
                placeholder_text_color=Colors.TEXT_TERTIARY
            )
            entry.grid(row=i, column=1, padx=Styles.PADDING_MD, pady=Styles.PADDING_MD, sticky="ew")
            
            if self.is_edit and i < len(self.datos_actuales):
                entry.insert(0, str(self.datos_actuales[i]))
            
            self.entries[label_text] = entry
        
        # Botón guardar
        btn_text = "💾 Guardar Cambios" if self.is_edit else "💾 Guardar"
        customtkinter.CTkButton(
            self.frame,
            text=btn_text,
            fg_color=Colors.SECONDARY,
            hover_color=Colors.SECONDARY_LIGHT,
            text_color=Colors.TEXT_INVERSE,
            corner_radius=Styles.CORNER_RADIUS_SMALL,
            font=Styles.FONT_BOLD,
            command=self._guardar
        ).grid(row=len(campos) + 1, column=0, columnspan=2, pady=Styles.PADDING_LG, sticky="ew")
    
    def _guardar(self):
        """Valida y guarda los datos"""
        datos = {k: v.get() for k, v in self.entries.items()}
        
        # Validación básica
        if self.is_edit:
            if not datos["ISBN"] or not datos["Título"]:
                return messagebox.showerror("❌ Error", "ISBN y Título obligatorios.", parent=self)
        else:
            if not datos["ISBN:"] or not datos["Título:"]:
                return messagebox.showerror("❌ Error", "Título y ISBN obligatorios.", parent=self)
            try:
                ejemplares = int(datos.get("Nº Ejemplares:", "1"))
                if ejemplares <= 0:
                    raise ValueError
            except:
                return messagebox.showerror("❌ Error", "Ejemplares debe ser número positivo.", parent=self)
        
        # Llamar callback con datos
        if self.on_save(datos, self.is_edit):
            self.destroy()


class AlumnoDialog(customtkinter.CTkToplevel):
    """Diálogo para crear o editar un alumno"""
    
    def __init__(self, master, on_save: Callable, datos_actuales: Optional[tuple] = None):
        super().__init__(master)
        self.title("👤 Registrar Alumno" if not datos_actuales else "✏️ Editar Alumno")
        self.geometry("450x300")
        self.transient(master)
        self.grab_set()
        
        # Aplicar tema
        self.configure(fg_color=Colors.BG_DARK)
        
        self.on_save = on_save
        self.datos_actuales = datos_actuales
        self.is_edit = datos_actuales is not None
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz del diálogo"""
        # Marco principal
        self.frame = customtkinter.CTkFrame(self, fg_color=Colors.BG_DARK)
        self.frame.pack(pady=Styles.PADDING_LG, padx=Styles.PADDING_LG, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1)
        
        # RUT
        lbl_rut = customtkinter.CTkLabel(
            self.frame,
            text="RUT:",
            text_color=Colors.TEXT_PRIMARY,
            font=Styles.FONT_REGULAR
        )
        lbl_rut.grid(row=0, column=0, sticky="w", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
        
        self.entry_rut = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="12.345.678-9",
            fg_color=Colors.BG_TERTIARY,
            border_color=Colors.BORDER_ACCENT,
            text_color=Colors.TEXT_PRIMARY,
            placeholder_text_color=Colors.TEXT_TERTIARY
        )
        self.entry_rut.grid(row=0, column=1, sticky="ew", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
        
        # Nombre
        lbl_nom = customtkinter.CTkLabel(
            self.frame,
            text="Nombre:",
            text_color=Colors.TEXT_PRIMARY,
            font=Styles.FONT_REGULAR
        )
        lbl_nom.grid(row=1, column=0, sticky="w", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
        
        self.entry_nom = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="Nombre completo",
            fg_color=Colors.BG_TERTIARY,
            border_color=Colors.BORDER_ACCENT,
            text_color=Colors.TEXT_PRIMARY,
            placeholder_text_color=Colors.TEXT_TERTIARY
        )
        self.entry_nom.grid(row=1, column=1, sticky="ew", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
        
        # Curso
        lbl_curso = customtkinter.CTkLabel(
            self.frame,
            text="Curso:",
            text_color=Colors.TEXT_PRIMARY,
            font=Styles.FONT_REGULAR
        )
        lbl_curso.grid(row=2, column=0, sticky="w", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
        
        self.entry_curso = customtkinter.CTkEntry(
            self.frame,
            placeholder_text="2°B",
            fg_color=Colors.BG_TERTIARY,
            border_color=Colors.BORDER_ACCENT,
            text_color=Colors.TEXT_PRIMARY,
            placeholder_text_color=Colors.TEXT_TERTIARY
        )
        self.entry_curso.grid(row=2, column=1, sticky="ew", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
        
        # Cargar datos si es edición
        if self.is_edit and self.datos_actuales:
            self.entry_rut.insert(0, self.datos_actuales[0])
            self.entry_nom.insert(0, self.datos_actuales[1])
            self.entry_curso.insert(0, self.datos_actuales[2])
        
        # Botón guardar
        btn_text = "💾 Guardar Cambios" if self.is_edit else "💾 Guardar"
        customtkinter.CTkButton(
            self.frame,
            text=btn_text,
            fg_color=Colors.INFO,
            hover_color="#4291B5",
            text_color=Colors.TEXT_INVERSE,
            corner_radius=Styles.CORNER_RADIUS_SMALL,
            font=Styles.FONT_BOLD,
            command=self._guardar
        ).grid(row=3, column=0, columnspan=2, pady=Styles.PADDING_LG, sticky="ew")
    
    def _guardar(self):
        """Valida y guarda los datos"""
        rut = self.entry_rut.get()
        nom = self.entry_nom.get()
        curso = self.entry_curso.get()
        
        if not rut or not nom:
            return messagebox.showerror("❌ Error", "RUT y Nombre obligatorios.", parent=self)
        
        if self.on_save():
            self.destroy()
