---
id: MLP-002
type: mlp-experiment
status: completed
decision: adopt
implementation_module: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng
---

# MLP-002 — Компактный MLP baseline — 8 скрытых нейронов

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Эксперимент      | MLP-002 — Компактный MLP baseline — 8 скрытых нейронов                                                                                     |
| Гипотеза         | Если начать с компактной сети из 8 скрытых нейронов на базовых признаках, то её ёмкости будет достаточно для Titanic без лишней сложности. |
| Одно изменение   | Новый компактный MLP baseline: один скрытый слой из 8 нейронов, без дополнительного feature engineering.                                   |
| Решение          | adopt |
| Reference        | sklearn_champion: ml_project.experiments.exp_013_tt_comb                                                                                   |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                        |
| Основная метрика | accuracy                                                                                                                                   |
| Критерии         | passed                                                                                                                                     |
| Код              | ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng                                                                                       |
| Hash кода        | c396a3da3ea7…                                                                                                                              |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0011 |              0.0000 |   True |
| guardrail | balanced_accuracy |               0.0084 |              0.0000 |   True |
| guardrail | recall            |               0.0405 |             -0.0100 |   True |
| guardrail | f1                |               0.0113 |              0.0000 |   True |

## Сравнение всех метрик

| model            | metric            |   mean |    std |    min |    max |
| ---------------- | ----------------- | -----: | -----: | -----: | -----: |
| sklearn_champion | accuracy          | 0.8126 | 0.0152 | 0.7865 | 0.8258 |
| sklearn_champion | balanced_accuracy | 0.7846 | 0.0184 | 0.7543 | 0.8029 |
| sklearn_champion | precision         | 0.8141 | 0.0281 | 0.7778 | 0.8462 |
| sklearn_champion | recall            | 0.6638 | 0.0365 | 0.6176 | 0.7059 |
| sklearn_champion | f1                | 0.7308 | 0.0257 | 0.6885 | 0.7559 |
| sklearn_champion | roc_auc           | 0.8703 | 0.0194 | 0.8522 | 0.8997 |
| sklearn_champion | log_loss          | 0.4171 | 0.0200 | 0.3915 | 0.4447 |
| mlp_candidate    | accuracy          | 0.8137 | 0.0205 | 0.7865 | 0.8427 |
| mlp_candidate    | balanced_accuracy | 0.7929 | 0.0304 | 0.7515 | 0.8343 |
| mlp_candidate    | precision         | 0.7875 | 0.0088 | 0.7742 | 0.7971 |
| mlp_candidate    | recall            | 0.7043 | 0.0722 | 0.6029 | 0.7971 |
| mlp_candidate    | f1                | 0.7420 | 0.0418 | 0.6833 | 0.7971 |
| mlp_candidate    | roc_auc           | 0.8622 | 0.0196 | 0.8384 | 0.8879 |
| mlp_candidate    | log_loss          | 0.4313 | 0.0234 | 0.4005 | 0.4551 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8156 |    0.8212 |      0.0056 |
|    2 | accuracy          |    0.8146 |    0.8090 |     -0.0056 |
|    3 | accuracy          |    0.7865 |    0.7865 |      0.0000 |
|    4 | accuracy          |    0.8258 |    0.8090 |     -0.0169 |
|    5 | accuracy          |    0.8202 |    0.8427 |      0.0225 |
|    1 | balanced_accuracy |    0.7825 |    0.8059 |      0.0235 |
|    2 | balanced_accuracy |    0.7910 |    0.7837 |     -0.0074 |
|    3 | balanced_accuracy |    0.7543 |    0.7515 |     -0.0028 |
|    4 | balanced_accuracy |    0.8029 |    0.7893 |     -0.0136 |
|    5 | balanced_accuracy |    0.7920 |    0.8343 |      0.0423 |
|    1 | precision         |    0.8462 |    0.7846 |     -0.0615 |
|    2 | precision         |    0.7966 |    0.7931 |     -0.0035 |
|    3 | precision         |    0.7778 |    0.7885 |      0.0107 |
|    4 | precision         |    0.8136 |    0.7742 |     -0.0394 |
|    5 | precision         |    0.8364 |    0.7971 |     -0.0393 |
|    1 | recall            |    0.6377 |    0.7391 |      0.1014 |
|    2 | recall            |    0.6912 |    0.6765 |     -0.0147 |
|    3 | recall            |    0.6176 |    0.6029 |     -0.0147 |
|    4 | recall            |    0.7059 |    0.7059 |      0.0000 |
|    5 | recall            |    0.6667 |    0.7971 |      0.1304 |
|    1 | f1                |    0.7273 |    0.7612 |      0.0339 |
|    2 | f1                |    0.7402 |    0.7302 |     -0.0100 |
|    3 | f1                |    0.6885 |    0.6833 |     -0.0052 |
|    4 | f1                |    0.7559 |    0.7385 |     -0.0174 |
|    5 | f1                |    0.7419 |    0.7971 |      0.0552 |
|    1 | roc_auc           |    0.8997 |    0.8879 |     -0.0117 |
|    2 | roc_auc           |    0.8786 |    0.8651 |     -0.0135 |
|    3 | roc_auc           |    0.8522 |    0.8477 |     -0.0045 |
|    4 | roc_auc           |    0.8551 |    0.8384 |     -0.0166 |
|    5 | roc_auc           |    0.8660 |    0.8720 |      0.0059 |
|    1 | log_loss          |    0.3915 |    0.4005 |     -0.0090 |
|    2 | log_loss          |    0.4077 |    0.4175 |     -0.0098 |
|    3 | log_loss          |    0.4447 |    0.4551 |     -0.0104 |
|    4 | log_loss          |    0.4149 |    0.4534 |     -0.0386 |
|    5 | log_loss          |    0.4268 |    0.4301 |     -0.0033 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          40 |                     39 |         2 |           2 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-002/c396a3da3ea7/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-002/c396a3da3ea7/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-002/c396a3da3ea7/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-002/c396a3da3ea7/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
