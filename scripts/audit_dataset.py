"""Inspect class counts, PNG headers and exact train/test overlap."""

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

GRADES = [str(i) for i in range(5)]
SPLITS = ("train_split", "test_split")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def audit(root: Path) -> dict:
    """Report structural errors and byte-identical images crossing splits."""
    errors = []
    counts = {}
    hashes = defaultdict(list)
    manifest = hashlib.sha256()
    for split in SPLITS:
        folder = root / split
        counts[split] = {}
        if not folder.is_dir():
            errors.append(f"Missing split: {split}")
        elif any(p.is_dir() and p.name not in GRADES for p in folder.iterdir()):
            errors.append(f"Unexpected grade directory in {split}")
        for grade in GRADES:
            class_dir = folder / grade
            images = sorted(class_dir.glob("*.png")) if class_dir.is_dir() else []
            counts[split][grade] = len(images)
            if not images:
                errors.append(f"Missing or empty grade: {split}/{grade}")
            for path in images:
                data = path.read_bytes()
                relative = path.relative_to(root).as_posix()
                if not data.startswith(PNG_SIGNATURE):
                    errors.append(f"Invalid PNG signature: {relative}")
                digest = hashlib.sha256(data).hexdigest()
                manifest.update(f"{relative}\0{digest}\n".encode())
                hashes[digest].append(relative)
    cross_split = []
    for digest, paths in sorted(hashes.items()):
        if len({p.split("/", 1)[0] for p in paths}) > 1:
            cross_split.append({"sha256": digest, "paths": paths})
    return {
        "schema_version": 1,
        "root": root.as_posix(),
        "counts": counts,
        "totals": {split: sum(classes.values()) for split, classes in counts.items()},
        "manifest_sha256": manifest.hexdigest(),
        "cross_split_duplicate_groups": cross_split,
        "errors": errors,
        "scope": "Exact file content overlap only; this does not establish patient independence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("dataset"))
    parser.add_argument("--strict", action="store_true", help="Fail on exact cross-split overlap")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.root)
    except OSError as exc:
        parser.exit(2, f"Dataset audit failed: {exc}\n")
    result = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
        print(f"Dataset totals: {report['totals']}")
        print(f"Exact cross-split duplicate groups: {len(report['cross_split_duplicate_groups'])}")
        if report["cross_split_duplicate_groups"]:
            print("WARNING: overlapping splits do not establish independent test performance.")
    else:
        print(result, end="")
    return int(bool(report["errors"] or (args.strict and report["cross_split_duplicate_groups"])))


if __name__ == "__main__":
    raise SystemExit(main())
