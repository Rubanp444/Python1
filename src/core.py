"""Task 1: Python core, classes, inheritance and decorators."""

from functools import wraps
from typing import Callable, List


def calculate_bonus(
    salary: float, rate: float = 0.1, *extras: float, **options: float
) -> float:
    """Bonus = salary * rate + sum(extras); never above options['cap'] if given."""
    bonus = salary * rate + sum(extras)
    if "cap" in options:
        bonus = min(bonus, options["cap"])
    return bonus


def log_call(func: Callable) -> Callable:
    """Decorator: print the function name before running it."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary

    @property
    def annual_salary(self) -> float:
        """Salary figures are annual in this dataset."""
        return self.salary

    def get_details(self) -> str:
        return f"{self.name} - {self.salary}"


class Manager(Employee):
    def __init__(self, name: str, salary: float, team_size: int) -> None:
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self) -> str:
        return f"{super().get_details()} - Team Size: {self.team_size}"


def salary_category(salary: float) -> str:
    if salary < 50000:
        return "Low Salary"
    elif salary < 70000:
        return "Medium Salary"
    else:
        return "High Salary"


def print_categories(employees: List[dict]) -> None:
    for emp in employees:
        print(f"{emp['name']} - {salary_category(float(emp['salary']))}")
