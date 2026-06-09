from tkinter import messagebox, filedialog
import customtkinter as ctk
import pandas as pd
from datetime import datetime, timedelta
import calendar
import os
import shutil
from database.db_manager import DBManager

class GymController:
    def __init__(self):
        self.db = DBManager()
        self.view = None 
        self.modo_filtro = False 
        self.rol_actual = None
        self.filtro_actual = self.cargar_datos
        
        self.pin_file = os.path.join(self.db.data_dir, "admin_pin.txt")
        self.pin_recepcion_file = os.path.join(self.db.data_dir, "recepcion_pin.txt")
        self.user_admin_file = os.path.join(self.db.data_dir, "admin_user.txt")
        self.user_recepcion_file = os.path.join(self.db.data_dir, "recepcion_user.txt")
        self._cargar_credenciales()

    def _cargar_credenciales(self):
        import hashlib
        default_pin_hash = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4" # Hash de "1234"
        default_recepcion_hash = "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0" # Hash de "0000"
        
        # Cargar o crear PIN Admin
        if os.path.exists(self.pin_file):
            with open(self.pin_file, "r") as f:
                contenido = f.read().strip()
            if len(contenido) == 64 and all(c in "0123456789abcdefABCDEF" for c in contenido):
                self.pin_admin = contenido
            else:
                self.pin_admin = hashlib.sha256(contenido.encode()).hexdigest()
                with open(self.pin_file, "w") as f:
                    f.write(self.pin_admin)
        else:
            self.pin_admin = default_pin_hash
            with open(self.pin_file, "w") as f:
                f.write(self.pin_admin)

        # Cargar o crear PIN Recepcion
        if os.path.exists(self.pin_recepcion_file):
            with open(self.pin_recepcion_file, "r") as f:
                contenido = f.read().strip()
            if len(contenido) == 64 and all(c in "0123456789abcdefABCDEF" for c in contenido):
                self.pin_recepcion = contenido
            else:
                self.pin_recepcion = hashlib.sha256(contenido.encode()).hexdigest()
                with open(self.pin_recepcion_file, "w") as f:
                    f.write(self.pin_recepcion)
        else:
            self.pin_recepcion = default_recepcion_hash
            with open(self.pin_recepcion_file, "w") as f:
                f.write(self.pin_recepcion)

        # Cargar o crear Usuario Admin
        if os.path.exists(self.user_admin_file):
            with open(self.user_admin_file, "r") as f:
                self.user_admin = f.read().strip()
        else:
            self.user_admin = "ADMIN"
            with open(self.user_admin_file, "w") as f:
                f.write(self.user_admin)

        # Cargar o crear Usuario Recepcion
        if os.path.exists(self.user_recepcion_file):
            with open(self.user_recepcion_file, "r") as f:
                self.user_recepcion = f.read().strip()
        else:
            self.user_recepcion = "RECEPCION"
            with open(self.user_recepcion_file, "w") as f:
                f.write(self.user_recepcion)

    def cambiar_credenciales(self):
        if self.rol_actual != "Admin":
            messagebox.showerror("Error", "Solo el Administrador puede cambiar credenciales.")
            return

        import hashlib
        
        dialog = ctk.CTkToplevel()
        dialog.title("Cambiar Credenciales")
        dialog.geometry("400x550")
        if self.view:
            dialog.transient(self.view)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Seguridad: Ingrese credenciales de Admin", font=("Arial", 14, "bold")).pack(pady=10)
        
        user_actual = ctk.CTkEntry(dialog, placeholder_text="Usuario Admin Actual")
        user_actual.pack(pady=5)
        pin_actual = ctk.CTkEntry(dialog, placeholder_text="PIN Admin Actual", show="*")
        pin_actual.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Seleccione a quién cambiar credenciales:", font=("Arial", 12)).pack(pady=10)
        opcion_var = ctk.StringVar(value="Admin")
        ctk.CTkRadioButton(dialog, text="Administrador", variable=opcion_var, value="Admin").pack(pady=2)
        ctk.CTkRadioButton(dialog, text="Recepcionista", variable=opcion_var, value="Recepcion").pack(pady=2)
        
        ctk.CTkLabel(dialog, text="Nuevas Credenciales:", font=("Arial", 14, "bold")).pack(pady=10)
        user_nuevo = ctk.CTkEntry(dialog, placeholder_text="Nuevo Usuario")
        user_nuevo.pack(pady=5)
        pin_nuevo = ctk.CTkEntry(dialog, placeholder_text="Nuevo PIN", show="*")
        pin_nuevo.pack(pady=5)
        
        def guardar():
            ua = user_actual.get().strip()
            pa = pin_actual.get().strip()
            
            if not ua or not pa:
                messagebox.showerror("Error", "Ingrese credenciales actuales", parent=dialog)
                return
                
            hash_actual = hashlib.sha256(pa.encode()).hexdigest()
            if ua != self.user_admin or hash_actual != self.pin_admin:
                messagebox.showerror("Error", "Credenciales de Admin actuales incorrectas", parent=dialog)
                return
                
            un = user_nuevo.get().strip()
            pn = pin_nuevo.get().strip()
            if not un or not pn:
                messagebox.showerror("Error", "Ingrese usuario y PIN nuevos", parent=dialog)
                return
                
            hash_nuevo = hashlib.sha256(pn.encode()).hexdigest()
            
            if opcion_var.get() == "Admin":
                self.user_admin = un
                self.pin_admin = hash_nuevo
                with open(self.user_admin_file, "w") as f: f.write(un)
                with open(self.pin_file, "w") as f: f.write(hash_nuevo)
                messagebox.showinfo("Éxito", "Credenciales de Admin cambiadas.", parent=dialog)
            else:
                self.user_recepcion = un
                self.pin_recepcion = hash_nuevo
                with open(self.user_recepcion_file, "w") as f: f.write(un)
                with open(self.pin_recepcion_file, "w") as f: f.write(hash_nuevo)
                messagebox.showinfo("Éxito", "Credenciales de Recepcionista cambiadas.", parent=dialog)
            dialog.destroy()
            
        ctk.CTkButton(dialog, text="Guardar Cambios", command=guardar).pack(pady=20)

    def set_view(self, view):
        self.view = view
        self.cargar_datos()

    def verificar_credenciales(self, user_ingresado, pin_ingresado):
        import hashlib
        if not pin_ingresado or not user_ingresado:
            return None
            
        if pin_ingresado.strip() == "UNIGYM-RESCATE":
            default_pin_hash = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
            self.pin_admin = default_pin_hash
            self.user_admin = "ADMIN"
            with open(self.pin_file, "w") as f:
                f.write(self.pin_admin)
            with open(self.user_admin_file, "w") as f:
                f.write(self.user_admin)
            messagebox.showinfo("Master Key Activada", "Credenciales de Administrador reseteadas a ADMIN / 1234.\nIngresarás como Administrador ahora.")
            self.rol_actual = "Admin"
            return "Admin"
            
        hash_ingresado = hashlib.sha256(pin_ingresado.strip().encode()).hexdigest()
        user_ingresado = user_ingresado.strip()
        
        if hash_ingresado == self.pin_admin and user_ingresado == self.user_admin:
            self.rol_actual = "Admin"
            return "Admin"
        elif hash_ingresado == self.pin_recepcion and user_ingresado == self.user_recepcion:
            self.rol_actual = "Recepcionista"
            return "Recepcionista"
        else:
            return None

    def _parsear_fecha(self, fecha_str):
        """Intenta leer la fecha en múltiples formatos para evitar errores."""
        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(str(fecha_str).strip(), formato).date()
            except (ValueError, TypeError):
                continue
        return datetime.now().date()

    def cargar_datos(self):
        self.modo_filtro = False
        self.filtro_actual = self.cargar_datos
        if self.view:
            self.view.lbl_titulo.configure(text="Panel de Control - Todos los Clientes")
            self.view.entry_search.delete(0, "end") 
        self._llenar_tabla(self.db.obtener_todos())

    def cargar_activos(self):
        self.modo_filtro = True
        self.filtro_actual = self.cargar_activos
        if self.view:
            self.view.lbl_titulo.configure(text="🟢 Clientes Activos")
        todos = self.db.obtener_todos()
        filtrados = []
        hoy = datetime.now().date()
        for row in todos:
            dias = (self._parsear_fecha(row[4]) - hoy).days
            if dias >= 0: filtrados.append(row)
        self._llenar_tabla(filtrados)

    def cargar_notificados_hoy(self):
        self.modo_filtro = True
        self.filtro_actual = self.cargar_notificados_hoy
        if self.view:
            self.view.lbl_titulo.configure(text="📢 Clientes Notificados Hoy")
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        todos = self.db.obtener_todos()
        filtrados = []
        for row in todos:
            # row[7] es la columna 'ultima_notificacion'
            if len(row) > 7 and row[7] == hoy_str:
                filtrados.append(row)
        self._llenar_tabla(filtrados)

    def cargar_todos_notificados(self):
        self.modo_filtro = True
        self.filtro_actual = self.cargar_todos_notificados
        if self.view:
            self.view.lbl_titulo.configure(text="📋 Todos los Notificados")
        todos = self.db.obtener_todos()
        filtrados = []
        for row in todos:
            # row[7] es la columna 'ultima_notificacion'
            if len(row) > 7 and row[7] and row[7].strip():
                filtrados.append(row)
        self._llenar_tabla(filtrados)

    def cargar_por_terminar(self):
        self.modo_filtro = True
        self.filtro_actual = self.cargar_por_terminar
        if self.view:
            self.view.lbl_titulo.configure(text="⚠️ Clientes por Terminar")
        todos = self.db.obtener_todos()
        filtrados = []
        hoy = datetime.now().date()
        for row in todos:
            dias = (self._parsear_fecha(row[4]) - hoy).days
            if -60 <= dias <= 3: filtrados.append(row)
        self._llenar_tabla(filtrados)

    def cargar_inactivos(self):
        self.modo_filtro = True
        self.filtro_actual = self.cargar_inactivos
        if self.view:
            self.view.lbl_titulo.configure(text="💤 Clientes Inactivos")
        todos = self.db.obtener_todos()
        filtrados = []
        hoy = datetime.now().date()
        for row in todos:
            dias = (self._parsear_fecha(row[4]) - hoy).days
            if dias < -60: filtrados.append(row)
        self._llenar_tabla(filtrados)

    def cargar_comentarios(self):
        self.modo_filtro = True
        self.filtro_actual = self.cargar_comentarios
        if self.view:
            self.view.lbl_titulo.configure(text="💬 Notas y Deudas")
        filtrados = [row for row in self.db.obtener_todos() if row[6] and row[6].strip()]
        self._llenar_tabla(filtrados)

    def buscar_cliente(self, event=None):
        self.filtro_actual = self.buscar_cliente
        texto = self.view.entry_search.get().lower()
        if not texto:
            self.cargar_datos()
            return
        todos = self.db.obtener_todos()
        resultados = [r for r in todos if texto in str(r[1]).lower() or texto in str(r[2])]
        self._llenar_tabla(resultados)

    # ============================================================
    # 📊 LLENAR TABLA (ORDENADO Y ENUMERADO DESDE 1)
    # ============================================================
    def _llenar_tabla(self, datos):
        for item in self.view.tree.get_children(): self.view.tree.delete(item)
        
        # 1. Ordenar datos por fecha de vencimiento (índice 4 de la tupla original)
        datos_ordenados = sorted(datos, key=lambda x: self._parsear_fecha(x[4]))
        
        hoy = datetime.now().date()
        todos_db = self.db.obtener_todos()
        general = len(todos_db)
        activos = 0
        vencidos = 0
        inactivos = 0
        for r in todos_db:
            d_t = (self._parsear_fecha(r[4]) - hoy).days
            if d_t >= 0: activos += 1
            if -60 <= d_t <= 3: vencidos += 1
            elif d_t < -60: inactivos += 1

        # 2. Insertar en tabla con numeración 1, 2, 3...
        for idx, row in enumerate(datos_ordenados, start=1):
            f_ini_dt = self._parsear_fecha(row[3])
            f_ven_dt = self._parsear_fecha(row[4])
            inicio_vis = f_ini_dt.strftime("%d/%m/%Y")
            venc_vis = f_ven_dt.strftime("%d/%m/%Y")
            dias = (f_ven_dt - hoy).days
            
            estado, tag = "Al Día", "normal"
            if dias < -60: estado, tag = "INACTIVO", "inactivo"
            elif dias < 0: estado, tag = "VENCIDO", "vencido"
            elif dias == 0: estado, tag = "VENCE HOY", "alerta"
            elif dias <= 3: estado, tag = f"Vence en {dias} d", "alerta"
            
            if len(row) > 7 and row[7] and row[7].strip():
                try:
                    f_notif = datetime.strptime(row[7], "%Y-%m-%d").strftime("%d/%m/%Y")
                    estado = f"{estado} (Notif. {f_notif})"
                except Exception:
                    estado = f"{estado} (Notif. {row[7]})"
            
            nota_icono = "📝 Ver Nota" if len(row) > 6 and row[6] and str(row[6]).strip() else "➕ Agregar"
            
            # El primer valor es el índice visual (1, 2, 3), 
            # pero guardamos el ID real de la DB en el campo 'tags' o lo asociamos al item
            item_id = self.view.tree.insert("", "end", values=(idx, row[1], row[2], inicio_vis, venc_vis, estado, nota_icono), tags=(tag,))
            # Guardamos el ID real de la DB dentro del objeto treeview para usarlo después
            self.view.tree.set(item_id, column="ID", value=idx) # Esto solo cambia lo visual
            # Truco para guardar el ID real: lo guardamos en un diccionario interno o usamos iid
            self.view.tree.item(item_id, text=row[0]) # El atributo 'text' guardará el ID real de la DB

        self.view.actualizar_tarjetas(general, activos, vencidos, inactivos)

    def calcular_fecha_mensual(self, fecha_base):
        year = fecha_base.year
        month = fecha_base.month + 1
        if month > 12: month = 1; year += 1
        day = min(fecha_base.day, calendar.monthrange(year, month)[1])
        return fecha_base.replace(year=year, month=month, day=day)

    def abrir_formulario_nuevo(self):
        from views.form_cliente import FormularioCliente
        FormularioCliente(self.view, self.guardar_cliente)

    def _obtener_id_real(self):
        sel = self.view.tree.selection()
        if not sel: return None
        return self.view.tree.item(sel[0])['text'] # Recuperamos el ID real de la DB

    def abrir_formulario_editar(self):
        id_real = self._obtener_id_real()
        if not id_real: return
        db_row = next((r for r in self.db.obtener_todos() if str(r[0]) == str(id_real)), None)
        from views.form_cliente import FormularioCliente
        FormularioCliente(self.view, self.actualizar_cliente_db, datos_editar=db_row)

    def guardar_cliente(self, nombre, telefono, plan, fecha_inicio_input="HOY", monto=0.0):
        try:
            if fecha_inicio_input == "HOY":
                f_dt = datetime.now()
            else:
                f_dt = datetime.combine(self._parsear_fecha(fecha_inicio_input), datetime.min.time())
            venc_dt = f_dt + timedelta(days=1) if plan == "Diario" else self.calcular_fecha_mensual(f_dt)
            id_cliente = self.db.agregar_cliente(nombre, telefono, f_dt.strftime("%Y-%m-%d"), venc_dt.strftime("%Y-%m-%d"))
            self.db.registrar_pago(id_cliente, f_dt.strftime("%Y-%m-%d"), plan, monto)
            messagebox.showinfo("Éxito", "Registrado"); self.filtro_actual()
        except: messagebox.showerror("Error", "Formato: DD/MM/AAAA o Monto Inválido")

    def actualizar_cliente_db(self, nombre, telefono, fecha_inicio, fecha_venc, id_original):
        f_i = self._parsear_fecha(fecha_inicio).strftime("%Y-%m-%d")
        f_v = self._parsear_fecha(fecha_venc).strftime("%Y-%m-%d")
        self.db.actualizar_cliente(id_original, nombre, telefono, f_i, f_v)
        messagebox.showinfo("Éxito", "Actualizado"); self.filtro_actual()

    def renovar_seleccionado(self, tipo):
        id_real = self._obtener_id_real()
        if not id_real: return
        db_row = next((r for r in self.db.obtener_todos() if str(r[0]) == str(id_real)), None)
        if not db_row: return
        
        base = self._parsear_fecha(db_row[4])
        base_dt = datetime.combine(base, datetime.min.time())
        nuevo_venc = base_dt + timedelta(days=1) if tipo == "Diario" else self.calcular_fecha_mensual(base_dt)
        self.db.renovar_vencimiento(id_real, nuevo_venc.strftime("%Y-%m-%d"))
        
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        monto = 25.0 if tipo == "Mensual" else 2.0
        self.db.registrar_pago(id_real, hoy_str, tipo, monto)
        
        messagebox.showinfo("Pago", f"Vence: {nuevo_venc.strftime('%d/%m/%Y')}"); self.filtro_actual()

    def eliminar_seleccionado(self):
        if self.rol_actual != "Admin":
            messagebox.showerror("Acceso Denegado", "Solo el Administrador puede eliminar clientes.")
            return
        id_real = self._obtener_id_real()
        if not id_real: return
        dialog = ctk.CTkInputDialog(text="PIN Admin:", title="Borrar")
        pin_input = dialog.get_input()
        if pin_input is not None and self.verificar_credenciales(self.user_admin, pin_input) == "Admin":
            self.db.eliminar_cliente(id_real); self.filtro_actual()
        elif pin_input is not None:
            messagebox.showerror("Error", "PIN Incorrecto.")

    def gestionar_comentario(self, accion):
        id_real = self._obtener_id_real()
        if not id_real: return
        row = next((r for r in self.db.obtener_todos() if str(r[0]) == str(id_real)), None)
        if not row: return
        
        com = row[6] if row else ""
        
        def guardar_cb(nueva_nota):
            self.db.actualizar_comentario(id_real, nueva_nota)
            self.filtro_actual()

        if accion == "ver":
            from views.dialogo_nota import DialogoNota
            DialogoNota(self.view, titulo=f"Nota - {row[1]}", nota_inicial=com, modo="ver", callback=guardar_cb)
        elif accion == "editar":
            from views.dialogo_nota import DialogoNota
            DialogoNota(self.view, titulo=f"Editar Nota - {row[1]}", nota_inicial=com, modo="editar", callback=guardar_cb)
        elif accion == "eliminar":
            if messagebox.askyesno("Confirmar", "¿Borrar nota?"):
                self.db.actualizar_comentario(id_real, "")
                self.filtro_actual()

    def enviar_alertas_whatsapp(self):
        import urllib.request
        import json
        import threading
        
        def run_api_call():
            try:
                req = urllib.request.Request(
                    "http://127.0.0.1:8000/alertas/procesar-diario",
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    res_data = json.loads(response.read().decode())
                    if self.view:
                        self.view.after(0, lambda: messagebox.showinfo("WhatsApp", "Proceso de alertas de WhatsApp iniciado en segundo plano de forma segura."))
            except Exception as e:
                if self.view:
                    self.view.after(0, lambda: messagebox.showerror(
                        "Error", 
                        "No se pudo conectar con el microservicio de WhatsApp.\n\nAsegúrese de que el servidor de notificaciones esté activo.\nDetalle: " + str(e)
                    ))
                
        # Ejecutamos en un hilo para no congelar la interfaz GUI
        threading.Thread(target=run_api_call, daemon=True).start()

    def enviar_whatsapp_individual(self):
        id_real = self._obtener_id_real()
        if not id_real: return
        row = next((r for r in self.db.obtener_todos() if str(r[0]) == str(id_real)), None)
        if not row: return
        
        nombre = row[1]
        telefono = row[2]
        fecha_venc = row[4]
        
        if not telefono or telefono == "SN":
            messagebox.showwarning("Atención", f"El cliente {nombre} no tiene un teléfono válido registrado.")
            return
            
        telefono = str(telefono).strip()
        if not telefono.startswith("+"):
            telefono = f"+593{telefono}" # Prefijo por defecto para Ecuador (ajustable)
            
        try:
            f_ven_dt = self._parsear_fecha(fecha_venc)
            fecha_ven_vis = f_ven_dt.strftime("%d/%m/%Y")
        except:
            fecha_ven_vis = fecha_venc
            
        import random
        saludos = [
            f"¡Hola, {nombre}! 💪🏋️‍♂️",
            f"¡Hola, {nombre}! ¿Cómo estás? 🌟",
            f"¡Qué tal, {nombre}! Esperamos que estés super bien. 😊",
            f"¡Hola, {nombre}! Te saludamos de tu gimnasio *UNI GYM FITNESS*. 👍"
        ]
        
        cuerpos = [
            f"Te recordamos amigablemente que tu membresía vence el día *{fecha_ven_vis}*.",
            f"Te escribimos de *UNI GYM FITNESS* para recordarte que tu membresía mensual vence el día *{fecha_ven_vis}*.",
            f"Este es un recordatorio de tu plan de entrenamiento mensual que vence el día *{fecha_ven_vis}*."
        ]
        
        despedidas = [
            "Te esperamos en recepción para gestionar tu renovación y continuar entrenando sin perder ningún día. ¡A darle con todo! 🔥",
            "Pásate por recepción para realizar tu renovación y seguir entrenando sin interrupciones. ¡A darle duro! 💪⚡",
            "Te esperamos en recepción para renovar tu membresía y seguir con tu rutina fitness. ¡No pares! 🚀🏋️‍♀️"
        ]
        
        mensaje = f"{random.choice(saludos)}\n\n{random.choice(cuerpos)}\n\n{random.choice(despedidas)}"
        
        import urllib.parse
        import webbrowser
        mensaje_encoded = urllib.parse.quote(mensaje)
        url = f"https://web.whatsapp.com/send?phone={urllib.parse.quote(telefono)}&text={mensaje_encoded}"
        webbrowser.open(url)
        
        # Registrar última notificación en la base de datos
        try:
            hoy_str = datetime.now().strftime("%Y-%m-%d")
            self.db.actualizar_notificacion(id_real, hoy_str)
            self.filtro_actual()
        except Exception as e:
            print(f"Error al registrar última notificación: {e}")

    def exportar_respaldo(self):
        ruta_destino = filedialog.asksaveasfilename(
            defaultextension=".db",
            initialfile=f"Respaldo_UniGym_{datetime.now().strftime('%d_%m_%Y')}.db",
            title="Guardar copia de seguridad"
        )
        if ruta_destino:
            try:
                ruta_original = self.db.db_path
                shutil.copy2(ruta_original, ruta_destino)
                messagebox.showinfo("Éxito", "Copia creada correctamente.")
            except Exception as e: messagebox.showerror("Error", f"Fallo: {e}")

    def exportar_clientes_excel(self):
        try:
            todos = self.db.obtener_todos()
            if not todos:
                messagebox.showwarning("Atención", "No hay datos para exportar.")
                return
            df = pd.DataFrame(todos, columns=['ID_DB', 'Nombre', 'Teléfono', 'Inicio', 'Vencimiento', 'Estado', 'Notas', 'Última Notificación'])
            df['Inicio'] = df['Inicio'].apply(lambda x: self._parsear_fecha(x).strftime("%d/%m/%Y"))
            df['Vencimiento'] = df['Vencimiento'].apply(lambda x: self._parsear_fecha(x).strftime("%d/%m/%Y"))
            ruta = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel", "*.xlsx")],
                initialfile=f"Clientes_UniGym_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
            )
            if ruta:
                df.to_excel(ruta, index=False)
                messagebox.showinfo("Éxito", "Clientes exportados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def mostrar_historial_pagos(self):
        dialog = ctk.CTkToplevel()
        dialog.title("Reporte de Pagos Realizados")
        dialog.geometry("800x700")
        if self.view:
            dialog.transient(self.view)
            
        frame_filtros = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_filtros.pack(fill="x", padx=20, pady=(20, 0))
        
        ctk.CTkLabel(frame_filtros, text="Filtrar por:", font=("Arial", 14, "bold")).pack(side="left", padx=(0, 10))
        
        lbl_cant = ctk.StringVar(value="0")
        lbl_diario = ctk.StringVar(value="$0.00")
        lbl_mensual = ctk.StringVar(value="$0.00")
        lbl_total = ctk.StringVar(value="$0.00")
        
        from tkinter import ttk
        cols = ("ID Pago", "Cliente", "Fecha Pago", "Plan", "Monto ($)")
        tree = ttk.Treeview(dialog, columns=cols, show="headings", height=15)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor="center")
        tree.column("Cliente", width=250, anchor="w")
        
        def actualizar_datos(filtro="Todos"):
            pagos = self.db.obtener_pagos()
            hoy_str = datetime.now().strftime("%Y-%m-%d")
            mes_str = datetime.now().strftime("%Y-%m")
            
            pagos_filtrados = []
            for p in pagos:
                if filtro == "Hoy":
                    if p[2] == hoy_str: pagos_filtrados.append(p)
                elif filtro == "Este Mes":
                    if p[2].startswith(mes_str): pagos_filtrados.append(p)
                else:
                    pagos_filtrados.append(p)
                    
            for item in tree.get_children(): tree.delete(item)
            for p in pagos_filtrados: tree.insert("", "end", values=p)
                
            t_men = sum(p[4] for p in pagos_filtrados if p[3] == "Mensual")
            t_dia = sum(p[4] for p in pagos_filtrados if p[3] == "Diario")
            t_gen = sum(p[4] for p in pagos_filtrados)
            
            lbl_cant.set(str(len(pagos_filtrados)))
            lbl_diario.set(f"${t_dia:.2f}")
            lbl_mensual.set(f"${t_men:.2f}")
            lbl_total.set(f"${t_gen:.2f}")
            
        ctk.CTkButton(frame_filtros, text="Hoy", width=100, fg_color="#3498DB", command=lambda: actualizar_datos("Hoy")).pack(side="left", padx=5)
        ctk.CTkButton(frame_filtros, text="Este Mes", width=100, fg_color="#2980B9", command=lambda: actualizar_datos("Este Mes")).pack(side="left", padx=5)
        ctk.CTkButton(frame_filtros, text="Todos", width=100, fg_color="#1ABC9C", command=lambda: actualizar_datos("Todos")).pack(side="left", padx=5)
        
        def anular_pago():
            sel = tree.selection()
            if not sel: return
            id_pago = tree.item(sel[0])['values'][0]
            cliente_nombre = tree.item(sel[0])['values'][1]
            monto = tree.item(sel[0])['values'][4]
            
            if self.rol_actual != "Admin":
                messagebox.showerror("Acceso Denegado", "Solo el Administrador puede anular pagos.", parent=dialog)
                return
                
            dialogo_pin = ctk.CTkInputDialog(text=f"Anulando pago de {cliente_nombre} (${monto})\nIngrese PIN Admin:", title="Seguridad")
            pin_input = dialogo_pin.get_input()
            if pin_input is not None and self.verificar_credenciales(self.user_admin, pin_input) == "Admin":
                if messagebox.askyesno("Confirmar", f"¿Está completamente seguro de ELIMINAR el pago #{id_pago}?", parent=dialog):
                    self.db.eliminar_pago(id_pago)
                    messagebox.showinfo("Éxito", "Pago anulado de la contabilidad.", parent=dialog)
                    actualizar_datos("Todos")
            elif pin_input is not None:
                messagebox.showerror("Error", "PIN Incorrecto.", parent=dialog)
                
        ctk.CTkButton(frame_filtros, text="❌ Anular Pago", width=120, fg_color="#E74C3C", hover_color="#C0392B", command=anular_pago).pack(side="right", padx=5)
        
        frame_reporte = ctk.CTkFrame(dialog, fg_color="#F8F9FA", corner_radius=10)
        frame_reporte.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(frame_reporte, text="RESUMEN DE PAGOS", font=("Arial", 16, "bold"), text_color="#2C3E50").pack(pady=(10, 5))
        
        frame_totales = ctk.CTkFrame(frame_reporte, fg_color="transparent")
        frame_totales.pack(pady=10)
        
        def crear_caja_total(parent, titulo, text_var, color):
            caja = ctk.CTkFrame(parent, fg_color="white", corner_radius=8, width=160, height=80, border_width=1, border_color="#E0E0E0")
            caja.pack_propagate(False)
            caja.pack(side="left", padx=10)
            ctk.CTkLabel(caja, text=titulo, font=("Arial", 11, "bold"), text_color="#7F8C8D").pack(pady=(10, 0))
            ctk.CTkLabel(caja, textvariable=text_var, font=("Arial", 18, "bold"), text_color=color).pack(pady=(5, 0))
            
        crear_caja_total(frame_totales, "Cant. Pagos", lbl_cant, "#34495E")
        crear_caja_total(frame_totales, "Total Diario", lbl_diario, "#E67E22")
        crear_caja_total(frame_totales, "Total Mensual", lbl_mensual, "#27AE60")
        crear_caja_total(frame_totales, "GRAN TOTAL", lbl_total, "#2980B9")
        
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        actualizar_datos("Este Mes")

    def mostrar_pagos_faltantes(self):
        self.modo_filtro = True
        if self.view:
            self.view.lbl_titulo.configure(text="⚠️ Pagos Faltantes")
        todos = self.db.obtener_todos()
        filtrados = []
        hoy = datetime.now().date()
        for row in todos:
            dias = (self._parsear_fecha(row[4]) - hoy).days
            if dias < 0: filtrados.append(row)
        self._llenar_tabla(filtrados)

    def importar_excel(self):
        ruta = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
        if not ruta: return
        try:
            df = pd.read_excel(ruta)
            df.columns = [str(c).strip().upper() for c in df.columns]
            hoy_dt = datetime.now()
            meses_prioridad = ['DICIEMBRE', 'NOVIEMBRE', 'OCTUBRE', 'SEPTIEMBRE', 'AGOSTO', 'JULIO', 'JUNIO', 'MAYO', 'ABRIL', 'MARZO', 'FEBRERO', 'ENERO']

            for _, row in df.iterrows():
                nombre = str(row.get('NOMBRE', '')).strip()
                if nombre == 'nan' or not nombre or 'NOMBRE' in nombre.upper(): continue
                cel_raw = row.get('CELULAR')
                cel = "SN" if pd.isna(cel_raw) or str(cel_raw).strip() == "" else str(cel_raw).split('.')[0].strip()
                
                nota = ""
                cols = list(df.columns)
                if 'CELULAR' in cols:
                    idx_cel = cols.index('CELULAR')
                    if idx_cel + 1 < len(cols):
                        val_nota = row.iloc[idx_cel + 1]
                        if pd.notna(val_nota): nota = str(val_nota).strip()

                f_ini_db = hoy_dt.strftime("%Y-%m-%d")
                for mes in meses_prioridad:
                    if mes in df.columns:
                        val_f = row.get(mes)
                        if pd.notna(val_f):
                            try:
                                f_ini_db = pd.to_datetime(val_f).strftime("%Y-%m-%d")
                                break
                            except: continue

                f_ini_obj = datetime.strptime(f_ini_db, "%Y-%m-%d")
                f_ven_obj = self.calcular_fecha_mensual(f_ini_obj)
                id_c = self.db.agregar_cliente(nombre, cel, f_ini_db, f_ven_obj.strftime("%Y-%m-%d"))
                if nota: self.db.actualizar_comentario(id_c, nota)
            
            messagebox.showinfo("Éxito", "Importación completada.")
            self.filtro_actual()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el Excel: {str(e)}")