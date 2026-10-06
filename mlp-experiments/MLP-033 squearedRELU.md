---
id: MLP-033
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_033_squearedrelu
---

# MLP-033 — squearedRELU

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-033 — squearedRELU                                            |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_033_squearedrelu                   |
| Hash кода        | 99a3f9192aca…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0671 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0976 |              0.0000 |  False |
| guardrail | recall            |              -0.2299 |             -0.0100 |  False |
| guardrail | f1                |              -0.2030 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.7712 | 0.0877 | 0.6145 | 0.8146 |
| mlp_candidate     | balanced_accuracy | 0.7199 | 0.1231 | 0.5000 | 0.7826 |
| mlp_candidate     | precision         | 0.6734 | 0.3766 | 0.0000 | 0.8571 |
| mlp_candidate     | recall            | 0.4982 | 0.2789 | 0.0000 | 0.6471 |
| mlp_candidate     | f1                | 0.5725 | 0.3202 | 0.0000 | 0.7273 |
| mlp_candidate     | roc_auc           | 0.8592 | 0.0216 | 0.8301 | 0.8860 |
| mlp_candidate     | log_loss          | 0.4768 | 0.0469 | 0.4058 | 0.5214 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.6145 |     -0.2402 |
|    2 | accuracy          |    0.8371 |    0.8146 |     -0.0225 |
|    3 | accuracy          |    0.8315 |    0.8146 |     -0.0169 |
|    4 | accuracy          |    0.8427 |    0.8034 |     -0.0393 |
|    5 | accuracy          |    0.8258 |    0.8090 |     -0.0169 |
|    1 | balanced_accuracy |    0.8278 |    0.5000 |     -0.3278 |
|    2 | balanced_accuracy |    0.8233 |    0.7770 |     -0.0463 |
|    3 | balanced_accuracy |    0.8019 |    0.7826 |     -0.0193 |
|    4 | balanced_accuracy |    0.8250 |    0.7651 |     -0.0599 |
|    5 | balanced_accuracy |    0.8099 |    0.7749 |     -0.0350 |
|    1 | precision         |    0.8909 |    0.0000 |     -0.8909 |
|    2 | precision         |    0.8000 |    0.8571 |      0.0571 |
|    3 | precision         |    0.8519 |    0.8302 |     -0.0217 |
|    4 | precision         |    0.8226 |    0.8367 |      0.0142 |
|    5 | precision         |    0.7969 |    0.8431 |      0.0463 |
|    1 | recall            |    0.7101 |    0.0000 |     -0.7101 |
|    2 | recall            |    0.7647 |    0.6176 |     -0.1471 |
|    3 | recall            |    0.6765 |    0.6471 |     -0.0294 |
|    4 | recall            |    0.7500 |    0.6029 |     -0.1471 |
|    5 | recall            |    0.7391 |    0.6232 |     -0.1159 |
|    1 | f1                |    0.7903 |    0.0000 |     -0.7903 |
|    2 | f1                |    0.7820 |    0.7179 |     -0.0640 |
|    3 | f1                |    0.7541 |    0.7273 |     -0.0268 |
|    4 | f1                |    0.7846 |    0.7009 |     -0.0838 |
|    5 | f1                |    0.7669 |    0.7167 |     -0.0503 |
|    1 | roc_auc           |    0.9140 |    0.8733 |     -0.0407 |
|    2 | roc_auc           |    0.8779 |    0.8860 |      0.0080 |
|    3 | roc_auc           |    0.8592 |    0.8490 |     -0.0102 |
|    4 | roc_auc           |    0.8747 |    0.8301 |     -0.0447 |
|    5 | roc_auc           |    0.8643 |    0.8578 |     -0.0065 |
|    1 | log_loss          |    0.3786 |    0.5174 |     -0.1388 |
|    2 | log_loss          |    0.4027 |    0.4058 |     -0.0031 |
|    3 | log_loss          |    0.4403 |    0.4667 |     -0.0265 |
|    4 | log_loss          |    0.3891 |    0.4730 |     -0.0839 |
|    5 | log_loss          |    0.4184 |    0.5214 |     -0.1030 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          30 |                     90 |         0 |           5 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-033/99a3f9192aca/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-033/99a3f9192aca/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-033/99a3f9192aca/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-033/99a3f9192aca/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
