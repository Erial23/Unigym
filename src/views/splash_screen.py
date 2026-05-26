import customtkinter as ctk
from PIL import Image
import os
import sys

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuraciones de la ventana (sin bordes)
        self.overrideredirect(True) 
        self.attributes("-topmost", True) # Que siempre esté al frente
        self.geometry("400x450")
        
        # Centrar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 200
        y = (screen_height // 2) - 225
        self.geometry(f"400x450+{x}+{y}")
        
        self.configure(fg_color="white")

        # Cargar Logo
        if getattr(sys, 'frozen', False): basedir = sys._MEIPASS
        else: basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        ruta_logo = os.path.join(basedir, "assets", "logo.png")
        
        if os.path.exists(ruta_logo):
            try:
                pil_img = Image.open(ruta_logo)
                self.img_logo = ctk.CTkImage(light_image=pil_img, size=(200, 150))
                self.lbl_logo = ctk.CTkLabel(self, image=self.img_logo, text="")
                self.lbl_logo.pack(pady=(60, 20))
            except:
                self.lbl_txt = ctk.CTkLabel(self, text="UNIGYM", font=("Arial Black", 40), text_color="#1D6F42")
                self.lbl_txt.pack(pady=80)

        ctk.CTkLabel(self, text="Iniciando UniGym Pro...", font=("Arial", 14), text_color="#555").pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=300, height=15, corner_radius=10, progress_color="#1D6F42")
        self.progress.set(0)
        self.progress.pack(pady=20)

    def actualizar_progreso(self, valor):
        self.progress.set(valor)
        self.update_idletasks() # Actualiza solo los gráficos