import sqlite3

def get_connection():
    conn = sqlite3.connect("employee.db")
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary REAL
    )""")
    return conn

def close_connection(conn):
    if conn:
        conn.close()    

def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    close_connection(conn)
    return rows


