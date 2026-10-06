---
id: MLP-016
type: mlp-experiment
status: completed
decision: adopt
implementation_module: ml_project.mlp_experiments.mlp_016_allin16plus16layer
---

# MLP-016 — ALLin16plus16layer

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                              |
| ---------------- | --------------------------------------------------------------------- |
| Эксперимент      | MLP-016 — ALLin16plus16layer                                          |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                             |
| Одно изменение   | CHANGE ME — exactly one controlled change                             |
| Решение          | adopt |
| Reference        | MLP-012_reference: ml_project.mlp_experiments.mlp_012_allin_16neurons |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                   |
| Основная метрика | accuracy                                                              |
| Критерии         | passed                                                                |
| Код              | ml_project.mlp_experiments.mlp_016_allin16plus16layer                 |
| Hash кода        | d1e9d47ef34e…                                                         |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0011 |              0.0000 |   True |
| guardrail | balanced_accuracy |               0.0003 |              0.0000 |   True |
| guardrail | recall            |              -0.0030 |             -0.0100 |   True |
| guardrail | f1                |               0.0005 |              0.0000 |   True |

## Сравнение всех метрик

| model             | metric            |   mean |    std |    min |    max |
| ----------------- | ----------------- | -----: | -----: | -----: | -----: |
| MLP-012_reference | accuracy          | 0.8260 | 0.0119 | 0.8090 | 0.8427 |
| MLP-012_reference | balanced_accuracy | 0.8021 | 0.0129 | 0.7865 | 0.8222 |
| MLP-012_reference | precision         | 0.8218 | 0.0239 | 0.7833 | 0.8393 |
| MLP-012_reference | recall            | 0.6989 | 0.0227 | 0.6812 | 0.7353 |
| MLP-012_reference | f1                | 0.7551 | 0.0168 | 0.7344 | 0.7812 |
| MLP-012_reference | roc_auc           | 0.8769 | 0.0188 | 0.8604 | 0.9093 |
| MLP-012_reference | log_loss          | 0.4112 | 0.0226 | 0.3826 | 0.4412 |
| mlp_candidate     | accuracy          | 0.8271 | 0.0154 | 0.8146 | 0.8492 |
| mlp_candidate     | balanced_accuracy | 0.8024 | 0.0139 | 0.7854 | 0.8179 |
| mlp_candidate     | precision         | 0.8286 | 0.0449 | 0.7903 | 0.9038 |
| mlp_candidate     | recall            | 0.6960 | 0.0255 | 0.6618 | 0.7206 |
| mlp_candidate     | f1                | 0.7557 | 0.0188 | 0.7317 | 0.7769 |
| mlp_candidate     | roc_auc           | 0.8750 | 0.0211 | 0.8569 | 0.9097 |
| mlp_candidate     | log_loss          | 0.4132 | 0.0235 | 0.3911 | 0.4469 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8268 |    0.8492 |      0.0223 |
|    2 | accuracy          |    0.8258 |    0.8202 |     -0.0056 |
|    3 | accuracy          |    0.8090 |    0.8146 |      0.0056 |
|    4 | accuracy          |    0.8427 |    0.8371 |     -0.0056 |
|    5 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    1 | balanced_accuracy |    0.7997 |    0.8179 |      0.0182 |
|    2 | balanced_accuracy |    0.8029 |    0.8012 |     -0.0017 |
|    3 | balanced_accuracy |    0.7865 |    0.7854 |     -0.0011 |
|    4 | balanced_accuracy |    0.8222 |    0.8148 |     -0.0074 |
|    5 | balanced_accuracy |    0.7993 |    0.7928 |     -0.0065 |
|    1 | precision         |    0.8393 |    0.9038 |      0.0646 |
|    2 | precision         |    0.8136 |    0.7903 |     -0.0232 |
|    3 | precision         |    0.7833 |    0.8182 |      0.0348 |
|    4 | precision         |    0.8333 |    0.8305 |     -0.0028 |
|    5 | precision         |    0.8393 |    0.8000 |     -0.0393 |
|    1 | recall            |    0.6812 |    0.6812 |      0.0000 |
|    2 | recall            |    0.7059 |    0.7206 |      0.0147 |
|    3 | recall            |    0.6912 |    0.6618 |     -0.0294 |
|    4 | recall            |    0.7353 |    0.7206 |     -0.0147 |
|    5 | recall            |    0.6812 |    0.6957 |      0.0145 |
|    1 | f1                |    0.7520 |    0.7769 |      0.0249 |
|    2 | f1                |    0.7559 |    0.7538 |     -0.0021 |
|    3 | f1                |    0.7344 |    0.7317 |     -0.0027 |
|    4 | f1                |    0.7812 |    0.7717 |     -0.0096 |
|    5 | f1                |    0.7520 |    0.7442 |     -0.0078 |
|    1 | roc_auc           |    0.9093 |    0.9097 |      0.0004 |
|    2 | roc_auc           |    0.8735 |    0.8797 |      0.0061 |
|    3 | roc_auc           |    0.8604 |    0.8569 |     -0.0035 |
|    4 | roc_auc           |    0.8717 |    0.8650 |     -0.0067 |
|    5 | roc_auc           |    0.8698 |    0.8636 |     -0.0061 |
|    1 | log_loss          |    0.3826 |    0.3911 |     -0.0085 |
|    2 | log_loss          |    0.4125 |    0.3941 |      0.0185 |
|    3 | log_loss          |    0.4412 |    0.4469 |     -0.0057 |
|    4 | log_loss          |    0.3971 |    0.4072 |     -0.0101 |
|    5 | log_loss          |    0.4226 |    0.4266 |     -0.0040 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          14 |                     13 |         2 |           3 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-016/d1e9d47ef34e/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-016/d1e9d47ef34e/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-016/d1e9d47ef34e/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-016/d1e9d47ef34e/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
