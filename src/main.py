import sys
import os
import customtkinter as ctk
import time
import subprocess

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from controllers.gym_controller import GymController
from views.main_window import MainWindow
from views.splash_screen import SplashScreen

def iniciar_microservicio():
    """
    Inicia de manera invisible el servidor FastAPI (FastUvicorn) en segundo plano.
    Evita abrir ventanas negras de terminal en sistemas Windows.
    """
    try:
        cmd = [sys.executable, "-m", "uvicorn", "services.fast:app", "--port", "8000", "--host", "127.0.0.1"]
        # creationflags=0x08000000 (CREATE_NO_WINDOW) evita abrir ventana de consola en Windows
        creationflags = 0x08000000 if sys.platform == "win32" else 0
        
        proc = subprocess.Popen(
            cmd,
            cwd=BASE_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags
        )
        return proc
    except Exception as e:
        print(f"Aviso: No se pudo iniciar el microservicio de notificaciones de WhatsApp: {e}")
        return None

def iniciar_sistema():
    # 0. Lanzamos el microservicio de notificaciones de forma invisible en segundo plano
    fast_process = iniciar_microservicio()

    # 1. Creamos el controlador primero
    controller = GymController()
    
    # 2. Creamos la ventana principal (Esta será nuestra raíz ÚNICA)
    main_gui = MainWindow(controller)
    main_gui.withdraw() # La ocultamos inmediatamente

    # 3. Lanzamos el Splash Screen pasándole la ventana principal como padre
    splash = SplashScreen(main_gui)
    
    # --- PROCESO DE CARGA SIMULADO ---
    etapas = [0.2, 0.5, 0.8, 1.0]
    for progreso in etapas:
        splash.actualizar_progreso(progreso)
        main_gui.update() # Mantiene viva la interfaz
        time.sleep(0.5)
    
    # 4. Conectamos la vista al controlador
    controller.set_view(main_gui)

    # 5. Cerramos Splash y mostramos App
    splash.destroy()
    main_gui.deiconify() # Mostramos la ventana principal
    main_gui.focus_force()
    
    # 6. Interceptamos el cierre de ventana para apagar limpiamente el microservicio
    def al_cerrar_ventana():
        if fast_process:
            try:
                fast_process.terminate()
                fast_process.wait(timeout=2)
            except:
                pass
        main_gui.destroy()

    main_gui.protocol("WM_DELETE_WINDOW", al_cerrar_ventana)
    
    main_gui.mainloop()

if __name__ == "__main__":
    iniciar_sistema()