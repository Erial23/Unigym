import sqlite3
import os

class DBManager:
    def __init__(self):
        # --- RUTA SEGURA EN DATOS DE APLICACIÓN ---
        # Usamos %APPDATA% para no requerir permisos de Administrador
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        self.data_dir = os.path.join(appdata, "UniGym_Pro")
        
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        except Exception:
            # Fallback seguro
            self.data_dir = os.path.join(os.path.expanduser("~"), "UniGym_Datos")
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)

        self.db_path = os.path.join(self.data_dir, "gym_database.db")
        
        # Creamos y actualizamos la tabla
        self._crear_tabla()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _crear_tabla(self):
        conn = self._conectar()
        cursor = conn.cursor()
        
        # Tabla original
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                fecha_inscripcion TEXT,
                fecha_vencimiento TEXT,
                estado TEXT
            )
        ''')
        
        # --- ACTUALIZACIÓN DE COLUMNAS ---
        try:
            cursor.execute("ALTER TABLE clientes ADD COLUMN comentario TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            # La columna ya existe
            pass

        try:
            cursor.execute("ALTER TABLE clientes ADD COLUMN ultima_notificacion TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            # La columna ya existe
            pass
            
        # Tabla de pagos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                fecha_pago TEXT,
                tipo_plan TEXT,
                monto REAL,
                FOREIGN KEY(id_cliente) REFERENCES clientes(id)
            )
        ''')
            
        conn.commit()
        conn.close()

    def agregar_cliente(self, nombre, telefono, inicio, vencimiento):
        """Agrega un cliente y devuelve su ID (necesario para la importación de notas)"""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, telefono, fecha_inscripcion, fecha_vencimiento, estado, comentario) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, telefono, inicio, vencimiento, "Activo", ""))
        nuevo_id = cursor.lastrowid # Recuperamos el ID recién creado
        conn.commit()
        conn.close()
        return nuevo_id

    def obtener_todos(self):
        """Retorna todos los clientes para la tabla del Panel Principal"""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nombre, telefono, fecha_inscripcion, fecha_vencimiento, estado, comentario, ultima_notificacion 
            FROM clientes 
            ORDER BY fecha_vencimiento ASC
        ''')
        datos = cursor.fetchall()
        conn.close()
        return datos

    def eliminar_cliente(self, id_cliente):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
        conn.commit()
        conn.close()

    def renovar_vencimiento(self, id_cliente, nueva_fecha):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET fecha_vencimiento=?, estado='Activo' WHERE id=?", (nueva_fecha, id_cliente))
        conn.commit()
        conn.close()

    def actualizar_cliente(self, id_cliente, nombre, telefono, fecha_inscripcion, fecha_vencimiento):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clientes 
            SET nombre=?, telefono=?, fecha_inscripcion=?, fecha_vencimiento=? 
            WHERE id=?
        ''', (nombre, telefono, fecha_inscripcion, fecha_vencimiento, id_cliente))
        conn.commit()
        conn.close()

    def actualizar_comentario(self, id_cliente, comentario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET comentario=? WHERE id=?", (comentario, id_cliente))
        conn.commit()
        conn.close()

    def actualizar_notificacion(self, id_cliente, fecha):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET ultima_notificacion=? WHERE id=?", (fecha, id_cliente))
        conn.commit()
        conn.close()

    def insertar_masivo(self, lista_clientes):
        """Inserta varios clientes a la vez (Usado en el botón de Excel)"""
        conn = self._conectar()
        cursor = conn.cursor()
        query = '''
            INSERT INTO clientes (nombre, telefono, fecha_inscripcion, fecha_vencimiento, estado, comentario) 
            VALUES (?, ?, ?, ?, 'Activo', '')
        '''
        cursor.executemany(query, lista_clientes)
        conn.commit()
        conn.close()

    def registrar_pago(self, id_cliente, fecha_pago, tipo_plan, monto=0.0):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pagos (id_cliente, fecha_pago, tipo_plan, monto)
            VALUES (?, ?, ?, ?)
        ''', (id_cliente, fecha_pago, tipo_plan, monto))
        conn.commit()
        conn.close()

    def obtener_pagos(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, COALESCE(c.nombre, 'Cliente Eliminado'), p.fecha_pago, p.tipo_plan, p.monto 
            FROM pagos p
            LEFT JOIN clientes c ON p.id_cliente = c.id
            ORDER BY p.id DESC
        ''')
        datos = cursor.fetchall()
        conn.close()
        return datos

    def eliminar_pago(self, id_pago):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pagos WHERE id=?", (id_pago,))
        conn.commit()
        conn.close()