---
id: MLP-026
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_026_dpoutlight_1layer
---

# MLP-026 — Dpoutlight 1layer

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-026 — Dpoutlight 1layer                                       |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_026_dpoutlight_1layer              |
| Hash кода        | bf7e45016f23…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0146 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0179 |              0.0000 |  False |
| guardrail | recall            |              -0.0322 |             -0.0100 |  False |
| guardrail | f1                |              -0.0233 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8238 | 0.0170 | 0.8090 | 0.8492 |
| mlp_candidate     | balanced_accuracy | 0.7997 | 0.0140 | 0.7882 | 0.8206 |
| mlp_candidate     | precision         | 0.8198 | 0.0447 | 0.7742 | 0.8889 |
| mlp_candidate     | recall            | 0.6959 | 0.0120 | 0.6765 | 0.7059 |
| mlp_candidate     | f1                | 0.7523 | 0.0186 | 0.7385 | 0.7805 |
| mlp_candidate     | roc_auc           | 0.8777 | 0.0211 | 0.8565 | 0.9123 |
| mlp_candidate     | log_loss          | 0.4079 | 0.0235 | 0.3851 | 0.4452 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8492 |     -0.0056 |
|    2 | accuracy          |    0.8371 |    0.8315 |     -0.0056 |
|    3 | accuracy          |    0.8315 |    0.8202 |     -0.0112 |
|    4 | accuracy          |    0.8427 |    0.8090 |     -0.0337 |
|    5 | accuracy          |    0.8258 |    0.8090 |     -0.0169 |
|    1 | balanced_accuracy |    0.8278 |    0.8206 |     -0.0072 |
|    2 | balanced_accuracy |    0.8233 |    0.8075 |     -0.0158 |
|    3 | balanced_accuracy |    0.8019 |    0.7928 |     -0.0091 |
|    4 | balanced_accuracy |    0.8250 |    0.7893 |     -0.0357 |
|    5 | balanced_accuracy |    0.8099 |    0.7882 |     -0.0217 |
|    1 | precision         |    0.8909 |    0.8889 |     -0.0020 |
|    2 | precision         |    0.8000 |    0.8276 |      0.0276 |
|    3 | precision         |    0.8519 |    0.8214 |     -0.0304 |
|    4 | precision         |    0.8226 |    0.7742 |     -0.0484 |
|    5 | precision         |    0.7969 |    0.7869 |     -0.0100 |
|    1 | recall            |    0.7101 |    0.6957 |     -0.0145 |
|    2 | recall            |    0.7647 |    0.7059 |     -0.0588 |
|    3 | recall            |    0.6765 |    0.6765 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7059 |     -0.0441 |
|    5 | recall            |    0.7391 |    0.6957 |     -0.0435 |
|    1 | f1                |    0.7903 |    0.7805 |     -0.0098 |
|    2 | f1                |    0.7820 |    0.7619 |     -0.0201 |
|    3 | f1                |    0.7541 |    0.7419 |     -0.0122 |
|    4 | f1                |    0.7846 |    0.7385 |     -0.0462 |
|    5 | f1                |    0.7669 |    0.7385 |     -0.0285 |
|    1 | roc_auc           |    0.9140 |    0.9123 |     -0.0017 |
|    2 | roc_auc           |    0.8779 |    0.8790 |      0.0011 |
|    3 | roc_auc           |    0.8592 |    0.8565 |     -0.0027 |
|    4 | roc_auc           |    0.8747 |    0.8735 |     -0.0012 |
|    5 | roc_auc           |    0.8643 |    0.8672 |      0.0029 |
|    1 | log_loss          |    0.3786 |    0.3851 |     -0.0065 |
|    2 | log_loss          |    0.4027 |    0.3948 |      0.0079 |
|    3 | log_loss          |    0.4403 |    0.4452 |     -0.0049 |
|    4 | log_loss          |    0.3891 |    0.3991 |     -0.0100 |
|    5 | log_loss          |    0.4184 |    0.4155 |      0.0029 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           4 |                     17 |         0 |           5 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-026/bf7e45016f23/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-026/bf7e45016f23/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-026/bf7e45016f23/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-026/bf7e45016f23/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
