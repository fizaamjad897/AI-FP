# Reproducibility

## Two environments

**Maintenance/evaluation:** Python 3.12+; install the hash-locked `requirements-dev.lock.txt`. It supports notebook schema checks, documentation checks, dataset audit, tests, and CSV metric computation without TensorFlow. CI runs this toolchain on Python 3.12 and 3.13.

**Historical research:** original Colab notebooks, with some metadata recording Python 3.11.4 and a T4 GPU. No exact original package lock was committed. `requirements-research.txt` is a proposed current research environment, not a reconstruction of that runtime. The manifest was dependency-resolved for Linux/Python 3.12. Dependency resolution is distinct from executing and validating a training run.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements-dev.lock.txt
python -m pytest
python -m scripts.check_repository
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`.

## Audit the committed data first

```sh
python -m scripts.audit_dataset dataset --output reports/dataset-audit.json
python -m scripts.audit_dataset dataset --strict
```

The strict check fails for the current data because cross-split duplicate images are known. Fix the split methodology and preserve new manifests before attempting an independent evaluation. The audit checks directory structure, PNG signatures, class counts, and exact duplicate hashes; it is not a complete image-decoding or patient-level validation tool.

## Research notebook setup

Use a separate environment for research:

```sh
python3.12 -m venv .venv-research
source .venv-research/bin/activate
python -m pip install -r requirements-research.txt
jupyter lab
```

For Colab, use a dedicated copy of the notebooks and install compatible versions in that runtime. `google.colab` is provided by Colab and is not a normal local dependency. On Linux, TensorFlow GPU support requires a compatible driver/runtime; hardware execution has not been verified by repository CI. Other platforms may require different TensorFlow versions or CPU execution.

Before running any historical notebook:

1. Read [KNOWN_ISSUES.md](KNOWN_ISSUES.md). Several notebooks will not execute cleanly from a fresh kernel as committed.
2. Replace `/content/extracted_files/dataset` with your intended dataset root. Do not assume an uploaded `dataset.zip` is the same snapshot as the committed tree.
3. Replace upload/download-only cells using `google.colab.files` when working locally.
4. Set and record Python, NumPy and TensorFlow seeds; rebuild sampled folders from frozen manifests rather than appending into old directories.
5. Verify the intended backbone, preprocessing, input shape, compiled model variable, and class order.
6. Use separate participant-disjoint validation and final-test manifests.
7. Provide the correct complete checkpoint for test/explanation notebooks. `/content/xception_model (1).h5` is not included. The ResNet50 weights file is not a substitute.
8. Start with a fresh kernel and run top to bottom, then retain the environment, model checksum, predictions, logs, and split manifests for that exact run.

The old scores must not be reused as results from modified code or data.

## What CI establishes

- Maintained Python code passes lint, formatting, and functional tests.
- Notebook JSON follows its declared schema; **notebook cells are not executed**.
- Local documentation links and expected repository files exist.
- Dataset directories and PNG signatures are structurally valid; known duplicate overlap is reported as a warning.
- The synthetic prediction example runs through the evaluator.

CI does not train models, download ImageNet weights, reproduce saved notebook scores, or certify clinical correctness. Expensive GPU runs require a separately configured experiment workflow.

## Version and release practice

Use pull requests for changes, and record meaningful changes in [CHANGELOG.md](../CHANGELOG.md). A new scientific result needs a new run identifier. Before creating a release/tag, review the checklist in [MAINTENANCE.md](MAINTENANCE.md). No software release or paper DOI is invented by this documentation pass.

## Refresh the maintenance lock

After reviewing changes to `requirements.txt` or `requirements-dev.txt`, regenerate `requirements-dev.lock.txt` with `uv pip compile --python-version 3.12 --universal --generate-hashes requirements-dev.txt --output-file requirements-dev.lock.txt`, then run the same tests and CI. The research manifest is separate and is not claimed to recreate the original Colab runtime.
