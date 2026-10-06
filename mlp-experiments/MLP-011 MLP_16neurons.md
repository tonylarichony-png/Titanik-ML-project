---
id: MLP-011
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_011_mlp_16neurons
---

# MLP-011 — MLP_16neurons

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                        |
| ---------------- | --------------------------------------------------------------- |
| Эксперимент      | MLP-011 — MLP_16neurons                                         |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                       |
| Одно изменение   | CHANGE ME — exactly one controlled change                       |
| Решение          | reject |
| Reference        | MLP-010_reference: ml_project.mlp_experiments.mlp_010_mlp_allin |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)             |
| Основная метрика | accuracy                                                        |
| Критерии         | failed                                                          |
| Код              | ml_project.mlp_experiments.mlp_011_mlp_16neurons                |
| Hash кода        | d8dcac0df0ac…                                                   |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0045 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0016 |              0.0000 |  False |
| guardrail | recall            |               0.0113 |             -0.0100 |   True |
| guardrail | f1                |              -0.0017 |              0.0000 |  False |

## Сравнение всех метрик

| model             | metric            |   mean |    std |    min |    max |
| ----------------- | ----------------- | -----: | -----: | -----: | -----: |
| MLP-010_reference | accuracy          | 0.8193 | 0.0138 | 0.8090 | 0.8427 |
| MLP-010_reference | balanced_accuracy | 0.7945 | 0.0175 | 0.7779 | 0.8222 |
| MLP-010_reference | precision         | 0.8139 | 0.0233 | 0.7778 | 0.8333 |
| MLP-010_reference | recall            | 0.6873 | 0.0405 | 0.6377 | 0.7353 |
| MLP-010_reference | f1                | 0.7445 | 0.0237 | 0.7213 | 0.7812 |
| MLP-010_reference | roc_auc           | 0.8762 | 0.0176 | 0.8590 | 0.9043 |
| MLP-010_reference | log_loss          | 0.4104 | 0.0210 | 0.3892 | 0.4423 |
| mlp_candidate     | accuracy          | 0.8148 | 0.0134 | 0.8034 | 0.8315 |
| mlp_candidate     | balanced_accuracy | 0.7929 | 0.0179 | 0.7707 | 0.8145 |
| mlp_candidate     | precision         | 0.7945 | 0.0214 | 0.7619 | 0.8113 |
| mlp_candidate     | recall            | 0.6986 | 0.0413 | 0.6324 | 0.7391 |
| mlp_candidate     | f1                | 0.7428 | 0.0251 | 0.7107 | 0.7727 |
| mlp_candidate     | roc_auc           | 0.8675 | 0.0192 | 0.8463 | 0.8882 |
| mlp_candidate     | log_loss          | 0.4276 | 0.0242 | 0.4013 | 0.4533 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8101 |    0.8268 |      0.0168 |
|    2 | accuracy          |    0.8146 |    0.8090 |     -0.0056 |
|    3 | accuracy          |    0.8090 |    0.8034 |     -0.0056 |
|    4 | accuracy          |    0.8427 |    0.8034 |     -0.0393 |
|    5 | accuracy          |    0.8202 |    0.8315 |      0.0112 |
|    1 | balanced_accuracy |    0.7779 |    0.8078 |      0.0298 |
|    2 | balanced_accuracy |    0.7967 |    0.7865 |     -0.0102 |
|    3 | balanced_accuracy |    0.7809 |    0.7707 |     -0.0102 |
|    4 | balanced_accuracy |    0.8222 |    0.7848 |     -0.0374 |
|    5 | balanced_accuracy |    0.7947 |    0.8145 |      0.0198 |
|    1 | precision         |    0.8302 |    0.8065 |     -0.0237 |
|    2 | precision         |    0.7778 |    0.7833 |      0.0056 |
|    3 | precision         |    0.8036 |    0.8113 |      0.0077 |
|    4 | precision         |    0.8333 |    0.7619 |     -0.0714 |
|    5 | precision         |    0.8246 |    0.8095 |     -0.0150 |
|    1 | recall            |    0.6377 |    0.7246 |      0.0870 |
|    2 | recall            |    0.7206 |    0.6912 |     -0.0294 |
|    3 | recall            |    0.6618 |    0.6324 |     -0.0294 |
|    4 | recall            |    0.7353 |    0.7059 |     -0.0294 |
|    5 | recall            |    0.6812 |    0.7391 |      0.0580 |
|    1 | f1                |    0.7213 |    0.7634 |      0.0420 |
|    2 | f1                |    0.7481 |    0.7344 |     -0.0137 |
|    3 | f1                |    0.7258 |    0.7107 |     -0.0151 |
|    4 | f1                |    0.7812 |    0.7328 |     -0.0484 |
|    5 | f1                |    0.7460 |    0.7727 |      0.0267 |
|    1 | roc_auc           |    0.9043 |    0.8882 |     -0.0161 |
|    2 | roc_auc           |    0.8811 |    0.8725 |     -0.0087 |
|    3 | roc_auc           |    0.8590 |    0.8485 |     -0.0106 |
|    4 | roc_auc           |    0.8687 |    0.8463 |     -0.0224 |
|    5 | roc_auc           |    0.8676 |    0.8818 |      0.0142 |
|    1 | log_loss          |    0.3892 |    0.4013 |     -0.0122 |
|    2 | log_loss          |    0.3985 |    0.4120 |     -0.0134 |
|    3 | log_loss          |    0.4423 |    0.4533 |     -0.0110 |
|    4 | log_loss          |    0.4022 |    0.4532 |     -0.0510 |
|    5 | log_loss          |    0.4197 |    0.4182 |      0.0014 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          34 |                     38 |         2 |           3 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-011/d8dcac0df0ac/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-011/d8dcac0df0ac/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-011/d8dcac0df0ac/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-011/d8dcac0df0ac/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
