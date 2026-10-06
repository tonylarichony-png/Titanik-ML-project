---
id: MLP-025
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_025_dpoutmed_hard
---

# MLP-025 — dpoutmed-hard

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-025 — dpoutmed-hard                                           |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_025_dpoutmed_hard                  |
| Hash кода        | f842958f085b…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0112 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0119 |              0.0000 |  False |
| guardrail | recall            |              -0.0147 |             -0.0100 |  False |
| guardrail | f1                |              -0.0154 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8271 | 0.0186 | 0.8034 | 0.8492 |
| mlp_candidate     | balanced_accuracy | 0.8057 | 0.0184 | 0.7791 | 0.8250 |
| mlp_candidate     | precision         | 0.8151 | 0.0445 | 0.7797 | 0.8889 |
| mlp_candidate     | recall            | 0.7134 | 0.0306 | 0.6765 | 0.7500 |
| mlp_candidate     | f1                | 0.7601 | 0.0245 | 0.7244 | 0.7846 |
| mlp_candidate     | roc_auc           | 0.8770 | 0.0231 | 0.8564 | 0.9151 |
| mlp_candidate     | log_loss          | 0.4045 | 0.0266 | 0.3739 | 0.4416 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8492 |     -0.0056 |
|    2 | accuracy          |    0.8371 |    0.8202 |     -0.0169 |
|    3 | accuracy          |    0.8315 |    0.8034 |     -0.0281 |
|    4 | accuracy          |    0.8427 |    0.8427 |      0.0000 |
|    5 | accuracy          |    0.8258 |    0.8202 |     -0.0056 |
|    1 | balanced_accuracy |    0.8278 |    0.8206 |     -0.0072 |
|    2 | balanced_accuracy |    0.8233 |    0.7984 |     -0.0249 |
|    3 | balanced_accuracy |    0.8019 |    0.7791 |     -0.0227 |
|    4 | balanced_accuracy |    0.8250 |    0.8250 |      0.0000 |
|    5 | balanced_accuracy |    0.8099 |    0.8053 |     -0.0046 |
|    1 | precision         |    0.8909 |    0.8889 |     -0.0020 |
|    2 | precision         |    0.8000 |    0.8000 |      0.0000 |
|    3 | precision         |    0.8519 |    0.7797 |     -0.0722 |
|    4 | precision         |    0.8226 |    0.8226 |      0.0000 |
|    5 | precision         |    0.7969 |    0.7846 |     -0.0123 |
|    1 | recall            |    0.7101 |    0.6957 |     -0.0145 |
|    2 | recall            |    0.7647 |    0.7059 |     -0.0588 |
|    3 | recall            |    0.6765 |    0.6765 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7500 |      0.0000 |
|    5 | recall            |    0.7391 |    0.7391 |      0.0000 |
|    1 | f1                |    0.7903 |    0.7805 |     -0.0098 |
|    2 | f1                |    0.7820 |    0.7500 |     -0.0320 |
|    3 | f1                |    0.7541 |    0.7244 |     -0.0297 |
|    4 | f1                |    0.7846 |    0.7846 |      0.0000 |
|    5 | f1                |    0.7669 |    0.7612 |     -0.0057 |
|    1 | roc_auc           |    0.9140 |    0.9151 |      0.0011 |
|    2 | roc_auc           |    0.8779 |    0.8769 |     -0.0011 |
|    3 | roc_auc           |    0.8592 |    0.8564 |     -0.0028 |
|    4 | roc_auc           |    0.8747 |    0.8755 |      0.0008 |
|    5 | roc_auc           |    0.8643 |    0.8613 |     -0.0031 |
|    1 | log_loss          |    0.3786 |    0.3739 |      0.0047 |
|    2 | log_loss          |    0.4027 |    0.3979 |      0.0048 |
|    3 | log_loss          |    0.4403 |    0.4416 |     -0.0013 |
|    4 | log_loss          |    0.3891 |    0.3892 |     -0.0002 |
|    5 | log_loss          |    0.4184 |    0.4198 |     -0.0015 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           3 |                     13 |         0 |           4 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-025/f842958f085b/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-025/f842958f085b/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-025/f842958f085b/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-025/f842958f085b/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
