from fastapi import FastAPI, BackgroundTasks, HTTPException
from datetime import datetime, timedelta
import sqlite3
import pywhatkit as kit
import os
import time
import random
import threading

app = FastAPI(
    title="UniGym Pro - API de Notificaciones Automáticas",
    description="Microservicio local para el envío automatizado de alertas de vencimiento vía WhatsApp"
)

# --- RUTA REAL ALINEADA CON DB_MANAGER ---
DB_PATH = r"C:\UniGym_Datos\gym_database.db"
STATE_FILE = r"C:\UniGym_Datos\ultimo_envio.txt"

def generar_mensaje_personalizado(nombre, fecha_ven):
    """
    Genera un mensaje con variaciones aleatorias de textos y emojis (Spintax)
    para evitar que WhatsApp identifique patrones repetitivos y los bloquee como spam.
    """
    saludos = [
        f"¡Hola, {nombre}! 💪🏋️‍♂️",
        f"¡Hola, {nombre}! ¿Cómo estás? 🌟",
        f"¡Qué tal, {nombre}! Esperamos que estés super bien. 😊",
        f"¡Hola, {nombre}! Te saludamos de tu gimnasio. 👍"
    ]
    
    cuerpos = [
        f"Te recordamos amigablemente que tu membresía en *UNI GYM FITNESS* vence el día de mañana (*{fecha_ven}*).",
        f"Te escribimos desde *UNI GYM FITNESS* para recordarte que tu membresía mensual vence el día de mañana (*{fecha_ven}*).",
        f"Este es un recordatorio de *UNI GYM FITNESS*: tu plan de entrenamiento mensual vence mañana (*{fecha_ven}*)."
    ]
    
    despedidas = [
        "Te esperamos en recepción para gestionar tu renovación y que no pierdas ni un solo día de entrenamiento. ¡A darle con todo! 🔥",
        "Pásate por recepción para realizar tu renovación y continuar entrenando sin interrupciones. ¡A darle duro! 💪⚡",
        "Te esperamos en recepción para renovar tu membresía y seguir con tu rutina fitness. ¡No pares tu entrenamiento! 🚀🏋️‍♀️"
    ]
    
    return f"{random.choice(saludos)}\n\n{random.choice(cuerpos)}\n\n{random.choice(despedidas)}"

def verificar_y_enviar_alertas():
    """
    Busca clientes que vencen mañana y les envía un mensaje automatizado con técnicas anti-spam.
    """
    if not os.path.exists(DB_PATH):
        print(f"Error: La base de datos no existe en la ruta especificada: {DB_PATH}")
        return

    # Calcular la fecha de mañana (formato YYYY-MM-DD como se guarda en la base de datos)
    manana = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # --- TABLA REAL ALINEADA: 'clientes' en lugar de 'CLIENTE' ---
        cursor.execute("""
            SELECT id, nombre, telefono, fecha_vencimiento 
            FROM clientes 
            WHERE fecha_vencimiento = ? AND (estado = 'Activo' OR estado = 'Al Día')
        """, (manana,))
        
        clientes_por_vencer = cursor.fetchall()
        
        print(f"--- Escaneo Diario: Se encontraron {len(clientes_por_vencer)} clientes por vencer mañana ({manana}) ---")
        
        for cliente in clientes_por_vencer:
            id_cliente, nombre, telefono, fecha_ven = cliente
            
            if not telefono or telefono == "SN":
                print(f"Saltando a {nombre} porque no tiene número de teléfono registrado.")
                continue
                
            # Validar formato de número para WhatsApp (Debe incluir código de país, ej: +593 para Ecuador)
            telefono = str(telefono).strip()
            if not telefono.startswith("+"):
                # Si guardas los números sin código de país, le concatenamos por defecto (+593 para Ecuador)
                # Puedes cambiar este prefijo según tu país
                telefono = f"+593{telefono}" 
            
            # Generar texto con variaciones aleatorias anti-spam
            mensaje = generar_mensaje_personalizado(nombre, datetime.strptime(fecha_ven, "%Y-%m-%d").strftime("%d/%m/%Y"))
            
            print(f"Enviando recordatorio seguro a {nombre} ({telefono})...")
            
            # pywhatkit envía el mensaje abriendo una pestaña en el navegador.
            kit.sendwhatmsg_instantly(
                phone_no=telefono, 
                message=mensaje, 
                wait_time=20,     # Aumentado a 20s para conexiones lentas (mayor robustez)
                tab_close=True,   # Cierra la pestaña automáticamente
                close_time=5      # Tiempo para cerrar pestaña después de enviar
            )
            
            # Registrar la notificación en la base de datos
            try:
                conn_log = sqlite3.connect(DB_PATH)
                cursor_log = conn_log.cursor()
                cursor_log.execute("UPDATE clientes SET ultima_notificacion=? WHERE id=?", (datetime.now().strftime('%Y-%m-%d'), id_cliente))
                conn_log.commit()
                conn_log.close()
                print(f"Notificación registrada en base de datos para {nombre}.")
            except Exception as db_err:
                print(f"Error al registrar notificación para {nombre}: {db_err}")
            
            # --- MEDIDA ANTI-SPAM CLAVE ---
            # Pausa larga y aleatoria entre mensajes para simular comportamiento humano (entre 25 y 55 segundos)
            delay = random.randint(25, 55)
            print(f"Pausa de seguridad anti-spam: esperando {delay} segundos antes de continuar...")
            time.sleep(delay)
            
        conn.close()
        print("--- Envío diario de alertas finalizado ---")
    except Exception as e:
        print(f"Ocurrió un error en el proceso automatizado: {str(e)}")

# ============================================================
# ⏰ PLANIFICADOR DIARIO DIARIO EN SEGUNDO PLANO (AUTOMÁTICO)
# ============================================================
def planificador_envio_automatico():
    """
    Loop que corre indefinidamente en segundo plano.
    Escanea la base de datos a las 09:00 AM todos los días y envía recordatorios.
    """
    print("Iniciando planificador diario de alertas por WhatsApp...")
    while True:
        try:
            ahora = datetime.now()
            # Se dispara de forma automática a las 09:00 AM
            if ahora.hour == 9:
                hoy_str = ahora.strftime("%Y-%m-%d")
                
                # Evitar doble envío en el mismo día mediante archivo de estado
                ya_enviado = False
                if os.path.exists(STATE_FILE):
                    with open(STATE_FILE, "r") as f:
                        if f.read().strip() == hoy_str:
                            ya_enviado = True
                
                if not ya_enviado:
                    print(f"⏰ ¡Son las 09:00 AM! Iniciando envío automático diario...")
                    verificar_y_enviar_alertas()
                    
                    # Registrar que ya se envió hoy
                    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
                    with open(STATE_FILE, "w") as f:
                        f.write(hoy_str)
                        
        except Exception as e:
            print(f"Error en el hilo planificador: {e}")
        
        # Espera 30 minutos antes del siguiente chequeo de la hora
        time.sleep(1800)

@app.on_event("startup")
def iniciar_planificador():
    """Se ejecuta al iniciar el servidor FastAPI y arranca el hilo planificador"""
    threading.Thread(target=planificador_envio_automatico, daemon=True).start()

# ============================================================
# 🔗 ENDPOINTS DE LA API
# ============================================================
@app.post("/alertas/procesar-diario", summary="Disparar auditoría manual de alertas")
def disparar_alertas(background_tasks: BackgroundTasks):
    """
    Ruta para disparar el escaneo manualmente en cualquier momento
    de forma asíncrona sin bloquear la API.
    """
    background_tasks.add_task(verificar_y_enviar_alertas)
    return {"status": "Proceso de escaneo manual lanzado en segundo plano de forma segura."}

@app.get("/status", summary="Verificar estado del microservicio")
def check_status():
    ahora = datetime.now()
    hoy_str = ahora.strftime("%Y-%m-%d")
    ya_enviado_hoy = False
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            if f.read().strip() == hoy_str:
                ya_enviado_hoy = True
                
    return {
        "status": "Online",
        "database_connected": os.path.exists(DB_PATH),
        "db_path": DB_PATH,
        "timestamp": ahora.isoformat(),
        "alertas_enviadas_hoy": ya_enviado_hoy
    }