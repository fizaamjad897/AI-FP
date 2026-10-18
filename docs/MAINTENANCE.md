# Maintainer checklist

## Pull requests

Run the documented checks. Review scientific changes for participant overlap, class order, preprocessing and model identity; schema-valid notebooks can still be scientifically wrong. Keep the original research outputs separate from results of changed code. Avoid unrelated notebook-output churn.

## Before a result or release

- Resolve or disclose every relevant item in [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
- Confirm dataset/model redistribution rights.
- Freeze participant-disjoint split manifests and include data/checkpoint checksums.
- Record code, Python/package versions, seed and hardware.
- Reproduce results from a fresh kernel and retain prediction exports.
- Update dataset/model cards, changelog and citation metadata.
- Run CI and review dependency/security alerts.
- Tag only a tested commit; never publish a fabricated DOI or unverified metric.

## Routine upkeep

Dependabot proposes dependency and Action updates monthly; review them through pull requests. A dependency bump can change model behavior, so it does not silently validate old training scores. Do not auto-merge changes to the research environment without an appropriate rerun.

The original large assets are retained for provenance. Before adding more large data or model files, establish rights and prefer a versioned external artifact store with checksums. Avoid rewriting published history merely to reduce repository size.

## Recommended account-side settings

Enable private vulnerability reports. Protect `main` with a pull-request rule and require the two repository-check jobs once their first successful run exists. Keep the maintainer's ability to merge reviewed changes; do not add a self-approval requirement that makes solo maintenance impossible. GitHub account plan/settings may affect which controls are available.
