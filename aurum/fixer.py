from __future__ import annotations

from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
BLUEPRINTS_DIR = Path(__file__).resolve().parent.parent / "blueprints"


def apply_templates(project: Path, blueprint: str = "fullstack-web") -> None:
    project = project.resolve()
    project.mkdir(parents=True, exist_ok=True)

    _ensure_file(project, ".gitignore", "templates/.gitignore")
    _ensure_file(project, ".env.example", "templates/.env.example")
    _ensure_file(project, ".pre-commit-config.yaml", "templates/.pre-commit-config.yaml")
    _ensure_file(project, "Makefile", "templates/Makefile")
    _ensure_file(project, "CLAUDE.md", "templates/CLAUDE.md")

    if blueprint in ("fullstack-web", "data-pipeline"):
        _ensure_dir(project, "tests")
        _ensure_dir(project, "docs/adr")
        _ensure_dir(project, "docs/spec")
        _ensure_file(project, "docker-compose.yml", "templates/docker-compose.yml")
        _ensure_file(project, "Dockerfile", "templates/Dockerfile")
        _ensure_file(project, "pyproject.toml", "templates/pyproject.toml")

    if blueprint == "data-pipeline":
        for sub in ("producer", "consumer", "dbt", "airflow", "api", "frontend", "scripts", "data"):
            _ensure_dir(project, sub)

    if blueprint == "agent-system":
        for sub in ("agents", "skills", "output"):
            _ensure_dir(project, sub)

    _ensure_dir(project, ".github/workflows")


def _ensure_file(project: Path, rel_path: str, template_rel: str) -> None:
    dest = project / rel_path
    if dest.exists():
        return
    template = TEMPLATES_DIR / template_rel.removeprefix("templates/")
    if template.exists():
        dest.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")


def _ensure_dir(project: Path, rel_path: str) -> None:
    directory = project / rel_path
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ".gitkeep").write_text("")
