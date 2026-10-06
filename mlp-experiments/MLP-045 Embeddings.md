---
id: MLP-045
type: mlp-experiment
status: completed
decision: pending
implementation_module: ml_project.mlp_experiments.mlp_045_embeddings
---

# MLP-045 — Embeddings

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-045 — Embeddings                                                                                                                                                                                |
| Гипотеза         | If low-cardinality categorical features are represented by learned embeddings instead of one-hot columns, then the network may learn useful category similarities and improve official CV accuracy. |
| Одно изменение   | Replace one-hot encoding with fold-fitted ordinal indices and embeddings for all six categorical features; keep the MLP-024 hidden network and all optimization settings unchanged.                 |
| Решение          | pending |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium                                                                                                                                   |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                                 |
| Основная метрика | accuracy                                                                                                                                                                                            |
| Критерии         | failed                                                                                                                                                                                              |
| Код              | ml_project.mlp_experiments.mlp_045_embeddings                                                                                                                                                       |
| Hash кода        | eaa034b9cd1b…                                                                                                                                                                                       |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0202 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0180 |              0.0000 |  False |
| guardrail | recall            |              -0.0087 |             -0.0100 |   True |
| guardrail | f1                |              -0.0239 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8182 | 0.0217 | 0.7921 | 0.8427 |
| mlp_candidate     | balanced_accuracy | 0.7996 | 0.0267 | 0.7701 | 0.8250 |
| mlp_candidate     | precision         | 0.7884 | 0.0243 | 0.7541 | 0.8226 |
| mlp_candidate     | recall            | 0.7194 | 0.0515 | 0.6522 | 0.7681 |
| mlp_candidate     | f1                | 0.7517 | 0.0352 | 0.7132 | 0.7846 |
| mlp_candidate     | roc_auc           | 0.8664 | 0.0258 | 0.8288 | 0.9002 |
| mlp_candidate     | log_loss          | 0.4305 | 0.0583 | 0.3950 | 0.5325 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.7989 |     -0.0559 |
|    2 | accuracy          |    0.8371 |    0.8258 |     -0.0112 |
|    3 | accuracy          |    0.8315 |    0.7921 |     -0.0393 |
|    4 | accuracy          |    0.8427 |    0.8427 |      0.0000 |
|    5 | accuracy          |    0.8258 |    0.8315 |      0.0056 |
|    1 | balanced_accuracy |    0.8278 |    0.7715 |     -0.0563 |
|    2 | balanced_accuracy |    0.8233 |    0.8114 |     -0.0119 |
|    3 | balanced_accuracy |    0.8019 |    0.7701 |     -0.0318 |
|    4 | balanced_accuracy |    0.8250 |    0.8250 |      0.0000 |
|    5 | balanced_accuracy |    0.8099 |    0.8198 |      0.0099 |
|    1 | precision         |    0.8909 |    0.7895 |     -0.1014 |
|    2 | precision         |    0.8000 |    0.7846 |     -0.0154 |
|    3 | precision         |    0.8519 |    0.7541 |     -0.0978 |
|    4 | precision         |    0.8226 |    0.8226 |      0.0000 |
|    5 | precision         |    0.7969 |    0.7910 |     -0.0058 |
|    1 | recall            |    0.7101 |    0.6522 |     -0.0580 |
|    2 | recall            |    0.7647 |    0.7500 |     -0.0147 |
|    3 | recall            |    0.6765 |    0.6765 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7500 |      0.0000 |
|    5 | recall            |    0.7391 |    0.7681 |      0.0290 |
|    1 | f1                |    0.7903 |    0.7143 |     -0.0760 |
|    2 | f1                |    0.7820 |    0.7669 |     -0.0150 |
|    3 | f1                |    0.7541 |    0.7132 |     -0.0409 |
|    4 | f1                |    0.7846 |    0.7846 |      0.0000 |
|    5 | f1                |    0.7669 |    0.7794 |      0.0125 |
|    1 | roc_auc           |    0.9140 |    0.9002 |     -0.0138 |
|    2 | roc_auc           |    0.8779 |    0.8741 |     -0.0039 |
|    3 | roc_auc           |    0.8592 |    0.8288 |     -0.0303 |
|    4 | roc_auc           |    0.8747 |    0.8690 |     -0.0057 |
|    5 | roc_auc           |    0.8643 |    0.8598 |     -0.0045 |
|    1 | log_loss          |    0.3786 |    0.3967 |     -0.0181 |
|    2 | log_loss          |    0.4027 |    0.3950 |      0.0077 |
|    3 | log_loss          |    0.4403 |    0.5325 |     -0.0922 |
|    4 | log_loss          |    0.3891 |    0.4029 |     -0.0138 |
|    5 | log_loss          |    0.4184 |    0.4255 |     -0.0071 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          15 |                     33 |         1 |           3 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-045/eaa034b9cd1b/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-045/eaa034b9cd1b/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-045/eaa034b9cd1b/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-045/eaa034b9cd1b/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
