import logging
from pathlib import Path

import pytest

from src import file_utils as fu


def test_csv_json_and_high_earners(tmp_path):
    rows = fu.read_employees_csv()
    assert len(rows) == 5
    fu.write_json(rows, tmp_path / "e.json")
    assert fu.write_high_earners(rows, tmp_path / "h.csv") == 3
    assert len(fu.read_file(tmp_path / "e.json")) == 5


def test_xlsx_round_trip(tmp_path):
    rows = fu.read_employees_csv()
    assert fu.create_salary_xlsx(rows, tmp_path / "s.xlsx") == 5


def test_read_file_missing_logs_error(caplog):
    with caplog.at_level(logging.ERROR):
        assert fu.read_file("missing.txt") is None
    assert "File not found" in caplog.text


def test_read_file_bad_json(tmp_path, caplog):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    with caplog.at_level(logging.ERROR):
        assert fu.read_file(bad) is None
    assert "Invalid JSON" in caplog.text


def test_find_employee(tmp_path):
    path = tmp_path / "e.json"
    fu.write_json(fu.read_employees_csv(), path)
    assert fu.find_employee("divya", path)["name"] == "Divya"
    assert fu.find_employee("Ravi", path) is None


def test_extract_pdf_text():
    pytest.importorskip("fitz")
    pdf = Path(__file__).resolve().parent.parent / "docs" / "sample.pdf"
    assert len(fu.extract_pdf_text(pdf)) > 0
