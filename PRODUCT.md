# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Delegated to Claude. No live model inference is needed (confirmed), so the default is static HTML/CSS/JS with no server, hostable on GitHub Pages or Netlify. Revisit this if the surface the user names later needs something a static page can't do.

## Users

**Open decision.** The user will name the audience and job when they request a surface. Do not assume examiners, clinicians, recruiters or patients until then.

## Product Purpose

A final-year Computer Science research project (2022-CS-172, Fiza Amjad) titled *Automated Detection and Severity Grading of Knee Osteoarthritis Using Deep Learning*. It classifies knee X-rays into Kellgren-Lawrence (KL) grades 0–4 with transfer-learned CNNs and explains each prediction with SHAP and LIME.

**Open decision:** what the interface itself should do (presentation, explainability view, dataset browser, and so on). The user will specify it.

## Positioning

A side-by-side comparison of four ImageNet backbones on the same KL-graded dataset, paired with per-image explainability (SHAP and LIME). That pairing is the project's distinguishing claim. Measured results on the 2,750-image evaluation set:

| Model | Accuracy | Balanced accuracy |
|---|---|---|
| Xception | 86.6% | 90.2% |
| InceptionResNetV2 | 78.6% | 84.3% |
| DenseNet201 | 76.1% | 80.4% |
| ResNet50 | 70.1% | 76.8% |

The separate Xception test notebook reports 83.7% test accuracy (loss 0.43). When either Xception figure is shown, cite which notebook it comes from.

## Operating Context

The work was done in Google Colab notebooks: data preparation and augmentation, one modeling notebook per backbone, an Xception test notebook, and a SHAP/LIME explanation notebook. The paper is the PDF in the project root, and the zip archive holds the source media.

## Capabilities and Constraints

- **No live inference.** The interface does not run a model. The Xception `.h5` file is not in the repo; only `media_files/resnet50_.weights.h5` is.
- **Data is class-imbalanced:**
  - Train split: grade 0 = 2,315, 1 = 1,064, 2 = 1,558, 3 = 777, 4 = 177.
  - Test split: grade 0 = 1,139, 1 = 530, 2 = 757, 3 = 380, 4 = 83.
- **Terminology:**
  - "Kellgren-Lawrence (KL) grade", 0 to 4, where 0 means no OA and 4 means severe OA.
  - "Balanced accuracy" is the metric that is honest under the class imbalance.
- **Clinical claims:** This is academic research, not a clinical device. Do not imply diagnostic approval or clinical validation.

## Evidence on Hand

- **Dataset:** `dataset/train_split/{0..4}` and `dataset/test_split/{0..4}` hold real knee X-ray PNGs.
- **Figures in `media_files/`:**
  - accuracy/loss curves for each model;
  - confusion matrices: `cof-xception`, `conf-densenet`, `confmetr-resnetv2`, `confusion_metrics_resnet50`;
  - ROC curves: `roc-exception`, `roc-densenet`, `roc-resnetv2`, `roc-res50-2`;
  - augmentation examples: rotation, shear, zoom, flips, width/height shift, brightness, channel shift, fill mode;
  - SHAP outputs (`shap-1`…`shap-5`) and LIME outputs (`lime-1`…`lime-5`);
  - grade examples: `grade0`, `grade-0`, `grade4`.
- **Paper:** the PDF in the project root.
- **Absent:** testimonials, clinical partners, external validation, deployment and usage data. Never fabricate any of these.

## Product Principles

1. **Report results honestly.** Show balanced accuracy next to accuracy, name the class imbalance, and never round numbers up.
2. **Show the evidence.** Real X-rays, real heatmaps and real figures come before illustrations or stock imagery.
3. **Explanations come first.** The SHAP and LIME outputs are the heart of the work, not an appendix.
4. **Research, not a medical device.** The tone and the claims stay academic.
