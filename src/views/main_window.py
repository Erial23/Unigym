import sys
import os
import ctypes
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
from .styles import *

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.title("UniGym Pro - Gestión Inteligente")
        self.geometry("1100x700")
        ctk.set_appearance_mode("Light")

        try:
            myappid = 'erickmoreno.unigympro.v1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception: pass

        if getattr(sys, 'frozen', False): self.basedir = sys._MEIPASS
        else: self.basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.assets_dir = os.path.join(self.basedir, "assets")

        try:
            ruta_icono = os.path.join(self.assets_dir, "logo.ico")
            self.iconbitmap(ruta_icono)
        except Exception: pass 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.bg_label = tk.Label(self, bd=0)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._cargar_fondo()

        # SIDEBAR CON SCROLL
        self.sidebar = ctk.CTkScrollableFrame(
            self, width=240, corner_radius=0, fg_color="#FFFFFF", border_width=0,
            scrollbar_button_color="#FFFFFF", 
            scrollbar_button_hover_color="#F2F2F2"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self._cargar_logo()
        
        self.lbl_rol_actual = ctk.CTkLabel(self.sidebar, text="👤 Rol: Ninguno", font=("Arial", 12, "bold"), text_color="#2E86C1")
        self.lbl_rol_actual.pack(pady=(0, 15))
        
        ctk.CTkLabel(self.sidebar, text="MENÚ GENERAL", font=("Arial", 11, "bold"), text_color="#999").pack(anchor="w", padx=30, pady=(10,15))
        self.btn_panel = self._btn_menu("📊  Panel Principal", self.controller.cargar_datos)
        self.btn_cargar_excel = self._btn_menu("📂  Cargar Excel", self.controller.importar_excel)
        
        ctk.CTkButton(self.sidebar, text="+  NUEVO CLIENTE", fg_color=C_VERDE_LOGO, hover_color=C_VERDE_HOVER, height=50, font=("Arial", 13, "bold"), text_color="white", corner_radius=8, command=self.controller.abrir_formulario_nuevo).pack(fill="x", padx=20, pady=(15, 5))
        
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#F0F0F0").pack(fill="x", padx=30, pady=15)
        
        ctk.CTkLabel(self.sidebar, text="COBRANZAS Y NOTAS", font=("Arial", 11, "bold"), text_color="#999").pack(anchor="w", padx=30, pady=(10,15))
        
        self.btn_pagos_realizados = ctk.CTkButton(self.sidebar, text="💰  Pagos Realizados", anchor="w", fg_color="#E8F8F5", text_color="#1ABC9C", hover_color="#D1F2EB", font=("Arial", 12, "bold"), height=40, corner_radius=8, command=self.controller.mostrar_historial_pagos)
        self.btn_pagos_realizados.pack(fill="x", padx=20, pady=5)

        self.btn_pagos_faltantes = ctk.CTkButton(self.sidebar, text="❌  Pagos Faltantes", anchor="w", fg_color="#FDEDEC", text_color="#E74C3C", hover_color="#FADBD8", font=("Arial", 12, "bold"), height=40, corner_radius=8, command=self.controller.mostrar_pagos_faltantes)
        self.btn_pagos_faltantes.pack(fill="x", padx=20, pady=5)

        self.btn_alertas = ctk.CTkButton(self.sidebar, text="⚠️  Por Terminar", anchor="w", fg_color="#FFF8E1", text_color="#F39C12", hover_color="#FFE082", font=("Arial", 12, "bold"), height=40, corner_radius=8, command=self.controller.cargar_por_terminar)
        self.btn_alertas.pack(fill="x", padx=20, pady=5)
        
        self.btn_comentarios = ctk.CTkButton(self.sidebar, text="💬  Ver Notas / Deudas", anchor="w", fg_color="#E8F8F5", text_color="#1ABC9C", hover_color="#D1F2EB", font=("Arial", 12, "bold"), height=40, corner_radius=8, command=self.controller.cargar_comentarios)
        self.btn_comentarios.pack(fill="x", padx=20, pady=5)

        self.btn_notificados = ctk.CTkButton(self.sidebar, text="📢  Notificados Hoy", anchor="w", fg_color="#EBF5FB", text_color="#2980B9", hover_color="#AED6F1", font=("Arial", 12, "bold"), height=40, corner_radius=8, command=self.controller.cargar_notificados_hoy)
        self.btn_notificados.pack(fill="x", padx=20, pady=5)

        self.btn_todos_notificados = ctk.CTkButton(self.sidebar, text="📋  Todos los Notificados", anchor="w", fg_color="#F4ECF7", text_color="#8E44AD", hover_color="#E8DAEF", font=("Arial", 12, "bold"), height=40, corner_radius=8, command=self.controller.cargar_todos_notificados)
        self.btn_todos_notificados.pack(fill="x", padx=20, pady=5)

        self.btn_whatsapp = ctk.CTkButton(
            self.sidebar, 
            text="📲  Enviar Alertas WhatsApp", 
            anchor="w", 
            fg_color="#E8F5E9", 
            text_color="#2E7D32", 
            hover_color="#C8E6C9", 
            font=("Arial", 12, "bold"), 
            height=40, 
            corner_radius=8, 
            command=self.controller.enviar_alertas_whatsapp
        )
        self.btn_whatsapp.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#F0F0F0").pack(fill="x", padx=30, pady=15)
        
        ctk.CTkLabel(self.sidebar, text="CONFIGURACIÓN", font=("Arial", 11, "bold"), text_color="#999").pack(anchor="w", padx=30, pady=(5,10))
        self.btn_cambiar_pin = self._btn_menu("🔐  Cambiar Credenciales", self.controller.cambiar_credenciales)
        self.btn_respaldo = self._btn_menu("💾  Crear Respaldo DB", self.controller.exportar_respaldo)
        self.btn_bloquear = self._btn_menu("🔒  Cerrar Sistema", self.bloquear_pantalla)

        ctk.CTkLabel(self.sidebar, text="By Erick Moreno", font=("Arial", 10), text_color="#CCC").pack(pady=40)

        # CONTENIDO PRINCIPAL
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_container.grid_rowconfigure(3, weight=1) 
        self.main_container.grid_columnconfigure(0, weight=1)

        # Encabezado con Título y Botón Exportar Excel
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.lbl_titulo = ctk.CTkLabel(self.header_frame, text="Panel de Control", font=("Arial", 28, "bold"), text_color="#333")
        self.lbl_titulo.pack(side="left")

        # BOTÓN EXPORTAR EXCEL (Superior Derecha)
        self.btn_exportar_excel = ctk.CTkButton(
            self.header_frame, 
            text="📥  EXPORTAR EXCEL", 
            fg_color="#1D6F42", # Verde Excel
            hover_color="#155231", 
            font=("Arial", 12, "bold"), 
            height=40,
            command=self.controller.exportar_clientes_excel
        )
        self.btn_exportar_excel.pack(side="right")

        self.frame_cards = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frame_cards.grid(row=1, column=0, sticky="w", pady=(0, 20))
        
        self.lbl_total = self._crear_boton_resumen(self.frame_cards, "GENERAL", "#3498DB", self.controller.cargar_datos)
        self.lbl_activos = self._crear_boton_resumen(self.frame_cards, "ACTIVOS", C_VERDE_LOGO, self.controller.cargar_activos)
        self.lbl_vencidos = self._crear_boton_resumen(self.frame_cards, "POR VENCER", C_ROJO_ALERTA, self.controller.cargar_por_terminar)
        self.lbl_inactivos = self._crear_boton_resumen(self.frame_cards, "INACTIVOS", "#95A5A6", self.controller.cargar_inactivos)

        self.search_container = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=12, height=50)
        self.search_container.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.search_container.pack_propagate(False)
        self.lbl_search_icon = ctk.CTkLabel(self.search_container, text="🔍", font=("Arial", 18), text_color="#AAA")
        self.lbl_search_icon.pack(side="left", padx=(20, 10))
        self.entry_search = ctk.CTkEntry(self.search_container, placeholder_text="Buscar cliente...", height=40, fg_color="transparent", border_width=0, text_color="#333")
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.entry_search.bind("<KeyRelease>", self.controller.buscar_cliente)

        self.frame_tabla = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=12)
        self.frame_tabla.grid(row=3, column=0, sticky="nsew")
        self._configurar_tabla()

        # ============================================================
        # 🖱️ MENÚ CONTEXTUAL ACTUALIZADO
        # ============================================================
        self.menu = tk.Menu(self, tearoff=0, bg="white", fg="#333", relief="flat", bd=1)
        self.menu.add_command(label="✅  Registrar PAGO MES ($25)", command=lambda: self.controller.renovar_seleccionado("Mensual"))
        self.menu.add_command(label="✅  Registrar PAGO DIARIO ($2)", command=lambda: self.controller.renovar_seleccionado("Diario"))
        self.menu.add_command(label="📲  Enviar Alerta WhatsApp", command=self.controller.enviar_whatsapp_individual)
        self.menu.add_separator()
        self.menu.add_command(label="✏️  Editar Cliente / Fechas", command=self.controller.abrir_formulario_editar)
        self.menu.add_separator()
        
        # Opciones de Notas
        self.menu.add_command(label="👁️  Ver Nota", command=lambda: self.controller.gestionar_comentario("ver"))
        self.menu.add_command(label="➕  Agregar Nota", command=lambda: self.controller.gestionar_comentario("editar"))
        self.menu.add_command(label="📝  Editar Nota", command=lambda: self.controller.gestionar_comentario("editar"))
        self.menu.add_command(label="🗑️  Eliminar Nota", command=lambda: self.controller.gestionar_comentario("eliminar"))
        
        self.menu.add_separator()
        self.menu.add_command(label="❌  Eliminar Cliente", command=self.controller.eliminar_seleccionado)

        self.bind("<Configure>", self._redimensionar_fondo)

        self._construir_pantalla_bloqueo()
        self.is_locked = False
        self.tiempo_inactivo = 0
        self.intentos_fallidos = 0
        self.bloqueado_hasta = 0
        self.bind_all("<Any-KeyPress>", self._reset_timer)
        self.bind_all("<Any-Button>", self._reset_timer)
        self.bind_all("<Motion>", self._reset_timer)
        self.bloquear_pantalla()

    def _construir_pantalla_bloqueo(self):
        self.frame_bloqueo = ctk.CTkFrame(self, corner_radius=0)
        self.bg_label_bloqueo = tk.Label(self.frame_bloqueo, bd=0, bg="#FFFFFF") 
        self.bg_label_bloqueo.place(x=0, y=0, relwidth=1, relheight=1)
        ruta_fondo_bloqueo = os.path.join(self.assets_dir, "pro.png")
        if os.path.exists(ruta_fondo_bloqueo):
            try: self.original_lock_bg = Image.open(ruta_fondo_bloqueo)
            except: pass
        self.blur_label = tk.Label(self.frame_bloqueo, bd=0)
        self.caja_login = ctk.CTkFrame(self.frame_bloqueo, fg_color="transparent", corner_radius=22, width=420, height=450, border_width=1, border_color="#E0E0E0")
        self.caja_login.place(relx=0.5, rely=0.5, anchor="center")
        self.caja_login.pack_propagate(False)
        ruta_logo = os.path.join(self.assets_dir, "logo.png")
        if os.path.exists(ruta_logo):
            try:
                pil_logo_central = Image.open(ruta_logo)
                self.img_candado = ctk.CTkImage(light_image=pil_logo_central, dark_image=pil_logo_central, size=(110, 110))
                self.lbl_candado = ctk.CTkLabel(self.caja_login, text="", image=self.img_candado)
            except: self.lbl_candado = ctk.CTkLabel(self.caja_login, text="🔒", font=("Arial", 70))
        else: self.lbl_candado = ctk.CTkLabel(self.caja_login, text="🔒", font=("Arial", 70))
        self.lbl_candado.pack(pady=(35, 10))
        self.lbl_lock_title = ctk.CTkLabel(self.caja_login, text="UniGym", font=("Arial", 26, "bold"), text_color="#222")
        self.lbl_lock_title.pack(pady=10)
        self.lbl_lock_sub = ctk.CTkLabel(self.caja_login, text="Ingrese su Usuario y PIN", font=("Arial", 14), text_color="#666")
        self.lbl_lock_sub.pack(pady=(0, 10))
        self.entry_user = ctk.CTkEntry(self.caja_login, placeholder_text="Usuario", width=220, height=50, justify="center", font=("Arial", 18, "bold"), fg_color="#F8F9FA", border_width=1, border_color="#D5D8DC", text_color="#333")
        self.entry_user.pack(pady=5)
        self.entry_user.bind("<Return>", lambda e: self.entry_pin.focus())
        self.entry_pin = ctk.CTkEntry(self.caja_login, placeholder_text="****", show="●", width=220, height=50, justify="center", font=("Arial", 24, "bold"), fg_color="#F8F9FA", border_width=1, border_color="#D5D8DC", text_color="#333")
        self.entry_pin.pack(pady=5)
        self.entry_pin.bind("<Return>", lambda e: self.desbloquear())
        self.btn_unlock = ctk.CTkButton(self.caja_login, text="DESBLOQUEAR", font=("Arial", 14, "bold"), height=50, width=220, fg_color=C_VERDE_LOGO, hover_color=C_VERDE_HOVER, command=self.desbloquear)
        self.btn_unlock.pack(pady=20)

    def _crear_blur_central(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 100 or h < 100:
            self.after(100, self._crear_blur_central)
            return
        if not hasattr(self, 'original_lock_bg'): return
        bg_resized = self.original_lock_bg.resize((w, h), Image.Resampling.LANCZOS)
        card_w, card_h = 420, 450
        x1, y1 = int((w - card_w) / 2), int((h - card_h) / 2)
        x2, y2 = x1 + card_w, y1 + card_h
        recorte = bg_resized.crop((x1, y1, x2, y2))
        blur = recorte.filter(ImageFilter.GaussianBlur(radius=18))
        tint = Image.new("RGBA", blur.size, (255, 255, 255, 140)) 
        glass = Image.alpha_composite(blur.convert("RGBA"), tint)
        self.blur_img = ImageTk.PhotoImage(glass)
        self.blur_label.configure(image=self.blur_img)
        self.blur_label.place(x=x1, y=y1, width=card_w, height=card_h)
        self.caja_login.tkraise()

    def bloquear_pantalla(self):
        self.is_locked = True
        self.frame_bloqueo.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_bloqueo.tkraise()
        self.entry_user.delete(0, 'end')
        self.entry_pin.delete(0, 'end')
        self.entry_user.focus()
        self._crear_blur_central()

    def desbloquear(self):
        import time
        ahora = time.time()
        if hasattr(self, 'bloqueado_hasta') and ahora < self.bloqueado_hasta:
            restante = int(self.bloqueado_hasta - ahora)
            messagebox.showerror("Bloqueo temporal", f"Demasiados intentos. Intente de nuevo en {restante} segundos.")
            return

        user_input = self.entry_user.get()
        pin_input = self.entry_pin.get()
        rol = self.controller.verificar_credenciales(user_input, pin_input)
        if rol:
            self.is_locked = False
            self.intentos_fallidos = 0
            self.frame_bloqueo.place_forget()
            self.tiempo_inactivo = 0
            self._aplicar_permisos(rol)
            self.verificar_inactividad()
        else:
            if not hasattr(self, 'intentos_fallidos'):
                self.intentos_fallidos = 0
            self.intentos_fallidos += 1
            self.entry_pin.delete(0, 'end')
            
            if self.intentos_fallidos >= 3:
                self.bloqueado_hasta = time.time() + 60
                self.intentos_fallidos = 0
                messagebox.showerror("Acceso Denegado", "PIN Incorrecto.\n\nSe ha bloqueado el acceso por 60 segundos debido a múltiples intentos fallidos.")
                self._aplicar_bloqueo_interfaz()
            else:
                intentos_restantes = 3 - self.intentos_fallidos
                messagebox.showerror("Acceso", f"PIN Incorrecto.\n\nIntentos restantes: {intentos_restantes}")

    def _aplicar_bloqueo_interfaz(self):
        self.entry_user.configure(state="disabled")
        self.entry_pin.configure(state="disabled")
        self.btn_unlock.configure(state="disabled")
        self._cuenta_regresiva_bloqueo(60)

    def _cuenta_regresiva_bloqueo(self, segundos):
        if segundos > 0 and self.is_locked:
            self.lbl_lock_sub.configure(text=f"Bloqueado. Reintente en {segundos}s", text_color="#D9534F")
            self.after(1000, lambda: self._cuenta_regresiva_bloqueo(segundos - 1))
        else:
            if self.is_locked:
                self.entry_user.configure(state="normal")
                self.entry_pin.configure(state="normal")
                self.btn_unlock.configure(state="normal")
                self.lbl_lock_sub.configure(text="Ingrese su Usuario y PIN", text_color="#666")
                self.entry_user.focus()

    def _aplicar_permisos(self, rol):
        self.lbl_rol_actual.configure(text=f"👤 Rol: {rol}")
        if rol == "Admin":
            self.btn_exportar_excel.configure(state="normal")
            self.btn_cargar_excel.configure(state="normal")
            self.btn_respaldo.configure(state="normal")
            self.btn_cambiar_pin.configure(state="normal")
            try:
                self.menu.entryconfig("❌  Eliminar Cliente", state="normal")
            except Exception:
                pass
        elif rol == "Recepcionista":
            self.btn_exportar_excel.configure(state="disabled")
            self.btn_cargar_excel.configure(state="disabled")
            self.btn_respaldo.configure(state="disabled")
            self.btn_cambiar_pin.configure(state="disabled")
            try:
                self.menu.entryconfig("❌  Eliminar Cliente", state="disabled")
            except Exception:
                pass

    def verificar_inactividad(self):
        if self.is_locked: return
        self.tiempo_inactivo += 1
        if self.tiempo_inactivo >= 120: self.bloquear_pantalla(); return
        self.after(1000, self.verificar_inactividad)
        
    def _reset_timer(self, event=None): self.tiempo_inactivo = 0

    def _cargar_fondo(self):
        rutas = [os.path.join(self.assets_dir, "fondo.png"), os.path.join(self.assets_dir, "fondo.jpg")]
        ruta_final = next((r for r in rutas if os.path.exists(r)), None)
        if ruta_final:
            try: self.original_image = Image.open(ruta_final)
            except: self.bg_label.configure(bg="#E5E5E5")
        else: self.bg_label.configure(bg="#E5E5E5")

    def _redimensionar_fondo(self, event):
        if event.widget == self:
            if not hasattr(self, '_last_width') or abs(self._last_width - event.width) > 5:
                self._last_width, self._last_height = event.width, event.height
                if hasattr(self, 'original_image'):
                    resized = self.original_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
                    self.new_bg_image = ImageTk.PhotoImage(resized)
                    self.bg_label.configure(image=self.new_bg_image)
                if hasattr(self, 'original_lock_bg'):
                    resized_lock = self.original_lock_bg.resize((event.width, event.height), Image.Resampling.LANCZOS)
                    self.new_lock_image = ImageTk.PhotoImage(resized_lock)
                    self.bg_label_bloqueo.configure(image=self.new_lock_image)
                if self.is_locked: self._crear_blur_central()

    def _cargar_logo(self):
        ruta_final = os.path.join(self.assets_dir, "logo.png")
        if os.path.exists(ruta_final):
            pil_img = Image.open(ruta_final)
            img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(180, 110))
            ctk.CTkLabel(self.sidebar, text="", image=img).pack(pady=(20, 10))
        else: ctk.CTkLabel(self.sidebar, text="UNIGYM", font=("Arial Black", 24), text_color=C_VERDE_LOGO).pack(pady=40)

    def _btn_menu(self, texto, comando):
        btn = ctk.CTkButton(self.sidebar, text=texto, anchor="w", fg_color="transparent", text_color="#555", hover_color="#F5F5F5", font=("Arial", 12, "bold"), height=40, corner_radius=8, command=comando)
        btn.pack(fill="x", padx=20, pady=2)
        return btn

    def _crear_boton_resumen(self, parent, titulo, color_barra, comando):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, width=175, height=90)
        card.pack_propagate(False); card.pack(side="left", padx=(0, 15))
        card.configure(border_width=1, border_color="#EAEAEA")
        bar = ctk.CTkFrame(card, width=6, fg_color=color_barra, corner_radius=0, height=90)
        bar.place(x=0, y=0)
        lbl_tit = ctk.CTkLabel(card, text=titulo, font=("Arial", 9, "bold"), text_color="#999")
        lbl_tit.place(x=15, y=15)
        lbl_val = ctk.CTkLabel(card, text="0", font=("Arial", 32, "bold"), text_color="#333")
        lbl_val.place(x=15, y=35)
        for w in [card, bar, lbl_tit, lbl_val]:
            w.bind("<Button-1>", lambda e: comando()); w.configure(cursor="hand2")
        return lbl_val

    def _configurar_tabla(self):
        style = ttk.Style(); style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="#333", fieldbackground="white", rowheight=45, borderwidth=0, font=("Arial", 11))
        style.configure("Treeview.Heading", background="white", foreground="#777", relief="flat", font=("Arial", 10, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview", background=[('selected', '#F0F9F0')], foreground=[('selected', '#333')])
        cols = ("ID", "Nombre", "Teléfono", "Inicio", "Vencimiento", "Estado", "Notas")
        self.tree = ttk.Treeview(self.frame_tabla, columns=cols, show="headings", selectmode="browse")
        anchos = [40, 220, 100, 100, 100, 120, 80]
        for c, w in zip(cols, anchos): self.tree.heading(c, text=c.upper()); self.tree.column(c, width=w, anchor="center")
        self.tree.column("Nombre", anchor="w")
        self.tree.tag_configure("vencido", foreground=C_ROJO_ALERTA)
        self.tree.tag_configure("alerta", foreground="#E67E22")
        self.tree.tag_configure("inactivo", foreground="#95A5A6") 
        scrolly = ctk.CTkScrollbar(self.frame_tabla, orientation="vertical", command=self.tree.yview, fg_color="transparent", button_color="#E0E0E0", width=12)
        self.tree.configure(yscroll=scrolly.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        scrolly.pack(side="right", fill="y", padx=(0,5), pady=15)
        self.tree.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root))
        
        def _on_tree_click(event):
            region = self.tree.identify("region", event.x, event.y)
            if region == "cell":
                col_id = self.tree.identify_column(event.x)
                if col_id == "#7":  # Columna Notas
                    row_id = self.tree.identify_row(event.y)
                    if row_id:
                        self.tree.selection_set(row_id)
                        # Verificamos qué dice la celda
                        valor_celda = self.tree.item(row_id, "values")[6]
                        if "📝" in valor_celda:
                            self.controller.gestionar_comentario("ver")
                        else:
                            self.controller.gestionar_comentario("editar")
                            
        self.tree.bind("<ButtonRelease-1>", _on_tree_click)

    def actualizar_tarjetas(self, total, activos, vencidos, inactivos=0):
        self.lbl_total.configure(text=str(total))
        self.lbl_activos.configure(text=str(activos))
        self.lbl_vencidos.configure(text=str(vencidos))
        self.lbl_inactivos.configure(text=str(inactivos))