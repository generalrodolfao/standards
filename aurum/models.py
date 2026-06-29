from __future__ import annotations as _annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class BlueprintType(Enum):
    FULLSTACK_WEB = "fullstack-web"
    DATA_PIPELINE = "data-pipeline"
    AGENT_SYSTEM = "agent-system"
    RAG_SYSTEM = "rag-system"
    AI_AGENT = "ai-agent"
    LANDING_PAGE = "landing-page"
    PYTHON_TOOL = "python-tool"
    GENERIC = "generic"


    @staticmethod
    def detect(project: Path) -> BlueprintType:
        """Detecta o tipo de projeto baseado nos arquivos presentes."""
        has = lambda *p: (project / Path(*p)).exists()
        read = lambda *p: _read_file(project, *p)

        squad_yaml = has("squad.yaml")
        pipeline_yaml = has("pipeline.yaml")
        dbt_dir = has("dbt") or has("dbt_project.yml")
        airflow_dir = has("airflow") or has("dags")
        producer_dir = has("producer")
        consumer_dir = has("consumer")
        chroma_dir = has("chroma_db") or has("chromadb")
        has_langchain = _has_import(project, "langchain") or has("langchain")
        has_llamaindex = _has_import(project, "llama_index") or has("llama_index")
        has_agent_file = has("agent.py") or has("agents")
        has_squad_file = (
            (project / "squad.yaml").exists()
            or any(p.parent.name == "agents" for p in project.rglob("*.agent.yaml"))
        )
        html_files = list(project.glob("*.html"))
        pyproject = has("pyproject.toml")
        has_src = has("main.py") or has("cli.py") or has("app.py")

        if (squad_yaml or pipeline_yaml) and not chroma_dir and not has_langchain:
            return BlueprintType.AGENT_SYSTEM

        if (dbt_dir or airflow_dir or producer_dir or consumer_dir) and not has_langchain:
            return BlueprintType.DATA_PIPELINE

        if chroma_dir or has_langchain or has_llamaindex:
            return BlueprintType.RAG_SYSTEM

        if has_agent_file or has_squad_file:
            return BlueprintType.AI_AGENT

        if html_files and not pyproject and not has_src:
            return BlueprintType.LANDING_PAGE

        if pyproject and has_src and not _has_dir(project, "backend") and not _has_dir(project, "frontend"):
            return BlueprintType.PYTHON_TOOL

        if _has_dir(project, "backend") or _has_dir(project, "frontend"):
            return BlueprintType.FULLSTACK_WEB

        return BlueprintType.GENERIC


def _read_file(project: Path, *parts: str) -> str | None:
    path = project / Path(*parts)
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return None


def _has_import(project: Path, module: str) -> bool:
    for pattern in ("*.py", "*.pyx"):
        for f in project.rglob(pattern):
            if "site-packages" in str(f) or ".venv" in str(f):
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if f"import {module}" in content or f"from {module}" in content:
                    return True
            except OSError:
                continue
    return False


def _has_dir(project: Path, name: str) -> bool:
    d = project / name
    return d.is_dir() and not d.name.startswith(".")


@dataclass
class CheckResult:
    id: str
    message: str
    severity: Severity
    passed: bool
    path: Path | None = None
    suggestion: str | None = None
    fixable: bool = False
    skipped: bool = False

    @property
    def icon(self) -> str:
        if self.skipped:
            return "⊘"
        if self.passed:
            return "✔"
        if self.severity == Severity.ERROR:
            return "✘"
        if self.severity == Severity.WARNING:
            return "⚠"
        return "ℹ"


@dataclass
class Report:
    project: Path
    project_type: BlueprintType = BlueprintType.GENERIC
    results: list[CheckResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> list[CheckResult]:
        return [r for r in self.results if r.passed]

    @property
    def failed(self) -> list[CheckResult]:
        return [r for r in self.results if not r.passed and not r.skipped]

    @property
    def skipped(self) -> list[CheckResult]:
        return [r for r in self.results if r.skipped]

    @property
    def errors(self) -> list[CheckResult]:
        return [r for r in self.failed if r.severity == Severity.ERROR]

    @property
    def warnings(self) -> list[CheckResult]:
        return [r for r in self.failed if r.severity == Severity.WARNING]

    @property
    def fixable(self) -> list[CheckResult]:
        return [r for r in self.failed if r.fixable]

    @property
    def score(self) -> int:
        active = self.passed_count + self.failed_count
        if active == 0:
            return 100
        return round((self.passed_count / active) * 100)

    @property
    def passed_count(self) -> int:
        return len(self.passed)

    @property
    def failed_count(self) -> int:
        return len(self.failed)

    @property
    def skipped_count(self) -> int:
        return len(self.skipped)
