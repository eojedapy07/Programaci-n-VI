import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def rows_to_list(rows):
    return [dict(r) for r in rows]

def ensure_tables():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        nota TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS barberos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        especialidad TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        barbero_id INTEGER,
        servicio_id INTEGER,
        fecha TEXT,
        hora TEXT,
        estado TEXT DEFAULT 'pendiente'
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turno_id INTEGER,
        cliente_id INTEGER,
        servicio_id INTEGER,
        monto REAL,
        fecha TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Clientes
def get_clientes():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM clientes ORDER BY id DESC")
    data = rows_to_list(c.fetchall())
    conn.close()
    return data

def create_cliente(nombre, telefono="", nota=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO clientes (nombre, telefono, nota) VALUES (?, ?, ?)", (nombre, telefono, nota))
    conn.commit()
    conn.close()

def update_cliente(cid, nombre, telefono="", nota=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE clientes SET nombre=?, telefono=?, nota=? WHERE id=?", (nombre, telefono, nota, cid))
    conn.commit()
    conn.close()

def delete_cliente(cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM clientes WHERE id=?", (cid,))
    conn.commit()
    conn.close()

# Barberos
def get_barberos():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM barberos ORDER BY id DESC")
    data = rows_to_list(c.fetchall())
    conn.close()
    return data

def create_barbero(nombre, especialidad=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO barberos (nombre, especialidad) VALUES (?, ?)", (nombre, especialidad))
    conn.commit()
    conn.close()

def update_barbero(bid, nombre, especialidad=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE barberos SET nombre=?, especialidad=? WHERE id=?", (nombre, especialidad, bid))
    conn.commit()
    conn.close()

def delete_barbero(bid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM barberos WHERE id=?", (bid,))
    conn.commit()
    conn.close()

# Servicios
def get_servicios():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM servicios ORDER BY id DESC")
    data = rows_to_list(c.fetchall())
    conn.close()
    return data

def create_servicio(nombre, precio=0.0):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO servicios (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()
    conn.close()

def update_servicio(sid, nombre, precio):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE servicios SET nombre=?, precio=? WHERE id=?", (nombre, precio, sid))
    conn.commit()
    conn.close()

def delete_servicio(sid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM servicios WHERE id=?", (sid,))
    conn.commit()
    conn.close()

# Turnos (joined names)
def get_turnos():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    SELECT t.*,
           (SELECT nombre FROM clientes WHERE id = t.cliente_id) AS cliente,
           (SELECT nombre FROM barberos WHERE id = t.barbero_id) AS barbero,
           (SELECT nombre FROM servicios WHERE id = t.servicio_id) AS servicio
    FROM turnos t
    ORDER BY t.id DESC
    """)
    data = rows_to_list(c.fetchall())
    conn.close()
    return data

def create_turno(cliente_id, barbero_id, servicio_id, fecha, hora=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO turnos (cliente_id, barbero_id, servicio_id, fecha, hora) VALUES (?, ?, ?, ?, ?)",
              (cliente_id, barbero_id, servicio_id, fecha, hora))
    conn.commit()
    conn.close()

def update_turno(tid, cliente_id, barbero_id, servicio_id, fecha, hora="", estado="pendiente"):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE turnos SET cliente_id=?, barbero_id=?, servicio_id=?, fecha=?, hora=?, estado=? WHERE id=?",
              (cliente_id, barbero_id, servicio_id, fecha, hora, estado, tid))
    conn.commit()
    conn.close()

def delete_turno(tid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM turnos WHERE id=?", (tid,))
    conn.commit()
    conn.close()

# Ventas (joined)
def get_ventas():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    SELECT v.*,
           (SELECT nombre FROM clientes WHERE id = v.cliente_id) AS cliente,
           (SELECT nombre FROM servicios WHERE id = v.servicio_id) AS servicio
    FROM ventas v
    ORDER BY v.id DESC
    """)
    data = rows_to_list(c.fetchall())
    conn.close()
    return data

def create_venta(cliente_id, servicio_id, monto, fecha):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO ventas (cliente_id, servicio_id, monto, fecha) VALUES (?, ?, ?, ?)",
              (cliente_id, servicio_id, monto, fecha))
    conn.commit()
    conn.close()

def update_venta(vid, cliente_id, servicio_id, monto, fecha):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE ventas SET cliente_id=?, servicio_id=?, monto=?, fecha=? WHERE id=?",
              (cliente_id, servicio_id, monto, fecha, vid))
    conn.commit()
    conn.close()

def delete_venta(vid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM ventas WHERE id=?", (vid,))
    conn.commit()
    conn.close()

# Users helper
def get_user_by_username(username):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Ensure tables now
ensure_tables()
