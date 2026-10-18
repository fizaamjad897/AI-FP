import json
import subprocess
import sys

import pytest

from scripts.evaluate import evaluate, load_predictions


def csv_file(tmp_path, rows, header="sample_id,y_true,y_pred"):
    path = tmp_path / "predictions.csv"
    path.write_text(header + "\n" + rows)
    return path


def test_perfect_five_grade_predictions(tmp_path):
    path = csv_file(tmp_path, "\n".join(f"id-{i},{i},{i}" for i in range(5)))
    report = evaluate(path, model="test-model", split="test-split")
    assert report["sample_count"] == 5
    assert report["accuracy"] == 1
    assert report["balanced_accuracy"] == 1
    assert report["macro_f1_all_five_grades"] == 1
    assert report["quadratic_weighted_kappa"] == 1
    assert report["confusion_matrix"] == [[int(i == j) for j in range(5)] for i in range(5)]
    assert len(report["input_sha256"]) == 64


def test_known_error_has_correct_ordinal_and_class_metrics(tmp_path):
    path = csv_file(tmp_path, "a,0,0\nb,1,1\nc,2,3\nd,3,3\ne,4,4\n")
    report = evaluate(path, model="test", split="synthetic")
    assert report["accuracy"] == pytest.approx(0.8)
    assert report["balanced_accuracy"] == pytest.approx(0.8)
    assert report["macro_f1_all_five_grades"] == pytest.approx(11 / 15)
    assert report["quadratic_weighted_kappa"] == pytest.approx(20 / 21)
    assert report["confusion_matrix"][2][3] == 1


def test_single_class_has_explicitly_undefined_kappa(tmp_path):
    report = evaluate(csv_file(tmp_path, "a,0,0\nb,0,0"), model="test", split="partial")
    assert report["quadratic_weighted_kappa"] is None
    assert report["observed_true_labels"] == [0]
    assert report["macro_f1_all_five_grades"] == pytest.approx(0.2)
    json.dumps(report, allow_nan=False)


@pytest.mark.parametrize("rows", ["", "a,0,0\na,1,1", ",0,0", "a,5,0", "a,0,-1", "a,1.0,1", "a,,2"])
def test_rejects_invalid_predictions(tmp_path, rows):
    with pytest.raises(ValueError):
        load_predictions(csv_file(tmp_path, rows))


def test_requires_all_contract_columns(tmp_path):
    with pytest.raises(ValueError, match="columns"):
        load_predictions(csv_file(tmp_path, "a,0", header="sample_id,y_true"))


def test_utf8_bom_and_whitespace(tmp_path):
    path = csv_file(tmp_path, " a , 2 , 2 ", header="\ufeffsample_id,y_true,y_pred")
    assert load_predictions(path) == (["a"], [2], [2])


def test_cli_writes_json_to_new_output_directory(tmp_path):
    path = csv_file(tmp_path, "a,0,0\nb,1,1")
    output = tmp_path / "new" / "metrics.json"
    run = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.evaluate",
            str(path),
            "--model",
            "run-001",
            "--split",
            "manifest-sha",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stderr
    report = json.loads(output.read_text())
    assert report["model"] == "run-001"
    assert report["split"] == "manifest-sha"
