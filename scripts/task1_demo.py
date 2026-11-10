"""Run: python -m scripts.task1_demo"""

from src.core import Manager, calculate_bonus, print_categories
from src.file_utils import read_employees_csv

if __name__ == "__main__":
    print_categories(read_employees_csv())
    print(Manager("Divya", 75000, 5).get_details())
    print("Bonus:", calculate_bonus(50000, 0.1, 500, 250, cap=5000))
