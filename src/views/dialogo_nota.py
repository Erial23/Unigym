# src/views/dialogo_nota.py
import customtkinter as ctk
from .styles import *

class DialogoNota(ctk.CTkToplevel):
    def __init__(self, parent, titulo, nota_inicial, modo="ver", callback=None):
        super().__init__(parent)
        self.callback = callback
        self.modo = modo  # "ver" o "editar"
        self.nota_inicial = nota_inicial
        
        self.title("Nota / Comentario")
        self.geometry("450x420")
        self.configure(fg_color=C_FONDO_BLANCO)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Centrar ventana con respecto al padre
        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width() - 450) // 2
        py = parent.winfo_y() + (parent.winfo_height() - 420) // 2
        self.geometry(f"450x420+{px}+{py}")

        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text=titulo.upper(), font=FONT_TITULO, text_color=C_TEXTO_TITULO)
        self.lbl_titulo.pack(pady=(25, 15), padx=20)

        # Contenedor del textbox
        self.textbox = ctk.CTkTextbox(
            self, 
            width=370, 
            height=200, 
            fg_color="#F0F0F0" if self.modo == "ver" else "white", 
            text_color="black",
            font=FONT_NORMAL,
            wrap="word",  # Envuelve el texto al final del renglón (hacia abajo)
            border_width=0 if self.modo == "ver" else 2,
            border_color=C_VERDE_LOGO
        )
        self.textbox.pack(padx=40, pady=10)
        self.textbox.insert("1.0", self.nota_inicial)
        
        if self.modo == "ver":
            self.textbox.configure(state="disabled")

        # Frame de botones
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=40, pady=(15, 0))

        self.mostrar_botones()

    def mostrar_botones(self):
        # Limpiar botones anteriores
        for widget in self.btn_frame.winfo_children():
            widget.destroy()

        if self.modo == "ver":
            # Botón Editar
            self.btn_edit = ctk.CTkButton(
                self.btn_frame, 
                text="📝  EDITAR", 
                fg_color=C_VERDE_LOGO, 
                hover_color=C_VERDE_HOVER, 
                text_color="white", 
                font=("Arial", 12, "bold"),
                width=160, 
                height=45,
                command=self.activar_edicion
            )
            self.btn_edit.pack(side="left", padx=(0, 10))

            # Botón Cerrar
            self.btn_close = ctk.CTkButton(
                self.btn_frame, 
                text="CERRAR", 
                fg_color="#95A5A6", 
                hover_color="#7F8C8D", 
                text_color="white", 
                font=("Arial", 12, "bold"),
                width=160, 
                height=45,
                command=self.destroy
            )
            self.btn_close.pack(side="right", padx=(10, 0))
        else:
            # Botón Cancelar
            self.btn_cancel = ctk.CTkButton(
                self.btn_frame, 
                text="CANCELAR", 
                fg_color="#95A5A6", 
                hover_color="#7F8C8D", 
                text_color="white", 
                font=("Arial", 12, "bold"),
                width=160, 
                height=45,
                command=self.cancelar_edicion
            )
            self.btn_cancel.pack(side="left", padx=(0, 10))

            # Botón Guardar
            self.btn_save = ctk.CTkButton(
                self.btn_frame, 
                text="💾  GUARDAR", 
                fg_color=C_VERDE_LOGO, 
                hover_color=C_VERDE_HOVER, 
                text_color="white", 
                font=("Arial", 12, "bold"),
                width=160, 
                height=45,
                command=self.guardar_nota
            )
            self.btn_save.pack(side="right", padx=(10, 0))

    def activar_edicion(self):
        self.modo = "editar"
        self.textbox.configure(state="normal", fg_color="white", border_width=2)
        self.textbox.focus()
        self.mostrar_botones()

    def cancelar_edicion(self):
        # Si venía originalmente de modo "ver" o si tiene callback
        self.modo = "ver"
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", self.nota_inicial)
        self.textbox.configure(state="disabled", fg_color="#F0F0F0", border_width=0)
        self.mostrar_botones()

    def guardar_nota(self):
        texto = self.textbox.get("1.0", "end-1c").strip()
        if self.callback:
            self.callback(texto)
        self.destroy()
