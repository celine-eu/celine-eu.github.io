from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

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
                shutil.copytree(src, site_dir / rel, dirs_exist_ok=True)
            elif src.is_file():
                # README.md ALWAYS becomes index.md (directory landing page)
                if src.name.lower() == "readme.md":
                    dst = site_dir / rel.parent / "index.md"
                else:
                    dst = site_dir / rel

                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)


# ---------------------------------------------------------------------------
# Index pages
# ---------------------------------------------------------------------------


def generate_tools_index(repos: list[dict]) -> None:
    index = SITE_PROJECTS / "index.md"
    lines = ["# Tools", "", "CELINE tools and services.", ""]

    for repo in repos:
        lines.extend(
            [
                f"## {repo['name']}",
                "",
                f"- [{repo['slug']}](./{repo['slug']}/)",
                "",
            ]
        )

    index.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# URL shortcuts (symbolic-link semantics, isolated)
# ---------------------------------------------------------------------------


def _generate_listing_index(
    folder: Path,
    title: str | None,
    config: dict,
) -> None:
    """
    Create an index.md listing files in `folder`.

    - Will NOT overwrite existing index.md
    - Supports recursion
    - Supports extension filtering
    - Deterministic ordering
    """
    index = folder / "index.md"
    if index.exists():
        return

    recursive: bool = bool(config.get("recursive", False))
    extensions: list[str] = config.get("extensions", [".md"])
    sort_mode: str = config.get("sort", "alpha")

    # Normalize extensions
    extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]

    files: list[Path] = []

    if recursive:
        for p in folder.rglob("*"):
            if p.is_file() and p.suffix in extensions:
                files.append(p)
    else:
        for p in folder.iterdir():
            if p.is_file() and p.suffix in extensions:
                files.append(p)
            elif p.is_dir():
                files.append(p)

    if sort_mode == "alpha":
        files.sort(key=lambda p: p.name.lower())

    heading = (
        title.replace("-", " ").title()
        if title
        else folder.name.replace("-", " ").title()
    )

    lines: list[str] = [
        f"# {heading}",
        "",
    ]

    for p in files:
        rel = p.relative_to(folder)
        if p.is_dir():
            lines.append(f"- [{p.name}]({p.name}/)")
        else:
            label = p.name
            lines.append(f"- [{label}]({rel.as_posix()})")

    index.write_text("\n".join(lines))


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

            list_cfg = link.get("list")
            if list_cfg:
                _generate_listing_index(
                    folder=target,
                    title=link.get("name"),
                    config=list_cfg,
                )


# ---------------------------------------------------------------------------
# MkDocs generation (merge template nav + generated Tools)
# ---------------------------------------------------------------------------


NavItem = Dict[
    str, Any
]  # MkDocs nav is a list of dicts (or strings, but we use dict form)


def build_site() -> None:
    run(["mkdocs", "build", "--clean"], cwd=ROOT)


def generate_mkdocs_yml(repos: list[dict]) -> None:
    with MKDOCS_TEMPLATE.open() as f:
        config: Dict[str, Any] = yaml.safe_load(f) or {}

    template_nav = config.get("nav")
    if not isinstance(template_nav, list):
        raise ValueError("mkdocs.tpl.yml must define nav: as a YAML list")

    tools_nav = _tools_nav(repos)

    merged_nav: list[NavItem] = []
    for entry in template_nav:
        # We expect dict entries like {"Home": "index.md"}
        if isinstance(entry, dict) and len(entry) == 1:
            title, value = next(iter(entry.items()))

            # Replace Tools entry (regardless of whether template uses "projects/" or anything else)
            if title.strip().lower() == "tools":
                merged_nav.append({title: tools_nav})
                continue

            # Normalize directory targets in template nav:
            #   "ontologies/" -> "ontologies/index.md" (if exists)
            #   "schemas/"    -> "schemas/index.md"    (if exists)
            merged_nav.append({title: _normalize_template_target(value)})
            continue

        # Allow passthrough for uncommon MkDocs nav shapes (rare)
        merged_nav.append(entry)

    config["nav"] = merged_nav

    with MKDOCS_FILE.open("w") as f:
        yaml.safe_dump(config, f, sort_keys=False)


def _normalize_template_target(value: Any) -> Any:
    """
    If template nav points to a directory (string ending with '/'), and that directory has an index.md
    in the generated SITE_DIR tree, convert to 'dir/index.md' so Material loads a concrete page.
    Otherwise leave as-is.
    """
    if not isinstance(value, str):
        return value

    if value.endswith("/"):
        candidate = SITE_DIR / value / "index.md"
        if candidate.exists():
            return f"{value}index.md"
        return value

    # If template points to a directory without trailing slash, optionally normalize too
    # (but only if it exists and has index.md).
    candidate = SITE_DIR / value / "index.md"
    if candidate.exists():
        return f"{value}/index.md"

    return value


def _tools_nav(repos: list[dict]) -> list[dict]:
    """
    Returns the nested nav list for the Tools section:
      - Repo Name:
          - Overview: projects/<slug>/index.md
          - ...
    """
    return [{repo["name"]: _repo_nav(repo)} for repo in repos]


def _repo_nav(repo: dict) -> list[dict]:
    """
    Repo nav supports:
      - README
      - "path" or "path/" (directory -> path/index.md)
      - "path/file.md" (file)
      - {Title: "path/file.md"} (explicit title)
    """
    base = f"projects/{repo['slug']}"
    entries: list[dict] = []

    for item in repo.get("nav", []):
        # README -> root index
        if isinstance(item, str) and item.upper() == "README":
            entries.append({"Overview": f"{base}/index.md"})
            continue

        # Explicit title mapping
        if isinstance(item, dict):
            title, path = next(iter(item.items()))
            entries.append({title: f"{base}/{path}"})
            continue

        if not isinstance(item, str):
            raise ValueError(f"Unsupported nav entry type: {item!r}")

        # Explicit file reference (do NOT rewrite)
        if item.endswith(".md"):
            title = _title_from_path(item)
            entries.append({title: f"{base}/{item}"})
            continue

        # Directory reference (implicit or with trailing slash)
        path = item.rstrip("/")
        entries.append({_title_from_path(path): f"{base}/{path}/index.md"})

    return entries


def _title_from_path(path: str) -> str:
    """
    Generates a reasonable title for a nav entry when not explicitly provided.
    Keeps this conservative and predictable.
    """
    p = Path(path)
    stem = p.stem if p.suffix else p.name

    # Small, intentional mapping to match your example expectation
    # without changing URLs:
    if stem.lower() == "schemas" and "docs" in p.parts:
        return "Governance Schemas"

    return stem.replace("-", " ").replace("_", " ").title()


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

    generate_tools_index(repos)
    materialize_links(repos)

    generate_mkdocs_yml(repos)
    build_site()


if __name__ == "__main__":
    main()
