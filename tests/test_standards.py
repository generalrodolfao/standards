from __future__ import annotations

from pathlib import Path

from aurum.engine import run_checks
from aurum.models import Severity, Report, CheckResult
from aurum.checks import (
    PyprojectExists,
    PytestConfigured,
    CoverageConfigured,
    TestFilesExist,
    RuffConfigured,
    MypyConfigured,
    MakefileExists,
    GitignoreExists,
    GitignoreHasDStore,
    GitignoreHasPycache,
    GitignoreHasVenv,
    GitignoreHasEnv,
    EnvExampleExists,
    ReadmeExists,
    DockerComposeExists,
    DockerfileExists,
    DockerignoreExists,
    CiWorkflowExists,
    ClaudeMdExists,
    PreCommitConfigExists,
    AdrDirExists,
)


def test_report_creation():
    r = Report(project=Path("/tmp/test"))
    assert r.total == 0
    assert r.score == 100
    assert r.passed_count == 0
    assert r.failed_count == 0


def test_report_with_results():
    r = Report(project=Path("/tmp/test"))
    def _r(passed, sev, skipped=False):
        return type("obj", (), {"passed": passed, "severity": sev, "id": "T", "message": "x", "fixable": False, "skipped": skipped})()
    r.results.append(_r(True, Severity.ERROR))
    r.results.append(_r(False, Severity.ERROR))
    assert r.total == 2
    assert r.passed_count == 1
    assert r.failed_count == 1
    assert r.score == 50


class TestGoodProject:
    def test_all_passes(self, python_project: Path):
        report = run_checks(python_project)
        errors = [r for r in report.results if not r.passed and not r.skipped and r.severity == Severity.ERROR]
        error_msgs = [f"{r.id}: {r.message} (skipped={r.skipped})" for r in report.results if not r.passed and r.severity == Severity.ERROR]
        assert not errors, f"Checks com ERRO:\n" + "\n".join(error_msgs) + "\n(destes, skipped: {sum(1 for r in report.results if not r.passed and r.skipped)})"
        assert report.score >= 80

    def test_specific_checks(self, python_project: Path):
        for check_cls in [
            PyprojectExists, PytestConfigured, CoverageConfigured,
            TestFilesExist, RuffConfigured, MypyConfigured,
            MakefileExists, GitignoreExists, GitignoreHasDStore,
            GitignoreHasPycache, GitignoreHasVenv, GitignoreHasEnv,
            EnvExampleExists, ReadmeExists,
            DockerComposeExists, DockerfileExists,
            CiWorkflowExists, ClaudeMdExists, PreCommitConfigExists,
        ]:
            result = check_cls(python_project).run()
            assert result.passed, f"{check_cls.id}: {result.message}"

    def test_adr_check(self, python_project: Path):
        result = AdrDirExists(python_project).run()
        assert result.passed

    def test_dockerignore_exists(self, python_project: Path):
        result = DockerignoreExists(python_project).run()
        assert result.passed


class TestBadProject:
    def test_most_fail(self, bad_project: Path):
        report = run_checks(bad_project)
        passed = len([r for r in report.results if r.passed])
        assert passed < 5

    def test_pyproject_missing(self, bad_project: Path):
        result = PyprojectExists(bad_project).run()
        assert not result.passed

    def test_gitignore_missing(self, bad_project: Path):
        result = GitignoreExists(bad_project).run()
        assert not result.passed

    def test_docker_compose_missing(self, bad_project: Path):
        result = DockerComposeExists(bad_project).run()
        assert not result.passed

    def test_env_example_missing(self, bad_project: Path):
        result = EnvExampleExists(bad_project).run()
        assert not result.passed

    def test_readme_missing(self, bad_project: Path):
        result = ReadmeExists(bad_project).run()
        assert not result.passed

    def test_ci_missing(self, bad_project: Path):
        result = CiWorkflowExists(bad_project).run()
        assert not result.passed


class TestCheckEdgeCases:
    def test_pycache_not_committed(self, tmp_project: Path):
        from aurum.checks import PcacheNotCommitted
        result = PcacheNotCommitted(tmp_project).run()
        assert result.passed

    def test_gitignore_fix(self, tmp_project: Path):
        gitignore = tmp_project / ".gitignore"
        gitignore.write_text("# empty\n")
        result = GitignoreHasDStore(tmp_project).run()
        assert not result.passed
        GitignoreHasDStore(tmp_project).fix()
        content = gitignore.read_text()
        assert ".DS_Store" in content

    def test_pyproject_not_python(self, tmp_project: Path):
        result = PyprojectExists(tmp_project).run()
        assert not result.passed

    def test_env_example_fix(self, tmp_project: Path):
        from aurum.checks import EnvExampleExists
        result = EnvExampleExists(tmp_project).run()
        assert not result.passed
        result2 = EnvExampleExists(tmp_project)
        result2.fix()
        assert (tmp_project / ".env.example").exists()
