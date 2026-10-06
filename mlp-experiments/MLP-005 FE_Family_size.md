---
id: MLP-005
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_005_fe_family_size
---

# MLP-005 — FE_Family_size

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                |
| ---------------- | ----------------------------------------------------------------------- |
| Эксперимент      | MLP-005 — FE_Family_size                                                |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                               |
| Одно изменение   | CHANGE ME — exactly one controlled change                               |
| Решение          | reject |
| Reference        | MLP-002_reference: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                     |
| Основная метрика | accuracy                                                                |
| Критерии         | failed                                                                  |
| Код              | ml_project.mlp_experiments.mlp_005_fe_family_size                       |
| Hash кода        | bdb3d5556fb5…                                                           |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0034 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0043 |              0.0000 |  False |
| guardrail | recall            |              -0.0086 |             -0.0100 |   True |
| guardrail | f1                |              -0.0049 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8103 | 0.0172 | 0.7865 | 0.8315 |
| mlp_candidate     | balanced_accuracy | 0.7887 | 0.0231 | 0.7543 | 0.8172 |
| mlp_candidate     | precision         | 0.7855 | 0.0205 | 0.7656 | 0.8136 |
| mlp_candidate     | recall            | 0.6957 | 0.0502 | 0.6176 | 0.7536 |
| mlp_candidate     | f1                | 0.7372 | 0.0322 | 0.6885 | 0.7761 |
| mlp_candidate     | roc_auc           | 0.8662 | 0.0222 | 0.8426 | 0.8898 |
| mlp_candidate     | log_loss          | 0.4258 | 0.0232 | 0.3998 | 0.4584 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8212 |    0.8212 |      0.0000 |
|    2 | accuracy          |    0.8090 |    0.8090 |      0.0000 |
|    3 | accuracy          |    0.7865 |    0.7865 |      0.0000 |
|    4 | accuracy          |    0.8090 |    0.8034 |     -0.0056 |
|    5 | accuracy          |    0.8427 |    0.8315 |     -0.0112 |
|    1 | balanced_accuracy |    0.8059 |    0.7978 |     -0.0081 |
|    2 | balanced_accuracy |    0.7837 |    0.7921 |      0.0084 |
|    3 | balanced_accuracy |    0.7515 |    0.7543 |      0.0028 |
|    4 | balanced_accuracy |    0.7893 |    0.7820 |     -0.0074 |
|    5 | balanced_accuracy |    0.8343 |    0.8172 |     -0.0172 |
|    1 | precision         |    0.7846 |    0.8136 |      0.0289 |
|    2 | precision         |    0.7931 |    0.7656 |     -0.0275 |
|    3 | precision         |    0.7885 |    0.7778 |     -0.0107 |
|    4 | precision         |    0.7742 |    0.7705 |     -0.0037 |
|    5 | precision         |    0.7971 |    0.8000 |      0.0029 |
|    1 | recall            |    0.7391 |    0.6957 |     -0.0435 |
|    2 | recall            |    0.6765 |    0.7206 |      0.0441 |
|    3 | recall            |    0.6029 |    0.6176 |      0.0147 |
|    4 | recall            |    0.7059 |    0.6912 |     -0.0147 |
|    5 | recall            |    0.7971 |    0.7536 |     -0.0435 |
|    1 | f1                |    0.7612 |    0.7500 |     -0.0112 |
|    2 | f1                |    0.7302 |    0.7424 |      0.0123 |
|    3 | f1                |    0.6833 |    0.6885 |      0.0052 |
|    4 | f1                |    0.7385 |    0.7287 |     -0.0098 |
|    5 | f1                |    0.7971 |    0.7761 |     -0.0210 |
|    1 | roc_auc           |    0.8879 |    0.8898 |      0.0018 |
|    2 | roc_auc           |    0.8651 |    0.8667 |      0.0016 |
|    3 | roc_auc           |    0.8477 |    0.8426 |     -0.0051 |
|    4 | roc_auc           |    0.8384 |    0.8454 |      0.0070 |
|    5 | roc_auc           |    0.8720 |    0.8866 |      0.0146 |
|    1 | log_loss          |    0.4005 |    0.3998 |      0.0007 |
|    2 | log_loss          |    0.4175 |    0.4158 |      0.0017 |
|    3 | log_loss          |    0.4551 |    0.4584 |     -0.0032 |
|    4 | log_loss          |    0.4534 |    0.4400 |      0.0134 |
|    5 | log_loss          |    0.4301 |    0.4149 |      0.0152 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           9 |                     12 |         0 |           2 |    3 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-005/bdb3d5556fb5/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-005/bdb3d5556fb5/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-005/bdb3d5556fb5/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-005/bdb3d5556fb5/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
