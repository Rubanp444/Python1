from src.core import (
    Employee,
    Manager,
    calculate_bonus,
    print_categories,
    salary_category,
)


def test_bonus_default_rate():
    assert calculate_bonus(50000) == 5000


def test_bonus_with_extras_and_cap():
    assert calculate_bonus(50000, 0.1, 500, 250) == 5750
    assert calculate_bonus(50000, 0.1, 500, 250, cap=5000) == 5000


def test_employee_and_manager(capsys):
    assert Employee("Arun", 30000).annual_salary == 30000
    details = Manager("Divya", 75000, 5).get_details()
    assert details == "Divya - 75000 - Team Size: 5"
    assert "Calling get_details" in capsys.readouterr().out


def test_salary_category():
    assert salary_category(30000) == "Low Salary"
    assert salary_category(60000) == "Medium Salary"
    assert salary_category(75000) == "High Salary"


def test_print_categories(capsys):
    print_categories([{"name": "Arun", "salary": "30000"}])
    assert capsys.readouterr().out.strip() == "Arun - Low Salary"
