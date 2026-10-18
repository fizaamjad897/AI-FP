# Evaluation protocol and historical results

## Status

This repository provides research artifacts and an evaluation format. It is **not currently an independently validated benchmark**. The existing saved scores are retained for provenance; confirmed train/test duplication prevents treating them as evidence of held-out performance.

## Saved output provenance

The four modeling notebooks print classification reports with grade support `[1000, 530, 757, 380, 83]`, totaling 2,750 images. They cap sampled classes at 1,000 using `random.shuffle` without a recorded seed or filename manifest. Their sampled test directory is used as validation during training/selection.

[legacy-results.json](../benchmarks/legacy-results.json) records notebook filenames, output cell indices, printed accuracy/balanced accuracy, and limitations. Values are transcribed from saved outputs; they are not recomputed from predictions.

The file named `data_modeling_ResNet50.ipynb` imports and constructs InceptionResNetV2. Its printed ResNet50 label is not sufficient to establish model identity. It is excluded from any verified cross-architecture claim.

The additional Xception test notebook prints 0.8371 accuracy and 0.4297 loss. This run must remain separate from the modeling notebook's 0.8662 accuracy. It expects a complete Xception checkpoint that is not committed.

## Evaluate future prediction exports

CSV contract:

```csv
sample_id,y_true,y_pred
image-001,0,0
image-002,2,3
```

- One row per image, with a unique, nonempty sample identifier.
- True and predicted labels must be integer strings `0` through `4`.
- Keep a separate frozen split manifest and model/checkpoint checksum.
- Predictions must follow the same image order and class mapping as the labels.

```sh
python -m scripts.evaluate path/to/predictions.csv \
  --model xception-run-001 --split heldout-manifest-sha256 \
  --output reports/xception-run-001.json
```

The JSON records the input file SHA-256, model/split identifiers, sample count, observed true labels, accuracy, balanced accuracy, macro F1 over all five grades, quadratic weighted kappa, a fixed 5 × 5 confusion matrix, and per-grade scores. Balanced accuracy averages recalls over the true classes present in the file; a file missing grades is not directly comparable to a full five-grade evaluation. Undefined kappa is JSON `null`.

The supplied [example CSV](../examples/predictions.csv) is synthetic. Its metrics are not research findings. AUROC is not computed from hard predictions; future probability-based metrics require validated probability columns and class-order checks.

## New result checklist

Before reporting a new result, record:

- Dataset source and license, participant grouping, split manifests and hashes.
- Overlap audits and the exact held-out protocol.
- Code commit, package versions, hardware, seed, and preprocessing.
- Architecture, trained checkpoint checksum and model-selection criterion.
- Every grade's support, accuracy, balanced accuracy, macro F1, and ordinal agreement.
- Confidence intervals with a justified participant-level resampling unit.
- Calibration and subgroup analyses when the required evidence is available.

Do not invent missing metadata, confidence intervals, or external validation.
