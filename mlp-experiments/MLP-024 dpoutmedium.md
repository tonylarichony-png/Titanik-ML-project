---
id: MLP-024
type: mlp-experiment
status: completed
decision: adopt
implementation_module: ml_project.mlp_experiments.mlp_024_dpoutmedium
---

# MLP-024 — dpoutmedium

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                          |
| ---------------- | ----------------------------------------------------------------- |
| Эксперимент      | MLP-024 — dpoutmedium                                             |
| Гипотеза         | CHANGE ME — if ..., then ..., because ...                         |
| Одно изменение   | CHANGE ME — exactly one controlled change                         |
| Решение          | adopt |
| Reference        | MLP-018_reference: ml_project.mlp_experiments.mlp_018_allin161616 |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)               |
| Основная метрика | accuracy                                                          |
| Критерии         | passed                                                            |
| Код              | ml_project.mlp_experiments.mlp_024_dpoutmedium                    |
| Hash кода        | a529898dd4ea…                                                     |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |               0.0067 |              0.0000 |   True |
| guardrail | balanced_accuracy |               0.0098 |              0.0000 |   True |
| guardrail | recall            |               0.0232 |             -0.0100 |   True |
| guardrail | f1                |               0.0133 |              0.0000 |   True |

## Сравнение всех метрик

| model             | metric            |   mean |    std |    min |    max |
| ----------------- | ----------------- | -----: | -----: | -----: | -----: |
| MLP-018_reference | accuracy          | 0.8316 | 0.0128 | 0.8146 | 0.8492 |
| MLP-018_reference | balanced_accuracy | 0.8078 | 0.0156 | 0.7875 | 0.8205 |
| MLP-018_reference | precision         | 0.8343 | 0.0447 | 0.7879 | 0.9038 |
| MLP-018_reference | recall            | 0.7049 | 0.0487 | 0.6618 | 0.7647 |
| MLP-018_reference | f1                | 0.7623 | 0.0206 | 0.7360 | 0.7786 |
| MLP-018_reference | roc_auc           | 0.8768 | 0.0189 | 0.8598 | 0.9077 |
| MLP-018_reference | log_loss          | 0.4101 | 0.0216 | 0.3844 | 0.4407 |
| mlp_candidate     | accuracy          | 0.8384 | 0.0111 | 0.8258 | 0.8547 |
| mlp_candidate     | balanced_accuracy | 0.8176 | 0.0111 | 0.8019 | 0.8278 |
| mlp_candidate     | precision         | 0.8324 | 0.0394 | 0.7969 | 0.8909 |
| mlp_candidate     | recall            | 0.7281 | 0.0351 | 0.6765 | 0.7647 |
| mlp_candidate     | f1                | 0.7756 | 0.0148 | 0.7541 | 0.7903 |
| mlp_candidate     | roc_auc           | 0.8780 | 0.0215 | 0.8592 | 0.9140 |
| mlp_candidate     | log_loss          | 0.4058 | 0.0244 | 0.3786 | 0.4403 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8492 |    0.8547 |      0.0056 |
|    2 | accuracy          |    0.8315 |    0.8371 |      0.0056 |
|    3 | accuracy          |    0.8258 |    0.8315 |      0.0056 |
|    4 | accuracy          |    0.8371 |    0.8427 |      0.0056 |
|    5 | accuracy          |    0.8146 |    0.8258 |      0.0112 |
|    1 | balanced_accuracy |    0.8179 |    0.8278 |      0.0099 |
|    2 | balanced_accuracy |    0.8187 |    0.8233 |      0.0045 |
|    3 | balanced_accuracy |    0.7945 |    0.8019 |      0.0074 |
|    4 | balanced_accuracy |    0.8205 |    0.8250 |      0.0045 |
|    5 | balanced_accuracy |    0.7875 |    0.8099 |      0.0225 |
|    1 | precision         |    0.9038 |    0.8909 |     -0.0129 |
|    2 | precision         |    0.7879 |    0.8000 |      0.0121 |
|    3 | precision         |    0.8491 |    0.8519 |      0.0028 |
|    4 | precision         |    0.8095 |    0.8226 |      0.0131 |
|    5 | precision         |    0.8214 |    0.7969 |     -0.0246 |
|    1 | recall            |    0.6812 |    0.7101 |      0.0290 |
|    2 | recall            |    0.7647 |    0.7647 |      0.0000 |
|    3 | recall            |    0.6618 |    0.6765 |      0.0147 |
|    4 | recall            |    0.7500 |    0.7500 |      0.0000 |
|    5 | recall            |    0.6667 |    0.7391 |      0.0725 |
|    1 | f1                |    0.7769 |    0.7903 |      0.0135 |
|    2 | f1                |    0.7761 |    0.7820 |      0.0058 |
|    3 | f1                |    0.7438 |    0.7541 |      0.0103 |
|    4 | f1                |    0.7786 |    0.7846 |      0.0060 |
|    5 | f1                |    0.7360 |    0.7669 |      0.0309 |
|    1 | roc_auc           |    0.9077 |    0.9140 |      0.0063 |
|    2 | roc_auc           |    0.8802 |    0.8779 |     -0.0023 |
|    3 | roc_auc           |    0.8598 |    0.8592 |     -0.0007 |
|    4 | roc_auc           |    0.8717 |    0.8747 |      0.0031 |
|    5 | roc_auc           |    0.8644 |    0.8643 |     -0.0001 |
|    1 | log_loss          |    0.3844 |    0.3786 |      0.0058 |
|    2 | log_loss          |    0.4000 |    0.4027 |     -0.0027 |
|    3 | log_loss          |    0.4407 |    0.4403 |      0.0004 |
|    4 | log_loss          |    0.4036 |    0.3891 |      0.0145 |
|    5 | log_loss          |    0.4217 |    0.4184 |      0.0033 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          12 |                      6 |         5 |           0 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-024/a529898dd4ea/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-024/a529898dd4ea/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-024/a529898dd4ea/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-024/a529898dd4ea/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
