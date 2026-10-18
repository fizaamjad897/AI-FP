import nbformat

from scripts.check_repository import REQUIRED, check


def repository(root):
    for name in REQUIRED:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("")
    return root


def test_valid_notebook_and_encoded_local_link(tmp_path):
    root = repository(tmp_path)
    nbformat.write(nbformat.v4.new_notebook(), root / "example.ipynb")
    (root / "file with spaces.txt").write_text("asset")
    (root / "README.md").write_text("[asset](file%20with%20spaces.txt) [web](https://example.com)")
    assert check(root) == []


def test_invalid_notebook_and_missing_file_are_detected(tmp_path):
    root = repository(tmp_path)
    (root / "broken.ipynb").write_text("not json")
    (root / "README.md").write_text("[missing](missing.txt)")
    (root / "LICENSE").unlink()
    errors = check(root)
    assert any("Invalid notebook" in e for e in errors)
    assert any("Broken local link" in e for e in errors)
    assert any("LICENSE" in e for e in errors)
