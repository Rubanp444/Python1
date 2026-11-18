"""Task 4: FastAPI Employee Data Service."""

import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Employee Data Service")

# Tests override this with a temporary file.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "employees.json"


class EmployeeIn(BaseModel):
    name: str = Field(..., min_length=1)
    department: str = "Unknown"
    salary: float = Field(..., gt=0)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be empty")
        return v


def _load() -> List[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def _save(rows: List[dict]) -> None:
    DATA_FILE.write_text(json.dumps(rows, indent=2), encoding="utf-8")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/employees")
def list_employees() -> List[dict]:
    return _load()


@app.get("/employees/{name}")
def get_employee(name: str) -> dict:
    for emp in _load():
        if emp["name"].lower() == name.lower():
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeIn) -> dict:
    rows = _load()
    new = employee.model_dump()
    rows.append(new)
    _save(rows)
    return new
