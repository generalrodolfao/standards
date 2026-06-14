from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterator

import pytest


@pytest.fixture
def tmp_project() -> Iterator[Path]:
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def python_project(tmp_project: Path) -> Path:
    project = tmp_project
    pyproject = project / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "test-project"
version = "0.1.0"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.report]
fail_under = 80

[tool.ruff]
line-length = 100

[tool.mypy]
strict = true
""")
    (project / "tests").mkdir()
    (project / "tests" / "test_example.py").write_text("def test_pass():\n    assert 1 + 1 == 2\n")
    (project / ".gitignore").write_text("__pycache__/\n.venv/\n.DS_Store\n.env\n")
    (project / ".env.example").write_text("SECRET=\n")
    (project / "README.md").write_text("# Test Project\n")
    (project / "Makefile").write_text("test:\n\tpytest\n")
    (project / "CLAUDE.md").write_text("# Test Project\n")
    (project / ".pre-commit-config.yaml").write_text("repos: []\n")
    (project / "docker-compose.yml").write_text("services: {}\n")
    (project / "Dockerfile").write_text("FROM python:3.12\n")
    (project / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (project / ".github/workflows/ci.yml").write_text("name: CI\n")
    (project / ".github" / "dependabot.yml").write_text("version: 2\n")
    (project / ".dockerignore").write_text("__pycache__/\n")
    (project / "adr").mkdir()
    (project / "adr" / "ADR-001.md").write_text("# ADR-001\n")
    return project


@pytest.fixture
def bad_project(tmp_project: Path) -> Path:
    project = tmp_project
    (project / "main.py").write_text("def foo():\n    pass\n")
    return project
