from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from .models import BlueprintType, CheckResult, Severity


FIX_TEMPLATES = Path(__file__).resolve().parent.parent / "templates"


class BaseCheck(ABC):
    __test__ = False
    id: str = ""
    message: str = ""
    severity: Severity = Severity.ERROR
    fixable: bool = False
    relevant_for: list[BlueprintType] | None = None

    def __init__(self, project: Path) -> None:
        self.project = project

    @abstractmethod
    def run(self) -> CheckResult:
        ...

    def fix(self) -> None:
        pass

    def ok(self, extra: str | None = None) -> CheckResult:
        return CheckResult(
            id=self.id, message=extra or self.message,
            severity=self.severity, passed=True, path=self.project,
        )

    def fail(self, suggestion: str | None = None) -> CheckResult:
        return CheckResult(
            id=self.id, message=self.message,
            severity=self.severity, passed=False,
            path=self.project, suggestion=suggestion, fixable=self.fixable,
        )

    def _has_file(self, *parts: str) -> bool:
        return (self.project / Path(*parts)).exists()

    def _read_file(self, *parts: str) -> str | None:
        try:
            return (self.project / Path(*parts)).read_text(encoding="utf-8")
        except (FileNotFoundError, OSError):
            return None

    def _copy_template(self, name: str, dest: Path) -> None:
        template = FIX_TEMPLATES / name
        if template.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")


# ═══════════════════════════════════════════════════════════
# Git & Repo
# ═══════════════════════════════════════════════════════════

class GitignoreExists(BaseCheck):
    id = "GIT-IGNORE-001"; message = ".gitignore não encontrado."
    severity = Severity.ERROR; fixable = True
    def run(self) -> CheckResult:
        if self._has_file(".gitignore"): return self.ok()
        return self.fail(suggestion="Copie templates/.gitignore")
    def fix(self) -> None:
        self._copy_template(".gitignore", self.project / ".gitignore")

class GitignoreHasDStore(BaseCheck):
    id = "GIT-IGNORE-002"; message = ".gitignore não inclui .DS_Store."
    severity = Severity.WARNING; fixable = True
    def run(self) -> CheckResult:
        c = self._read_file(".gitignore")
        if c is None: return self.fail()
        if ".DS_Store" in c: return self.ok()
        return self.fail(suggestion='Adicione ".DS_Store"')
    def fix(self) -> None:
        p = self.project / ".gitignore"
        if p.exists() and ".DS_Store" not in p.read_text("utf-8"):
            p.write_text(p.read_text("utf-8") + "\n.DS_Store\n", "utf-8")

class GitignoreHasPycache(BaseCheck):
    id = "GIT-IGNORE-003"; message = ".gitignore não inclui __pycache__/."
    severity = Severity.WARNING; fixable = True
    def run(self) -> CheckResult:
        c = self._read_file(".gitignore")
        if c is None: return self.fail()
        if "__pycache__" in c: return self.ok()
        return self.fail(suggestion='Adicione "__pycache__/"')
    def fix(self) -> None:
        p = self.project / ".gitignore"
        if p.exists() and "__pycache__" not in p.read_text("utf-8"):
            p.write_text(p.read_text("utf-8") + "\n__pycache__/\n", "utf-8")

class GitignoreHasVenv(BaseCheck):
    id = "GIT-IGNORE-004"; message = ".gitignore não inclui .venv/."
    severity = Severity.WARNING; fixable = True
    def run(self) -> CheckResult:
        c = self._read_file(".gitignore")
        if c is None: return self.fail()
        if ".venv" in c: return self.ok()
        return self.fail(suggestion='Adicione ".venv/"')
    def fix(self) -> None:
        p = self.project / ".gitignore"
        if p.exists() and ".venv" not in p.read_text("utf-8"):
            p.write_text(p.read_text("utf-8") + "\n.venv/\n", "utf-8")

class GitignoreHasEnv(BaseCheck):
    id = "GIT-IGNORE-005"; message = ".gitignore não inclui .env."
    severity = Severity.ERROR; fixable = True
    def run(self) -> CheckResult:
        c = self._read_file(".gitignore")
        if c is None: return self.fail()
        if ".env" in c and ".env.example" not in c: return self.ok()
        return self.fail(suggestion='Adicione ".env"')

class EnvExampleExists(BaseCheck):
    id = "GIT-ENV-001"; message = ".env.example não encontrado."
    severity = Severity.WARNING; fixable = True
    def run(self) -> CheckResult:
        if self._has_file(".env.example"): return self.ok()
        return self.fail(suggestion="Copie templates/.env.example")
    def fix(self) -> None:
        self._copy_template(".env.example", self.project / ".env.example")

class ReadmeExists(BaseCheck):
    id = "GIT-README-001"; message = "README.md não encontrado."
    severity = Severity.WARNING
    def run(self) -> CheckResult:
        if self._has_file("README.md"): return self.ok()
        return self.fail(suggestion="Crie README.md")

class PcacheNotCommitted(BaseCheck):
    id = "GIT-DIRT-001"; message = "__pycache__ rastreado pelo git."
    severity = Severity.WARNING
    def run(self) -> CheckResult:
        if not (self.project / ".git").exists():
            return CheckResult(id=self.id, message="Não é git repo.", severity=Severity.INFO, passed=True)
        try:
            r = subprocess.run(["git", "ls-files", "*__pycache__*"], capture_output=True, text=True, timeout=10, cwd=self.project)
            if r.stdout.strip(): return self.fail(suggestion="git rm -r --cached __pycache__/")
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return self.ok()


# ═══════════════════════════════════════════════════════════
# Python (projetos com pyproject.toml)
# ═══════════════════════════════════════════════════════════

PYTHON_TYPES = [
    BlueprintType.FULLSTACK_WEB, BlueprintType.DATA_PIPELINE,
    BlueprintType.RAG_SYSTEM, BlueprintType.AI_AGENT,
    BlueprintType.PYTHON_TOOL, BlueprintType.AGENT_SYSTEM,
]

class PyprojectExists(BaseCheck):
    id = "PY-CONFIG-001"; message = "pyproject.toml não encontrado."
    severity = Severity.ERROR; fixable = True; relevant_for = PYTHON_TYPES
    def run(self) -> CheckResult:
        if self._has_file("pyproject.toml"): return self.ok()
        return self.fail(suggestion="Crie pyproject.toml")
    def fix(self) -> None:
        self._copy_template("pyproject.toml", self.project / "pyproject.toml")

class PytestConfigured(BaseCheck):
    id = "PY-TEST-001"; message = "pytest não configurado."
    severity = Severity.ERROR; relevant_for = PYTHON_TYPES
    def run(self) -> CheckResult:
        c = self._read_file("pyproject.toml")
        if c is None: return self.fail()
        if "[tool.pytest.ini_options]" in c: return self.ok()
        return self.fail(suggestion="Adicione [tool.pytest.ini_options]")

class CoverageConfigured(BaseCheck):
    id = "PY-TEST-002"; message = "Coverage fail_under não configurado."
    severity = Severity.ERROR; relevant_for = PYTHON_TYPES
    def run(self) -> CheckResult:
        c = self._read_file("pyproject.toml")
        if c is None: return self.fail()
        if "fail_under" in c: return self.ok()
        return self.fail(suggestion="Adicione [tool.coverage.report] fail_under = 80")

class TestFilesExist(BaseCheck):
    id = "PY-TEST-003"; message = "Nenhum teste em tests/."
    severity = Severity.WARNING; relevant_for = PYTHON_TYPES
    def run(self) -> CheckResult:
        d = self.project / "tests"
        if not d.exists(): return self.fail(suggestion="Crie tests/")
        files = list(d.rglob("test_*.py"))
        if files: return self.ok(f"{len(files)} arquivos de teste")
        return self.fail(suggestion="Crie tests/test_example.py")

class RuffConfigured(BaseCheck):
    id = "PY-LINT-001"; message = "ruff não configurado."
    severity = Severity.ERROR; fixable = True; relevant_for = PYTHON_TYPES
    def run(self) -> CheckResult:
        c = self._read_file("pyproject.toml")
        if c is None: return self.fail()
        if "[tool.ruff]" in c: return self.ok()
        return self.fail(suggestion="Adicione [tool.ruff]")

class MypyConfigured(BaseCheck):
    id = "PY-TYPE-001"; message = "mypy não configurado."
    severity = Severity.WARNING; fixable = True; relevant_for = PYTHON_TYPES
    def run(self) -> CheckResult:
        c = self._read_file("pyproject.toml")
        if c is None: return self.fail()
        if "[tool.mypy]" in c: return self.ok()
        return self.fail(suggestion="Adicione [tool.mypy]")

class MakefileExists(BaseCheck):
    id = "PY-MAKE-001"; message = "Makefile não encontrado."
    severity = Severity.WARNING; fixable = True; relevant_for = PYTHON_TYPES
    def run(self) -> CheckResult:
        if self._has_file("Makefile"): return self.ok()
        return self.fail(suggestion="Copie templates/Makefile")
    def fix(self) -> None:
        self._copy_template("Makefile", self.project / "Makefile")


# ═══════════════════════════════════════════════════════════
# Docker (projetos web / serviço)
# ═══════════════════════════════════════════════════════════

DOCKER_TYPES = [
    BlueprintType.FULLSTACK_WEB, BlueprintType.DATA_PIPELINE,
    BlueprintType.RAG_SYSTEM, BlueprintType.AI_AGENT,
]

class DockerComposeExists(BaseCheck):
    id = "DK-COMPOSE-001"; message = "docker-compose.yml não encontrado."
    severity = Severity.WARNING; fixable = True; relevant_for = DOCKER_TYPES
    def run(self) -> CheckResult:
        if self._has_file("docker-compose.yml"): return self.ok()
        return self.fail(suggestion="Copie templates/docker-compose.yml")

class DockerfileExists(BaseCheck):
    id = "DK-DOCKER-001"; message = "Dockerfile não encontrado."
    severity = Severity.INFO; fixable = True; relevant_for = DOCKER_TYPES
    def run(self) -> CheckResult:
        if self._has_file("Dockerfile"): return self.ok()
        return self.fail(suggestion="Copie templates/Dockerfile")

class DockerignoreExists(BaseCheck):
    id = "DK-IGNORE-001"; message = ".dockerignore não encontrado."
    severity = Severity.INFO; fixable = True; relevant_for = DOCKER_TYPES
    def run(self) -> CheckResult:
        if self._has_file(".dockerignore"): return self.ok()
        return self.fail(suggestion="Crie .dockerignore")
    def fix(self) -> None:
        d = self.project / ".dockerignore"
        if not d.exists():
            d.write_text("__pycache__/\n.venv/\n.env\n.git\n.gitignore\n*.md\ntests/\n.DS_Store\n")


# ═══════════════════════════════════════════════════════════
# CI/CD
# ═══════════════════════════════════════════════════════════

CI_TYPES = [
    BlueprintType.FULLSTACK_WEB, BlueprintType.DATA_PIPELINE,
    BlueprintType.RAG_SYSTEM, BlueprintType.AI_AGENT,
    BlueprintType.PYTHON_TOOL, BlueprintType.AGENT_SYSTEM,
]

class CiWorkflowExists(BaseCheck):
    id = "CI-WORKFLOW-001"; message = ".github/workflows/ci.yml não encontrado."
    severity = Severity.WARNING; fixable = True; relevant_for = CI_TYPES
    def run(self) -> CheckResult:
        if self._has_file(".github", "workflows", "ci.yml"): return self.ok()
        return self.fail(suggestion="Crie .github/workflows/ci.yml")
    def fix(self) -> None:
        self._copy_template(".github/workflows/ci.yml", self.project / ".github" / "workflows" / "ci.yml")

class DependabotConfigured(BaseCheck):
    id = "CI-DEPENDABOT-001"; message = ".github/dependabot.yml não encontrado."
    severity = Severity.INFO; relevant_for = CI_TYPES
    def run(self) -> CheckResult:
        if self._has_file(".github", "dependabot.yml"): return self.ok()
        return self.fail(suggestion="Crie .github/dependabot.yml")


# ═══════════════════════════════════════════════════════════
# Documentação
# ═══════════════════════════════════════════════════════════

class ClaudeMdExists(BaseCheck):
    id = "DOC-CLAUDE-001"; message = "CLAUDE.md não encontrado (AI context)."
    severity = Severity.INFO; fixable = True
    def run(self) -> CheckResult:
        if self._has_file("CLAUDE.md"): return self.ok()
        return self.fail(suggestion="Copie templates/CLAUDE.md")
    def fix(self) -> None:
        self._copy_template("CLAUDE.md", self.project / "CLAUDE.md")

class AdrDirExists(BaseCheck):
    id = "DOC-ADR-001"; message = "docs/adr/ ou adr/ não encontrado."
    severity = Severity.INFO
    def run(self) -> CheckResult:
        if self._has_file("docs", "adr") or self._has_file("adr"): return self.ok()
        return self.fail(suggestion="Crie adr/ com ADR-001")


# ═══════════════════════════════════════════════════════════
# Pre-commit
# ═══════════════════════════════════════════════════════════

PC_TYPES = [
    BlueprintType.FULLSTACK_WEB, BlueprintType.DATA_PIPELINE,
    BlueprintType.RAG_SYSTEM, BlueprintType.AI_AGENT,
    BlueprintType.PYTHON_TOOL, BlueprintType.AGENT_SYSTEM,
]

class PreCommitConfigExists(BaseCheck):
    id = "PC-CONFIG-001"; message = ".pre-commit-config.yaml não encontrado."
    severity = Severity.WARNING; fixable = True; relevant_for = PC_TYPES
    def run(self) -> CheckResult:
        if self._has_file(".pre-commit-config.yaml"): return self.ok()
        return self.fail(suggestion="Copie templates/.pre-commit-config.yaml")
    def fix(self) -> None:
        self._copy_template(".pre-commit-config.yaml", self.project / ".pre-commit-config.yaml")

class PreCommitInstalled(BaseCheck):
    id = "PC-HOOKS-001"; message = "Pre-commit hooks não instalados."
    severity = Severity.INFO; relevant_for = PC_TYPES
    def run(self) -> CheckResult:
        if (self.project / ".git" / "hooks" / "pre-commit").exists(): return self.ok()
        return self.fail(suggestion="Rode: pre-commit install")


# ═══════════════════════════════════════════════════════════
# Landing Page
# ═══════════════════════════════════════════════════════════

LPT = BlueprintType.LANDING_PAGE

class LandingHtml5Doctype(BaseCheck):
    id = "LP-HTML-001"; message = "HTML sem doctype ou <!DOCTYPE html>."
    severity = Severity.WARNING; relevant_for = [LPT]
    def run(self) -> CheckResult:
        htmls = sorted(self.project.glob("*.html"))
        if not htmls: return self.ok("Nenhum arquivo .html encontrado")
        for h in htmls:
            c = self._read_file(h.name)
            if c and "<!DOCTYPE html" not in c:
                return self.fail(suggestion=f"Adicione <!DOCTYPE html> em {h.name}")
        return self.ok()

class LandingMetaViewport(BaseCheck):
    id = "LP-HTML-002"; message = "Meta viewport não encontrado nos HTMLs."
    severity = Severity.WARNING; relevant_for = [LPT]
    def run(self) -> CheckResult:
        htmls = sorted(self.project.glob("*.html"))
        if not htmls: return self.ok()
        for h in htmls:
            c = self._read_file(h.name)
            if c and "viewport" not in c:
                return self.fail(suggestion=f"Adicione <meta name='viewport'> em {h.name}")
        return self.ok()

class LandingNoVenv(BaseCheck):
    id = "LP-DIRT-001"; message = "Landing page não deveria ter .venv/."
    severity = Severity.WARNING; relevant_for = [LPT]
    def run(self) -> CheckResult:
        if self._has_file(".venv") or self._has_file("venv"):
            return self.fail(suggestion="Remova .venv/ — landing pages são estáticas")
        return self.ok()

class LandingNoPycache(BaseCheck):
    id = "LP-DIRT-002"; message = "Landing page não deveria ter __pycache__/."
    severity = Severity.WARNING; relevant_for = [LPT]
    def run(self) -> CheckResult:
        if (self.project / "__pycache__").exists():
            return self.fail(suggestion="Remova __pycache__/")
        return self.ok()


# ═══════════════════════════════════════════════════════════
# Python Tool (CLI / Script)
# ═══════════════════════════════════════════════════════════

PTT = BlueprintType.PYTHON_TOOL

class ToolEntryPoint(BaseCheck):
    id = "TOOL-CLI-001"; message = "Script sem entry point (main() / cli())."
    severity = Severity.WARNING; relevant_for = [PTT]
    def run(self) -> CheckResult:
        for pat in ("main.py", "cli.py", "app.py"):
            c = self._read_file(pat)
            if c and ("if __name__" in c or "def main" in c or "def cli" in c):
                return self.ok()
        py_files = list(self.project.glob("*.py"))
        for f in py_files:
            c = self._read_file(f.name)
            if c and ("if __name__" in c or "def main" in c):
                return self.ok(f"Entry point em {f.name}")
        return self.fail(suggestion="Adicione if __name__ == '__main__': main()")

class ToolHasTests(BaseCheck):
    id = "TOOL-TEST-001"; message = "Ferramenta sem testes."
    severity = Severity.WARNING; relevant_for = [PTT]
    def run(self) -> CheckResult:
        tests = list(self.project.rglob("test_*.py"))
        if tests: return self.ok(f"{len(tests)} arquivos de teste")
        return self.fail(suggestion="Crie tests/test_tool.py")

class ToolHasReadme(BaseCheck):
    id = "TOOL-DOC-001"; message = "README.md sem exemplos de uso."
    severity = Severity.INFO; relevant_for = [PTT]
    def run(self) -> CheckResult:
        c = self._read_file("README.md")
        if c is None: return self.fail()
        if "```" in c or "$ " in c or "Usage" in c or "Uso" in c:
            return self.ok()
        return self.fail(suggestion="Adicione exemplos de uso no README")


# ═══════════════════════════════════════════════════════════
# RAG System
# ═══════════════════════════════════════════════════════════

RAGT = BlueprintType.RAG_SYSTEM

class RagVectorStore(BaseCheck):
    id = "RAG-INFRA-001"; message = "Vector store (chroma_db/) não encontrado."
    severity = Severity.WARNING; relevant_for = [RAGT]
    def run(self) -> CheckResult:
        for d in ("chroma_db", "chromadb", "vector_store", "vectordb"):
            if (self.project / d).exists():
                return self.ok()
        c = self._read_file(".env")
        if c and ("CHROMA" in c or "QDRANT" in c or "PINECONE" in c or "WEAVIATE" in c):
            return self.ok("Vector store configurado via .env")
        py_files = list(self.project.rglob("*.py"))
        for f in py_files:
            try:
                c = f.read_text("utf-8", errors="ignore")
                if any(x in c for x in ("Chroma(", "chromadb", "QdrantClient", "Pinecone")):
                    return self.ok(f"Vector store detectado em {f.name}")
            except OSError:
                continue
        return self.fail(suggestion="Configure chroma_db/, Qdrant, ou Pinecone")

class RagEmbeddingModel(BaseCheck):
    id = "RAG-MODEL-001"; message = "Modelo de embedding não configurado."
    severity = Severity.WARNING; relevant_for = [RAGT]
    def run(self) -> CheckResult:
        c = self._read_file(".env")
        if c and ("EMBEDDING" in c or "OPENAI_API_KEY" in c or "VOYAGE" in c):
            return self.ok()
        py_files = list(self.project.rglob("*.py"))
        for f in py_files:
            try:
                c = f.read_text("utf-8", errors="ignore")
                if any(x in c for x in ("OpenAIEmbeddings", "HuggingFaceEmbeddings", "OllamaEmbeddings", "embedding")):
                    return self.ok(f"Embedding detectado em {f.name}")
            except OSError:
                continue
        return self.fail(suggestion="Configure modelo de embedding (OpenAI, Ollama, etc)")

class RagPromptTemplate(BaseCheck):
    id = "RAG-PROMPT-001"; message = "Template de prompt não encontrado."
    severity = Severity.INFO; relevant_for = [RAGT]
    def run(self) -> CheckResult:
        py_files = list(self.project.rglob("*.py"))
        for f in py_files:
            try:
                c = f.read_text("utf-8", errors="ignore")
                if any(x in c for x in ("PromptTemplate", "ChatPromptTemplate", "SystemMessagePromptTemplate")):
                    return self.ok(f"Prompt template em {f.name}")
            except OSError:
                continue
        return self.fail(suggestion="Adicione PromptTemplate para controle do prompt")

class RagTestExists(BaseCheck):
    id = "RAG-TEST-001"; message = "Testes de RAG (retrieval/qa) não encontrados."
    severity = Severity.WARNING; relevant_for = [RAGT]
    def run(self) -> CheckResult:
        tests = list(self.project.rglob("test_*.py"))
        for t in tests:
            try:
                c = t.read_text("utf-8", errors="ignore")
                if any(x in c for x in ("retrieval", "qa", "rag", "embed")):
                    return self.ok(f"Teste RAG em {t.name}")
            except OSError:
                continue
        return self.fail(suggestion="Crie tests/test_rag.py com teste de retrieval")


# ═══════════════════════════════════════════════════════════
# AI Agent (Agentes de IA Conversacionais)
# ═══════════════════════════════════════════════════════════

AIT = BlueprintType.AI_AGENT

class AgentDefinition(BaseCheck):
    id = "AGENT-CONFIG-001"; message = "Definição de agente não encontrada."
    severity = Severity.WARNING; relevant_for = [AIT]
    def run(self) -> CheckResult:
        if self._has_file("agent.py") or self._has_file("agents"):
            return self.ok()
        if list(self.project.rglob("*.agent.yaml")):
            return self.ok()
        py_files = list(self.project.rglob("*.py"))
        for f in py_files:
            try:
                c = f.read_text("utf-8", errors="ignore")
                if any(x in c for x in ("class Agent", "AgentExecutor", "create_agent", "load_agent")):
                    return self.ok(f"Agente detectado em {f.name}")
            except OSError:
                continue
        return self.fail(suggestion="Crie agent.py com a definição do agente")

class AgentToolDefinition(BaseCheck):
    id = "AGENT-TOOL-001"; message = "Tools do agente não encontradas."
    severity = Severity.INFO; relevant_for = [AIT]
    def run(self) -> CheckResult:
        py_files = list(self.project.rglob("*.py"))
        tools_found = []
        for f in py_files:
            try:
                c = f.read_text("utf-8", errors="ignore")
                if "def " in c and ("@tool" in c or "Tool(" in c or "StructuredTool" in c):
                    tools_found.append(f.name)
            except OSError:
                continue
        if tools_found:
            return self.ok(f"Tools em: {', '.join(tools_found)}")
        return self.fail(suggestion="Adicione @tool decorator ou Tool() às funções")

class AgentMemory(BaseCheck):
    id = "AGENT-MEMORY-001"; message = "Memória do agente não configurada."
    severity = Severity.INFO; relevant_for = [AIT]
    def run(self) -> CheckResult:
        py_files = list(self.project.rglob("*.py"))
        for f in py_files:
            try:
                c = f.read_text("utf-8", errors="ignore")
                if any(x in c for x in ("ConversationBufferMemory", "ConversationSummaryMemory", "Memory", "chat_history")):
                    return self.ok(f"Memória detectada em {f.name}")
            except OSError:
                continue
        return self.fail(suggestion="Configure ConversationBufferMemory")

class AgentTestExists(BaseCheck):
    id = "AGENT-TEST-001"; message = "Testes do agente não encontrados."
    severity = Severity.WARNING; relevant_for = [AIT]
    def run(self) -> CheckResult:
        tests = list(self.project.rglob("test_*.py"))
        for t in tests:
            try:
                c = t.read_text("utf-8", errors="ignore")
                if any(x in c for x in ("agent", "tool", "chain")):
                    return self.ok(f"Teste de agente em {t.name}")
            except OSError:
                continue
        return self.fail(suggestion="Crie tests/test_agent.py")


# ═══════════════════════════════════════════════════════════
# Fullstack Web
# ═══════════════════════════════════════════════════════════

FWT = BlueprintType.FULLSTACK_WEB

class HasBackend(BaseCheck):
    id = "FW-BACKEND-001"; message = "backend/ não encontrado."
    severity = Severity.WARNING; relevant_for = [FWT]
    def run(self) -> CheckResult:
        if (self.project / "backend").is_dir(): return self.ok()
        return self.fail(suggestion="Estruture em backend/ + frontend/")

class HasFrontend(BaseCheck):
    id = "FW-FRONTEND-001"; message = "frontend/ não encontrado."
    severity = Severity.INFO; relevant_for = [FWT]
    def run(self) -> CheckResult:
        if (self.project / "frontend").is_dir(): return self.ok()
        return self.fail(suggestion="Crie frontend/ (React/Vite)")


# ═══════════════════════════════════════════════════════════
# Data Pipeline
# ═══════════════════════════════════════════════════════════

DPT = BlueprintType.DATA_PIPELINE

class HasDataDirs(BaseCheck):
    id = "DP-STRUCT-001"; message = "Estrutura de dados não encontrada."
    severity = Severity.INFO; relevant_for = [DPT]
    def run(self) -> CheckResult:
        found = [d for d in ("producer", "consumer", "dbt", "airflow", "api") if (self.project / d).is_dir()]
        if found: return self.ok(f"Diretórios: {', '.join(found)}")
        return self.fail(suggestion="Adicione producer/, consumer/, dbt/, airflow/")

class HasDbtProject(BaseCheck):
    id = "DP-DBT-001"; message = "dbt_project.yml não encontrado."
    severity = Severity.INFO; relevant_for = [DPT]
    def run(self) -> CheckResult:
        if self._has_file("dbt_project.yml"): return self.ok()
        dbt_dir = self.project / "dbt"
        if (dbt_dir / "dbt_project.yml").exists(): return self.ok()
        return self.fail(suggestion="Inicialize dbt com dbt init")


# ═══════════════════════════════════════════════════════════
# Agent System (Opensquad)
# ═══════════════════════════════════════════════════════════

AST = BlueprintType.AGENT_SYSTEM

class HasSquadYaml(BaseCheck):
    id = "AS-SQUAD-001"; message = "squad.yaml não encontrado."
    severity = Severity.ERROR; relevant_for = [AST]
    def run(self) -> CheckResult:
        if self._has_file("squad.yaml"): return self.ok()
        return self.fail(suggestion="Crie squad.yaml com agentes e skills")

class HasPipelineYaml(BaseCheck):
    id = "AS-PIPELINE-001"; message = "pipeline.yaml não encontrado."
    severity = Severity.ERROR; relevant_for = [AST]
    def run(self) -> CheckResult:
        if self._has_file("pipeline.yaml"): return self.ok()
        return self.fail(suggestion="Crie pipeline.yaml com steps")

class HasSkillsDir(BaseCheck):
    id = "AS-SKILLS-001"; message = "skills/ não encontrado."
    severity = Severity.WARNING; relevant_for = [AST]
    def run(self) -> CheckResult:
        if (self.project / "skills").is_dir(): return self.ok()
        return self.fail(suggestion="Crie skills/ com SKILL.md para cada skill")


# ═══════════════════════════════════════════════════════════
# Registro Global
# ═══════════════════════════════════════════════════════════

ALL_CHECKS: list[type[BaseCheck]] = [
    # Universais
    GitignoreExists, GitignoreHasDStore, GitignoreHasPycache,
    GitignoreHasVenv, GitignoreHasEnv, EnvExampleExists,
    ReadmeExists, PcacheNotCommitted,
    ClaudeMdExists, AdrDirExists,

    # Python
    PyprojectExists, PytestConfigured, CoverageConfigured,
    TestFilesExist, RuffConfigured, MypyConfigured, MakefileExists,

    # Docker
    DockerComposeExists, DockerfileExists, DockerignoreExists,

    # CI/CD
    CiWorkflowExists, DependabotConfigured,

    # Pre-commit
    PreCommitConfigExists, PreCommitInstalled,

    # Landing Page
    LandingHtml5Doctype, LandingMetaViewport, LandingNoVenv, LandingNoPycache,

    # Python Tool
    ToolEntryPoint, ToolHasTests, ToolHasReadme,

    # RAG
    RagVectorStore, RagEmbeddingModel, RagPromptTemplate, RagTestExists,

    # AI Agent
    AgentDefinition, AgentToolDefinition, AgentMemory, AgentTestExists,

    # Fullstack
    HasBackend, HasFrontend,

    # Data Pipeline
    HasDataDirs, HasDbtProject,

    # Agent System
    HasSquadYaml, HasPipelineYaml, HasSkillsDir,
]
