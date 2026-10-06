import  employee_utils

employees = [
    {"id": "E001", "name": "Raj", "department": "IT", "salary": 1200},
    {"id": "E002", "name": "Priya", "department": "Finance", "salary": 850},
    {"id": "E003", "name": "Vikaan", "department": "IT", "salary": 500},
    {"id": "E004", "name": "Gayathri", "department": "HR", "salary": 950}
]

total_salary = employee_utils.get_total_salary(employees)
average_salary = employee_utils.get_average_salary(employees)
highest_paid_employee = employee_utils.get_highest_paid_employee(employees)
it_employees = employee_utils.get_department_employees(employees, "IT")
finance_employees = employee_utils.get_department_employees(employees, "Finance")
hr_employees = employee_utils.get_department_employees(employees, "HR")

print(f"Total Salary: {total_salary}")
print(f"Average Salary: {average_salary}")           
print(f"Highest Paid Employee: {highest_paid_employee['name'] if highest_paid_employee else None}")     
print(f"IT Employees: {len(it_employees)}")
print(f"Finance Employees: {len(finance_employees)}")
print(f"HR Employees: {len(hr_employees)}")