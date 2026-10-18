import subprocess
import sys

from scripts.audit_dataset import PNG_SIGNATURE, audit


def fixture_dataset(root):
    for split in ("train_split", "test_split"):
        for grade in range(5):
            folder = root / split / str(grade)
            folder.mkdir(parents=True)
            # Header-only fixtures test the audit's declared signature/hash scope.
            (folder / "sample.png").write_bytes(PNG_SIGNATURE + f"{split}-{grade}".encode())
    return root


def test_reports_counts_without_overlap(tmp_path):
    report = audit(fixture_dataset(tmp_path))
    assert report["totals"] == {"train_split": 5, "test_split": 5}
    assert report["cross_split_duplicate_groups"] == []
    assert report["errors"] == []


def test_hashes_detect_same_image_with_different_filename(tmp_path):
    root = fixture_dataset(tmp_path)
    image = root / "train_split/0/sample.png"
    (root / "test_split/0/sample.png").unlink()
    (root / "test_split/0/renamed.png").write_bytes(image.read_bytes())
    report = audit(root)
    assert len(report["cross_split_duplicate_groups"]) == 1
    paths = report["cross_split_duplicate_groups"][0]["paths"]
    assert paths == ["train_split/0/sample.png", "test_split/0/renamed.png"]


def test_content_change_changes_manifest_hash(tmp_path):
    root = fixture_dataset(tmp_path)
    before = audit(root)["manifest_sha256"]
    (root / "test_split/2/sample.png").write_bytes(PNG_SIGNATURE + b"changed")
    assert audit(root)["manifest_sha256"] != before


def test_missing_grade_or_invalid_png_is_reported(tmp_path):
    root = fixture_dataset(tmp_path)
    (root / "test_split/2/sample.png").unlink()
    (root / "train_split/4/sample.png").write_bytes(b"not-a-png")
    errors = audit(root)["errors"]
    assert any("empty grade" in e for e in errors)
    assert any("Invalid PNG" in e for e in errors)


def test_unexpected_class_is_reported(tmp_path):
    root = fixture_dataset(tmp_path)
    (root / "test_split/5").mkdir()
    assert any("Unexpected grade" in e for e in audit(root)["errors"])


def test_strict_cli_fails_on_overlap(tmp_path):
    root = fixture_dataset(tmp_path)
    (root / "test_split/1/sample.png").write_bytes((root / "train_split/1/sample.png").read_bytes())
    for extra, expected in [([], 0), (["--strict"], 1)]:
        run = subprocess.run(
            [sys.executable, "-m", "scripts.audit_dataset", str(root), *extra],
            capture_output=True,
            text=True,
        )
        assert run.returncode == expected, run.stderr
