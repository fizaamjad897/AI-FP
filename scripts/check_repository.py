"""Validate notebook schemas and local Markdown links without executing research."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import nbformat

REQUIRED = (
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "requirements.txt",
    "requirements-dev.txt",
    "docs/DATASET_CARD.md",
    "docs/MODEL_CARD.md",
    "docs/REPRODUCIBILITY.md",
)


def check(root: Path) -> list[str]:
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")
    for path in sorted(root.glob("*.ipynb")):
        try:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
        except (OSError, ValueError, json.JSONDecodeError, nbformat.ValidationError) as exc:
            errors.append(f"Invalid notebook {path.name}: {exc}")
    documents = [
        root / name for name in ("README.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md")
    ]
    documents += sorted((root / "docs").rglob("*.md"))
    for path in documents:
        if not path.is_file():
            continue
        for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            target = match.group(1).strip().split(' "', 1)[0].strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            local = path.parent / unquote(parts.path)
            if not local.exists():
                errors.append(f"Broken local link in {path.relative_to(root)}: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()
    errors = check(args.root)
    for error in errors:
        print(error)
    if not errors:
        print(
            "Notebook schemas, required maintenance files and local documentation links are valid."
        )
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
