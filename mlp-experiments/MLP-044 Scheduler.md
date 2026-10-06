---
id: MLP-044
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_044_scheduler
---

# MLP-044 — Scheduler

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-044 — Scheduler                                               |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_044_scheduler                      |
| Hash кода        | 3ec42e5a2874…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0067 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0071 |              0.0000 |  False |
| guardrail | recall            |              -0.0087 |             -0.0100 |   True |
| guardrail | f1                |              -0.0093 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8316 | 0.0157 | 0.8146 | 0.8547 |
| mlp_candidate     | balanced_accuracy | 0.8105 | 0.0154 | 0.7928 | 0.8251 |
| mlp_candidate     | precision         | 0.8229 | 0.0477 | 0.7903 | 0.9057 |
| mlp_candidate     | recall            | 0.7194 | 0.0370 | 0.6765 | 0.7647 |
| mlp_candidate     | f1                | 0.7663 | 0.0202 | 0.7419 | 0.7869 |
| mlp_candidate     | roc_auc           | 0.8781 | 0.0210 | 0.8596 | 0.9128 |
| mlp_candidate     | log_loss          | 0.4069 | 0.0231 | 0.3800 | 0.4405 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8547 |      0.0000 |
|    2 | accuracy          |    0.8371 |    0.8371 |      0.0000 |
|    3 | accuracy          |    0.8315 |    0.8202 |     -0.0112 |
|    4 | accuracy          |    0.8427 |    0.8315 |     -0.0112 |
|    5 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    1 | balanced_accuracy |    0.8278 |    0.8251 |     -0.0027 |
|    2 | balanced_accuracy |    0.8233 |    0.8233 |      0.0000 |
|    3 | balanced_accuracy |    0.8019 |    0.7928 |     -0.0091 |
|    4 | balanced_accuracy |    0.8250 |    0.8159 |     -0.0091 |
|    5 | balanced_accuracy |    0.8099 |    0.7954 |     -0.0145 |
|    1 | precision         |    0.8909 |    0.9057 |      0.0148 |
|    2 | precision         |    0.8000 |    0.8000 |      0.0000 |
|    3 | precision         |    0.8519 |    0.8214 |     -0.0304 |
|    4 | precision         |    0.8226 |    0.7969 |     -0.0257 |
|    5 | precision         |    0.7969 |    0.7903 |     -0.0066 |
|    1 | recall            |    0.7101 |    0.6957 |     -0.0145 |
|    2 | recall            |    0.7647 |    0.7647 |      0.0000 |
|    3 | recall            |    0.6765 |    0.6765 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7500 |      0.0000 |
|    5 | recall            |    0.7391 |    0.7101 |     -0.0290 |
|    1 | f1                |    0.7903 |    0.7869 |     -0.0034 |
|    2 | f1                |    0.7820 |    0.7820 |      0.0000 |
|    3 | f1                |    0.7541 |    0.7419 |     -0.0122 |
|    4 | f1                |    0.7846 |    0.7727 |     -0.0119 |
|    5 | f1                |    0.7669 |    0.7481 |     -0.0188 |
|    1 | roc_auc           |    0.9140 |    0.9128 |     -0.0012 |
|    2 | roc_auc           |    0.8779 |    0.8794 |      0.0015 |
|    3 | roc_auc           |    0.8592 |    0.8596 |      0.0004 |
|    4 | roc_auc           |    0.8747 |    0.8745 |     -0.0003 |
|    5 | roc_auc           |    0.8643 |    0.8642 |     -0.0001 |
|    1 | log_loss          |    0.3786 |    0.3800 |     -0.0014 |
|    2 | log_loss          |    0.4027 |    0.4007 |      0.0020 |
|    3 | log_loss          |    0.4403 |    0.4405 |     -0.0003 |
|    4 | log_loss          |    0.3891 |    0.3958 |     -0.0067 |
|    5 | log_loss          |    0.4184 |    0.4174 |      0.0009 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           3 |                      9 |         0 |           3 |    2 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-044/3ec42e5a2874/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-044/3ec42e5a2874/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-044/3ec42e5a2874/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-044/3ec42e5a2874/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
