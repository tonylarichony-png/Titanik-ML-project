---
id: MLP-006
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_006_fe_familysize_16neurons
---

# MLP-006 — FE_FAmilySize_16Neurons

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-006 — FE_FAmilySize_16Neurons                                                                                   |
| Гипотеза         | CHANGE ME — if добавить нвоый признак_, then 16 нейронов нейросеть отработает лучше..., because больше лог связей.. |
| Одно изменение   | CHANGE ME — exactly one controlled change                                                                           |
| Решение          | reject |
| Reference        | MLP-002_reference: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng                                             |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                 |
| Основная метрика | accuracy                                                                                                            |
| Критерии         | failed                                                                                                              |
| Код              | ml_project.mlp_experiments.mlp_006_fe_familysize_16neurons                                                          |
| Hash кода        | 4db24a585d74…                                                                                                       |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0034 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0043 |              0.0000 |  False |
| guardrail | recall            |              -0.0087 |             -0.0100 |   True |
| guardrail | f1                |              -0.0050 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8103 | 0.0108 | 0.7978 | 0.8258 |
| mlp_candidate     | balanced_accuracy | 0.7886 | 0.0180 | 0.7634 | 0.8126 |
| mlp_candidate     | precision         | 0.7864 | 0.0166 | 0.7692 | 0.8077 |
| mlp_candidate     | recall            | 0.6957 | 0.0508 | 0.6176 | 0.7536 |
| mlp_candidate     | f1                | 0.7371 | 0.0257 | 0.7000 | 0.7704 |
| mlp_candidate     | roc_auc           | 0.8651 | 0.0190 | 0.8374 | 0.8828 |
| mlp_candidate     | log_loss          | 0.4306 | 0.0214 | 0.4128 | 0.4567 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8212 |    0.8101 |     -0.0112 |
|    2 | accuracy          |    0.8090 |    0.8146 |      0.0056 |
|    3 | accuracy          |    0.7865 |    0.7978 |      0.0112 |
|    4 | accuracy          |    0.8090 |    0.8034 |     -0.0056 |
|    5 | accuracy          |    0.8427 |    0.8258 |     -0.0169 |
|    1 | balanced_accuracy |    0.8059 |    0.7941 |     -0.0118 |
|    2 | balanced_accuracy |    0.7837 |    0.7910 |      0.0074 |
|    3 | balanced_accuracy |    0.7515 |    0.7634 |      0.0119 |
|    4 | balanced_accuracy |    0.7893 |    0.7820 |     -0.0074 |
|    5 | balanced_accuracy |    0.8343 |    0.8126 |     -0.0217 |
|    1 | precision         |    0.7846 |    0.7692 |     -0.0154 |
|    2 | precision         |    0.7931 |    0.7966 |      0.0035 |
|    3 | precision         |    0.7885 |    0.8077 |      0.0192 |
|    4 | precision         |    0.7742 |    0.7705 |     -0.0037 |
|    5 | precision         |    0.7971 |    0.7879 |     -0.0092 |
|    1 | recall            |    0.7391 |    0.7246 |     -0.0145 |
|    2 | recall            |    0.6765 |    0.6912 |      0.0147 |
|    3 | recall            |    0.6029 |    0.6176 |      0.0147 |
|    4 | recall            |    0.7059 |    0.6912 |     -0.0147 |
|    5 | recall            |    0.7971 |    0.7536 |     -0.0435 |
|    1 | f1                |    0.7612 |    0.7463 |     -0.0149 |
|    2 | f1                |    0.7302 |    0.7402 |      0.0100 |
|    3 | f1                |    0.6833 |    0.7000 |      0.0167 |
|    4 | f1                |    0.7385 |    0.7287 |     -0.0098 |
|    5 | f1                |    0.7971 |    0.7704 |     -0.0267 |
|    1 | roc_auc           |    0.8879 |    0.8828 |     -0.0051 |
|    2 | roc_auc           |    0.8651 |    0.8668 |      0.0017 |
|    3 | roc_auc           |    0.8477 |    0.8564 |      0.0087 |
|    4 | roc_auc           |    0.8384 |    0.8374 |     -0.0011 |
|    5 | roc_auc           |    0.8720 |    0.8819 |      0.0100 |
|    1 | log_loss          |    0.4005 |    0.4133 |     -0.0128 |
|    2 | log_loss          |    0.4175 |    0.4128 |      0.0047 |
|    3 | log_loss          |    0.4551 |    0.4508 |      0.0043 |
|    4 | log_loss          |    0.4534 |    0.4567 |     -0.0033 |
|    5 | log_loss          |    0.4301 |    0.4194 |      0.0108 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           9 |                     12 |         2 |           3 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-006/4db24a585d74/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-006/4db24a585d74/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-006/4db24a585d74/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-006/4db24a585d74/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
