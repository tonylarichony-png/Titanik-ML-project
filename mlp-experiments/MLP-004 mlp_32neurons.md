---
id: MLP-004
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_004_mlp_32neurons
---

# MLP-004 — mlp_32neurons

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                       |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-004 — mlp_32neurons                                                                                        |
| Гипотеза         | CHANGE ME — if увеличить количество нейронов, then .улучшится точность.., because .больше связей логических .. |
| Одно изменение   | CHANGE ME — exactly one controlled change                                                                      |
| Решение          | reject |
| Reference        | MLP-002_reference: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng                                        |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                            |
| Основная метрика | accuracy                                                                                                       |
| Критерии         | failed                                                                                                         |
| Код              | ml_project.mlp_experiments.mlp_004_mlp_32neurons                                                               |
| Hash кода        | d03918e4eb15…                                                                                                  |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0011 |              0.0000 |   True |
| guardrail | balanced_accuracy |              -0.0001 |              0.0000 |  False |
| guardrail | recall            |              -0.0057 |             -0.0100 |   True |
| guardrail | f1                |               0.0008 |              0.0000 |   True |

## Сравнение всех метрик

| model             | metric            |   mean |    std |    min |    max |
| ----------------- | ----------------- | -----: | -----: | -----: | -----: |
| MLP-002_reference | accuracy          | 0.8137 | 0.0205 | 0.7865 | 0.8427 |
| MLP-002_reference | balanced_accuracy | 0.7929 | 0.0304 | 0.7515 | 0.8343 |
| MLP-002_reference | precision         | 0.7875 | 0.0088 | 0.7742 | 0.7971 |
| MLP-002_reference | recall            | 0.7043 | 0.0722 | 0.6029 | 0.7971 |
| MLP-002_reference | f1                | 0.7420 | 0.0418 | 0.6833 | 0.7971 |
| MLP-002_reference | roc_auc           | 0.8622 | 0.0196 | 0.8384 | 0.8879 |
| MLP-002_reference | log_loss          | 0.4313 | 0.0234 | 0.4005 | 0.4551 |
| mlp_candidate     | accuracy          | 0.8148 | 0.0134 | 0.8034 | 0.8315 |
| mlp_candidate     | balanced_accuracy | 0.7929 | 0.0179 | 0.7707 | 0.8145 |
| mlp_candidate     | precision         | 0.7945 | 0.0214 | 0.7619 | 0.8113 |
| mlp_candidate     | recall            | 0.6986 | 0.0413 | 0.6324 | 0.7391 |
| mlp_candidate     | f1                | 0.7428 | 0.0251 | 0.7107 | 0.7727 |
| mlp_candidate     | roc_auc           | 0.8675 | 0.0192 | 0.8463 | 0.8882 |
| mlp_candidate     | log_loss          | 0.4276 | 0.0242 | 0.4013 | 0.4533 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8212 |    0.8268 |      0.0056 |
|    2 | accuracy          |    0.8090 |    0.8090 |      0.0000 |
|    3 | accuracy          |    0.7865 |    0.8034 |      0.0169 |
|    4 | accuracy          |    0.8090 |    0.8034 |     -0.0056 |
|    5 | accuracy          |    0.8427 |    0.8315 |     -0.0112 |
|    1 | balanced_accuracy |    0.8059 |    0.8078 |      0.0018 |
|    2 | balanced_accuracy |    0.7837 |    0.7865 |      0.0028 |
|    3 | balanced_accuracy |    0.7515 |    0.7707 |      0.0193 |
|    4 | balanced_accuracy |    0.7893 |    0.7848 |     -0.0045 |
|    5 | balanced_accuracy |    0.8343 |    0.8145 |     -0.0198 |
|    1 | precision         |    0.7846 |    0.8065 |      0.0218 |
|    2 | precision         |    0.7931 |    0.7833 |     -0.0098 |
|    3 | precision         |    0.7885 |    0.8113 |      0.0229 |
|    4 | precision         |    0.7742 |    0.7619 |     -0.0123 |
|    5 | precision         |    0.7971 |    0.8095 |      0.0124 |
|    1 | recall            |    0.7391 |    0.7246 |     -0.0145 |
|    2 | recall            |    0.6765 |    0.6912 |      0.0147 |
|    3 | recall            |    0.6029 |    0.6324 |      0.0294 |
|    4 | recall            |    0.7059 |    0.7059 |      0.0000 |
|    5 | recall            |    0.7971 |    0.7391 |     -0.0580 |
|    1 | f1                |    0.7612 |    0.7634 |      0.0022 |
|    2 | f1                |    0.7302 |    0.7344 |      0.0042 |
|    3 | f1                |    0.6833 |    0.7107 |      0.0274 |
|    4 | f1                |    0.7385 |    0.7328 |     -0.0056 |
|    5 | f1                |    0.7971 |    0.7727 |     -0.0244 |
|    1 | roc_auc           |    0.8879 |    0.8882 |      0.0003 |
|    2 | roc_auc           |    0.8651 |    0.8725 |      0.0074 |
|    3 | roc_auc           |    0.8477 |    0.8485 |      0.0008 |
|    4 | roc_auc           |    0.8384 |    0.8463 |      0.0079 |
|    5 | roc_auc           |    0.8720 |    0.8818 |      0.0098 |
|    1 | log_loss          |    0.4005 |    0.4013 |     -0.0008 |
|    2 | log_loss          |    0.4175 |    0.4120 |      0.0055 |
|    3 | log_loss          |    0.4551 |    0.4533 |      0.0018 |
|    4 | log_loss          |    0.4534 |    0.4532 |      0.0002 |
|    5 | log_loss          |    0.4301 |    0.4182 |      0.0119 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          13 |                     12 |         2 |           2 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-004/d03918e4eb15/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-004/d03918e4eb15/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-004/d03918e4eb15/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-004/d03918e4eb15/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
