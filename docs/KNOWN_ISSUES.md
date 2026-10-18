# Known research issues

These findings concern the historical artifacts, not failures of the maintenance scripts.

| Finding | Evidence | Required follow-up |
| --- | --- | --- |
| Cross-split duplication | SHA-256 audit: 2,834 identical image groups cross committed splits | Establish participant-disjoint splits and evaluate again |
| Validation uses test-named source | Modeling notebooks sample `test_split` into `sampled_test` and pass it as `validation_data` | Separate validation and final test |
| Architecture attribution mismatch | `data_modeling_ResNet50.ipynb` constructs `InceptionResNetV2` | Recover correct code/checkpoint and rerun; do not label the existing result verified ResNet50 |
| Missing complete Xception checkpoint | Test and explanation notebooks load `/content/xception_model (1).h5` | Publish an appropriately licensed checkpoint with checksum or training recipe |
| Colab-only paths and setup order | `/content/` paths and upload/unzip cells occur after modeling cells in some notebooks | Create a clean environment and reorder a separate reproducibility copy |
| Hidden notebook state | Modeling cells refer to variables such as `img_shape` and `model_ft` without consistent definitions in the committed code | Reconstruct explicit model definitions and validate from a fresh kernel |
| Unrecorded random sampling | `random.shuffle` with no persisted split manifest | Seed and save the exact image list |
| Dataset rights not established | No verified source license/consent record accompanies the images | Establish provenance and redistribution terms |

Original outputs remain attached to the original notebook files. A green repository-check workflow means the tooling and file structure passed its declared checks, not that these research issues have been resolved.
