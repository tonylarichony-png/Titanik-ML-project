---
id: MLP-008
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_008_age_by_title
---

# MLP-008 — Заполнение Age медианой по Title

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-008 — Заполнение Age медианой по Title                                                                                                                                       |
| Гипотеза         | Если заполнять пропуски Age медианой возраста пассажиров с тем же нормализованным Title внутри train-fold, то MLP точнее учтёт возрастные различия между Mr, Mrs, Miss и Master. |
| Одно изменение   | Относительно принятого MLP-002 изменяется только заполнение Age: медиана по Title с fallback на общую медиану train-fold.                                                        |
| Решение          | reject |
| Reference        | MLP-002_reference: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng                                                                                                          |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                              |
| Основная метрика | accuracy                                                                                                                                                                         |
| Критерии         | failed                                                                                                                                                                           |
| Код              | ml_project.mlp_experiments.mlp_008_age_by_title                                                                                                                                  |
| Hash кода        | 5bf4f53d8bc6…                                                                                                                                                                    |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0022 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0034 |              0.0000 |  False |
| guardrail | recall            |              -0.0086 |             -0.0100 |   True |
| guardrail | f1                |              -0.0038 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8114 | 0.0137 | 0.7921 | 0.8258 |
| mlp_candidate     | balanced_accuracy | 0.7895 | 0.0201 | 0.7588 | 0.8126 |
| mlp_candidate     | precision         | 0.7884 | 0.0159 | 0.7619 | 0.8033 |
| mlp_candidate     | recall            | 0.6957 | 0.0494 | 0.6176 | 0.7536 |
| mlp_candidate     | f1                | 0.7383 | 0.0285 | 0.6942 | 0.7704 |
| mlp_candidate     | roc_auc           | 0.8635 | 0.0186 | 0.8435 | 0.8897 |
| mlp_candidate     | log_loss          | 0.4285 | 0.0221 | 0.3974 | 0.4512 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8212 |    0.8212 |      0.0000 |
|    2 | accuracy          |    0.8090 |    0.8146 |      0.0056 |
|    3 | accuracy          |    0.7865 |    0.7921 |      0.0056 |
|    4 | accuracy          |    0.8090 |    0.8034 |     -0.0056 |
|    5 | accuracy          |    0.8427 |    0.8258 |     -0.0169 |
|    1 | balanced_accuracy |    0.8059 |    0.8005 |     -0.0054 |
|    2 | balanced_accuracy |    0.7837 |    0.7910 |      0.0074 |
|    3 | balanced_accuracy |    0.7515 |    0.7588 |      0.0074 |
|    4 | balanced_accuracy |    0.7893 |    0.7848 |     -0.0045 |
|    5 | balanced_accuracy |    0.8343 |    0.8126 |     -0.0217 |
|    1 | precision         |    0.7846 |    0.8033 |      0.0187 |
|    2 | precision         |    0.7931 |    0.7966 |      0.0035 |
|    3 | precision         |    0.7885 |    0.7925 |      0.0040 |
|    4 | precision         |    0.7742 |    0.7619 |     -0.0123 |
|    5 | precision         |    0.7971 |    0.7879 |     -0.0092 |
|    1 | recall            |    0.7391 |    0.7101 |     -0.0290 |
|    2 | recall            |    0.6765 |    0.6912 |      0.0147 |
|    3 | recall            |    0.6029 |    0.6176 |      0.0147 |
|    4 | recall            |    0.7059 |    0.7059 |      0.0000 |
|    5 | recall            |    0.7971 |    0.7536 |     -0.0435 |
|    1 | f1                |    0.7612 |    0.7538 |     -0.0073 |
|    2 | f1                |    0.7302 |    0.7402 |      0.0100 |
|    3 | f1                |    0.6833 |    0.6942 |      0.0109 |
|    4 | f1                |    0.7385 |    0.7328 |     -0.0056 |
|    5 | f1                |    0.7971 |    0.7704 |     -0.0267 |
|    1 | roc_auc           |    0.8879 |    0.8897 |      0.0017 |
|    2 | roc_auc           |    0.8651 |    0.8648 |     -0.0003 |
|    3 | roc_auc           |    0.8477 |    0.8483 |      0.0007 |
|    4 | roc_auc           |    0.8384 |    0.8435 |      0.0051 |
|    5 | roc_auc           |    0.8720 |    0.8714 |     -0.0006 |
|    1 | log_loss          |    0.4005 |    0.3974 |      0.0032 |
|    2 | log_loss          |    0.4175 |    0.4179 |     -0.0004 |
|    3 | log_loss          |    0.4551 |    0.4512 |      0.0039 |
|    4 | log_loss          |    0.4534 |    0.4473 |      0.0061 |
|    5 | log_loss          |    0.4301 |    0.4289 |      0.0013 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           6 |                      8 |         2 |           2 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-008/5bf4f53d8bc6/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-008/5bf4f53d8bc6/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-008/5bf4f53d8bc6/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-008/5bf4f53d8bc6/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
