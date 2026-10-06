---
id: MLP-041
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_041_lr_4mindelta
---

# MLP-041 — LR-4mindelta

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-041 — LR-4mindelta                                            |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_041_lr_4mindelta                   |
| Hash кода        | cc5c3fbee12d…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0112 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0135 |              0.0000 |  False |
| guardrail | recall            |              -0.0233 |             -0.0100 |  False |
| guardrail | f1                |              -0.0180 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8271 | 0.0117 | 0.8146 | 0.8380 |
| mlp_candidate     | balanced_accuracy | 0.8041 | 0.0154 | 0.7854 | 0.8205 |
| mlp_candidate     | precision         | 0.8203 | 0.0210 | 0.8065 | 0.8571 |
| mlp_candidate     | recall            | 0.7048 | 0.0370 | 0.6618 | 0.7500 |
| mlp_candidate     | f1                | 0.7575 | 0.0204 | 0.7317 | 0.7786 |
| mlp_candidate     | roc_auc           | 0.8771 | 0.0184 | 0.8601 | 0.9059 |
| mlp_candidate     | log_loss          | 0.4063 | 0.0245 | 0.3829 | 0.4427 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8380 |     -0.0168 |
|    2 | accuracy          |    0.8371 |    0.8315 |     -0.0056 |
|    3 | accuracy          |    0.8315 |    0.8146 |     -0.0169 |
|    4 | accuracy          |    0.8427 |    0.8371 |     -0.0056 |
|    5 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    1 | balanced_accuracy |    0.8278 |    0.8115 |     -0.0163 |
|    2 | balanced_accuracy |    0.8233 |    0.8131 |     -0.0102 |
|    3 | balanced_accuracy |    0.8019 |    0.7854 |     -0.0164 |
|    4 | balanced_accuracy |    0.8250 |    0.8205 |     -0.0045 |
|    5 | balanced_accuracy |    0.8099 |    0.7901 |     -0.0198 |
|    1 | precision         |    0.8909 |    0.8571 |     -0.0338 |
|    2 | precision         |    0.8000 |    0.8065 |      0.0065 |
|    3 | precision         |    0.8519 |    0.8182 |     -0.0337 |
|    4 | precision         |    0.8226 |    0.8095 |     -0.0131 |
|    5 | precision         |    0.7969 |    0.8103 |      0.0135 |
|    1 | recall            |    0.7101 |    0.6957 |     -0.0145 |
|    2 | recall            |    0.7647 |    0.7353 |     -0.0294 |
|    3 | recall            |    0.6765 |    0.6618 |     -0.0147 |
|    4 | recall            |    0.7500 |    0.7500 |      0.0000 |
|    5 | recall            |    0.7391 |    0.6812 |     -0.0580 |
|    1 | f1                |    0.7903 |    0.7680 |     -0.0223 |
|    2 | f1                |    0.7820 |    0.7692 |     -0.0127 |
|    3 | f1                |    0.7541 |    0.7317 |     -0.0224 |
|    4 | f1                |    0.7846 |    0.7786 |     -0.0060 |
|    5 | f1                |    0.7669 |    0.7402 |     -0.0268 |
|    1 | roc_auc           |    0.9140 |    0.9059 |     -0.0082 |
|    2 | roc_auc           |    0.8779 |    0.8836 |      0.0056 |
|    3 | roc_auc           |    0.8592 |    0.8601 |      0.0009 |
|    4 | roc_auc           |    0.8747 |    0.8714 |     -0.0033 |
|    5 | roc_auc           |    0.8643 |    0.8646 |      0.0003 |
|    1 | log_loss          |    0.3786 |    0.3829 |     -0.0043 |
|    2 | log_loss          |    0.4027 |    0.3894 |      0.0132 |
|    3 | log_loss          |    0.4403 |    0.4427 |     -0.0024 |
|    4 | log_loss          |    0.3891 |    0.3971 |     -0.0080 |
|    5 | log_loss          |    0.4184 |    0.4192 |     -0.0009 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           7 |                     17 |         0 |           5 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-041/cc5c3fbee12d/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-041/cc5c3fbee12d/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-041/cc5c3fbee12d/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-041/cc5c3fbee12d/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
