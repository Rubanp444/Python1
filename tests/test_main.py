import json

import pytest
from fastapi.testclient import TestClient

from src import main

SAMPLE = [
    {"name": "Divya", "department": "IT", "salary": 75000},
    {"name": "Arun", "department": "Sales", "salary": 30000},
]


@pytest.fixture()
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "employees.json"
    data_file.write_text(json.dumps(SAMPLE))
    monkeypatch.setattr(main, "DATA_FILE", data_file)
    return TestClient(main.app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_employee_success(client):
    response = client.get("/employees/Divya")
    assert response.status_code == 200
    assert response.json()["salary"] == 75000


def test_get_employee_not_found(client):
    assert client.get("/employees/Ravi").status_code == 404


def test_post_invalid_salary(client):
    response = client.post("/employees", json={"name": "Ravi", "salary": -5})
    assert response.status_code == 422


def test_post_empty_name(client):
    response = client.post("/employees", json={"name": "", "salary": 1000})
    assert response.status_code == 422


def test_post_blank_name(client):
    response = client.post("/employees", json={"name": "   ", "salary": 1000})
    assert response.status_code == 422


def test_post_success_persists(client):
    response = client.post(
        "/employees", json={"name": "Ravi", "department": "IT", "salary": 50000}
    )
    assert response.status_code == 201
    assert client.get("/employees/Ravi").status_code == 200


def test_list_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DATA_FILE", tmp_path / "none.json")
    assert TestClient(main.app).get("/employees").json() == []
