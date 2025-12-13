from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List

import yaml

ROOT = Path(__file__).resolve().parents[1]

WORKDIR = ROOT / ".work"
SITE_DIR = ROOT / "site"
SITE_PROJECTS = SITE_DIR / "projects"

CONFIG_FILE = ROOT / "repos.yaml"
MKDOCS_TEMPLATE = ROOT / "mkdocs.tpl.yml"
MKDOCS_FILE = ROOT / "mkdocs.yml"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=cwd)


def load_config() -> list[dict]:
    with CONFIG_FILE.open() as f:
        return yaml.safe_load(f).get("repos", [])


def clone_or_update(repo_url: str, target: Path) -> None:
    if target.exists():
        run(["git", "pull"], cwd=target)
    else:
        run(["git", "clone", repo_url, str(target)])


# ---------------------------------------------------------------------------
# Copy logic (README is canonical index)
# ---------------------------------------------------------------------------


def copy_paths(repo_dir: Path, site_dir: Path, paths: List[str]) -> None:
    for pattern in paths:
        for src in repo_dir.glob(pattern):
            rel = src.relative_to(repo_dir)

            if src.is_dir():
                shutil.copytree(
                    src,
                    site_dir / rel,
                    dirs_exist_ok=True,
                )
            elif src.is_file():
                # README.md ALWAYS becomes index.md
                if src.name.lower() == "readme.md":
                    dst = site_dir / rel.parent / "index.md"
                else:
                    dst = site_dir / rel

                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)


# ---------------------------------------------------------------------------
# Navigation (.pages)
# ---------------------------------------------------------------------------


def generate_project_pages(repo: dict) -> None:
    project_dir = SITE_PROJECTS / repo["slug"]
    pages = project_dir / ".pages"

    lines = [
        f"title: {repo['name']}",
        "nav:",
        "  - index.md",
    ]

    for item in repo.get("nav", []):
        if item.upper() == "README":
            continue
        lines.append(f"  - {item}/")

    pages.write_text("\n".join(lines))


def generate_tools_pages(repos: list[dict]) -> None:
    pages = SITE_PROJECTS / ".pages"

    lines = [
        "title: Tools",
        "nav:",
        "  - index.md",
    ]

    for repo in repos:
        lines.append(f"  - {repo['slug']}/")

    pages.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Index pages
# ---------------------------------------------------------------------------


def generate_tools_index(repos: list[dict]) -> None:
    index = SITE_PROJECTS / "index.md"

    lines = [
        "# Tools",
        "",
        "CELINE tools and services.",
        "",
    ]

    for repo in repos:
        lines.extend(
            [
                f"## {repo['name']}",
                "",
                f"- [{repo['slug']}]({repo['slug']}/index.md)",
                "",
            ]
        )

    index.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# URL shortcuts (symbolic-link semantics, isolated)
# ---------------------------------------------------------------------------


def materialize_links(repos: list[dict]) -> None:
    for repo in repos:
        for link in repo.get("links", []):
            source = SITE_DIR / link["source"]
            target = SITE_DIR / link["target"]

            if not source.exists():
                continue

            if target.exists():
                shutil.rmtree(target)

            shutil.copytree(source, target)


# ---------------------------------------------------------------------------
# MkDocs generation
# ---------------------------------------------------------------------------


def generate_mkdocs_yml() -> None:
    shutil.copy2(MKDOCS_TEMPLATE, MKDOCS_FILE)


def build_site() -> None:
    run(["mkdocs", "build", "--clean"], cwd=ROOT)


def generate_mkdocs_yml(repos: list[dict]) -> None:
    with MKDOCS_TEMPLATE.open() as f:
        config = yaml.safe_load(f)

    nav = [
        {"Home": "index.md"},
        {"Tools": [{repo["name"]: _repo_nav(repo)} for repo in repos]},
    ]

    # Optional global ontologies shortcut
    if (SITE_DIR / "ontologies" / "index.md").exists():
        nav.append({"Ontologies": "ontologies/index.md"})

    config["nav"] = nav

    with MKDOCS_FILE.open("w") as f:
        yaml.safe_dump(config, f, sort_keys=False)


def _repo_nav(repo: dict) -> list[dict]:
    base = f"projects/{repo['slug']}"

    entries: list[dict] = [{"Overview": f"{base}/index.md"}]

    for item in repo.get("nav", []):
        if item.upper() == "README":
            continue

        entries.append({item.capitalize(): f"{base}/{item}/index.md"})

    return entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    WORKDIR.mkdir(exist_ok=True)
    SITE_PROJECTS.mkdir(parents=True, exist_ok=True)

    repos = load_config()

    for repo in repos:
        repo_dir = WORKDIR / repo["slug"]
        site_dir = SITE_PROJECTS / repo["slug"]

        clone_or_update(repo["git"], repo_dir)

        if site_dir.exists():
            shutil.rmtree(site_dir)
        site_dir.mkdir(parents=True)

        copy_paths(repo_dir, site_dir, repo.get("paths", []))
        generate_project_pages(repo)

    generate_tools_index(repos)
    materialize_links(repos)

    generate_mkdocs_yml(repos)
    build_site()


if __name__ == "__main__":
    main()
