from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from contextlib import closing
 
app=FastAPI()


class Employees(BaseModel):
    employeeid: int
    employeeName: str
    salary: int
    department: str
    

def create_table():
    with closing(sqlite3.connect("employee.db")) as conn:
        conn.execute("""
                        CREATE TABLE IF NOT EXISTS EMPLOYEE(
                            EMPLOYEEID INT,
                            EMPLOYEENAME TXT,
                            SALARY REAL,
                            DEPARTMENT TXT
                            )
                    """)
        conn.commit()
        

create_table()


@app.post("/employee")
def create_employee(employees: list[Employees]):
    with closing(sqlite3.connect("employee.db")) as conn:

        for employee in employees:
             conn.execute("""
                        INSERT INTO EMPLOYEE(
                            EMPLOYEEID,
                            EMPLOYEENAME,
                            SALARY,
                            DEPARTMENT)
                        Values(?,?,?,?)
                        """,(
                            employee.employeeid,
                            employee.employeeName,
                            employee.salary,
                            employee.department
                        )
                    )
        conn.commit()
        
        return {
        "message": "Employee created successfully",
        "employee": [employees.model_dump() for employee in employees]
    }
    
@app.get("/employee")
def get_employee():
    with closing(sqlite3.connect("employee.db")) as conn:
        conn.row_factory = sqlite3.Row
        cursor=conn.execute("""SELECT * FROM EMPLOYEE""")
        employees=cursor.fetchall()
        return [
            dict(employee)
            for employee in employees
        ]
        

@app.post("/employee/{id}")
def get_employeeById(id: str):
    with closing(sqlite3.connect("employee.db")) as conn:
        conn.row_factory=sqlite3.Row
        cursor=conn.execute("SELECT * FROM EMPLOYEE WHERE EMPLOYEEID=?",(id,))
        employee=cursor.fetchone()
        return[
            dict(employee)
            ]

@app.get("/calculateBonus")
def calculateBonus():

    with closing(sqlite3.connect("employee.db")) as conn:

        conn.row_factory = sqlite3.Row

        cursor = conn.execute("SELECT * FROM EMPLOYEE")

        employees = cursor.fetchall()

        result = []

        for employee in employees:

            if employee["SALARY"] > 200000:
                bonus = employee["SALARY"] * 0.5
            else:
                bonus = employee["SALARY"] * 0.2

            result.append({
                "employeeId": employee["EMPLOYEEID"],
                "employeeName": employee["EMPLOYEENAME"],
                "salary": employee["SALARY"],
                "bonus": bonus
            })

        return result



        