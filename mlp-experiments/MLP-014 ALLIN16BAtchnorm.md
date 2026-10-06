---
id: MLP-014
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_014_allin16batchnorm
---

# MLP-014 — ALLIN16BAtchnorm

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-014 — ALLIN16BAtchnorm                                                                                                             |
| Гипотеза         | CHANGE ME — if добавлю батчнорм, then он поможет сети лучше обрабатывать данные, потому что между батчами будут нормализованы признаки |
| Одно изменение   | Добавил только BatchNorm после первого слоя, чтобы проверить, улучшит ли это обучение                                                  |
| Решение          | reject |
| Reference        | MLP-012_reference: ml_project.mlp_experiments.mlp_012_allin_16neurons                                                                  |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                    |
| Основная метрика | accuracy                                                                                                                               |
| Критерии         | failed                                                                                                                                 |
| Код              | ml_project.mlp_experiments.mlp_014_allin16batchnorm                                                                                    |
| Hash кода        | 84ab26ddae61…                                                                                                                          |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0090 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0128 |              0.0000 |  False |
| guardrail | recall            |              -0.0292 |             -0.0100 |  False |
| guardrail | f1                |              -0.0177 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8170 | 0.0143 | 0.8034 | 0.8371 |
| mlp_candidate     | balanced_accuracy | 0.7894 | 0.0153 | 0.7703 | 0.8120 |
| mlp_candidate     | precision         | 0.8222 | 0.0341 | 0.7833 | 0.8654 |
| mlp_candidate     | recall            | 0.6698 | 0.0327 | 0.6232 | 0.7059 |
| mlp_candidate     | f1                | 0.7374 | 0.0209 | 0.7107 | 0.7680 |
| mlp_candidate     | roc_auc           | 0.8706 | 0.0204 | 0.8470 | 0.9015 |
| mlp_candidate     | log_loss          | 0.4171 | 0.0286 | 0.3928 | 0.4646 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8268 |    0.8268 |      0.0000 |
|    2 | accuracy          |    0.8258 |    0.8090 |     -0.0169 |
|    3 | accuracy          |    0.8090 |    0.8090 |      0.0000 |
|    4 | accuracy          |    0.8427 |    0.8371 |     -0.0056 |
|    5 | accuracy          |    0.8258 |    0.8034 |     -0.0225 |
|    1 | balanced_accuracy |    0.7997 |    0.7943 |     -0.0054 |
|    2 | balanced_accuracy |    0.8029 |    0.7837 |     -0.0193 |
|    3 | balanced_accuracy |    0.7865 |    0.7865 |      0.0000 |
|    4 | balanced_accuracy |    0.8222 |    0.8120 |     -0.0102 |
|    5 | balanced_accuracy |    0.7993 |    0.7703 |     -0.0290 |
|    1 | precision         |    0.8393 |    0.8654 |      0.0261 |
|    2 | precision         |    0.8136 |    0.7931 |     -0.0205 |
|    3 | precision         |    0.7833 |    0.7833 |      0.0000 |
|    4 | precision         |    0.8333 |    0.8421 |      0.0088 |
|    5 | precision         |    0.8393 |    0.8269 |     -0.0124 |
|    1 | recall            |    0.6812 |    0.6522 |     -0.0290 |
|    2 | recall            |    0.7059 |    0.6765 |     -0.0294 |
|    3 | recall            |    0.6912 |    0.6912 |      0.0000 |
|    4 | recall            |    0.7353 |    0.7059 |     -0.0294 |
|    5 | recall            |    0.6812 |    0.6232 |     -0.0580 |
|    1 | f1                |    0.7520 |    0.7438 |     -0.0082 |
|    2 | f1                |    0.7559 |    0.7302 |     -0.0257 |
|    3 | f1                |    0.7344 |    0.7344 |      0.0000 |
|    4 | f1                |    0.7812 |    0.7680 |     -0.0132 |
|    5 | f1                |    0.7520 |    0.7107 |     -0.0413 |
|    1 | roc_auc           |    0.9093 |    0.9015 |     -0.0078 |
|    2 | roc_auc           |    0.8735 |    0.8773 |      0.0037 |
|    3 | roc_auc           |    0.8604 |    0.8470 |     -0.0134 |
|    4 | roc_auc           |    0.8717 |    0.8638 |     -0.0079 |
|    5 | roc_auc           |    0.8698 |    0.8632 |     -0.0065 |
|    1 | log_loss          |    0.3826 |    0.3928 |     -0.0102 |
|    2 | log_loss          |    0.4125 |    0.4071 |      0.0054 |
|    3 | log_loss          |    0.4412 |    0.4646 |     -0.0234 |
|    4 | log_loss          |    0.3971 |    0.3993 |     -0.0021 |
|    5 | log_loss          |    0.4226 |    0.4219 |      0.0007 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          16 |                     24 |         0 |           3 |    2 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-014/84ab26ddae61/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-014/84ab26ddae61/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-014/84ab26ddae61/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-014/84ab26ddae61/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
