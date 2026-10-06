def get_total_salary(employees):
    return sum(employee["salary"] for employee in employees)


def get_average_salary(employees):
    total_salary = get_total_salary(employees)
    return total_salary / len(employees) if employees else 0


def get_highest_paid_employee(employees):
    return max(employees, key=lambda employee: employee["salary"]) if employees else None


def get_department_employees(employees, department):
    return [employee for employee in employees if employee["department"] == department]



def get_lowest_paid_employee(employees):
    return min(employees, key=lambda employee: employee["salary"]) if employees else None

def get_employees_above_salary(employees, salary):
    return [employee for employee in employees if employee["salary"] > salary]



def get_department_total_salary(employees, department):
    department_employees = get_department_employees(employees, department)
    return get_total_salary(department_employees)   


def get_department_average_salary(employees, department):
    department_employees = get_department_employees(employees, department)
    return get_average_salary(department_employees) if department_employees else 0  

