#!/usr/bin/env bash
# Usage: bash scripts/git_workflow.sh <your-github-repo-url>
# Creates feature/employee-service, commits in small steps, pushes.
set -e
REPO_URL="$1"
[ -z "$REPO_URL" ] && { echo "Usage: bash scripts/git_workflow.sh <repo-url>"; exit 1; }

[ -d .git ] || git init -b main
git add .gitignore .env.example README.md requirements.txt pyproject.toml \
  .pre-commit-config.yaml data/employees.csv config docs
git commit -m "chore: add project structure, configs and sample data"
git remote add origin "$REPO_URL" 2>/dev/null || true
git push -u origin main

git checkout -b feature/employee-service

# Auto-format so the pre-commit hooks pass
black . && ruff check --fix .

git add src/__init__.py src/core.py scripts/__init__.py scripts/task1_demo.py tests/__init__.py tests/test_core.py
git commit -m "feat(task1): bonus calculator, Employee/Manager classes, log_call decorator"

git add src/file_utils.py scripts/task2_demo.py tests/test_file_utils.py
git commit -m "feat(task2): CSV/JSON/Excel/PDF handling with logging and type hints"

git add src/api_client.py scripts/task3_demo.py tests/test_api_client.py
git commit -m "feat(task3): retry session, nested JSON access, HMAC signature check"

git add src/main.py tests/test_main.py
git commit -m "feat(task4): FastAPI employee service with Pydantic validation and tests"

git add -A
git diff --cached --quiet || git commit -m "chore: final formatting and cleanup"

git push -u origin feature/employee-service
echo "Now open a Pull Request on GitHub: feature/employee-service -> main"
