from __future__ import annotations

from pathlib import Path

import typer

from .engine import run_checks
from .models import BlueprintType
from .reporter import Reporter, console

app = typer.Typer(
    name="aurum",
    help="Padrão Ouro — validador inteligente de qualidade de projetos",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        from importlib.metadata import version

        try:
            v = version("aurum")
        except ImportError:
            v = "0.3.0 (dev)"
        console.print(f"[bold]aurum[/bold] v{v}")
        raise typer.Exit()


def _type_callback(value: str | None) -> BlueprintType | None:
    if value is None:
        return None
    try:
        return BlueprintType(value)
    except ValueError:
        valid = ", ".join(b.value for b in BlueprintType)
        console.print(f"[red]✘[/red] Tipo inválido: {value}")
        console.print(f"  Válidos: {valid}")
        raise typer.Exit(code=1)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Mostra versão",
        callback=_version_callback,
    ),
) -> None:
    pass


@app.command()
def check(
    project: Path = typer.Argument(
        ".",
        help="Caminho do projeto",
        exists=True,
        file_okay=False,
        readable=True,
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        help="Tenta corrigir problemas automaticamente",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Saída em JSON (para CI)",
    ),
    markdown: bool = typer.Option(
        False,
        "--md",
        help="Saída em Markdown",
    ),
    project_type: str | None = typer.Option(
        None,
        "--type",
        "-t",
        help="Tipo de projeto (auto-detect se omitido)",
        callback=_type_callback,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Mostra detalhes",
    ),
) -> None:
    """Audita um projeto contra os padrões de qualidade."""
    ptype = BlueprintType(project_type) if project_type else None
    quiet = json_output or markdown
    report = run_checks(project, fix=fix, project_type=ptype, verbose=verbose, quiet=quiet)

    if json_output:
        console.print(report_to_json(report))
    elif markdown:
        console.print(report_to_md(report))
    else:
        Reporter(report).terminal()

    if report.errors:
        raise typer.Exit(code=1)


def report_to_json(r):
    import json

    from .models import Severity

    data = {
        "project": str(r.project),
        "project_type": r.project_type.value,
        "score": r.score,
        "total": r.total,
        "passed": r.passed_count,
        "failed": r.failed_count,
        "skipped": r.skipped_count,
        "results": [
            {
                "id": res.id,
                "message": res.message,
                "severity": res.severity.value
                if isinstance(res.severity, Severity)
                else res.severity,
                "passed": res.passed,
                "skipped": res.skipped,
                "suggestion": res.suggestion,
                "fixable": res.fixable,
            }
            for res in r.results
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def report_to_md(r):
    lines = [
        f"# aurum check: {r.project.name}",
        "",
        f"**Tipo:** {r.project_type.value} | **Score:** {r.score}%",
        f"**Passed:** {r.passed_count}/{r.total} | **Failed:** {r.failed_count} | **Skipped:** {r.skipped_count}",
        "",
    ]
    for res in r.results:
        if res.skipped:
            status = "SKIP"
        else:
            status = "PASS" if res.passed else "FAIL"
        lines.append(f"- [{status}] {res.id}: {res.message}")
        if res.suggestion:
            lines.append(f"  - → {res.suggestion}")
    lines.append("")
    return "\n".join(lines)


@app.command()
def init(
    project: Path = typer.Argument(
        ".",
        help="Caminho do projeto",
        file_okay=False,
        readable=True,
    ),
    blueprint: str = typer.Option(
        "fullstack-web",
        "--blueprint",
        "-b",
        help="Tipo de projeto (data-pipeline, fullstack-web, agent-system, rag-system, ai-agent, landing-page, python-tool)",
    ),
) -> None:
    """Inicializa um projeto com os templates padrão."""
    from .fixer import apply_templates

    apply_templates(project, blueprint)
    console.print(f"[green]✔[/green] Templates aplicados em [bold]{project}[/bold]")
    console.print("Execute [bold]aurum check[/bold] para verificar")


@app.command()
def blueprints() -> None:
    """Lista blueprints disponíveis."""
    from rich.table import Table

    table = Table(title="Blueprints Disponíveis")
    table.add_column("Nome", style="cyan")
    table.add_column("Descrição", style="white")
    table.add_column("Detecção", style="dim")

    infos = {
        "fullstack-web": "FastAPI + React/Vite + Docker",
        "data-pipeline": "Kafka + dbt + Airflow + MinIO",
        "agent-system": "Opensquad (squad.yaml + pipeline.yaml)",
        "rag-system": "ChromaDB + LangChain + embeddings",
        "ai-agent": "Agentes conversacionais com tools + memory",
        "landing-page": "HTML estático / CSS puro",
        "python-tool": "Script CLI / utilitário Python",
    }
    bp_dir = Path(__file__).resolve().parent.parent / "blueprints"
    if bp_dir.exists():
        for bp_file in sorted(bp_dir.glob("*.yaml")):
            name = bp_file.stem.replace("blueprint-", "")
            desc = infos.get(name, "")
            table.add_row(name, desc, "automática")

    console.print(table)


if __name__ == "__main__":
    app()
