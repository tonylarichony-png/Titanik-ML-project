---
id: MLP-034
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_034_batchsize16
---

# MLP-034 — batchsize16

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-034 — batchsize16                                             |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | failed                                                            |
| Код              | ml_project.mlp_experiments.mlp_034_batchsize16                    |
| Hash кода        | 9040ab43b005…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0079 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0081 |              0.0000 |  False |
| guardrail | recall            |              -0.0089 |             -0.0100 |   True |
| guardrail | f1                |              -0.0102 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8305 | 0.0210 | 0.8034 | 0.8547 |
| mlp_candidate     | balanced_accuracy | 0.8095 | 0.0201 | 0.7820 | 0.8332 |
| mlp_candidate     | precision         | 0.8183 | 0.0405 | 0.7705 | 0.8644 |
| mlp_candidate     | recall            | 0.7192 | 0.0203 | 0.6912 | 0.7391 |
| mlp_candidate     | f1                | 0.7653 | 0.0264 | 0.7287 | 0.7969 |
| mlp_candidate     | roc_auc           | 0.8801 | 0.0185 | 0.8640 | 0.9097 |
| mlp_candidate     | log_loss          | 0.4034 | 0.0222 | 0.3784 | 0.4330 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8547 |      0.0000 |
|    2 | accuracy          |    0.8371 |    0.8371 |      0.0000 |
|    3 | accuracy          |    0.8315 |    0.8034 |     -0.0281 |
|    4 | accuracy          |    0.8427 |    0.8427 |      0.0000 |
|    5 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    1 | balanced_accuracy |    0.8278 |    0.8332 |      0.0054 |
|    2 | balanced_accuracy |    0.8233 |    0.8120 |     -0.0112 |
|    3 | balanced_accuracy |    0.8019 |    0.7820 |     -0.0199 |
|    4 | balanced_accuracy |    0.8250 |    0.8222 |     -0.0028 |
|    5 | balanced_accuracy |    0.8099 |    0.7981 |     -0.0118 |
|    1 | precision         |    0.8909 |    0.8644 |     -0.0265 |
|    2 | precision         |    0.8000 |    0.8421 |      0.0421 |
|    3 | precision         |    0.8519 |    0.7705 |     -0.0814 |
|    4 | precision         |    0.8226 |    0.8333 |      0.0108 |
|    5 | precision         |    0.7969 |    0.7812 |     -0.0156 |
|    1 | recall            |    0.7101 |    0.7391 |      0.0290 |
|    2 | recall            |    0.7647 |    0.7059 |     -0.0588 |
|    3 | recall            |    0.6765 |    0.6912 |      0.0147 |
|    4 | recall            |    0.7500 |    0.7353 |     -0.0147 |
|    5 | recall            |    0.7391 |    0.7246 |     -0.0145 |
|    1 | f1                |    0.7903 |    0.7969 |      0.0066 |
|    2 | f1                |    0.7820 |    0.7680 |     -0.0140 |
|    3 | f1                |    0.7541 |    0.7287 |     -0.0254 |
|    4 | f1                |    0.7846 |    0.7812 |     -0.0034 |
|    5 | f1                |    0.7669 |    0.7519 |     -0.0150 |
|    1 | roc_auc           |    0.9140 |    0.9097 |     -0.0043 |
|    2 | roc_auc           |    0.8779 |    0.8864 |      0.0084 |
|    3 | roc_auc           |    0.8592 |    0.8688 |      0.0096 |
|    4 | roc_auc           |    0.8747 |    0.8714 |     -0.0033 |
|    5 | roc_auc           |    0.8643 |    0.8640 |     -0.0003 |
|    1 | log_loss          |    0.3786 |    0.3784 |      0.0002 |
|    2 | log_loss          |    0.4027 |    0.3917 |      0.0110 |
|    3 | log_loss          |    0.4403 |    0.4330 |      0.0073 |
|    4 | log_loss          |    0.3891 |    0.3945 |     -0.0054 |
|    5 | log_loss          |    0.4184 |    0.4195 |     -0.0011 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           9 |                     16 |         0 |           2 |    3 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-034/9040ab43b005/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-034/9040ab43b005/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-034/9040ab43b005/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-034/9040ab43b005/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
