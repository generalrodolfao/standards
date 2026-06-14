from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import Report, Severity

console = Console()


class Reporter:
    def __init__(self, report: Report) -> None:
        self.report = report

    def terminal(self) -> None:
        r = self.report
        type_label = f"  [bold cyan]{r.project_type.value}[/bold cyan]"
        console.print()
        console.print(Panel(
            f"[bold]aurum check[/bold]  [dim]{r.project}[/dim]{type_label}",
            border_style="blue",
        ))
        console.print()

        groups: dict[str, list] = {}
        for result in r.results:
            prefix = result.id.split("-")[0]
            groups.setdefault(prefix, []).append(result)

        for prefix in sorted(groups):
            items = groups[prefix]
            label = self._group_label(prefix)
            table = Table(show_header=False, box=None, padding=(0, 1))
            for item in items:
                color = "green" if item.passed else ("red" if item.severity == Severity.ERROR else "yellow")
                icon = item.icon
                table.add_row(
                    f"[{color}]{icon}[/{color}]",
                    f"[{color}]{item.id}[/{color}]",
                    item.message,
                )
            console.print(Panel(table, title=f"[bold]{label}[/bold]", border_style="dim"))
            console.print()

        self._summary()

    def _group_label(self, prefix: str) -> str:
        labels = {
            "PY": "Python",
            "GIT": "Git & Repo",
            "DK": "Docker",
            "CI": "CI/CD",
            "DOC": "Documentação",
            "PC": "Pre-commit",
            "RAG": "RAG System",
            "AGENT": "AI Agent",
            "LP": "Landing Page",
            "TOOL": "Python Tool",
            "FW": "Fullstack Web",
            "DP": "Data Pipeline",
            "AS": "Agent System",
        }
        return labels.get(prefix, prefix)

    def _summary(self) -> None:
        r = self.report
        passed = r.passed_count
        failed = r.failed_count
        skipped = r.skipped_count
        total = r.total
        score = r.score

        color = "green" if score >= 80 else ("yellow" if score >= 50 else "red")
        bar_len = 30
        filled = int(bar_len * score / 100)
        bar = "█" * filled + "░" * (bar_len - filled)

        parts = [f"[bold green]✔ {passed} passed[/bold green]"]
        if failed:
            parts.append(f"[bold red]✘ {failed} failed[/bold red]")
        if skipped:
            parts.append(f"[dim]⊘ {skipped} skipped[/dim]")
        parts.append(f"[bold]{total} total[/bold]")
        stats = Columns(parts)
        console.print(stats)
        console.print()
        console.print(f"Score: [bold {color}]{score}%[/bold {color}]  [dim](tipo: {r.project_type.value})[/dim]")
        console.print(f"[{color}]{bar}[/{color}]")
        console.print()

        fixable = r.fixable
        if fixable:
            console.print(f"[yellow]ℹ {len(fixable)} problemas podem ser corrigidos com --fix[/yellow]")

    def json_output(self) -> str:
        r = self.report
        data = {
            "project": str(r.project),
            "score": r.score,
            "total": r.total,
            "passed": r.passed_count,
            "failed": r.failed_count,
            "skipped": r.skipped_count,
            "results": [
                {
                    "id": res.id,
                    "message": res.message,
                    "severity": res.severity.value,
                    "passed": res.passed,
                    "skipped": res.skipped,
                    "suggestion": res.suggestion,
                    "fixable": res.fixable,
                }
                for res in r.results
            ],
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def markdown(self) -> str:
        r = self.report
        lines = [        f"# aurum check: {r.project.name}", ""]
        lines.append(f"**Score:** {r.score}% | **Passed:** {r.passed_count}/{r.total}")
        lines.append("")

        for result in r.results:
            icon = result.icon
            status = "PASS" if result.passed else "FAIL"
            lines.append(f"- [{status}] {result.id}: {result.message}")
            if result.suggestion:
                lines.append(f"  - → {result.suggestion}")

        lines.append("")
        return "\n".join(lines)
