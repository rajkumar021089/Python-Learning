import presistToDB
import employee_utils


while True:
    print("\nEmployee Management System")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. View Department Total Salary")
    print("4. View Department Average Salary")
    print("5. View Employees with Salary Above a Certain Amount")
    print("6. View Highest Paid Employee")
    print("7. view Lowest Paid Employee")
    print("8. Exit")



    choice = input("Enter your choice:").strip()

   

    if choice == "1":
        employee_id = input("Enter Employee ID: ")
        name = input("Enter Employee Name: ")
        department = input("Enter Employee Department: ")
        salary = float(input("Enter Employee Salary: "))

        employee = {
            "id": employee_id,
            "name": name,
            "department": department,
            "salary": salary
        }

        conn = presistToDB.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (id, name, department, salary) VALUES (?, ?, ?, ?)",
                       (employee["id"], employee["name"], employee["department"], employee["salary"]))
        conn.commit()
        print(f"Employee {name} added successfully.")

    elif choice == "2":
            print("Employee List:")
            employees = presistToDB.get_all_employees()
            for employee in employees:
                print(f"ID: {employee['id']}, Name: {employee['name']}, Department: {employee['department']}, Salary: {employee ['salary']}")

            input("\nPress Enter to return to the menu...")
        
    elif choice == "3":
        department = input("Enter Department Name: ")
        total_salary = employee_utils.get_department_total_salary(employees, department)
        print(f"Total Salary for {department}: {total_salary}") 
        input("\nPress Enter to return to the menu...")

    elif choice == "4":
            department = input("Enter Department Name: ")
            average_salary = employee_utils.get_department_average_salary(employees, department)
            print(f"Average Salary for {department}: {average_salary}") 
            input("\nPress Enter to return to the menu...")

    elif choice == "5":
            salary_threshold = float(input("Enter Salary to get the employees details more than that: "))
            high_earners = employee_utils.get_employees_above_salary(employees, salary_threshold)
            print(f"Employees with salary above {salary_threshold}:")
            for emp in high_earners:
                print(f"ID: {emp['id']}, Name: {emp['name']}, Department: {emp['department']}, Salary: {emp['salary']}") 
            input("\nPress Enter to return to the menu...")

    elif choice == "6":
                highest_paid = employee_utils.get_highest_paid_employee(employees)
                print(f"Highest Paid Employee: {highest_paid['name']}, Salary: {highest_paid['salary']}")
                input("\nPress Enter to return to the menu...")

    elif choice == "7":
                lowest_paid = employee_utils.get_lowest_paid_employee(employees)
                print(f"Lowest Paid Employee: {lowest_paid['name']}, Salary: {lowest_paid['salary']}")
                input("\nPress Enter to return to the menu...")

    elif choice == "8":
        print("Exiting Employee Management System.")
        break
    
    else:
        print("Invalid choice. Please try again.")



