"""Evaluate a CSV of KL grades without loading model weights."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
)

LABELS = [0, 1, 2, 3, 4]


def load_predictions(path: Path) -> tuple[list[str], list[int], list[int]]:
    """Require unique sample IDs and integer true/predicted KL grades."""
    ids, truth, prediction = [], [], []
    seen = set()
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"sample_id", "y_true", "y_pred"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires sample_id,y_true,y_pred columns")
        for number, row in enumerate(reader, start=2):
            sample = (row.get("sample_id") or "").strip()
            if not sample or sample in seen:
                raise ValueError(f"Row {number}: missing or duplicate sample_id")
            values = []
            for field in ("y_true", "y_pred"):
                value = (row.get(field) or "").strip()
                if value not in {"0", "1", "2", "3", "4"}:
                    raise ValueError(f"Row {number}: {field} must be a KL grade 0-4")
                values.append(int(value))
            seen.add(sample)
            ids.append(sample)
            truth.append(values[0])
            prediction.append(values[1])
    if not ids:
        raise ValueError("CSV contains no predictions")
    return ids, truth, prediction


def evaluate(path: Path, *, model: str, split: str) -> dict:
    """Return metrics and input provenance; absent-class kappa is undefined."""
    ids, truth, prediction = load_predictions(path)
    # A single constant label yields a zero denominator for kappa.
    kappa = None
    if len(set(truth + prediction)) > 1:
        value = float(cohen_kappa_score(truth, prediction, labels=LABELS, weights="quadratic"))
        if math.isfinite(value):
            kappa = value
    return {
        "schema_version": 1,
        "model": model,
        "split": split,
        "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "sample_count": len(ids),
        "labels": LABELS,
        "observed_true_labels": sorted(set(truth)),
        "accuracy": float(accuracy_score(truth, prediction)),
        "balanced_accuracy": 1.0
        if len(set(truth + prediction)) == 1
        else float(balanced_accuracy_score(truth, prediction)),
        "macro_f1_all_five_grades": float(
            f1_score(truth, prediction, labels=LABELS, average="macro", zero_division=0)
        ),
        "quadratic_weighted_kappa": kappa,
        "confusion_matrix": confusion_matrix(truth, prediction, labels=LABELS).tolist(),
        "per_grade": classification_report(
            truth, prediction, labels=LABELS, output_dict=True, zero_division=0
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--model", required=True, help="Model/run identifier")
    parser.add_argument("--split", required=True, help="Exact split or manifest identifier")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = evaluate(args.predictions, model=args.model, split=args.split)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Evaluation failed: {exc}\n")
    result = json.dumps(report, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    else:
        print(result, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
