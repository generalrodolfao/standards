from __future__ import annotations

from pathlib import Path

from rich.progress import Progress, SpinnerColumn, TextColumn

from .checks import ALL_CHECKS, BaseCheck
from .models import BlueprintType, CheckResult, Report, Severity
from .reporter import console


def run_checks(
    project: Path,
    fix: bool = False,
    project_type: BlueprintType | None = None,
    verbose: bool = False,
    quiet: bool = False,
) -> Report:
    project = project.resolve()

    if project_type is None:
        project_type = BlueprintType.detect(project)

    report = Report(project=project, project_type=project_type)

    total = len(ALL_CHECKS)
    applicable = 0

    show_progress = not quiet
    if show_progress:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        )
        progress.__enter__()
        task = progress.add_task(
            f"[bold cyan]Executando {total} checks para {project_type.value}...",
            total=total,
        )

    for check_cls in ALL_CHECKS:
            check = check_cls(project)

            if not _is_relevant(check, project_type):
                report.results.append(CheckResult(
                    id=check.id,
                    message=check.message,
                    severity=check.severity,
                    passed=False,
                    skipped=True,
                    path=project,
                ))
                if show_progress:
                    progress.update(task, advance=1)
                continue

            applicable += 1

            if verbose and show_progress:
                progress.update(task, description=f"[dim]{check.id}[/dim] - {check.message}")

            result = check.run()
            report.results.append(result)

            if fix and not result.passed and result.fixable:
                try:
                    check.fix()
                    after = check.run()
                    if after.passed:
                        report.results.append(CheckResult(
                            id=f"{result.id}-FIXED",
                            message=f"Auto-fix aplicado: {result.message}",
                            severity=Severity.INFO,
                            passed=True,
                            path=result.path,
                        ))
                    else:
                        report.results.append(CheckResult(
                            id=f"{result.id}-FAILED",
                            message=f"Auto-fix falhou: {result.message}",
                            severity=Severity.ERROR,
                            passed=False,
                            path=result.path,
                        ))
                except Exception:
                    report.results.append(CheckResult(
                        id=f"{result.id}-FAILED",
                        message=f"Auto-fix exception: {result.message}",
                        severity=Severity.ERROR,
                        passed=False,
                        path=result.path,
                    ))

            if show_progress:
                progress.update(task, advance=1)

    if show_progress:
        progress.__exit__(None, None, None)

    return report


def _is_relevant(check: BaseCheck, type_: BlueprintType) -> bool:
    relevant = check.relevant_for
    if relevant is None or BlueprintType.GENERIC in relevant:
        return True
    if type_ not in relevant:
        return False
    if check.id.startswith("PY-") and not _has_python_evidence(check.project):
        return False
    if check.id.startswith("DK-") and type_ == BlueprintType.FULLSTACK_WEB and not _has_python_evidence(check.project):
        return False
    return True


def _has_python_evidence(project: Path) -> bool:
    markers = ["pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "requirements.txt"]
    for m in markers:
        if (project / m).exists():
            return True
    for f in project.rglob("*.py"):
        if ".venv" not in str(f) and "site-packages" not in str(f):
            return True
    return False
