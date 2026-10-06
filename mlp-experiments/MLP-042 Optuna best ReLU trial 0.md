---
id: MLP-042
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_042_optuna_relu_trial0
---

# MLP-042 — Optuna best ReLU trial 0

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-042 — Optuna best ReLU trial 0                                                                                                          |
| Гипотеза         | If the best configuration from MLP-TUNE-001 is evaluated on the official five folds, then its screening advantage will generalize.          |
| Одно изменение   | Apply Optuna trial 86 / MLP-TUNE-002 trial 0 as one selected bundle: four 8-unit ReLU layers, dropout 0.30, lr 0.0017503535 and decay 1e-4. |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium                                                                           |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                         |
| Основная метрика | accuracy                                                                                                                                    |
| Критерии         | failed                                                                                                                                      |
| Код              | ml_project.mlp_experiments.mlp_042_optuna_relu_trial0                                                                                       |
| Hash кода        | 5ee9d3f948e6…                                                                                                                               |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0191 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0183 |              0.0000 |  False |
| guardrail | recall            |              -0.0147 |             -0.0100 |  False |
| guardrail | f1                |              -0.0242 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8193 | 0.0094 | 0.8090 | 0.8268 |
| mlp_candidate     | balanced_accuracy | 0.7993 | 0.0140 | 0.7809 | 0.8179 |
| mlp_candidate     | precision         | 0.7966 | 0.0296 | 0.7656 | 0.8393 |
| mlp_candidate     | recall            | 0.7133 | 0.0464 | 0.6618 | 0.7826 |
| mlp_candidate     | f1                | 0.7514 | 0.0191 | 0.7258 | 0.7770 |
| mlp_candidate     | roc_auc           | 0.8713 | 0.0162 | 0.8509 | 0.8949 |
| mlp_candidate     | log_loss          | 0.4300 | 0.0262 | 0.4052 | 0.4682 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8268 |     -0.0279 |
|    2 | accuracy          |    0.8371 |    0.8090 |     -0.0281 |
|    3 | accuracy          |    0.8315 |    0.8090 |     -0.0225 |
|    4 | accuracy          |    0.8427 |    0.8258 |     -0.0169 |
|    5 | accuracy          |    0.8258 |    0.8258 |      0.0000 |
|    1 | balanced_accuracy |    0.8278 |    0.7997 |     -0.0281 |
|    2 | balanced_accuracy |    0.8233 |    0.7921 |     -0.0311 |
|    3 | balanced_accuracy |    0.8019 |    0.7809 |     -0.0210 |
|    4 | balanced_accuracy |    0.8250 |    0.8057 |     -0.0193 |
|    5 | balanced_accuracy |    0.8099 |    0.8179 |      0.0080 |
|    1 | precision         |    0.8909 |    0.8393 |     -0.0516 |
|    2 | precision         |    0.8000 |    0.7656 |     -0.0344 |
|    3 | precision         |    0.8519 |    0.8036 |     -0.0483 |
|    4 | precision         |    0.8226 |    0.8033 |     -0.0193 |
|    5 | precision         |    0.7969 |    0.7714 |     -0.0254 |
|    1 | recall            |    0.7101 |    0.6812 |     -0.0290 |
|    2 | recall            |    0.7647 |    0.7206 |     -0.0441 |
|    3 | recall            |    0.6765 |    0.6618 |     -0.0147 |
|    4 | recall            |    0.7500 |    0.7206 |     -0.0294 |
|    5 | recall            |    0.7391 |    0.7826 |      0.0435 |
|    1 | f1                |    0.7903 |    0.7520 |     -0.0383 |
|    2 | f1                |    0.7820 |    0.7424 |     -0.0395 |
|    3 | f1                |    0.7541 |    0.7258 |     -0.0283 |
|    4 | f1                |    0.7846 |    0.7597 |     -0.0249 |
|    5 | f1                |    0.7669 |    0.7770 |      0.0101 |
|    1 | roc_auc           |    0.9140 |    0.8949 |     -0.0191 |
|    2 | roc_auc           |    0.8779 |    0.8769 |     -0.0011 |
|    3 | roc_auc           |    0.8592 |    0.8509 |     -0.0082 |
|    4 | roc_auc           |    0.8747 |    0.8695 |     -0.0052 |
|    5 | roc_auc           |    0.8643 |    0.8644 |      0.0001 |
|    1 | log_loss          |    0.3786 |    0.4173 |     -0.0387 |
|    2 | log_loss          |    0.4027 |    0.4136 |     -0.0109 |
|    3 | log_loss          |    0.4403 |    0.4682 |     -0.0279 |
|    4 | log_loss          |    0.3891 |    0.4052 |     -0.0161 |
|    5 | log_loss          |    0.4184 |    0.4455 |     -0.0272 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          13 |                     30 |         0 |           4 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-042/5ee9d3f948e6/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-042/5ee9d3f948e6/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-042/5ee9d3f948e6/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-042/5ee9d3f948e6/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Гипотеза не подтвердилась. Преимущество trial 86 на трёх screening-folds
  (`0.8328` против `0.8159` у screening baseline) не перенеслось на официальные
  пять folds: accuracy снизилась с `0.8384` у MLP-024 до `0.8193` (`Δ=-0.0191`).
- Кандидат исправил 13 ошибок MLP-024, но добавил 30 новых. Он проиграл reference
  на четырёх folds, на пятом получилась ничья. Balanced accuracy, F1, ROC AUC и
  log loss также ухудшились.
- Early stopping выбрал эпохи 15, 57, 63, 36 и 17; разброс показывает сильную
  зависимость компактной четырёхслойной сети от состава fold, а продолжение
  обучения не устраняет разрыв с reference.
- Решение: `reject`. Trial был выбран после 140 сравнений на одних и тех же трёх
  folds и подстроился под их случайные особенности. Чемпионом остаётся MLP-024.
- Следующий шаг: менять информацию в признаках или семейство модели, а не
  продолжать tuning этой конфигурации на прежних screening-folds.
