---
id: MLP-010
type: mlp-experiment
status: completed
decision: adopt
implementation_module: ml_project.mlp_experiments.mlp_010_mlp_allin
---

# MLP-010 — MLP All In — все созданные признаки

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-010 — MLP All In — все созданные признаки                                                                                                                                                   |
| Гипотеза         | Если одновременно передать компактной MLP все содержательные признаки из логистической цепочки, то сеть сможет использовать их взаимодействия лучше, чем базовый MLP-002 на исходных признаках. |
| Одно изменение   | All-in bundle: Age по Title × Pclass, FamilySizeGroup, TicketGroupSize, log1p(FarePerPerson), IsnotAlone, CabinKnown, Deck и SexPclass; архитектура MLP-002 из 8 скрытых нейронов не меняется.  |
| Решение          | adopt |
| Reference        | MLP-002_reference: ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng                                                                                                                         |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                             |
| Основная метрика | accuracy                                                                                                                                                                                        |
| Критерии         | failed                                                                                                                                                                                          |
| Код              | ml_project.mlp_experiments.mlp_010_mlp_allin                                                                                                                                                    |
| Hash кода        | a7c3f6e2d627…                                                                                                                                                                                   |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0056 |              0.0000 |   True |
| guardrail | balanced_accuracy |               0.0015 |              0.0000 |   True |
| guardrail | recall            |              -0.0170 |             -0.0100 |  False |
| guardrail | f1                |               0.0024 |              0.0000 |   True |

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
| mlp_candidate     | accuracy          | 0.8193 | 0.0138 | 0.8090 | 0.8427 |
| mlp_candidate     | balanced_accuracy | 0.7945 | 0.0175 | 0.7779 | 0.8222 |
| mlp_candidate     | precision         | 0.8139 | 0.0233 | 0.7778 | 0.8333 |
| mlp_candidate     | recall            | 0.6873 | 0.0405 | 0.6377 | 0.7353 |
| mlp_candidate     | f1                | 0.7445 | 0.0237 | 0.7213 | 0.7812 |
| mlp_candidate     | roc_auc           | 0.8762 | 0.0176 | 0.8590 | 0.9043 |
| mlp_candidate     | log_loss          | 0.4104 | 0.0210 | 0.3892 | 0.4423 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8212 |    0.8101 |     -0.0112 |
|    2 | accuracy          |    0.8090 |    0.8146 |      0.0056 |
|    3 | accuracy          |    0.7865 |    0.8090 |      0.0225 |
|    4 | accuracy          |    0.8090 |    0.8427 |      0.0337 |
|    5 | accuracy          |    0.8427 |    0.8202 |     -0.0225 |
|    1 | balanced_accuracy |    0.8059 |    0.7779 |     -0.0280 |
|    2 | balanced_accuracy |    0.7837 |    0.7967 |      0.0130 |
|    3 | balanced_accuracy |    0.7515 |    0.7809 |      0.0294 |
|    4 | balanced_accuracy |    0.7893 |    0.8222 |      0.0329 |
|    5 | balanced_accuracy |    0.8343 |    0.7947 |     -0.0396 |
|    1 | precision         |    0.7846 |    0.8302 |      0.0456 |
|    2 | precision         |    0.7931 |    0.7778 |     -0.0153 |
|    3 | precision         |    0.7885 |    0.8036 |      0.0151 |
|    4 | precision         |    0.7742 |    0.8333 |      0.0591 |
|    5 | precision         |    0.7971 |    0.8246 |      0.0275 |
|    1 | recall            |    0.7391 |    0.6377 |     -0.1014 |
|    2 | recall            |    0.6765 |    0.7206 |      0.0441 |
|    3 | recall            |    0.6029 |    0.6618 |      0.0588 |
|    4 | recall            |    0.7059 |    0.7353 |      0.0294 |
|    5 | recall            |    0.7971 |    0.6812 |     -0.1159 |
|    1 | f1                |    0.7612 |    0.7213 |     -0.0399 |
|    2 | f1                |    0.7302 |    0.7481 |      0.0179 |
|    3 | f1                |    0.6833 |    0.7258 |      0.0425 |
|    4 | f1                |    0.7385 |    0.7812 |      0.0428 |
|    5 | f1                |    0.7971 |    0.7460 |     -0.0511 |
|    1 | roc_auc           |    0.8879 |    0.9043 |      0.0163 |
|    2 | roc_auc           |    0.8651 |    0.8811 |      0.0160 |
|    3 | roc_auc           |    0.8477 |    0.8590 |      0.0114 |
|    4 | roc_auc           |    0.8384 |    0.8687 |      0.0303 |
|    5 | roc_auc           |    0.8720 |    0.8676 |     -0.0043 |
|    1 | log_loss          |    0.4005 |    0.3892 |      0.0114 |
|    2 | log_loss          |    0.4175 |    0.3985 |      0.0190 |
|    3 | log_loss          |    0.4551 |    0.4423 |      0.0128 |
|    4 | log_loss          |    0.4534 |    0.4022 |      0.0512 |
|    5 | log_loss          |    0.4301 |    0.4197 |      0.0104 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          39 |                     34 |         3 |           2 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-010/a7c3f6e2d627/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-010/a7c3f6e2d627/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-010/a7c3f6e2d627/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-010/a7c3f6e2d627/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
