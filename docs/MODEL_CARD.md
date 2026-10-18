# Model card

## Purpose and intended use

Academic exploration of five-class knee osteoarthritis grading from X-rays using transfer learning, plus SHAP and LIME explanation examples. Intended for research inspection, learning, and method development. Not a diagnostic product, treatment recommendation system, or substitute for clinical assessment.

## Model inventory

| Artifact | What is present | Limitations |
| --- | --- | --- |
| Xception | Modeling notebook and saved figures | Required complete model checkpoint absent |
| InceptionResNetV2 | Modeling notebook and saved figures | Notebook state and split limitations |
| DenseNet201 | Modeling notebook and saved figures | Notebook state and split limitations |
| ResNet50 label | Notebook, figures, `media_files/resnet50_.weights.h5` | Notebook constructs InceptionResNetV2; saved score/model attribution not verified |

A weights-only HDF5 file is not evidence of a complete deployable model. Do not treat it as the missing Xception checkpoint.

## Input and output

The modeling notebooks resize images to 224 × 224 and use categorical targets for five KL grades. Preprocessing differs between notebook cells and must be checked against the chosen backbone before any new run. Outputs are grade probabilities and a selected class; explanations are post-hoc visualizations.

## Evaluation evidence

See [BENCHMARKS.md](BENCHMARKS.md) for the exact saved metrics and [DATASET_CARD.md](DATASET_CARD.md) for the confirmed cross-split image overlap. No independent rerun, external cohort validation, confidence intervals, or participant-level leakage audit is provided by the historical outputs.

## Known risks and unresolved questions

- Extensive byte-identical overlap in the committed train/test splits.
- Class imbalance and limited severe-grade support.
- Validation/tuning performed on the directory named as the test split.
- Unseeded random subsampling and missing run manifests.
- Out-of-order or undefined notebook variables; one architecture mismatch.
- No verified acquisition/demographic metadata or subgroup analysis.
- No calibration, robustness, external generalization, or prospective clinical validation.
- SHAP/LIME images describe a particular model/input pipeline and are not causal explanations.

## Maintenance and changes

Original notebooks and saved outputs are retained as historical evidence. Maintained scripts evaluate exported predictions and audit repository assets. Changes to preprocessing, data splits, checkpoints, or model architecture require a new run identifier and fresh evaluation; do not attach historical numbers to altered code.
