---
id: MLP-013
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_013_allin32_neurons
---

# MLP-013 — ALLIN32_neurons

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                                                    |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-013 — ALLIN32_neurons                                                                                                                                                   |
| Гипотеза         | Если увеличить скрытый слой принятого all-in MLP с 16 до 32 нейронов, то дополнительная ёмкость поможет сети использовать взаимодействия между всеми созданными признаками. |
| Одно изменение   | Относительно MLP-012 изменяется только hidden_dim: 16 → 32;                                                                                                                 |
| Решение          | reject |
| Reference        | MLP-012_reference: ml_project.mlp_experiments.mlp_012_allin_16neurons                                                                                                       |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                         |
| Основная метрика | accuracy                                                                                                                                                                    |
| Критерии         | failed                                                                                                                                                                      |
| Код              | ml_project.mlp_experiments.mlp_013_allin32_neurons                                                                                                                          |
| Hash кода        | a3d62cdb6885…                                                                                                                                                               |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0067 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0071 |              0.0000 |  False |
| guardrail | recall            |              -0.0088 |             -0.0100 |   True |
| guardrail | f1                |              -0.0095 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8193 | 0.0184 | 0.7921 | 0.8427 |
| mlp_candidate     | balanced_accuracy | 0.7950 | 0.0191 | 0.7701 | 0.8222 |
| mlp_candidate     | precision         | 0.8121 | 0.0376 | 0.7541 | 0.8491 |
| mlp_candidate     | recall            | 0.6902 | 0.0304 | 0.6522 | 0.7353 |
| mlp_candidate     | f1                | 0.7456 | 0.0251 | 0.7132 | 0.7812 |
| mlp_candidate     | roc_auc           | 0.8797 | 0.0164 | 0.8646 | 0.9076 |
| mlp_candidate     | log_loss          | 0.4053 | 0.0194 | 0.3847 | 0.4310 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8268 |    0.8212 |     -0.0056 |
|    2 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    3 | accuracy          |    0.8090 |    0.7921 |     -0.0169 |
|    4 | accuracy          |    0.8427 |    0.8427 |      0.0000 |
|    5 | accuracy          |    0.8258 |    0.8258 |      0.0000 |
|    1 | balanced_accuracy |    0.7997 |    0.7897 |     -0.0099 |
|    2 | balanced_accuracy |    0.8029 |    0.7910 |     -0.0119 |
|    3 | balanced_accuracy |    0.7865 |    0.7701 |     -0.0164 |
|    4 | balanced_accuracy |    0.8222 |    0.8222 |      0.0000 |
|    5 | balanced_accuracy |    0.7993 |    0.8020 |      0.0027 |
|    1 | precision         |    0.8393 |    0.8491 |      0.0098 |
|    2 | precision         |    0.8136 |    0.7966 |     -0.0169 |
|    3 | precision         |    0.7833 |    0.7541 |     -0.0292 |
|    4 | precision         |    0.8333 |    0.8333 |      0.0000 |
|    5 | precision         |    0.8393 |    0.8276 |     -0.0117 |
|    1 | recall            |    0.6812 |    0.6522 |     -0.0290 |
|    2 | recall            |    0.7059 |    0.6912 |     -0.0147 |
|    3 | recall            |    0.6912 |    0.6765 |     -0.0147 |
|    4 | recall            |    0.7353 |    0.7353 |      0.0000 |
|    5 | recall            |    0.6812 |    0.6957 |      0.0145 |
|    1 | f1                |    0.7520 |    0.7377 |     -0.0143 |
|    2 | f1                |    0.7559 |    0.7402 |     -0.0157 |
|    3 | f1                |    0.7344 |    0.7132 |     -0.0212 |
|    4 | f1                |    0.7812 |    0.7812 |      0.0000 |
|    5 | f1                |    0.7520 |    0.7559 |      0.0039 |
|    1 | roc_auc           |    0.9093 |    0.9076 |     -0.0017 |
|    2 | roc_auc           |    0.8735 |    0.8775 |      0.0040 |
|    3 | roc_auc           |    0.8604 |    0.8646 |      0.0043 |
|    4 | roc_auc           |    0.8717 |    0.8762 |      0.0045 |
|    5 | roc_auc           |    0.8698 |    0.8726 |      0.0028 |
|    1 | log_loss          |    0.3826 |    0.3847 |     -0.0021 |
|    2 | log_loss          |    0.4125 |    0.4047 |      0.0078 |
|    3 | log_loss          |    0.4412 |    0.4310 |      0.0102 |
|    4 | log_loss          |    0.3971 |    0.3888 |      0.0084 |
|    5 | log_loss          |    0.4226 |    0.4175 |      0.0050 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           4 |                     10 |         0 |           3 |    2 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-013/a3d62cdb6885/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-013/a3d62cdb6885/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-013/a3d62cdb6885/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-013/a3d62cdb6885/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
