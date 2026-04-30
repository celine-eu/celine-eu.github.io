from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPOS_ROOT = ROOT.parent
CONFIG_FILE = ROOT / "repos.yaml"

DAYS_THRESHOLD = 14
COMMITS_THRESHOLD = 10

CODE_EXCLUDE_GLOBS = [
    ".gitignore",
    "LICENSE",
    ".github/",
    ".vscode/",
    ".claude/",
    ".dumpster/",
    "*.lock",
    ".python-version",
    "CHANGELOG.md",
    "AGENTS.md",
    "CLAUDE.md",
    "dump.yaml",
]

SELF_SLUG = "celine-eu.github.io"


@dataclass
class RepoReport:
    name: str
    dirname: str
    exists: bool
    last_doc_date: datetime | None = None
    last_doc_hash: str | None = None
    last_code_date: datetime | None = None
    last_code_hash: str | None = None
    days_gap: int | None = None
    commits_ahead: int | None = None
    stale: bool = False
    status: str = "OK"
    error: str | None = None


def load_config() -> list[dict]:
    with CONFIG_FILE.open() as f:
        return yaml.safe_load(f).get("repos", [])


def repo_dirname(repo: dict) -> str:
    return Path(repo["git"]).stem


def doc_pathspecs(repo: dict) -> list[str]:
    paths = repo.get("paths", ["README.md", "docs/"])
    specs: list[str] = []
    for p in paths:
        if p.endswith("/**"):
            specs.append(p[: -len("/**")] + "/")
        else:
            specs.append(p)
    return specs


def code_exclude_pathspecs(doc_specs: list[str]) -> list[str]:
    excludes = [f":!{s}" for s in doc_specs]
    excludes += [f":!{g}" for g in CODE_EXCLUDE_GLOBS]
    return excludes


def git_last_commit(repo_dir: Path, pathspecs: list[str]) -> tuple[str, datetime] | None:
    cmd = ["git", "log", "-1", "--format=%H %aI", "--"] + pathspecs
    result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
    line = result.stdout.strip()
    if not line:
        return None
    parts = line.split(" ", 1)
    if len(parts) != 2:
        return None
    commit_hash = parts[0]
    commit_date = datetime.fromisoformat(parts[1])
    return commit_hash, commit_date


def git_commits_since(repo_dir: Path, since_hash: str, pathspecs: list[str]) -> int:
    cmd = ["git", "rev-list", "--count", f"{since_hash}..HEAD", "--"] + pathspecs
    result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def check_repo(
    repo_dir: Path,
    name: str,
    dirname: str,
    doc_specs: list[str],
    days_threshold: int,
    commits_threshold: int,
) -> RepoReport:
    report = RepoReport(name=name, dirname=dirname, exists=True)

    if not repo_dir.exists() or not (repo_dir / ".git").exists():
        report.exists = False
        report.status = "SKIP"
        report.error = "not cloned"
        return report

    doc_result = git_last_commit(repo_dir, doc_specs)
    if doc_result is None:
        report.status = "NO DOCS"
        report.error = "no doc commits found"
        return report
    report.last_doc_hash, report.last_doc_date = doc_result

    code_excludes = code_exclude_pathspecs(doc_specs)
    code_result = git_last_commit(repo_dir, ["."] + code_excludes)
    if code_result is None:
        report.status = "OK"
        return report
    report.last_code_hash, report.last_code_date = code_result

    delta = report.last_code_date - report.last_doc_date
    report.days_gap = delta.days

    if report.days_gap > 0 and report.last_doc_hash:
        report.commits_ahead = git_commits_since(
            repo_dir, report.last_doc_hash, ["."] + code_excludes
        )
    else:
        report.commits_ahead = 0

    if report.days_gap >= days_threshold or (report.commits_ahead or 0) >= commits_threshold:
        report.stale = True
        report.status = "STALE"

    return report


def scan_filesystem() -> list[dict]:
    repos: list[dict] = []
    for d in sorted(REPOS_ROOT.iterdir()):
        if not d.is_dir():
            continue
        if d.name == SELF_SLUG:
            continue
        if not (d / ".git").exists():
            continue
        repos.append(
            {
                "name": d.name,
                "slug": d.name,
                "git": f"https://github.com/celine-eu/{d.name}.git",
                "paths": ["README.md", "docs/**"],
            }
        )
    return repos


def format_date(dt: datetime | None) -> str:
    if dt is None:
        return "-"
    return dt.strftime("%Y-%m-%d")


def format_table(reports: list[RepoReport], days_threshold: int, commits_threshold: int) -> str:
    lines: list[str] = [
        "Documentation Staleness Report",
        "=" * 30,
        f"Thresholds: days={days_threshold}, commits={commits_threshold}",
        "",
    ]

    name_w = max(len(r.name) for r in reports) if reports else 20
    name_w = max(name_w, 10)
    header = (
        f"{'Repository':<{name_w}}  {'Last Docs':<12}{'Last Code':<12}"
        f"{'Days':>6}  {'Commits':>7}  Status"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for r in reports:
        days_str = str(r.days_gap) if r.days_gap is not None else "-"
        commits_str = str(r.commits_ahead) if r.commits_ahead is not None else "-"
        status = r.status
        if r.error and r.status in ("SKIP", "NO DOCS"):
            status = f"{r.status} ({r.error})"
        lines.append(
            f"{r.name:<{name_w}}  {format_date(r.last_doc_date):<12}"
            f"{format_date(r.last_code_date):<12}{days_str:>6}  {commits_str:>7}  {status}"
        )

    stale = sum(1 for r in reports if r.stale)
    ok = sum(1 for r in reports if r.status == "OK")
    skipped = sum(1 for r in reports if r.status in ("SKIP", "NO DOCS"))

    lines.append("")
    lines.append(f"Summary: {stale} stale, {ok} ok, {skipped} skipped")

    return "\n".join(lines)


def to_json(reports: list[RepoReport], days_threshold: int, commits_threshold: int) -> str:
    data: dict[str, Any] = {
        "thresholds": {"days": days_threshold, "commits": commits_threshold},
        "repos": [],
    }
    for r in reports:
        entry: dict[str, Any] = {
            "name": r.name,
            "dirname": r.dirname,
            "exists": r.exists,
            "last_doc_commit": format_date(r.last_doc_date),
            "last_code_commit": format_date(r.last_code_date),
            "days_gap": r.days_gap,
            "commits_ahead": r.commits_ahead,
            "stale": r.stale,
            "status": r.status,
        }
        if r.error:
            entry["error"] = r.error
        data["repos"].append(entry)
    return json.dumps(data, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check documentation staleness across CELINE repos")
    parser.add_argument("--all", action="store_true", help="Scan all repos on disk, not just repos.yaml")
    parser.add_argument("--days-threshold", type=int, default=DAYS_THRESHOLD)
    parser.add_argument("--commits-threshold", type=int, default=COMMITS_THRESHOLD)
    parser.add_argument("--json", action="store_true", help="Output JSON instead of table")
    parser.add_argument("--ci", action="store_true", help="Exit non-zero if any repo is stale")
    args = parser.parse_args()

    if args.all:
        repos = scan_filesystem()
    else:
        repos = load_config()

    reports: list[RepoReport] = []
    for repo in repos:
        dirname = repo_dirname(repo) if "git" in repo else repo["slug"]
        repo_dir = REPOS_ROOT / dirname
        doc_specs = doc_pathspecs(repo)
        report = check_repo(
            repo_dir=repo_dir,
            name=repo.get("name", dirname),
            dirname=dirname,
            doc_specs=doc_specs,
            days_threshold=args.days_threshold,
            commits_threshold=args.commits_threshold,
        )
        reports.append(report)

    if args.json:
        print(to_json(reports, args.days_threshold, args.commits_threshold))
    else:
        print(format_table(reports, args.days_threshold, args.commits_threshold))

    if args.ci and any(r.stale for r in reports):
        sys.exit(1)


if __name__ == "__main__":
    main()
