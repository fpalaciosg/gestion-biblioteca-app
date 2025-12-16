"""
Pestaña de Préstamos - Interfaz para registrar préstamos y devoluciones
"""
import customtkinter
from tkinter import messagebox
from models.libro import LibroModel
from models.alumno import AlumnoModel
from models.transaccion import TransaccionModel
from utils.theme import Colors, Styles


class PrestamosTab:
    """Construye y gestiona la pestaña de Préstamos"""
    
    def __init__(self, parent_tab, libro_model: LibroModel, alumno_model: AlumnoModel, 
                 transaccion_model: TransaccionModel):
        self.parent = parent_tab
        self.libro_model = libro_model
        self.alumno_model = alumno_model
        self.transaccion_model = transaccion_model
        self.parent.configure(fg_color=Colors.BG_DARK)
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz de la pestaña"""
        self.parent.grid_columnconfigure(0, weight=10)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, weight=10)
        self.parent.grid_rowconfigure(0, weight=1)
        
        # --- FRAME PRÉSTAMO ---
        fp = customtkinter.CTkFrame(self.parent, corner_radius=Styles.CORNER_RADIUS_LARGE, 
                                   border_width=2, border_color=Colors.SECONDARY,
                                   fg_color=Colors.BG_SECONDARY)
        fp.grid(row=0, column=0, padx=Styles.PADDING_LG, pady=Styles.PADDING_LG, sticky="nsew")
        fp.grid_columnconfigure(1, weight=1)
        
        customtkinter.CTkLabel(fp, text="📤 REALIZAR PRÉSTAMO", font=("Segoe UI", 18, "bold"), 
                              text_color=Colors.SECONDARY).grid(row=0, columnspan=2, pady=(Styles.PADDING_XL, Styles.PADDING_LG))
        
        customtkinter.CTkLabel(fp, text="RUT Alumno:", text_color=Colors.TEXT_PRIMARY,
                              font=Styles.FONT_REGULAR).grid(row=2, column=0, sticky="w", padx=Styles.PADDING_LG)
        self.entry_p_rut = customtkinter.CTkEntry(fp, placeholder_text="Ej: 12345678-9",
                                                  fg_color=Colors.BG_TERTIARY,
                                                  border_color=Colors.BORDER_ACCENT,
                                                  text_color=Colors.TEXT_PRIMARY,
                                                  placeholder_text_color=Colors.TEXT_TERTIARY)
        self.entry_p_rut.grid(row=2, column=1, sticky="ew", padx=Styles.PADDING_LG, pady=Styles.PADDING_SM)
        
        customtkinter.CTkLabel(fp, text="ISBN/Título:", text_color=Colors.TEXT_PRIMARY,
                              font=Styles.FONT_REGULAR).grid(row=3, column=0, sticky="w", padx=Styles.PADDING_LG)
        self.entry_p_isbn = customtkinter.CTkEntry(fp, placeholder_text="Escanee o escriba...",
                                                   fg_color=Colors.BG_TERTIARY,
                                                   border_color=Colors.BORDER_ACCENT,
                                                   text_color=Colors.TEXT_PRIMARY,
                                                   placeholder_text_color=Colors.TEXT_TERTIARY)
        self.entry_p_isbn.grid(row=3, column=1, sticky="ew", padx=Styles.PADDING_LG, pady=Styles.PADDING_SM)
        
        customtkinter.CTkButton(fp, text="✓ CONFIRMAR PRÉSTAMO", fg_color=Colors.SECONDARY,
                               hover_color=Colors.SECONDARY_LIGHT, text_color=Colors.TEXT_INVERSE,
                               height=Styles.BUTTON_HEIGHT_LG, corner_radius=Styles.CORNER_RADIUS_SMALL,
                               command=self.realizar_prestamo).grid(row=4, columnspan=2, pady=Styles.PADDING_XL, 
                                                                    padx=Styles.PADDING_LG, sticky="ew")
        
        # --- SEPARADOR ---
        customtkinter.CTkFrame(self.parent, width=2, fg_color=Colors.BORDER_LIGHT).grid(row=0, column=1, sticky="ns", pady=40)
        
        # --- FRAME DEVOLUCIÓN ---
        fd = customtkinter.CTkFrame(self.parent, corner_radius=Styles.CORNER_RADIUS_LARGE, 
                                   border_width=2, border_color=Colors.PRIMARY,
                                   fg_color=Colors.BG_SECONDARY)
        fd.grid(row=0, column=2, padx=Styles.PADDING_LG, pady=Styles.PADDING_LG, sticky="nsew")
        fd.grid_columnconfigure(1, weight=1)
        
        customtkinter.CTkLabel(fd, text="📥 REGISTRAR DEVOLUCIÓN", font=("Segoe UI", 18, "bold"),
                              text_color=Colors.PRIMARY).grid(row=0, columnspan=2, pady=(Styles.PADDING_XL, Styles.PADDING_LG))
        
        customtkinter.CTkLabel(fd, text="ISBN/Título:", text_color=Colors.TEXT_PRIMARY,
                              font=Styles.FONT_REGULAR).grid(row=2, column=0, sticky="w", padx=Styles.PADDING_LG)
        self.entry_d_isbn = customtkinter.CTkEntry(fd, placeholder_text="Libro a devolver...",
                                                   fg_color=Colors.BG_TERTIARY,
                                                   border_color=Colors.BORDER_ACCENT,
                                                   text_color=Colors.TEXT_PRIMARY,
                                                   placeholder_text_color=Colors.TEXT_TERTIARY)
        self.entry_d_isbn.grid(row=2, column=1, sticky="ew", padx=Styles.PADDING_LG, pady=Styles.PADDING_SM)
        
        customtkinter.CTkButton(fd, text="✓ CONFIRMAR DEVOLUCIÓN", fg_color=Colors.PRIMARY,
                               hover_color=Colors.PRIMARY_LIGHT, text_color=Colors.TEXT_INVERSE,
                               height=Styles.BUTTON_HEIGHT_LG, corner_radius=Styles.CORNER_RADIUS_SMALL,
                               command=self.realizar_devolucion).grid(row=4, columnspan=2, pady=Styles.PADDING_XL, 
                                                                      padx=Styles.PADDING_LG, sticky="ew")
    
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
