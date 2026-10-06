---
id: MLP-036
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_036_batch64
---

# MLP-036 — Batch64

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-036 — Batch64                                                 |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_036_batch64                        |
| Hash кода        | f2a10809e9f4…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0112 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0167 |              0.0000 |  False |
| guardrail | recall            |              -0.0408 |             -0.0100 |  False |
| guardrail | f1                |              -0.0225 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8271 | 0.0172 | 0.8034 | 0.8483 |
| mlp_candidate     | balanced_accuracy | 0.8009 | 0.0176 | 0.7791 | 0.8267 |
| mlp_candidate     | precision         | 0.8367 | 0.0522 | 0.7797 | 0.9167 |
| mlp_candidate     | recall            | 0.6873 | 0.0401 | 0.6377 | 0.7353 |
| mlp_candidate     | f1                | 0.7531 | 0.0233 | 0.7244 | 0.7874 |
| mlp_candidate     | roc_auc           | 0.8773 | 0.0194 | 0.8646 | 0.9103 |
| mlp_candidate     | log_loss          | 0.4103 | 0.0212 | 0.3930 | 0.4427 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8380 |     -0.0168 |
|    2 | accuracy          |    0.8371 |    0.8258 |     -0.0112 |
|    3 | accuracy          |    0.8315 |    0.8034 |     -0.0281 |
|    4 | accuracy          |    0.8427 |    0.8483 |      0.0056 |
|    5 | accuracy          |    0.8258 |    0.8202 |     -0.0056 |
|    1 | balanced_accuracy |    0.8278 |    0.8007 |     -0.0271 |
|    2 | balanced_accuracy |    0.8233 |    0.8057 |     -0.0175 |
|    3 | balanced_accuracy |    0.8019 |    0.7791 |     -0.0227 |
|    4 | balanced_accuracy |    0.8250 |    0.8267 |      0.0017 |
|    5 | balanced_accuracy |    0.8099 |    0.7920 |     -0.0179 |
|    1 | precision         |    0.8909 |    0.9167 |      0.0258 |
|    2 | precision         |    0.8000 |    0.8033 |      0.0033 |
|    3 | precision         |    0.8519 |    0.7797 |     -0.0722 |
|    4 | precision         |    0.8226 |    0.8475 |      0.0249 |
|    5 | precision         |    0.7969 |    0.8364 |      0.0395 |
|    1 | recall            |    0.7101 |    0.6377 |     -0.0725 |
|    2 | recall            |    0.7647 |    0.7206 |     -0.0441 |
|    3 | recall            |    0.6765 |    0.6765 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7353 |     -0.0147 |
|    5 | recall            |    0.7391 |    0.6667 |     -0.0725 |
|    1 | f1                |    0.7903 |    0.7521 |     -0.0382 |
|    2 | f1                |    0.7820 |    0.7597 |     -0.0223 |
|    3 | f1                |    0.7541 |    0.7244 |     -0.0297 |
|    4 | f1                |    0.7846 |    0.7874 |      0.0028 |
|    5 | f1                |    0.7669 |    0.7419 |     -0.0250 |
|    1 | roc_auc           |    0.9140 |    0.9103 |     -0.0037 |
|    2 | roc_auc           |    0.8779 |    0.8794 |      0.0015 |
|    3 | roc_auc           |    0.8592 |    0.8649 |      0.0057 |
|    4 | roc_auc           |    0.8747 |    0.8674 |     -0.0074 |
|    5 | roc_auc           |    0.8643 |    0.8646 |      0.0003 |
|    1 | log_loss          |    0.3786 |    0.3930 |     -0.0144 |
|    2 | log_loss          |    0.4027 |    0.3956 |      0.0071 |
|    3 | log_loss          |    0.4403 |    0.4427 |     -0.0024 |
|    4 | log_loss          |    0.3891 |    0.3994 |     -0.0103 |
|    5 | log_loss          |    0.4184 |    0.4207 |     -0.0023 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          11 |                     21 |         1 |           4 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-036/f2a10809e9f4/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-036/f2a10809e9f4/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-036/f2a10809e9f4/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-036/f2a10809e9f4/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
