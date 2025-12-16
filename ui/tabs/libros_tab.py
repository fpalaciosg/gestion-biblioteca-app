"""
Pestaña de Libros - Interfaz para gestionar el catálogo de libros
"""
import customtkinter
from tkinter import messagebox
from models.libro import LibroModel
from ui.dialogs.dialogs import LibroDialog
from utils.theme import Colors, Styles


class LibrosTab:
    """Construye y gestiona la pestaña de Libros"""
    
    def __init__(self, parent_tab, libro_model: LibroModel):
        self.parent = parent_tab
        self.libro_model = libro_model
        self.win_e_libro = None
        self.win_n_libro = None
        self.parent.configure(fg_color=Colors.BG_DARK)
        
        self._build_ui()
        self.buscar_libros()  # Cargar inicial
    
    def _build_ui(self):
        """Construye la interfaz de la pestaña"""
        # --- BARRA DE BÚSQUEDA ---
        fl = customtkinter.CTkFrame(self.parent, fg_color=Colors.BG_SECONDARY,
                                   corner_radius=Styles.CORNER_RADIUS_SMALL)
        fl.pack(fill="x", padx=Styles.PADDING_LG, pady=Styles.PADDING_LG)
        
        customtkinter.CTkLabel(fl, text="🔍 Buscar:", text_color=Colors.TEXT_PRIMARY,
                              font=Styles.FONT_REGULAR).pack(side="left", padx=Styles.PADDING_MD)
        self.entry_bus_l = customtkinter.CTkEntry(fl, placeholder_text="Nombre del libro...",
                                                  fg_color=Colors.BG_TERTIARY,
                                                  border_color=Colors.BORDER_ACCENT,
                                                  text_color=Colors.TEXT_PRIMARY,
                                                  placeholder_text_color=Colors.TEXT_TERTIARY)
        self.entry_bus_l.pack(side="left", fill="x", expand=True, padx=Styles.PADDING_MD)
        
        customtkinter.CTkButton(fl, text="🔎 Buscar", width=100, fg_color=Colors.PRIMARY,
                               hover_color=Colors.PRIMARY_LIGHT, text_color=Colors.TEXT_INVERSE,
                               corner_radius=Styles.CORNER_RADIUS_SMALL,
                               command=self.buscar_libros).pack(side="left", padx=Styles.PADDING_SM)
        customtkinter.CTkButton(fl, text="➕ Nuevo / Stock", fg_color=Colors.SECONDARY,
                               hover_color=Colors.SECONDARY_LIGHT, text_color=Colors.TEXT_INVERSE,
                               corner_radius=Styles.CORNER_RADIUS_SMALL,
                               command=self.abrir_nuevo_libro).pack(side="right", padx=Styles.PADDING_MD)
        
        # --- CABECERA ---
        hl = customtkinter.CTkFrame(self.parent, height=40, fg_color=Colors.PRIMARY,
                                   corner_radius=Styles.CORNER_RADIUS_SMALL)
        hl.pack(fill="x", padx=Styles.PADDING_LG, pady=(0, Styles.PADDING_SM))
        hl.pack_propagate(False)
        hl.grid_columnconfigure(0, weight=2)  # ISBN
        hl.grid_columnconfigure(1, weight=5)  # TÍTULO
        hl.grid_columnconfigure(2, weight=4)  # AUTOR
        hl.grid_columnconfigure(3, weight=1)  # DISP/TOT
        hl.grid_columnconfigure(4, weight=2)  # ACCIONES
        
        customtkinter.CTkLabel(hl, text="ISBN", anchor="w", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=0, padx=Styles.PADDING_MD, sticky="w")
        customtkinter.CTkLabel(hl, text="TÍTULO", anchor="w", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=1, padx=Styles.PADDING_MD, sticky="w")
        customtkinter.CTkLabel(hl, text="AUTOR", anchor="w", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=2, padx=Styles.PADDING_MD, sticky="w")
        customtkinter.CTkLabel(hl, text="DISP/TOT", anchor="center", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=3, padx=Styles.PADDING_MD, sticky="ew")
        customtkinter.CTkLabel(hl, text="ACCIONES", anchor="center", text_color=Colors.TEXT_INVERSE,
                              font=Styles.FONT_BOLD).grid(row=0, column=4, padx=Styles.PADDING_MD, sticky="e")
        
        # --- ÁREA SCROLLABLE ---
        self.scroll_libros = customtkinter.CTkScrollableFrame(self.parent, fg_color=Colors.BG_DARK)
        self.scroll_libros.pack(fill="both", expand=True, padx=Styles.PADDING_LG, pady=(0, Styles.PADDING_LG))
        self.scroll_libros.grid_columnconfigure(0, weight=2)
        self.scroll_libros.grid_columnconfigure(1, weight=5)
        self.scroll_libros.grid_columnconfigure(2, weight=4)
        self.scroll_libros.grid_columnconfigure(3, weight=1)
        self.scroll_libros.grid_columnconfigure(4, weight=2)
    
    def buscar_libros(self):
        """Busca libros según el término ingresado"""
        for w in self.scroll_libros.winfo_children():
            w.destroy()
        
        term = self.entry_bus_l.get()
        rows = self.libro_model.buscar_libros(term)
        
        if not rows:
            msg = "📭 No se encontraron coincidencias." if term else "📭 No hay libros con préstamos activos."
            customtkinter.CTkLabel(self.scroll_libros, text=msg, text_color=Colors.TEXT_SECONDARY,
                                  font=Styles.FONT_REGULAR).pack(pady=Styles.PADDING_XL)
            return
        
        for idx, r in enumerate(rows):
            lid, isbn, tit, aut, edit, anio, cat, tot, disp = r
            
            tit_trunc = (tit[:35] + '...') if len(tit) > 35 else tit
            aut_trunc = (aut[:25] + '...') if len(aut) > 25 else aut
            
            # Colores según disponibilidad
            color_text = Colors.TEXT_PRIMARY if disp > 0 else Colors.WARNING
            
            customtkinter.CTkLabel(self.scroll_libros, text=str(isbn), anchor="w", 
                                  text_color=color_text, font=Styles.FONT_REGULAR).grid(
                row=idx, column=0, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="w"
            )
            customtkinter.CTkLabel(self.scroll_libros, text=tit_trunc, anchor="w", 
                                  text_color=color_text, font=Styles.FONT_REGULAR).grid(
                row=idx, column=1, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="w"
            )
            customtkinter.CTkLabel(self.scroll_libros, text=aut_trunc, anchor="w", 
                                  text_color=Colors.TEXT_SECONDARY, font=Styles.FONT_REGULAR).grid(
                row=idx, column=2, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="w"
            )
            customtkinter.CTkLabel(self.scroll_libros, text=f"{disp}/{tot}", anchor="center",
                                  text_color=color_text, font=Styles.FONT_BOLD).grid(
                row=idx, column=3, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="ew"
            )
            
            frame_acciones = customtkinter.CTkFrame(self.scroll_libros, fg_color="transparent")
            frame_acciones.grid(row=idx, column=4, padx=Styles.PADDING_MD, pady=Styles.PADDING_SM, sticky="e")
            
            datos_para_editar = (isbn, tit, aut, edit, anio, cat)
            customtkinter.CTkButton(frame_acciones, text="✏️ Editar", width=80, fg_color=Colors.PRIMARY,
                                   hover_color=Colors.PRIMARY_LIGHT, text_color=Colors.TEXT_INVERSE,
                                   corner_radius=Styles.CORNER_RADIUS_SMALL,
                                   command=lambda i=lid, d=datos_para_editar: self.abrir_editar_libro(i, d)).pack(side="left", padx=Styles.PADDING_SM)
            customtkinter.CTkButton(frame_acciones, text="🗑️", width=40, fg_color=Colors.DANGER,
                                   hover_color="#B02020", text_color=Colors.TEXT_INVERSE,
                                   corner_radius=Styles.CORNER_RADIUS_SMALL,
                                   command=lambda i=lid, t=tit: self.eliminar_libro(i, t)).pack(side="left", padx=Styles.PADDING_SM)
    
    def abrir_nuevo_libro(self):
        """Abre el diálogo para crear un nuevo libro"""
        if not self.win_n_libro or not self.win_n_libro.winfo_exists():
            self.win_n_libro = LibroDialog(self.parent, self._guardar_libro)
        else:
            self.win_n_libro.focus()
    
    def abrir_editar_libro(self, id_libro: int, datos):
        """Abre el diálogo para editar un libro"""
        if not self.win_e_libro or not self.win_e_libro.winfo_exists():
            self.win_e_libro = LibroDialog(self.parent, self._guardar_libro, datos)
        else:
            self.win_e_libro.focus()
    
    def _guardar_libro(self, datos: dict, is_edit: bool) -> bool:
        """Guarda un libro nuevo o edita uno existente"""
        try:
            if is_edit:
                # Edición
                isbn = datos.get("ISBN", "")
                titulo = datos.get("Título", "")
                autor = datos.get("Autor", "")
                editorial = datos.get("Editorial", "")
                anio = datos.get("Año_Publicacion", "")
                categoria = datos.get("Categoría", "")
                
                # Aquí necesitarías el ID del libro para editar
                # Por ahora asumimos que se actualiza por ISBN
                self.libro_model.actualizar_libro(1, isbn, titulo, autor, editorial, anio, categoria)
                messagebox.showinfo("Ok", "Libro actualizado.")
            else:
                # Creación
                isbn = datos.get("ISBN:", "")
                titulo = datos.get("Título:", "")
                autor = datos.get("Autor:", "")
                editorial = datos.get("Editorial:", "")
                anio = datos.get("Año Publicación:", "")
                categoria = datos.get("Categoría:", "")
                ejemplares = int(datos.get("Nº Ejemplares (a sumar):", "1"))
                
                # Verificar si ISBN existe
                if self.libro_model.obtener_libro_por_isbn(isbn):
                    if messagebox.askyesno("Stock", f"ISBN existente. ¿Sumar {ejemplares} copias?"):
                        self.libro_model.sumar_ejemplares(isbn, ejemplares)
                        messagebox.showinfo("Ok", "Stock sumado.")
                else:
                    self.libro_model.crear_libro(isbn, titulo, autor, editorial, anio, categoria, ejemplares)
                    messagebox.showinfo("Ok", "Libro creado.")
            
            self.buscar_libros()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def eliminar_libro(self, id_libro: int, titulo: str):
        """Elimina un libro de la base de datos"""
        try:
            if self.libro_model.tiene_prestamos_activos(id_libro):
                return messagebox.showerror("Error", f"'{titulo}' tiene préstamos activos.")
            
            if messagebox.askyesno("Borrar", f"¿Eliminar '{titulo}'?"):
                self.libro_model.eliminar_libro(id_libro)
                self.buscar_libros()
        except Exception as e:
            messagebox.showerror("Error", str(e))
