---
id: MLP-038
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_038_middecay
---

# MLP-038 — middecay

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-038 — middecay                                                |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_038_middecay                       |
| Hash кода        | 7f6ae9d1c237…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0168 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0203 |              0.0000 |  False |
| guardrail | recall            |              -0.0351 |             -0.0100 |  False |
| guardrail | f1                |              -0.0269 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8215 | 0.0109 | 0.8090 | 0.8371 |
| mlp_candidate     | balanced_accuracy | 0.7973 | 0.0124 | 0.7781 | 0.8120 |
| mlp_candidate     | precision         | 0.8154 | 0.0252 | 0.7903 | 0.8421 |
| mlp_candidate     | recall            | 0.6930 | 0.0295 | 0.6471 | 0.7206 |
| mlp_candidate     | f1                | 0.7486 | 0.0170 | 0.7213 | 0.7680 |
| mlp_candidate     | roc_auc           | 0.8753 | 0.0157 | 0.8558 | 0.8989 |
| mlp_candidate     | log_loss          | 0.4101 | 0.0235 | 0.3913 | 0.4486 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8268 |     -0.0279 |
|    2 | accuracy          |    0.8371 |    0.8202 |     -0.0169 |
|    3 | accuracy          |    0.8315 |    0.8090 |     -0.0225 |
|    4 | accuracy          |    0.8427 |    0.8371 |     -0.0056 |
|    5 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    1 | balanced_accuracy |    0.8278 |    0.7997 |     -0.0281 |
|    2 | balanced_accuracy |    0.8233 |    0.8012 |     -0.0221 |
|    3 | balanced_accuracy |    0.8019 |    0.7781 |     -0.0238 |
|    4 | balanced_accuracy |    0.8250 |    0.8120 |     -0.0130 |
|    5 | balanced_accuracy |    0.8099 |    0.7954 |     -0.0145 |
|    1 | precision         |    0.8909 |    0.8393 |     -0.0516 |
|    2 | precision         |    0.8000 |    0.7903 |     -0.0097 |
|    3 | precision         |    0.8519 |    0.8148 |     -0.0370 |
|    4 | precision         |    0.8226 |    0.8421 |      0.0195 |
|    5 | precision         |    0.7969 |    0.7903 |     -0.0066 |
|    1 | recall            |    0.7101 |    0.6812 |     -0.0290 |
|    2 | recall            |    0.7647 |    0.7206 |     -0.0441 |
|    3 | recall            |    0.6765 |    0.6471 |     -0.0294 |
|    4 | recall            |    0.7500 |    0.7059 |     -0.0441 |
|    5 | recall            |    0.7391 |    0.7101 |     -0.0290 |
|    1 | f1                |    0.7903 |    0.7520 |     -0.0383 |
|    2 | f1                |    0.7820 |    0.7538 |     -0.0281 |
|    3 | f1                |    0.7541 |    0.7213 |     -0.0328 |
|    4 | f1                |    0.7846 |    0.7680 |     -0.0166 |
|    5 | f1                |    0.7669 |    0.7481 |     -0.0188 |
|    1 | roc_auc           |    0.9140 |    0.8989 |     -0.0152 |
|    2 | roc_auc           |    0.8779 |    0.8787 |      0.0008 |
|    3 | roc_auc           |    0.8592 |    0.8558 |     -0.0033 |
|    4 | roc_auc           |    0.8747 |    0.8737 |     -0.0011 |
|    5 | roc_auc           |    0.8643 |    0.8695 |      0.0052 |
|    1 | log_loss          |    0.3786 |    0.3938 |     -0.0152 |
|    2 | log_loss          |    0.4027 |    0.4012 |      0.0015 |
|    3 | log_loss          |    0.4403 |    0.4486 |     -0.0083 |
|    4 | log_loss          |    0.3891 |    0.3913 |     -0.0022 |
|    5 | log_loss          |    0.4184 |    0.4159 |      0.0025 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           3 |                     18 |         0 |           5 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-038/7f6ae9d1c237/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-038/7f6ae9d1c237/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-038/7f6ae9d1c237/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-038/7f6ae9d1c237/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
