#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADER = ""

OUTFILE = ROOT / "source.txt"


DIRS = []
FILES = [
    ROOT / "scripts/build.py",
    ROOT / "mkdocs.tpl.yml",
    ROOT / "repos.yaml",
    ROOT / "taskfile.yaml",
    ROOT / ".github/workflows/build-site.yml",
]

README = None
# README = ROOT / "README.md"


def should_skip(path: Path) -> bool:
    """Return True if file or directory should be excluded."""
    parts = path.parts
    if "__pycache__" in parts:
        return True
    if path.suffix not in (".py", ".pyi"):
        return True
    return False


def main():
    with open(OUTFILE, "w", encoding="utf-8") as out:

        out.write(HEADER + "\n\n")

        if README:
            with open(README, "r") as readme:
                out.write(readme.read() + "\n\n")

        for source_dir in DIRS:
            for file in sorted(source_dir.rglob("*")):
                if file.is_file() and not should_skip(file):
                    rel = file.relative_to(source_dir.parent)
                    out.write(f"\n# file: {rel} \n")
                    out.write(file.read_text(encoding="utf-8"))
                    out.write("\n")

        for file in FILES:
            if file.is_file():
                rel = file.relative_to(ROOT)
                out.write(f"\n# file: {rel} \n")
                out.write(file.read_text(encoding="utf-8"))
                out.write("\n")

    print(f"Wrote: {OUTFILE}")


if __name__ == "__main__":
    main()
