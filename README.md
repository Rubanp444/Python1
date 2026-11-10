# Employee Data Service (Yoho Week 1 Assessment)

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then fill in real values
pre-commit install
```

## Run each task
```bash
python -m scripts.task1_demo   # classes, bonus, decorator, categories
python -m scripts.task2_demo   # CSV/JSON/Excel/PDF + logging
python -m scripts.task3_demo   # API client + HMAC (needs internet)
uvicorn src.main:app --reload  # FastAPI service, docs at /docs
pytest --cov=src               # tests + coverage
```

## Decisions
- `src/` holds reusable code; `scripts/` holds thin demo runners.
- Secrets live only in `.env` (git-ignored); `.env.example` documents them.
- `read_file` logs errors via `logging` and returns `None` instead of crashing.
- `verify_signature` uses `hmac.compare_digest` (constant-time) to avoid timing attacks.
- Zip uses `.get("zip")` to match the expected "Not Available" output; the API's real key is `zipcode`.
- FastAPI tests point `DATA_FILE` at a temp file so real data is never modified.
