# Dataset card

## Task and labels

The notebooks use knee X-ray PNGs organized into Kellgren–Lawrence grades `0`, `1`, `2`, `3`, and `4`. These are ordinal severity labels. The label meanings and clinical reliability have not been independently verified by this repository's tooling.

## Committed distribution

| KL grade | `train_split` | `test_split` |
| --- | ---: | ---: |
| 0 | 2,315 | 1,139 |
| 1 | 1,064 | 530 |
| 2 | 1,558 | 757 |
| 3 | 777 | 380 |
| 4 | 177 | 83 |
| Total | 5,891 | 2,889 |

Counts describe files, not independent participants. The class distribution is imbalanced. Sampling with a cap of 1,000 images per class produces the notebooks' 2,750-image evaluation set: 1,000 + 530 + 757 + 380 + 83.

## Confirmed overlap

A SHA-256 audit found **2,834 groups of byte-identical images crossing the two committed splits**, involving 2,834 of the 2,889 test images (approximately 98.1%). This means the committed split is unsuitable as evidence of independent generalization. The historical sampled manifests were not saved, so the exact overlap for each saved run cannot be reconstructed from the notebook output alone.

Reproduce the audit:

```sh
python -m scripts.audit_dataset dataset --output reports/dataset-audit.json
python -m scripts.audit_dataset dataset --strict
```

The second command intentionally returns a nonzero status for this dataset. The report lists the matching content hashes and paths. The committed summary is [dataset-audit-summary.json](dataset-audit-summary.json).

This check detects identical bytes only. It does not detect resized or re-encoded copies, longitudinal images, left/right knees from the same person, or other participant-level relationships. A clean hash audit alone would not establish a valid patient-level split.

## Provenance and permissions

The repository does not provide a verified source accession, dataset license, consent terms, acquisition protocol, or participant manifest. Do not assume that public availability grants redistribution rights. Establish the source and its terms before redistributing, deploying, or uploading images elsewhere. Do not attach patient identifiers or private medical records to issues.

## Required before new benchmark claims

1. Establish the source, permitted uses, and label definitions.
2. Group by verified participant identity before splitting.
3. Freeze separate training, validation, and final-test manifests.
4. Audit exact and near-duplicate overlap; document exclusions.
5. Use validation for tuning and inspect the final test only after selection.
6. Record per-grade support and uncertainty alongside every metric.

No images were removed, moved, or relabeled during this maintenance pass.
