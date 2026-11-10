"""Task 2: file handling (pathlib, CSV, JSON, Excel, PDF), logging, type hints."""

import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import openpyxl

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
EMPLOYEES_CSV = DATA_DIR / "employees.csv"
EMPLOYEES_JSON = DATA_DIR / "employees.json"


def read_employees_csv(path: Path = EMPLOYEES_CSV) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return [{**row, "salary": int(row["salary"])} for row in csv.DictReader(f)]


def write_json(rows: List[dict], path: Path = EMPLOYEES_JSON) -> None:
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def write_high_earners(rows: List[dict], path: Path, threshold: int = 50000) -> int:
    high = [r for r in rows if r["salary"] > threshold]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "department", "salary"])
        writer.writeheader()
        writer.writerows(high)
    return len(high)


def create_salary_xlsx(rows: List[dict], path: Path) -> int:
    """Create salary.xlsx, read it back, return number of data rows."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["name", "department", "salary"])
    for r in rows:
        ws.append([r["name"], r["department"], r["salary"]])
    wb.save(path)

    ws2 = openpyxl.load_workbook(path).active
    return sum(1 for _ in ws2.iter_rows(min_row=2, values_only=True))


def extract_pdf_text(pdf_path: Path, page: int = 0) -> str:
    import fitz  # PyMuPDF

    with fitz.open(pdf_path) as doc:
        return doc[page].get_text()


def read_file(path: Union[str, Path]) -> Optional[Union[dict, list]]:
    """Read a JSON file; log (not print) errors and return None on failure."""
    path = Path(path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        logger.error("File not found: %s", path)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in %s: %s", path, exc)
    return None


def find_employee(name: str, path: Path = EMPLOYEES_JSON) -> Optional[dict]:
    data = read_file(path) or []
    for emp in data:
        if emp["name"].lower() == name.lower():
            return emp
    return None
