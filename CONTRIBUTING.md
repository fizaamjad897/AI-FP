# Contributing

Contributions that improve reproducibility, documentation, and evaluation are welcome. Read [known issues](docs/KNOWN_ISSUES.md) and the [dataset card](docs/DATASET_CARD.md) first.

1. Open an issue describing the problem or experiment before a large change.
2. Work on a branch, install `requirements-dev.txt`, and keep the change focused.
3. Run `python -m pytest`, `ruff check scripts tests`, `ruff format --check scripts tests`, and `python -m scripts.check_repository`.
4. For dataset changes, run the audit and explain provenance, rights, split manifests, and overlap. Do not commit sensitive medical information.
5. Open a pull request using the template and distinguish reproduced findings from assumptions.

Do not replace historical notebook outputs with unrecorded reruns. If notebook code changes, include a fresh-kernel reproduction record and distinguish the new outputs from the old experiment. Commit useful figures, not entire local environments, generated sampled datasets, caches, or extra weight checkpoints.

A new score needs exact data/model/code identifiers and per-grade support. Claims of improved medical performance require appropriate evidence and review, not just a higher accuracy number.

By contributing your own code, you agree it may be distributed under the repository's MIT code license. Only submit material you have permission to share; third-party data/model rights remain separate. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
