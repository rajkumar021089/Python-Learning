import sqlite3

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(
    title="Employee Management API",
    description="CRUD API using FastAPI and SQLite",
    version="1.0"
)

DB_NAME = "employees.db"


# --------------------------------
# DATABASE CONNECTION
# --------------------------------

def get_connection():
    conn = sqlite3.connect(DB_NAME)

    # Allows us to access columns using column names
    conn.row_factory = sqlite3.Row

    return conn


# --------------------------------
# CREATE TABLE
# --------------------------------

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EMPLOYEE (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()


create_table()


# --------------------------------
# PYDANTIC MODEL
# --------------------------------

class Employee(BaseModel):
    name: str
    department: str
    salary: float
    email: str | None = None


# --------------------------------
# HOME API
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "Employee Management API"
    }


# --------------------------------
# CREATE EMPLOYEE
# POST /employees
# --------------------------------

@app.post(
    "/employees",
    status_code=status.HTTP_201_CREATED
)
def create_employee(employee: Employee):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO EMPLOYEE
        (
            name,
            department,
            salary,
            email
        )
        VALUES (?, ?, ?, ?)
    """, (
        employee.name,
        employee.department,
        employee.salary,
        employee.email
    ))

    conn.commit()

    employee_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Employee created successfully",
        "employee_id": employee_id
    }


# --------------------------------
# GET ALL EMPLOYEES
# GET /employees
# --------------------------------

@app.get("/employees")
def get_employees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM EMPLOYEE
        ORDER BY employee_id
    """)

    employees = cursor.fetchall()

    conn.close()

    return [
        dict(employee)
        for employee in employees
    ]


# --------------------------------
# GET EMPLOYEE BY ID
# GET /employees/1
# --------------------------------

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM EMPLOYEE
        WHERE employee_id = ?
    """, (employee_id,))

    employee = cursor.fetchone()

    conn.close()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return dict(employee)


# --------------------------------
# UPDATE EMPLOYEE
# PUT /employees/1
# --------------------------------

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: Employee
):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if employee exists
    cursor.execute("""
        SELECT employee_id
        FROM EMPLOYEE
        WHERE employee_id = ?
    """, (employee_id,))

    existing_employee = cursor.fetchone()

    if existing_employee is None:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    cursor.execute("""
        UPDATE EMPLOYEE

        SET name = ?,
            department = ?,
            salary = ?,
            email = ?

        WHERE employee_id = ?
    """, (
        employee.name,
        employee.department,
        employee.salary,
        employee.email,
        employee_id
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Employee updated successfully"
    }


# --------------------------------
# DELETE EMPLOYEE
# DELETE /employees/1
# --------------------------------

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM EMPLOYEE
        WHERE employee_id = ?
    """, (employee_id,))

    conn.commit()

    deleted_rows = cursor.rowcount

    conn.close()

    if deleted_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }