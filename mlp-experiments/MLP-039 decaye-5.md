---
id: MLP-039
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_039_decaye_5
---

# MLP-039 — decaye-5

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-039 — decaye-5                                                |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_039_decaye_5                       |
| Hash кода        | 992af5a8f805…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0123 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0132 |              0.0000 |  False |
| guardrail | recall            |              -0.0174 |             -0.0100 |  False |
| guardrail | f1                |              -0.0176 |              0.0000 |  False |

## Сравнение всех метрик

| model             | metric            |   mean |    std |    min |    max |
| ----------------- | ----------------- | -----: | -----: | -----: | -----: |
| MLP-024_reference | accuracy          | 0.8384 | 0.0111 | 0.8258 | 0.8547 |
| MLP-024_reference | balanced_accuracy | 0.8176 | 0.0111 | 0.8019 | 0.8278 |
| MLP-024_reference | precision         | 0.8324 | 0.0394 | 0.7969 | 0.8909 |
| MLP-024_reference | recall            | 0.7281 | 0.0351 | 0.6765 | 0.7647 |
| MLP-024_reference | f1                | 0.7756 | 0.0148 | 0.7541 | 0.7903 |
| MLP-024_reference | roc_auc           | 0.8780 | 0.0215 | 0.8592 | 0.9140 |
| MLP-024_reference | log_loss          | 0.4058 | 0.0244 | 0.3786 | 0.4403 |
| mlp_candidate     | accuracy          | 0.8260 | 0.0219 | 0.7978 | 0.8483 |
| mlp_candidate     | balanced_accuracy | 0.8043 | 0.0245 | 0.7746 | 0.8324 |
| mlp_candidate     | precision         | 0.8137 | 0.0392 | 0.7667 | 0.8727 |
| mlp_candidate     | recall            | 0.7107 | 0.0442 | 0.6667 | 0.7647 |
| mlp_candidate     | f1                | 0.7579 | 0.0319 | 0.7188 | 0.7939 |
| mlp_candidate     | roc_auc           | 0.8797 | 0.0216 | 0.8574 | 0.9134 |
| mlp_candidate     | log_loss          | 0.4088 | 0.0281 | 0.3793 | 0.4519 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8436 |     -0.0112 |
|    2 | accuracy          |    0.8371 |    0.8315 |     -0.0056 |
|    3 | accuracy          |    0.8315 |    0.7978 |     -0.0337 |
|    4 | accuracy          |    0.8427 |    0.8483 |      0.0056 |
|    5 | accuracy          |    0.8258 |    0.8090 |     -0.0169 |
|    1 | balanced_accuracy |    0.8278 |    0.8160 |     -0.0118 |
|    2 | balanced_accuracy |    0.8233 |    0.8159 |     -0.0074 |
|    3 | balanced_accuracy |    0.8019 |    0.7746 |     -0.0273 |
|    4 | balanced_accuracy |    0.8250 |    0.8324 |      0.0074 |
|    5 | balanced_accuracy |    0.8099 |    0.7829 |     -0.0271 |
|    1 | precision         |    0.8909 |    0.8727 |     -0.0182 |
|    2 | precision         |    0.8000 |    0.7969 |     -0.0031 |
|    3 | precision         |    0.8519 |    0.7667 |     -0.0852 |
|    4 | precision         |    0.8226 |    0.8254 |      0.0028 |
|    5 | precision         |    0.7969 |    0.8070 |      0.0101 |
|    1 | recall            |    0.7101 |    0.6957 |     -0.0145 |
|    2 | recall            |    0.7647 |    0.7500 |     -0.0147 |
|    3 | recall            |    0.6765 |    0.6765 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7647 |      0.0147 |
|    5 | recall            |    0.7391 |    0.6667 |     -0.0725 |
|    1 | f1                |    0.7903 |    0.7742 |     -0.0161 |
|    2 | f1                |    0.7820 |    0.7727 |     -0.0092 |
|    3 | f1                |    0.7541 |    0.7188 |     -0.0353 |
|    4 | f1                |    0.7846 |    0.7939 |      0.0093 |
|    5 | f1                |    0.7669 |    0.7302 |     -0.0368 |
|    1 | roc_auc           |    0.9140 |    0.9134 |     -0.0007 |
|    2 | roc_auc           |    0.8779 |    0.8834 |      0.0055 |
|    3 | roc_auc           |    0.8592 |    0.8574 |     -0.0017 |
|    4 | roc_auc           |    0.8747 |    0.8795 |      0.0048 |
|    5 | roc_auc           |    0.8643 |    0.8650 |      0.0007 |
|    1 | log_loss          |    0.3786 |    0.3793 |     -0.0006 |
|    2 | log_loss          |    0.4027 |    0.3967 |      0.0060 |
|    3 | log_loss          |    0.4403 |    0.4519 |     -0.0116 |
|    4 | log_loss          |    0.3891 |    0.3959 |     -0.0068 |
|    5 | log_loss          |    0.4184 |    0.4200 |     -0.0016 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           5 |                     16 |         1 |           4 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-039/992af5a8f805/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-039/992af5a8f805/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-039/992af5a8f805/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-039/992af5a8f805/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
