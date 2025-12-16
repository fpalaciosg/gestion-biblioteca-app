"""
Pestaña de Préstamos - Interfaz para registrar préstamos y devoluciones
"""
import customtkinter
from tkinter import messagebox
from models.libro import LibroModel
from models.alumno import AlumnoModel
from models.transaccion import TransaccionModel


class PrestamosTab:
    """Construye y gestiona la pestaña de Préstamos"""
    
    def __init__(self, parent_tab, libro_model: LibroModel, alumno_model: AlumnoModel, 
                 transaccion_model: TransaccionModel):
        self.parent = parent_tab
        self.libro_model = libro_model
        self.alumno_model = alumno_model
        self.transaccion_model = transaccion_model
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz de la pestaña"""
        self.parent.grid_columnconfigure(0, weight=10)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, weight=10)
        self.parent.grid_rowconfigure(0, weight=1)
        
        # --- FRAME PRÉSTAMO ---
        fp = customtkinter.CTkFrame(self.parent, corner_radius=15, border_width=2, border_color="#3B8ED0")
        fp.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        fp.grid_columnconfigure(1, weight=1)
        
        customtkinter.CTkLabel(fp, text="📤 REALIZAR PRÉSTAMO", font=("Arial", 18, "bold"), 
                              text_color="#3B8ED0").grid(row=0, columnspan=2, pady=(20, 10))
        
        customtkinter.CTkLabel(fp, text="RUT Alumno:").grid(row=2, column=0, sticky="w", padx=20)
        self.entry_p_rut = customtkinter.CTkEntry(fp, placeholder_text="Ej: 12345678-9")
        self.entry_p_rut.grid(row=2, column=1, sticky="ew", padx=20, pady=10)
        
        customtkinter.CTkLabel(fp, text="ISBN/Título:").grid(row=3, column=0, sticky="w", padx=20)
        self.entry_p_isbn = customtkinter.CTkEntry(fp, placeholder_text="Escanee o escriba...")
        self.entry_p_isbn.grid(row=3, column=1, sticky="ew", padx=20, pady=10)
        
        customtkinter.CTkButton(fp, text="CONFIRMAR PRÉSTAMO", fg_color="#3B8ED0", height=40,
                               command=self.realizar_prestamo).grid(row=4, columnspan=2, pady=30, padx=20, sticky="ew")
        
        # --- SEPARADOR ---
        customtkinter.CTkFrame(self.parent, width=2, fg_color="gray40").grid(row=0, column=1, sticky="ns", pady=40)
        
        # --- FRAME DEVOLUCIÓN ---
        fd = customtkinter.CTkFrame(self.parent, corner_radius=15, border_width=2, border_color="#2CC985")
        fd.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
        fd.grid_columnconfigure(1, weight=1)
        
        customtkinter.CTkLabel(fd, text="📥 REGISTRAR DEVOLUCIÓN", font=("Arial", 18, "bold"),
                              text_color="#2CC985").grid(row=0, columnspan=2, pady=(20, 10))
        
        customtkinter.CTkLabel(fd, text="ISBN/Título:").grid(row=2, column=0, sticky="w", padx=20)
        self.entry_d_isbn = customtkinter.CTkEntry(fd, placeholder_text="Libro a devolver...")
        self.entry_d_isbn.grid(row=2, column=1, sticky="ew", padx=20, pady=10)
        
        customtkinter.CTkButton(fd, text="CONFIRMAR DEVOLUCIÓN", fg_color="#2CC985", height=40,
                               command=self.realizar_devolucion).grid(row=4, columnspan=2, pady=30, padx=20, sticky="ew")
    
    def realizar_prestamo(self):
        """Realiza un préstamo de un libro a un alumno"""
        rut = self.entry_p_rut.get()
        item = self.entry_p_isbn.get()
        
        if not rut or not item:
            return messagebox.showerror("Error", "Datos incompletos.")
        
        try:
            # Buscar alumno
            res_a = self.alumno_model.obtener_alumno_por_rut(rut)
            if not res_a:
                return messagebox.showerror("Error", "Alumno no encontrado.")
            
            pid, pnom = res_a
            
            # Buscar libro
            res_l = self.libro_model.obtener_libro_por_titulo_o_isbn(item)
            if not res_l:
                return messagebox.showerror("Error", "Libro no disponible.")
            
            lid, ltit, _ = res_l
            
            # Verificar préstamo duplicado
            if self.transaccion_model.existe_prestamo_duplicado(lid, pid):
                return messagebox.showerror("Error", "Préstamo duplicado.")
            
            # Realizar préstamo
            self.libro_model.restar_disponibles(lid)
            self.transaccion_model.crear_prestamo(lid, pid)
            
            messagebox.showinfo("Éxito", f"Préstamo: {ltit} -> {pnom}")
            self.entry_p_rut.delete(0, "end")
            self.entry_p_isbn.delete(0, "end")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def realizar_devolucion(self):
        """Registra la devolución de un libro"""
        item = self.entry_d_isbn.get()
        
        if not item:
            return messagebox.showerror("Error", "Ingrese ISBN o Título.")
        
        try:
            # Buscar libro
            res = self.libro_model.obtener_libro_por_titulo_o_isbn(item)
            if not res:
                return messagebox.showerror("Error", "Libro no encontrado.")
            
            lid, ltit, _ = res
            
            # Buscar préstamo activo
            res_t = self.transaccion_model.obtener_prestamo_activo(lid)
            if not res_t:
                return messagebox.showerror("Error", "No hay préstamo activo.")
            
            tid = res_t[0]
            
            # Registrar devolución
            self.transaccion_model.registrar_devolucion(tid)
            self.libro_model.sumar_disponibles(lid)
            
            messagebox.showinfo("Éxito", f"Devuelto: {ltit}")
            self.entry_d_isbn.delete(0, "end")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
