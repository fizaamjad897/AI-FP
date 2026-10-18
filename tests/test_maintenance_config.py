import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_workflow_has_safe_triggers_and_pinned_actions():
    workflow = yaml.load((ROOT / ".github/workflows/ci.yml").read_text(), Loader=yaml.BaseLoader)
    assert set(workflow["on"]) == {"push", "pull_request", "workflow_dispatch"}
    assert workflow["permissions"] == {"contents": "read"}
    versions = workflow["jobs"]["checks"]["strategy"]["matrix"]["python-version"]
    assert versions == ["3.12", "3.13"]
    for step in workflow["jobs"]["checks"]["steps"]:
        if "uses" in step:
            assert re.fullmatch(r"[^@]+@[a-f0-9]{40}", step["uses"])


def test_issue_forms_and_citation_are_valid_yaml():
    for path in (ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml"):
        form = yaml.safe_load(path.read_text())
        if path.name != "config.yml":
            assert form["name"] and form["description"] and form["body"]
            ids = [field["id"] for field in form["body"] if "id" in field]
            assert len(ids) == len(set(ids))
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text())
    assert citation["cff-version"] == "1.2.0"
    assert citation["authors"][0]["family-names"] == "Amjad"
    assert citation["license"] == "MIT"
    assert citation["repository-code"].endswith("Knee-Osteoarthritis-Grading")


def test_lock_contains_all_pinned_direct_maintenance_dependencies():
    pattern = re.compile(r"^([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+-]+)", re.MULTILINE)

    def pins(path):
        return {
            name.lower().replace("_", "-"): version
            for name, version in pattern.findall(path.read_text())
        }

    locked = pins(ROOT / "requirements-dev.lock.txt")
    direct = pins(ROOT / "requirements.txt") | pins(ROOT / "requirements-dev.txt")
    for name, version in direct.items():
        assert locked.get(name) == version, f"Regenerate maintenance lock for {name}"
