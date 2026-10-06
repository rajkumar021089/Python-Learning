import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from Programs import employee


class Employee(BaseModel):
    id: str
    name: str
    department: str
    salary: float   


app = FastAPI(title="Employee Management API", description="CRUD API using FastAPI and SQLite", version="1.0")  



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

@app.get("/employees")
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    close_connection(conn)
    return rows

@app.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    row = cursor.fetchone()
    close_connection(conn)
    return row

@app.post("/employees")
def add_employee(employees:  list[Employee]):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for employee in employees:
            cursor.execute("INSERT INTO employees (id, name, department, salary) VALUES (?, ?, ?, ?)",
                           (employee.id, employee.name, employee.department, employee.salary))
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity Error: {str(e)}")
    conn.commit()       
    close_connection(conn)  

@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, employee: Employee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET name = ?, department = ?, salary = ? WHERE id = ?",
                   (employee.name, employee.department, employee.salary, employee_id))
    conn.commit()
    close_connection(conn)
 


