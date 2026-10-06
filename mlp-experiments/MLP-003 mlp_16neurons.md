---
id: MLP-003
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_003_mlp_16neurons
---

# MLP-003 — mlp_16neurons

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                       |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-003 — mlp_16neurons                                                                                        |
| Гипотеза         | CHANGE ME — if увеличить количество нейронов, then .улучшится точность.., because .больше связей логических .. |
| Одно изменение   | CHANGE ME — exactly one controlled change                                                                      |
| Решение          | reject |
| Reference        | MLP-002_reference: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng                                        |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                            |
| Основная метрика | accuracy                                                                                                       |
| Критерии         | failed                                                                                                         |
| Код              | ml_project.mlp_experiments.mlp_003_mlp_16neurons                                                               |
| Hash кода        | dd49713a1545…                                                                                                  |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0000 |              0.0000 |   True |
| guardrail | balanced_accuracy |              -0.0016 |              0.0000 |  False |
| guardrail | recall            |              -0.0086 |             -0.0100 |   True |
| guardrail | f1                |              -0.0012 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8137 | 0.0209 | 0.7933 | 0.8483 |
| mlp_candidate     | balanced_accuracy | 0.7914 | 0.0245 | 0.7751 | 0.8336 |
| mlp_candidate     | precision         | 0.7944 | 0.0344 | 0.7500 | 0.8281 |
| mlp_candidate     | recall            | 0.6957 | 0.0482 | 0.6324 | 0.7681 |
| mlp_candidate     | f1                | 0.7409 | 0.0326 | 0.7167 | 0.7970 |
| mlp_candidate     | roc_auc           | 0.8639 | 0.0146 | 0.8404 | 0.8778 |
| mlp_candidate     | log_loss          | 0.4308 | 0.0187 | 0.4115 | 0.4526 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8212 |    0.7933 |     -0.0279 |
|    2 | accuracy          |    0.8090 |    0.8146 |      0.0056 |
|    3 | accuracy          |    0.7865 |    0.8090 |      0.0225 |
|    4 | accuracy          |    0.8090 |    0.8034 |     -0.0056 |
|    5 | accuracy          |    0.8427 |    0.8483 |      0.0056 |
|    1 | balanced_accuracy |    0.8059 |    0.7751 |     -0.0308 |
|    2 | balanced_accuracy |    0.7837 |    0.7910 |      0.0074 |
|    3 | balanced_accuracy |    0.7515 |    0.7753 |      0.0238 |
|    4 | balanced_accuracy |    0.7893 |    0.7820 |     -0.0074 |
|    5 | balanced_accuracy |    0.8343 |    0.8336 |     -0.0007 |
|    1 | precision         |    0.7846 |    0.7500 |     -0.0346 |
|    2 | precision         |    0.7931 |    0.7966 |      0.0035 |
|    3 | precision         |    0.7885 |    0.8269 |      0.0385 |
|    4 | precision         |    0.7742 |    0.7705 |     -0.0037 |
|    5 | precision         |    0.7971 |    0.8281 |      0.0310 |
|    1 | recall            |    0.7391 |    0.6957 |     -0.0435 |
|    2 | recall            |    0.6765 |    0.6912 |      0.0147 |
|    3 | recall            |    0.6029 |    0.6324 |      0.0294 |
|    4 | recall            |    0.7059 |    0.6912 |     -0.0147 |
|    5 | recall            |    0.7971 |    0.7681 |     -0.0290 |
|    1 | f1                |    0.7612 |    0.7218 |     -0.0394 |
|    2 | f1                |    0.7302 |    0.7402 |      0.0100 |
|    3 | f1                |    0.6833 |    0.7167 |      0.0333 |
|    4 | f1                |    0.7385 |    0.7287 |     -0.0098 |
|    5 | f1                |    0.7971 |    0.7970 |     -0.0001 |
|    1 | roc_auc           |    0.8879 |    0.8740 |     -0.0140 |
|    2 | roc_auc           |    0.8651 |    0.8662 |      0.0011 |
|    3 | roc_auc           |    0.8477 |    0.8613 |      0.0136 |
|    4 | roc_auc           |    0.8384 |    0.8404 |      0.0020 |
|    5 | roc_auc           |    0.8720 |    0.8778 |      0.0059 |
|    1 | log_loss          |    0.4005 |    0.4249 |     -0.0244 |
|    2 | log_loss          |    0.4175 |    0.4115 |      0.0060 |
|    3 | log_loss          |    0.4551 |    0.4485 |      0.0066 |
|    4 | log_loss          |    0.4534 |    0.4526 |      0.0009 |
|    5 | log_loss          |    0.4301 |    0.4166 |      0.0135 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          14 |                     14 |         3 |           2 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-003/dd49713a1545/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-003/dd49713a1545/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-003/dd49713a1545/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-003/dd49713a1545/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
