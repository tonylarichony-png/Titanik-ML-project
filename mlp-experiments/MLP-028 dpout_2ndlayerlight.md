---
id: MLP-028
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_028_dpout_2ndlayerlight
---

# MLP-028 — dpout_2ndlayerlight

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-028 — dpout_2ndlayerlight                                     |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_028_dpout_2ndlayerlight            |
| Hash кода        | 73ff75c7ddc7…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0112 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0140 |              0.0000 |  False |
| guardrail | recall            |              -0.0263 |             -0.0100 |  False |
| guardrail | f1                |              -0.0184 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8271 | 0.0178 | 0.8090 | 0.8547 |
| mlp_candidate     | balanced_accuracy | 0.8036 | 0.0175 | 0.7865 | 0.8278 |
| mlp_candidate     | precision         | 0.8231 | 0.0405 | 0.7833 | 0.8909 |
| mlp_candidate     | recall            | 0.7018 | 0.0253 | 0.6667 | 0.7353 |
| mlp_candidate     | f1                | 0.7572 | 0.0235 | 0.7344 | 0.7903 |
| mlp_candidate     | roc_auc           | 0.8803 | 0.0217 | 0.8632 | 0.9169 |
| mlp_candidate     | log_loss          | 0.4058 | 0.0263 | 0.3726 | 0.4415 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8547 |      0.0000 |
|    2 | accuracy          |    0.8371 |    0.8258 |     -0.0112 |
|    3 | accuracy          |    0.8315 |    0.8090 |     -0.0225 |
|    4 | accuracy          |    0.8427 |    0.8315 |     -0.0112 |
|    5 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    1 | balanced_accuracy |    0.8278 |    0.8278 |      0.0000 |
|    2 | balanced_accuracy |    0.8233 |    0.8029 |     -0.0203 |
|    3 | balanced_accuracy |    0.8019 |    0.7865 |     -0.0154 |
|    4 | balanced_accuracy |    0.8250 |    0.8131 |     -0.0119 |
|    5 | balanced_accuracy |    0.8099 |    0.7875 |     -0.0225 |
|    1 | precision         |    0.8909 |    0.8909 |      0.0000 |
|    2 | precision         |    0.8000 |    0.8136 |      0.0136 |
|    3 | precision         |    0.8519 |    0.7833 |     -0.0685 |
|    4 | precision         |    0.8226 |    0.8065 |     -0.0161 |
|    5 | precision         |    0.7969 |    0.8214 |      0.0246 |
|    1 | recall            |    0.7101 |    0.7101 |      0.0000 |
|    2 | recall            |    0.7647 |    0.7059 |     -0.0588 |
|    3 | recall            |    0.6765 |    0.6912 |      0.0147 |
|    4 | recall            |    0.7500 |    0.7353 |     -0.0147 |
|    5 | recall            |    0.7391 |    0.6667 |     -0.0725 |
|    1 | f1                |    0.7903 |    0.7903 |      0.0000 |
|    2 | f1                |    0.7820 |    0.7559 |     -0.0260 |
|    3 | f1                |    0.7541 |    0.7344 |     -0.0197 |
|    4 | f1                |    0.7846 |    0.7692 |     -0.0154 |
|    5 | f1                |    0.7669 |    0.7360 |     -0.0309 |
|    1 | roc_auc           |    0.9140 |    0.9169 |      0.0029 |
|    2 | roc_auc           |    0.8779 |    0.8793 |      0.0013 |
|    3 | roc_auc           |    0.8592 |    0.8650 |      0.0059 |
|    4 | roc_auc           |    0.8747 |    0.8770 |      0.0023 |
|    5 | roc_auc           |    0.8643 |    0.8632 |     -0.0011 |
|    1 | log_loss          |    0.3786 |    0.3726 |      0.0060 |
|    2 | log_loss          |    0.4027 |    0.3992 |      0.0035 |
|    3 | log_loss          |    0.4403 |    0.4415 |     -0.0012 |
|    4 | log_loss          |    0.3891 |    0.3948 |     -0.0057 |
|    5 | log_loss          |    0.4184 |    0.4207 |     -0.0023 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           7 |                     17 |         0 |           4 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-028/73ff75c7ddc7/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-028/73ff75c7ddc7/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-028/73ff75c7ddc7/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-028/73ff75c7ddc7/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
