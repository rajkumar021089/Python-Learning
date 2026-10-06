
def calculate_bonus(salary):
    if salary < 1000:
        return salary * 0.1 
    elif salary > 500 and salary <= 1000:
        return salary * 0.05
    else:
        return 0

def get_salary_level(salary):
    if salary > 1000:
        return "High"
    elif salary > 700:
        return "Medium"
    else:
        return "Low"

def calculate_total_salary(salary):
    bonus = calculate_bonus(salary)
    total_salary = salary + bonus
    return total_salary
    