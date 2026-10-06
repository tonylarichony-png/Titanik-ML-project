---
id: MLP-015
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_015_allin16plus_new_layer
---

# MLP-015 — Allin16plus new layer

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Эксперимент      | MLP-015 — Allin16plus new layer                                                                                                |
| Гипотеза         | CHANGE ME — if добавлю новый слой, then он поможет сети лучше обрабатывать данные, потому что добавится дополнительная ёмкость |
| Одно изменение   | CHANGE ME — exactly one controlled change                                                                                      |
| Решение          | reject |
| Reference        | MLP-012_reference: ml_project.mlp_experiments.mlp_012_allin_16neurons                                                          |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                            |
| Основная метрика | accuracy                                                                                                                       |
| Критерии         | failed                                                                                                                         |
| Код              | ml_project.mlp_experiments.mlp_015_allin16plus_new_layer                                                                       |
| Hash кода        | 14571cca38c9…                                                                                                                  |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0000 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0012 |              0.0000 |  False |
| guardrail | recall            |              -0.0059 |             -0.0100 |   True |
| guardrail | f1                |              -0.0016 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8260 | 0.0140 | 0.8090 | 0.8427 |
| mlp_candidate     | balanced_accuracy | 0.8010 | 0.0145 | 0.7837 | 0.8222 |
| mlp_candidate     | precision         | 0.8272 | 0.0357 | 0.7931 | 0.8846 |
| mlp_candidate     | recall            | 0.6930 | 0.0288 | 0.6667 | 0.7353 |
| mlp_candidate     | f1                | 0.7535 | 0.0193 | 0.7302 | 0.7812 |
| mlp_candidate     | roc_auc           | 0.8771 | 0.0189 | 0.8601 | 0.9093 |
| mlp_candidate     | log_loss          | 0.4109 | 0.0233 | 0.3848 | 0.4467 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8268 |    0.8380 |      0.0112 |
|    2 | accuracy          |    0.8258 |    0.8090 |     -0.0169 |
|    3 | accuracy          |    0.8090 |    0.8202 |      0.0112 |
|    4 | accuracy          |    0.8427 |    0.8427 |      0.0000 |
|    5 | accuracy          |    0.8258 |    0.8202 |     -0.0056 |
|    1 | balanced_accuracy |    0.7997 |    0.8061 |      0.0064 |
|    2 | balanced_accuracy |    0.8029 |    0.7837 |     -0.0193 |
|    3 | balanced_accuracy |    0.7865 |    0.7928 |      0.0063 |
|    4 | balanced_accuracy |    0.8222 |    0.8222 |      0.0000 |
|    5 | balanced_accuracy |    0.7993 |    0.8000 |      0.0007 |
|    1 | precision         |    0.8393 |    0.8846 |      0.0453 |
|    2 | precision         |    0.8136 |    0.7931 |     -0.0205 |
|    3 | precision         |    0.7833 |    0.8214 |      0.0381 |
|    4 | precision         |    0.8333 |    0.8333 |      0.0000 |
|    5 | precision         |    0.8393 |    0.8033 |     -0.0360 |
|    1 | recall            |    0.6812 |    0.6667 |     -0.0145 |
|    2 | recall            |    0.7059 |    0.6765 |     -0.0294 |
|    3 | recall            |    0.6912 |    0.6765 |     -0.0147 |
|    4 | recall            |    0.7353 |    0.7353 |      0.0000 |
|    5 | recall            |    0.6812 |    0.7101 |      0.0290 |
|    1 | f1                |    0.7520 |    0.7603 |      0.0083 |
|    2 | f1                |    0.7559 |    0.7302 |     -0.0257 |
|    3 | f1                |    0.7344 |    0.7419 |      0.0076 |
|    4 | f1                |    0.7812 |    0.7812 |      0.0000 |
|    5 | f1                |    0.7520 |    0.7538 |      0.0018 |
|    1 | roc_auc           |    0.9093 |    0.9093 |      0.0000 |
|    2 | roc_auc           |    0.8735 |    0.8751 |      0.0016 |
|    3 | roc_auc           |    0.8604 |    0.8601 |     -0.0003 |
|    4 | roc_auc           |    0.8717 |    0.8737 |      0.0020 |
|    5 | roc_auc           |    0.8698 |    0.8675 |     -0.0023 |
|    1 | log_loss          |    0.3826 |    0.3848 |     -0.0021 |
|    2 | log_loss          |    0.4125 |    0.4075 |      0.0050 |
|    3 | log_loss          |    0.4412 |    0.4467 |     -0.0056 |
|    4 | log_loss          |    0.3971 |    0.3985 |     -0.0013 |
|    5 | log_loss          |    0.4226 |    0.4169 |      0.0057 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          12 |                     12 |         2 |           2 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-015/14571cca38c9/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-015/14571cca38c9/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-015/14571cca38c9/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-015/14571cca38c9/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
