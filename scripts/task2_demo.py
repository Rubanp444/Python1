"""Run: python -m scripts.task2_demo"""

from pathlib import Path

from src.file_utils import (
    DATA_DIR,
    create_salary_xlsx,
    extract_pdf_text,
    read_employees_csv,
    read_file,
    write_high_earners,
    write_json,
)

if __name__ == "__main__":
    rows = read_employees_csv()
    write_json(rows, DATA_DIR / "employees.json")
    high = write_high_earners(rows, DATA_DIR / "high_earners.csv")
    print(f"Rows read: {len(rows)} | High earners written: {high}")

    count = create_salary_xlsx(rows, DATA_DIR / "salary.xlsx")
    print(f"salary.xlsx created and read back: {count} rows")

    pdf = Path(__file__).resolve().parent.parent / "docs" / "sample.pdf"
    print(extract_pdf_text(pdf)[:100])

    read_file("missing.txt")
