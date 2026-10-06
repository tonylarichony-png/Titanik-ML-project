# PyTorch MLP experiments

<!-- auto:mlp-experiment-registry:start -->

| Эксперимент                                                                                                   | Reference         | Результат       | Δ       | Решение |
| ------------------------------------------------------------------------------------------------------------- | ----------------- | --------------- | ------- | ------- |
| [[mlp-experiments/MLP-001 Baseline.md\|MLP-001 — First reproducible MLP baseline]]                            | sklearn_champion  | 0.8148 ± 0.0134 | +0.0022 | pending |
| [[mlp-experiments/MLP-002 8 Neurons Baseline.md\|MLP-002 — Компактный MLP baseline — 8 скрытых нейронов]]     | sklearn_champion  | 0.8137 ± 0.0205 | +0.0011 | adopt   |
| [[mlp-experiments/MLP-003 mlp_16neurons.md\|MLP-003 — mlp_16neurons]]                                         | MLP-002_reference | 0.8137 ± 0.0209 | +0.0000 | reject  |
| [[mlp-experiments/MLP-004 mlp_32neurons.md\|MLP-004 — mlp_32neurons]]                                         | MLP-002_reference | 0.8148 ± 0.0134 | +0.0011 | reject  |
| [[mlp-experiments/MLP-005 FE_Family_size.md\|MLP-005 — FE_Family_size]]                                       | MLP-002_reference | 0.8103 ± 0.0172 | -0.0034 | reject  |
| [[mlp-experiments/MLP-006 FE_FAmilySize_16Neurons.md\|MLP-006 — FE_FAmilySize_16Neurons]]                     | MLP-002_reference | 0.8103 ± 0.0108 | -0.0034 | reject  |
| [[mlp-experiments/MLP-007 FE_familySize_32Neurons.md\|MLP-007 — FE_familySize_32Neurons]]                     | MLP-002_reference | 0.8103 ± 0.0231 | -0.0033 | reject  |
| [[mlp-experiments/MLP-008 Age median by Title.md\|MLP-008 — Заполнение Age медианой по Title]]                | MLP-002_reference | 0.8114 ± 0.0137 | -0.0022 | reject  |
| [[mlp-experiments/MLP-009 TABDDPM.md\|MLP-009 — TABDDPM]]                                                     | MLP-002_reference | 0.8126 ± 0.0182 | -0.0011 | reject  |
| [[mlp-experiments/MLP-010 MLP_ALLIN.md\|MLP-010 — MLP All In — все созданные признаки]]                       | MLP-002_reference | 0.8193 ± 0.0138 | +0.0056 | adopt   |
| [[mlp-experiments/MLP-011 MLP_16neurons.md\|MLP-011 — MLP_16neurons]]                                         | MLP-010_reference | 0.8148 ± 0.0134 | -0.0045 | reject  |
| [[mlp-experiments/MLP-012 ALLIN_16neurons.md\|MLP-012 — All In — 16 скрытых нейронов]]                        | MLP-010_reference | 0.8260 ± 0.0119 | +0.0067 | adopt   |
| [[mlp-experiments/MLP-013 ALLIN32_neurons.md\|MLP-013 — ALLIN32_neurons]]                                     | MLP-012_reference | 0.8193 ± 0.0184 | -0.0067 | reject  |
| [[mlp-experiments/MLP-014 ALLIN16BAtchnorm.md\|MLP-014 — ALLIN16BAtchnorm]]                                   | MLP-012_reference | 0.8170 ± 0.0143 | -0.0090 | reject  |
| [[mlp-experiments/MLP-015 Allin16plus new layer.md\|MLP-015 — Allin16plus new layer]]                         | MLP-012_reference | 0.8260 ± 0.0140 | -0.0000 | reject  |
| [[mlp-experiments/MLP-016 ALLin16plus16layer.md\|MLP-016 — ALLin16plus16layer]]                               | MLP-012_reference | 0.8271 ± 0.0154 | +0.0011 | adopt   |
| [[mlp-experiments/MLP-017 ALLIN16168.md\|MLP-017 — ALLIN16168]]                                               | MLP-016_reference | 0.8227 ± 0.0098 | -0.0045 | reject  |
| [[mlp-experiments/MLP-018 ALLIN161616.md\|MLP-018 — ALLIN161616]]                                             | MLP-016_reference | 0.8316 ± 0.0128 | +0.0045 | adopt   |
| [[mlp-experiments/MLP-019 323232.md\|MLP-019 — 323232]]                                                       | MLP-018_reference | 0.8227 ± 0.0129 | -0.0090 | reject  |
| [[mlp-experiments/MLP-020 16Batch1616.md\|MLP-020 — 16Batch1616]]                                             | MLP-018_reference | 0.8193 ± 0.0115 | -0.0123 | reject  |
| [[mlp-experiments/MLP-021 1616btch16.md\|MLP-021 — 1616btch16]]                                               | MLP-018_reference | 0.8103 ± 0.0146 | -0.0213 | reject  |
| [[mlp-experiments/MLP-022 161616batch.md\|MLP-022 — 161616batch]]                                             | MLP-018_reference | 0.8249 ± 0.0169 | -0.0067 | reject  |
| [[mlp-experiments/MLP-023 Dpoutlight.md\|MLP-023 — Dpoutlight]]                                               | MLP-018_reference | 0.8294 ± 0.0155 | -0.0023 | reject  |
| [[mlp-experiments/MLP-024 dpoutmedium.md\|MLP-024 — dpoutmedium]]                                             | MLP-018_reference | 0.8384 ± 0.0111 | +0.0067 | adopt   |
| [[mlp-experiments/MLP-025 dpoutmed-hard.md\|MLP-025 — dpoutmed-hard]]                                         | MLP-024_reference | 0.8271 ± 0.0186 | -0.0112 | reject  |
| [[mlp-experiments/MLP-026 Dpoutlight 1layer.md\|MLP-026 — Dpoutlight 1layer]]                                 | MLP-024_reference | 0.8238 ± 0.0170 | -0.0146 | reject  |
| [[mlp-experiments/MLP-027 Dpoutmed 1layer.md\|MLP-027 — Dpoutmed 1layer]]                                     | MLP-024_reference | 0.8171 ± 0.0123 | -0.0213 | reject  |
| [[mlp-experiments/MLP-028 dpout_2ndlayerlight.md\|MLP-028 — dpout_2ndlayerlight]]                             | MLP-024_reference | 0.8271 ± 0.0178 | -0.0112 | reject  |
| [[mlp-experiments/MLP-029 GELU.md\|MLP-029 — GELU]]                                                           | MLP-024_reference | 0.8271 ± 0.0103 | -0.0112 | reject  |
| [[mlp-experiments/MLP-030 Leakyrelu.md\|MLP-030 — Leakyrelu]]                                                 | MLP-024_reference | 0.8305 ± 0.0137 | -0.0079 | reject  |
| [[mlp-experiments/MLP-031 LeakyRelu01.md\|MLP-031 — LeakyRelu01]]                                             | MLP-024_reference | 0.8271 ± 0.0153 | -0.0112 | reject  |
| [[mlp-experiments/MLP-032 squaredReLU.md\|MLP-032 — squaredReLU]]                                             | MLP-024_reference | 0.8384 ± 0.0111 | +0.0000 | reject  |
| [[mlp-experiments/MLP-033 squearedRELU.md\|MLP-033 — squearedRELU]]                                           | MLP-024_reference | 0.7712 ± 0.0877 | -0.0671 | reject  |
| [[mlp-experiments/MLP-034 batchsize16.md\|MLP-034 — batchsize16]]                                             | MLP-024_reference | 0.8305 ± 0.0210 | -0.0079 | reject  |
| [[mlp-experiments/MLP-036 Batch64.md\|MLP-036 — Batch64]]                                                     | MLP-024_reference | 0.8271 ± 0.0172 | -0.0112 | reject  |
| [[mlp-experiments/MLP-037 decay0001.md\|MLP-037 — decay0.001]]                                                | MLP-024_reference | 0.8328 ± 0.0158 | -0.0056 | reject  |
| [[mlp-experiments/MLP-038 middecay.md\|MLP-038 — middecay]]                                                   | MLP-024_reference | 0.8215 ± 0.0109 | -0.0168 | reject  |
| [[mlp-experiments/MLP-039 decaye-5.md\|MLP-039 — decaye-5]]                                                   | MLP-024_reference | 0.8260 ± 0.0219 | -0.0123 | reject  |
| [[mlp-experiments/MLP-040 LRe-4.md\|MLP-040 — LRe-4]]                                                         | MLP-024_reference | 0.8260 ± 0.0115 | -0.0123 | reject  |
| [[mlp-experiments/MLP-041 LR-4mindelta.md\|MLP-041 — LR-4mindelta]]                                           | MLP-024_reference | 0.8271 ± 0.0117 | -0.0112 | reject  |
| [[mlp-experiments/MLP-042 Optuna best ReLU trial 0.md\|MLP-042 — Optuna best ReLU trial 0]]                   | MLP-024_reference | 0.8193 ± 0.0094 | -0.0191 | reject  |
| [[mlp-experiments/MLP-043 Optuna stable LeakyReLU trial 137.md\|MLP-043 — Optuna stable LeakyReLU trial 137]] | MLP-024_reference | 0.8238 ± 0.0132 | -0.0146 | reject  |
| [[mlp-experiments/MLP-044 Scheduler.md\|MLP-044 — Scheduler]]                                                 | MLP-024_reference | 0.8316 ± 0.0157 | -0.0067 | reject  |
| [[mlp-experiments/MLP-045 Embeddings.md\|MLP-045 — Embeddings]]                                               | MLP-024_reference | 0.8182 ± 0.0217 | -0.0202 | pending |

<!-- auto:mlp-experiment-registry:end -->
