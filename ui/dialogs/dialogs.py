"""
Módulo de Dialogs - Ventanas emergentes para crear/editar datos
"""
import customtkinter
from tkinter import messagebox
from typing import Optional, Callable

class LibroDialog(customtkinter.CTkToplevel):
    """Diálogo para crear o editar un libro"""
    
    def __init__(self, master, on_save: Callable, datos_actuales: Optional[tuple] = None):
        super().__init__(master)
        self.title("Registrar Nuevo Libro / Stock" if not datos_actuales else "Editar Libro")
        self.geometry("500x550")
        self.transient(master)
        self.grab_set()
        self.lift()
        
        self.on_save = on_save
        self.datos_actuales = datos_actuales
        self.is_edit = datos_actuales is not None
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz del diálogo"""
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1)
        
        if self.is_edit:
            campos = ["ISBN", "Título", "Autor", "Editorial", "Año_Publicacion", "Categoría"]
        else:
            campos = ["Título:", "Autor:", "ISBN:", "Editorial:", "Año Publicación:", 
                     "Categoría:", "Nº Ejemplares (a sumar):"]
        
        self.entries = {}
        for i, label_text in enumerate(campos):
            customtkinter.CTkLabel(self.frame, text=label_text).grid(
                row=i, column=0, sticky="w", padx=10, pady=5
            )
            entry = customtkinter.CTkEntry(self.frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            
            if self.is_edit and i < len(self.datos_actuales):
                entry.insert(0, str(self.datos_actuales[i]))
            
            self.entries[label_text] = entry
        
        btn_text = "Guardar Cambios" if self.is_edit else "Guardar"
        customtkinter.CTkButton(
            self.frame, text=btn_text, command=self._guardar
        ).grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)
    
    def _guardar(self):
        """Valida y guarda los datos"""
        datos = {k: v.get() for k, v in self.entries.items()}
        
        # Validación básica
        if self.is_edit:
            if not datos["ISBN"] or not datos["Título"]:
                return messagebox.showerror("Error", "ISBN y Título obligatorios.", parent=self)
        else:
            if not datos["ISBN:"] or not datos["Título:"]:
                return messagebox.showerror("Error", "Título y Autor obligatorios.", parent=self)
            try:
                ejemplares = int(datos.get("Nº Ejemplares (a sumar):", "1"))
                if ejemplares <= 0:
                    raise ValueError
            except:
                return messagebox.showerror("Error", "Ejemplares debe ser número positivo.", parent=self)
        
        # Llamar callback con datos
        if self.on_save(datos, self.is_edit):
            self.destroy()


class AlumnoDialog(customtkinter.CTkToplevel):
    """Diálogo para crear o editar un alumno"""
    
    def __init__(self, master, on_save: Callable, datos_actuales: Optional[tuple] = None):
        super().__init__(master)
        self.title("Registrar Alumno" if not datos_actuales else "Editar Alumno")
        self.geometry("400x250")
        self.transient(master)
        self.grab_set()
        
        self.on_save = on_save
        self.datos_actuales = datos_actuales
        self.is_edit = datos_actuales is not None
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz del diálogo"""
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(1, weight=1)
        
        # RUT
        customtkinter.CTkLabel(self.frame, text="RUT:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_rut = customtkinter.CTkEntry(
            self.frame, placeholder_text="12.345.678-9"
        )
        self.entry_rut.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # Nombre
        customtkinter.CTkLabel(self.frame, text="Nombre:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_nom = customtkinter.CTkEntry(
            self.frame, placeholder_text="Francisco Palacios González"
        )
        self.entry_nom.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Curso
        customtkinter.CTkLabel(self.frame, text="Curso:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_curso = customtkinter.CTkEntry(
            self.frame, placeholder_text="2°B"
        )
        self.entry_curso.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        if self.is_edit and self.datos_actuales:
            self.entry_rut.insert(0, self.datos_actuales[0])
            self.entry_nom.insert(0, self.datos_actuales[1])
            self.entry_curso.insert(0, self.datos_actuales[2])
        
        btn_text = "Guardar Cambios" if self.is_edit else "Guardar"
        customtkinter.CTkButton(
            self.frame, text=btn_text, command=self._guardar
        ).grid(row=3, column=0, columnspan=2, pady=20)
    
    def _guardar(self):
        """Valida y guarda los datos"""
        rut = self.entry_rut.get()
        nom = self.entry_nom.get()
        curso = self.entry_curso.get()
        
        if not rut or not nom:
            return messagebox.showerror("Error", "RUT y Nombre obligatorios.", parent=self)
        
        if self.on_save(rut, nom, curso, self.is_edit):
            self.destroy()
