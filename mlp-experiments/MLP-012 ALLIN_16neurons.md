---
id: MLP-012
type: mlp-experiment
status: completed
decision: adopt
implementation_module: ml_project.mlp_experiments.mlp_012_allin_16neurons
---

# MLP-012 — All In — 16 скрытых нейронов

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-012 — All In — 16 скрытых нейронов                                                                                                                                     |
| Гипотеза         | Если увеличить скрытый слой принятого all-in MLP с 8 до 16 нейронов, то дополнительная ёмкость поможет сети использовать взаимодействия между всеми созданными признаками. |
| Одно изменение   | Относительно MLP-010 изменяется только hidden_dim: 8 → 16; feature engineering, preprocessing и режим обучения сохраняются.                                                |
| Решение          | adopt |
| Reference        | MLP-010_reference: ml_project.mlp_experiments.mlp_010_mlp_allin                                                                                                            |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                        |
| Основная метрика | accuracy                                                                                                                                                                   |
| Критерии         | passed                                                                                                                                                                     |
| Код              | ml_project.mlp_experiments.mlp_012_allin_16neurons                                                                                                                         |
| Hash кода        | b42f362ef1ee…                                                                                                                                                              |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0067 |              0.0000 |   True |
| guardrail | balanced_accuracy |               0.0076 |              0.0000 |   True |
| guardrail | recall            |               0.0116 |             -0.0100 |   True |
| guardrail | f1                |               0.0106 |              0.0000 |   True |

## Сравнение всех метрик

| model             | metric            |   mean |    std |    min |    max |
| ----------------- | ----------------- | -----: | -----: | -----: | -----: |
| MLP-010_reference | accuracy          | 0.8193 | 0.0138 | 0.8090 | 0.8427 |
| MLP-010_reference | balanced_accuracy | 0.7945 | 0.0175 | 0.7779 | 0.8222 |
| MLP-010_reference | precision         | 0.8139 | 0.0233 | 0.7778 | 0.8333 |
| MLP-010_reference | recall            | 0.6873 | 0.0405 | 0.6377 | 0.7353 |
| MLP-010_reference | f1                | 0.7445 | 0.0237 | 0.7213 | 0.7812 |
| MLP-010_reference | roc_auc           | 0.8762 | 0.0176 | 0.8590 | 0.9043 |
| MLP-010_reference | log_loss          | 0.4104 | 0.0210 | 0.3892 | 0.4423 |
| mlp_candidate     | accuracy          | 0.8260 | 0.0119 | 0.8090 | 0.8427 |
| mlp_candidate     | balanced_accuracy | 0.8021 | 0.0129 | 0.7865 | 0.8222 |
| mlp_candidate     | precision         | 0.8218 | 0.0239 | 0.7833 | 0.8393 |
| mlp_candidate     | recall            | 0.6989 | 0.0227 | 0.6812 | 0.7353 |
| mlp_candidate     | f1                | 0.7551 | 0.0168 | 0.7344 | 0.7812 |
| mlp_candidate     | roc_auc           | 0.8769 | 0.0188 | 0.8604 | 0.9093 |
| mlp_candidate     | log_loss          | 0.4112 | 0.0226 | 0.3826 | 0.4412 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8101 |    0.8268 |      0.0168 |
|    2 | accuracy          |    0.8146 |    0.8258 |      0.0112 |
|    3 | accuracy          |    0.8090 |    0.8090 |      0.0000 |
|    4 | accuracy          |    0.8427 |    0.8427 |      0.0000 |
|    5 | accuracy          |    0.8202 |    0.8258 |      0.0056 |
|    1 | balanced_accuracy |    0.7779 |    0.7997 |      0.0217 |
|    2 | balanced_accuracy |    0.7967 |    0.8029 |      0.0063 |
|    3 | balanced_accuracy |    0.7809 |    0.7865 |      0.0056 |
|    4 | balanced_accuracy |    0.8222 |    0.8222 |      0.0000 |
|    5 | balanced_accuracy |    0.7947 |    0.7993 |      0.0046 |
|    1 | precision         |    0.8302 |    0.8393 |      0.0091 |
|    2 | precision         |    0.7778 |    0.8136 |      0.0358 |
|    3 | precision         |    0.8036 |    0.7833 |     -0.0202 |
|    4 | precision         |    0.8333 |    0.8333 |      0.0000 |
|    5 | precision         |    0.8246 |    0.8393 |      0.0147 |
|    1 | recall            |    0.6377 |    0.6812 |      0.0435 |
|    2 | recall            |    0.7206 |    0.7059 |     -0.0147 |
|    3 | recall            |    0.6618 |    0.6912 |      0.0294 |
|    4 | recall            |    0.7353 |    0.7353 |      0.0000 |
|    5 | recall            |    0.6812 |    0.6812 |      0.0000 |
|    1 | f1                |    0.7213 |    0.7520 |      0.0307 |
|    2 | f1                |    0.7481 |    0.7559 |      0.0078 |
|    3 | f1                |    0.7258 |    0.7344 |      0.0086 |
|    4 | f1                |    0.7812 |    0.7812 |      0.0000 |
|    5 | f1                |    0.7460 |    0.7520 |      0.0060 |
|    1 | roc_auc           |    0.9043 |    0.9093 |      0.0050 |
|    2 | roc_auc           |    0.8811 |    0.8735 |     -0.0076 |
|    3 | roc_auc           |    0.8590 |    0.8604 |      0.0013 |
|    4 | roc_auc           |    0.8687 |    0.8717 |      0.0029 |
|    5 | roc_auc           |    0.8676 |    0.8698 |      0.0021 |
|    1 | log_loss          |    0.3892 |    0.3826 |      0.0065 |
|    2 | log_loss          |    0.3985 |    0.4125 |     -0.0140 |
|    3 | log_loss          |    0.4423 |    0.4412 |      0.0012 |
|    4 | log_loss          |    0.4022 |    0.3971 |      0.0051 |
|    5 | log_loss          |    0.4197 |    0.4226 |     -0.0029 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          15 |                      9 |         3 |           0 |    2 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-012/b42f362ef1ee/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-012/b42f362ef1ee/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-012/b42f362ef1ee/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-012/b42f362ef1ee/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
