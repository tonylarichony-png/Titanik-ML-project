---
id: MLP-007
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_007_fe_familysize_32neurons
---

# MLP-007 — FE_familySize_32Neurons

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                             |
| ---------------- | ---------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-007 — FE_familySize_32Neurons                                                                    |
| Гипотеза         | CHANGE ME — if ..увеличить число нейронов ., then ..лучше отработает., because ..лог.связей боьлше . |
| Одно изменение   | CHANGE ME — exactly one controlled change                                                            |
| Решение          | reject |
| Reference        | MLP-002_reference: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng                              |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                  |
| Основная метрика | accuracy                                                                                             |
| Критерии         | failed                                                                                               |
| Код              | ml_project.mlp_experiments.mlp_007_fe_familysize_32neurons                                           |
| Hash кода        | a73c449975b2…                                                                                        |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0033 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0059 |              0.0000 |  False |
| guardrail | recall            |              -0.0174 |             -0.0100 |  False |
| guardrail | f1                |              -0.0075 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8103 | 0.0231 | 0.7921 | 0.8483 |
| mlp_candidate     | balanced_accuracy | 0.7870 | 0.0285 | 0.7560 | 0.8309 |
| mlp_candidate     | precision         | 0.7920 | 0.0328 | 0.7500 | 0.8387 |
| mlp_candidate     | recall            | 0.6869 | 0.0578 | 0.6029 | 0.7536 |
| mlp_candidate     | f1                | 0.7346 | 0.0392 | 0.6891 | 0.7939 |
| mlp_candidate     | roc_auc           | 0.8658 | 0.0178 | 0.8390 | 0.8799 |
| mlp_candidate     | log_loss          | 0.4278 | 0.0219 | 0.4037 | 0.4511 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8212 |    0.7933 |     -0.0279 |
|    2 | accuracy          |    0.8090 |    0.8034 |     -0.0056 |
|    3 | accuracy          |    0.7865 |    0.7921 |      0.0056 |
|    4 | accuracy          |    0.8090 |    0.8146 |      0.0056 |
|    5 | accuracy          |    0.8427 |    0.8483 |      0.0056 |
|    1 | balanced_accuracy |    0.8059 |    0.7751 |     -0.0308 |
|    2 | balanced_accuracy |    0.7837 |    0.7763 |     -0.0074 |
|    3 | balanced_accuracy |    0.7515 |    0.7560 |      0.0045 |
|    4 | balanced_accuracy |    0.7893 |    0.7967 |      0.0074 |
|    5 | balanced_accuracy |    0.8343 |    0.8309 |     -0.0034 |
|    1 | precision         |    0.7846 |    0.7500 |     -0.0346 |
|    2 | precision         |    0.7931 |    0.7895 |     -0.0036 |
|    3 | precision         |    0.7885 |    0.8039 |      0.0155 |
|    4 | precision         |    0.7742 |    0.7778 |      0.0036 |
|    5 | precision         |    0.7971 |    0.8387 |      0.0416 |
|    1 | recall            |    0.7391 |    0.6957 |     -0.0435 |
|    2 | recall            |    0.6765 |    0.6618 |     -0.0147 |
|    3 | recall            |    0.6029 |    0.6029 |      0.0000 |
|    4 | recall            |    0.7059 |    0.7206 |      0.0147 |
|    5 | recall            |    0.7971 |    0.7536 |     -0.0435 |
|    1 | f1                |    0.7612 |    0.7218 |     -0.0394 |
|    2 | f1                |    0.7302 |    0.7200 |     -0.0102 |
|    3 | f1                |    0.6833 |    0.6891 |      0.0057 |
|    4 | f1                |    0.7385 |    0.7481 |      0.0096 |
|    5 | f1                |    0.7971 |    0.7939 |     -0.0032 |
|    1 | roc_auc           |    0.8879 |    0.8799 |     -0.0080 |
|    2 | roc_auc           |    0.8651 |    0.8738 |      0.0087 |
|    3 | roc_auc           |    0.8477 |    0.8565 |      0.0088 |
|    4 | roc_auc           |    0.8384 |    0.8390 |      0.0005 |
|    5 | roc_auc           |    0.8720 |    0.8799 |      0.0080 |
|    1 | log_loss          |    0.4005 |    0.4143 |     -0.0138 |
|    2 | log_loss          |    0.4175 |    0.4037 |      0.0138 |
|    3 | log_loss          |    0.4551 |    0.4508 |      0.0043 |
|    4 | log_loss          |    0.4534 |    0.4511 |      0.0023 |
|    5 | log_loss          |    0.4301 |    0.4189 |      0.0112 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          16 |                     19 |         3 |           2 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-007/a73c449975b2/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-007/a73c449975b2/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-007/a73c449975b2/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-007/a73c449975b2/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
