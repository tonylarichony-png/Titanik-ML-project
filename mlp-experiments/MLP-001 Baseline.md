---
id: MLP-001
type: mlp-experiment
status: completed
decision: pending
implementation_module: ml_project.mlp_experiments.mlp_001_baseline
---

# MLP-001 — First reproducible MLP baseline

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-001 — First reproducible MLP baseline                                                                                               |
| Гипотеза         | Если обучить небольшой MLP на базовых Titanic-признаках, то получим воспроизводимую нейросетевую точку отсчёта для следующих изменений. |
| Одно изменение   | Первый PyTorch baseline: 7 исходных признаков, один скрытый слой из 32 нейронов и fold-safe preprocessing.                              |
| Решение          | pending |
| Reference        | sklearn_champion: ml_project.experiments.exp_013_tt_comb                                                                                |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                     |
| Основная метрика | accuracy                                                                                                                                |
| Критерии         | passed                                                                                                                                  |
| Код              | ml_project.mlp_experiments.mlp_001_baseline                                                                                             |
| Hash кода        | e002d84b9512…                                                                                                                           |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0022 |              0.0000 |   True |
| guardrail | balanced_accuracy |               0.0083 |              0.0000 |   True |
| guardrail | recall            |               0.0348 |             -0.0100 |   True |
| guardrail | f1                |               0.0120 |              0.0000 |   True |

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
| mlp_candidate    | accuracy          | 0.8148 | 0.0134 | 0.8034 | 0.8315 |
| mlp_candidate    | balanced_accuracy | 0.7929 | 0.0179 | 0.7707 | 0.8145 |
| mlp_candidate    | precision         | 0.7945 | 0.0214 | 0.7619 | 0.8113 |
| mlp_candidate    | recall            | 0.6986 | 0.0413 | 0.6324 | 0.7391 |
| mlp_candidate    | f1                | 0.7428 | 0.0251 | 0.7107 | 0.7727 |
| mlp_candidate    | roc_auc           | 0.8675 | 0.0192 | 0.8463 | 0.8882 |
| mlp_candidate    | log_loss          | 0.4276 | 0.0242 | 0.4013 | 0.4533 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8156 |    0.8268 |      0.0112 |
|    2 | accuracy          |    0.8146 |    0.8090 |     -0.0056 |
|    3 | accuracy          |    0.7865 |    0.8034 |      0.0169 |
|    4 | accuracy          |    0.8258 |    0.8034 |     -0.0225 |
|    5 | accuracy          |    0.8202 |    0.8315 |      0.0112 |
|    1 | balanced_accuracy |    0.7825 |    0.8078 |      0.0253 |
|    2 | balanced_accuracy |    0.7910 |    0.7865 |     -0.0045 |
|    3 | balanced_accuracy |    0.7543 |    0.7707 |      0.0164 |
|    4 | balanced_accuracy |    0.8029 |    0.7848 |     -0.0182 |
|    5 | balanced_accuracy |    0.7920 |    0.8145 |      0.0225 |
|    1 | precision         |    0.8462 |    0.8065 |     -0.0397 |
|    2 | precision         |    0.7966 |    0.7833 |     -0.0133 |
|    3 | precision         |    0.7778 |    0.8113 |      0.0335 |
|    4 | precision         |    0.8136 |    0.7619 |     -0.0517 |
|    5 | precision         |    0.8364 |    0.8095 |     -0.0268 |
|    1 | recall            |    0.6377 |    0.7246 |      0.0870 |
|    2 | recall            |    0.6912 |    0.6912 |      0.0000 |
|    3 | recall            |    0.6176 |    0.6324 |      0.0147 |
|    4 | recall            |    0.7059 |    0.7059 |      0.0000 |
|    5 | recall            |    0.6667 |    0.7391 |      0.0725 |
|    1 | f1                |    0.7273 |    0.7634 |      0.0361 |
|    2 | f1                |    0.7402 |    0.7344 |     -0.0058 |
|    3 | f1                |    0.6885 |    0.7107 |      0.0222 |
|    4 | f1                |    0.7559 |    0.7328 |     -0.0231 |
|    5 | f1                |    0.7419 |    0.7727 |      0.0308 |
|    1 | roc_auc           |    0.8997 |    0.8882 |     -0.0115 |
|    2 | roc_auc           |    0.8786 |    0.8725 |     -0.0061 |
|    3 | roc_auc           |    0.8522 |    0.8485 |     -0.0037 |
|    4 | roc_auc           |    0.8551 |    0.8463 |     -0.0088 |
|    5 | roc_auc           |    0.8660 |    0.8818 |      0.0158 |
|    1 | log_loss          |    0.3915 |    0.4013 |     -0.0098 |
|    2 | log_loss          |    0.4077 |    0.4120 |     -0.0043 |
|    3 | log_loss          |    0.4447 |    0.4533 |     -0.0086 |
|    4 | log_loss          |    0.4149 |    0.4532 |     -0.0383 |
|    5 | log_loss          |    0.4268 |    0.4182 |      0.0086 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          39 |                     37 |         3 |           2 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-001/e002d84b9512/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-001/e002d84b9512/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-001/e002d84b9512/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-001/e002d84b9512/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
