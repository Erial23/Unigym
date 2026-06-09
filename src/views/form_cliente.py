import customtkinter as ctk
from datetime import datetime
import calendar
from tkinter import messagebox
from .styles import *

class FormularioCliente(ctk.CTkToplevel):
    def __init__(self, parent, callback, datos_editar=None):
        super().__init__(parent)
        self.callback = callback
        self.datos_editar = datos_editar
        
        titulo_ventana = "Editar Cliente / Renovación" if datos_editar else "Nuevo Cliente"
        self.title(titulo_ventana)
        self.geometry("400x650" if datos_editar else "400x660") 
        self.configure(fg_color=C_FONDO_BLANCO)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        vcmd = (self.register(self._validar_telefono), '%P')
        ctk.CTkLabel(self, text=titulo_ventana.upper(), font=FONT_TITULO, text_color=C_TEXTO_TITULO).pack(pady=(25, 20))

        # --- Campos Generales ---
        self.entry_nom = self._crear_campo("Nombre Completo:")
        
        ctk.CTkLabel(self, text="Teléfono (10 números):", text_color=C_TEXTO_SECUNDARIO, font=FONT_NORMAL, anchor="w").pack(fill="x", padx=40, pady=(5,0))
        self.entry_tel = ctk.CTkEntry(self, width=320, height=40, fg_color="#F0F0F0", border_width=0, text_color="black", validate="key", validatecommand=vcmd)
        self.entry_tel.pack(pady=5)
        
        # Obtenemos la fecha de hoy para usarla como valor predeterminado solo en nuevos
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

        # COMBO DE TIPO DE PAGO (Visible en Nuevo y Editar)
        ctk.CTkLabel(self, text="Plan (Mensual/Diario):", text_color=C_TEXTO_SECUNDARIO, font=FONT_NORMAL, anchor="w").pack(fill="x", padx=40, pady=(10,0))
        self.var_plan = ctk.StringVar(value="Mensual")
        self.combo = ctk.CTkComboBox(self, variable=self.var_plan, values=["Mensual", "Diario"], width=320, height=40, state="readonly", fg_color="#F0F0F0", border_width=0, text_color="black", button_color=C_VERDE_LOGO)
        self.combo.pack(pady=5)

        # ============================================================
        # 🟢 LÓGICA SI ES NUEVO CLIENTE
        # ============================================================
        if not datos_editar:
            
            ctk.CTkLabel(self, text="Monto Pagado ($):", text_color=C_TEXTO_SECUNDARIO, font=FONT_NORMAL, anchor="w").pack(fill="x", padx=40, pady=(10,0))
            self.entry_monto = ctk.CTkEntry(self, width=320, height=40, fg_color="#F0F0F0", border_width=0, text_color="black")
            self.entry_monto.insert(0, "25.00")
            self.entry_monto.pack(pady=5)
            
            def _actualizar_monto(choice):
                self.entry_monto.delete(0, 'end')
                if choice == "Mensual":
                    self.entry_monto.insert(0, "25.00")
                else:
                    self.entry_monto.insert(0, "2.00")
            self.combo.configure(command=_actualizar_monto)

            ctk.CTkLabel(self, text="Fecha de Inicio:", text_color=C_TEXTO_SECUNDARIO, font=FONT_NORMAL, anchor="w").pack(fill="x", padx=40, pady=(15,5))
            self.frame_fecha = ctk.CTkFrame(self, fg_color="transparent")
            self.frame_fecha.pack(pady=5)
            self.var_tipo_fecha = ctk.StringVar(value="Hoy")
            
            self.radio_hoy = ctk.CTkRadioButton(self.frame_fecha, text="Hoy", variable=self.var_tipo_fecha, value="Hoy", command=self._toggle_fecha, text_color="#333", fg_color=C_VERDE_LOGO)
            self.radio_hoy.pack(side="left", padx=10)
            self.radio_otra = ctk.CTkRadioButton(self.frame_fecha, text="Elegir Fecha", variable=self.var_tipo_fecha, value="Otra", command=self._toggle_fecha, text_color="#333", fg_color=C_VERDE_LOGO)
            self.radio_otra.pack(side="left", padx=10)

            self.entry_fecha = ctk.CTkEntry(self, width=320, height=40, fg_color="#F0F0F0", text_color="gray", placeholder_text="DD/MM/AAAA")
            self.entry_fecha.insert(0, fecha_hoy)
            self.entry_fecha.configure(state="disabled")
            self.entry_fecha.pack(pady=5)

        # ============================================================
        # 🟡 LÓGICA SI ES EDITAR CLIENTE (Ciclo Personalizado)
        # ============================================================
        else:
            ctk.CTkLabel(self, text="📅 Ciclo de pago individual del cliente", font=("Arial", 10, "bold"), text_color=C_VERDE_LOGO).pack(pady=(10, 0))
            self.entry_inicio = self._crear_campo("Fecha de Inicio Actual:")
            self.entry_venc = self._crear_campo("Nuevo Vencimiento (+1 Mes):")
            
            # Recuperar fechas de la base de datos (datos_editar[3] inicio, [4] vencimiento)
            try:
                f_db_inicio = datetime.strptime(datos_editar[3], "%Y-%m-%d")
                f_db_venc = datetime.strptime(datos_editar[4], "%Y-%m-%d")
            except:
                # Si fallan los guiones (formatos viejos), intentamos barras
                f_db_inicio = datetime.now()
                f_db_venc = datetime.now()

            # Mantenemos su día original de inicio
            f_inicio_vis = f_db_inicio.strftime("%d/%m/%Y")
            
            # Calculamos el próximo vencimiento basándonos en su vencimiento actual
            f_nueva_venc = self._calcular_proximo_ciclo(f_db_venc)
            f_venc_vis = f_nueva_venc.strftime("%d/%m/%Y")

            # Cargamos nombre y teléfono originales
            self.entry_nom.insert(0, datos_editar[1])
            self.entry_tel.insert(0, datos_editar[2])
            
            # Cargamos las fechas respetando el día de cada cliente
            self.entry_inicio.insert(0, f_inicio_vis)
            self.entry_venc.insert(0, f_venc_vis)

            # Recalcular fecha de vencimiento si cambia el plan
            def _actualizar_vencimiento_edit(choice):
                f_nueva = self._calcular_proximo_ciclo(f_db_venc, choice)
                self.entry_venc.delete(0, 'end')
                self.entry_venc.insert(0, f_nueva.strftime("%d/%m/%Y"))
            self.combo.configure(command=_actualizar_vencimiento_edit)

        texto_btn = "ACTUALIZAR DATOS" if datos_editar else "GUARDAR CLIENTE"
        ctk.CTkButton(self, text=texto_btn, fg_color=C_VERDE_LOGO, hover_color=C_VERDE_HOVER, text_color="white", font=("Arial", 13, "bold"), width=320, height=45, command=self._enviar).pack(pady=30)

    def _calcular_proximo_ciclo(self, fecha_actual, plan="Mensual"):
        """Aumenta exactamente un mes o un día dependiendo del plan."""
        if plan == "Diario":
            from datetime import timedelta
            return fecha_actual + timedelta(days=1)
            
        anio = fecha_actual.year
        mes = fecha_actual.month + 1
        if mes > 12:
            mes = 1
            anio += 1
        # Ajuste para meses con menos días (ej. de día 31 a un mes de 30 días)
        dia = min(fecha_actual.day, calendar.monthrange(anio, mes)[1])
        return datetime(anio, mes, dia)

    def _validar_telefono(self, t):
        return t == "" or (t.isdigit() and len(t) <= 10)

    def _crear_campo(self, titulo):
        ctk.CTkLabel(self, text=titulo, text_color=C_TEXTO_SECUNDARIO, font=FONT_NORMAL, anchor="w").pack(fill="x", padx=40, pady=(5,0))
        entry = ctk.CTkEntry(self, width=320, height=40, fg_color="#F0F0F0", border_width=0, text_color="black")
        entry.pack(pady=5)
        return entry

    def _toggle_fecha(self):
        if self.var_tipo_fecha.get() == "Hoy":
            self.entry_fecha.configure(state="disabled", fg_color="#F0F0F0", text_color="gray", border_width=0)
            self.entry_fecha.delete(0, 'end')
            self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        else:
            self.entry_fecha.configure(state="normal", fg_color="white", text_color="black", border_width=2, border_color=C_VERDE_LOGO)
            self.entry_fecha.focus()

    def _enviar(self):
        nom = self.entry_nom.get().strip()
        tel = self.entry_tel.get().strip()
        if not nom: 
            messagebox.showwarning("Atención", "El nombre es obligatorio.")
            return

        if self.datos_editar:
            f_ini = self.entry_inicio.get().strip()
            f_ven = self.entry_venc.get().strip()
            if len(f_ini) != 10 or "/" not in f_ini or len(f_ven) != 10 or "/" not in f_ven:
                messagebox.showerror("Error", "Usa el formato DD/MM/AAAA")
                return
            self.callback(nom, tel, f_ini, f_ven, self.datos_editar[0])
        else:
            fecha_inicio = "HOY" if self.var_tipo_fecha.get() == "Hoy" else self.entry_fecha.get().strip()
            if fecha_inicio != "HOY" and (len(fecha_inicio) != 10 or "/" not in fecha_inicio):
                messagebox.showerror("Error", "Usa el formato DD/MM/AAAA")
                return
            monto_str = self.entry_monto.get().strip()
            try:
                monto_float = float(monto_str.replace(",", "."))
            except ValueError:
                messagebox.showerror("Error", "El monto ingresado no es válido.")
                return
            self.callback(nom, tel, self.var_plan.get(), fecha_inicio, monto_float)
        self.destroy()