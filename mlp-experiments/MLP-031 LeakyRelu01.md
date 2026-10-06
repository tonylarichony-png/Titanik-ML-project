---
id: MLP-031
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_031_leakyrelu01
---

# MLP-031 — LeakyRelu01

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-031 — LeakyRelu01                                             |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_031_leakyrelu01                    |
| Hash кода        | e06555bb023e…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0112 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0140 |              0.0000 |  False |
| guardrail | recall            |              -0.0262 |             -0.0100 |  False |
| guardrail | f1                |              -0.0185 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8271 | 0.0153 | 0.8034 | 0.8436 |
| mlp_candidate     | balanced_accuracy | 0.8036 | 0.0158 | 0.7791 | 0.8205 |
| mlp_candidate     | precision         | 0.8237 | 0.0412 | 0.7797 | 0.8868 |
| mlp_candidate     | recall            | 0.7019 | 0.0323 | 0.6765 | 0.7500 |
| mlp_candidate     | f1                | 0.7570 | 0.0209 | 0.7244 | 0.7786 |
| mlp_candidate     | roc_auc           | 0.8757 | 0.0217 | 0.8559 | 0.9115 |
| mlp_candidate     | log_loss          | 0.4141 | 0.0286 | 0.3840 | 0.4571 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8436 |     -0.0112 |
|    2 | accuracy          |    0.8371 |    0.8258 |     -0.0112 |
|    3 | accuracy          |    0.8315 |    0.8034 |     -0.0281 |
|    4 | accuracy          |    0.8427 |    0.8371 |     -0.0056 |
|    5 | accuracy          |    0.8258 |    0.8258 |      0.0000 |
|    1 | balanced_accuracy |    0.8278 |    0.8133 |     -0.0145 |
|    2 | balanced_accuracy |    0.8233 |    0.8057 |     -0.0175 |
|    3 | balanced_accuracy |    0.8019 |    0.7791 |     -0.0227 |
|    4 | balanced_accuracy |    0.8250 |    0.8205 |     -0.0045 |
|    5 | balanced_accuracy |    0.8099 |    0.7993 |     -0.0106 |
|    1 | precision         |    0.8909 |    0.8868 |     -0.0041 |
|    2 | precision         |    0.8000 |    0.8033 |      0.0033 |
|    3 | precision         |    0.8519 |    0.7797 |     -0.0722 |
|    4 | precision         |    0.8226 |    0.8095 |     -0.0131 |
|    5 | precision         |    0.7969 |    0.8393 |      0.0424 |
|    1 | recall            |    0.7101 |    0.6812 |     -0.0290 |
|    2 | recall            |    0.7647 |    0.7206 |     -0.0441 |
|    3 | recall            |    0.6765 |    0.6765 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7500 |      0.0000 |
|    5 | recall            |    0.7391 |    0.6812 |     -0.0580 |
|    1 | f1                |    0.7903 |    0.7705 |     -0.0198 |
|    2 | f1                |    0.7820 |    0.7597 |     -0.0223 |
|    3 | f1                |    0.7541 |    0.7244 |     -0.0297 |
|    4 | f1                |    0.7846 |    0.7786 |     -0.0060 |
|    5 | f1                |    0.7669 |    0.7520 |     -0.0149 |
|    1 | roc_auc           |    0.9140 |    0.9115 |     -0.0025 |
|    2 | roc_auc           |    0.8779 |    0.8771 |     -0.0008 |
|    3 | roc_auc           |    0.8592 |    0.8559 |     -0.0032 |
|    4 | roc_auc           |    0.8747 |    0.8721 |     -0.0027 |
|    5 | roc_auc           |    0.8643 |    0.8619 |     -0.0024 |
|    1 | log_loss          |    0.3786 |    0.3840 |     -0.0054 |
|    2 | log_loss          |    0.4027 |    0.4008 |      0.0018 |
|    3 | log_loss          |    0.4403 |    0.4571 |     -0.0169 |
|    4 | log_loss          |    0.3891 |    0.4010 |     -0.0119 |
|    5 | log_loss          |    0.4184 |    0.4274 |     -0.0090 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           9 |                     19 |         0 |           4 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-031/e06555bb023e/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-031/e06555bb023e/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-031/e06555bb023e/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-031/e06555bb023e/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
