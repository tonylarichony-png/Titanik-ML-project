---
id: MLP-023
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_023_dpoutlight
---

# MLP-023 — Dpoutlight

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент      | MLP-023 — Dpoutlight                                                                                                                                                      |
| Гипотеза         | CHANGE ME — if добавить слой дропаут, then сеть станет более устойчивой к переобучению,Усилит влияние задавленных признаков because заглушит часть параметров на обучении |
| Одно изменение   | CHANGE ME — exactly one controlled change                                                                                                                                 |
| Решение          | reject |
| Reference        | MLP-018_reference: ml_project.mlp_experiments.mlp_018_allin161616                                                                                                         |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                       |
| Основная метрика | accuracy                                                                                                                                                                  |
| Критерии         | failed                                                                                                                                                                    |
| Код              | ml_project.mlp_experiments.mlp_023_dpoutlight                                                                                                                             |
| Hash кода        | e93f59f057da…                                                                                                                                                             |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0023 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0024 |              0.0000 |  False |
| guardrail | recall            |              -0.0030 |             -0.0100 |   True |
| guardrail | f1                |              -0.0030 |              0.0000 |  False |

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
| mlp_candidate     | accuracy          | 0.8294 | 0.0155 | 0.8146 | 0.8547 |
| mlp_candidate     | balanced_accuracy | 0.8054 | 0.0169 | 0.7854 | 0.8251 |
| mlp_candidate     | precision         | 0.8303 | 0.0458 | 0.7879 | 0.9057 |
| mlp_candidate     | recall            | 0.7019 | 0.0424 | 0.6618 | 0.7647 |
| mlp_candidate     | f1                | 0.7593 | 0.0230 | 0.7317 | 0.7869 |
| mlp_candidate     | roc_auc           | 0.8775 | 0.0201 | 0.8606 | 0.9107 |
| mlp_candidate     | log_loss          | 0.4085 | 0.0244 | 0.3801 | 0.4435 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8492 |    0.8547 |      0.0056 |
|    2 | accuracy          |    0.8315 |    0.8315 |      0.0000 |
|    3 | accuracy          |    0.8258 |    0.8146 |     -0.0112 |
|    4 | accuracy          |    0.8371 |    0.8258 |     -0.0112 |
|    5 | accuracy          |    0.8146 |    0.8202 |      0.0056 |
|    1 | balanced_accuracy |    0.8179 |    0.8251 |      0.0072 |
|    2 | balanced_accuracy |    0.8187 |    0.8187 |      0.0000 |
|    3 | balanced_accuracy |    0.7945 |    0.7854 |     -0.0091 |
|    4 | balanced_accuracy |    0.8205 |    0.8057 |     -0.0147 |
|    5 | balanced_accuracy |    0.7875 |    0.7920 |      0.0046 |
|    1 | precision         |    0.9038 |    0.9057 |      0.0018 |
|    2 | precision         |    0.7879 |    0.7879 |      0.0000 |
|    3 | precision         |    0.8491 |    0.8182 |     -0.0309 |
|    4 | precision         |    0.8095 |    0.8033 |     -0.0062 |
|    5 | precision         |    0.8214 |    0.8364 |      0.0149 |
|    1 | recall            |    0.6812 |    0.6957 |      0.0145 |
|    2 | recall            |    0.7647 |    0.7647 |      0.0000 |
|    3 | recall            |    0.6618 |    0.6618 |      0.0000 |
|    4 | recall            |    0.7500 |    0.7206 |     -0.0294 |
|    5 | recall            |    0.6667 |    0.6667 |      0.0000 |
|    1 | f1                |    0.7769 |    0.7869 |      0.0100 |
|    2 | f1                |    0.7761 |    0.7761 |      0.0000 |
|    3 | f1                |    0.7438 |    0.7317 |     -0.0121 |
|    4 | f1                |    0.7786 |    0.7597 |     -0.0189 |
|    5 | f1                |    0.7360 |    0.7419 |      0.0059 |
|    1 | roc_auc           |    0.9077 |    0.9107 |      0.0030 |
|    2 | roc_auc           |    0.8802 |    0.8798 |     -0.0004 |
|    3 | roc_auc           |    0.8598 |    0.8606 |      0.0008 |
|    4 | roc_auc           |    0.8717 |    0.8723 |      0.0007 |
|    5 | roc_auc           |    0.8644 |    0.8638 |     -0.0007 |
|    1 | log_loss          |    0.3844 |    0.3801 |      0.0043 |
|    2 | log_loss          |    0.4000 |    0.4005 |     -0.0005 |
|    3 | log_loss          |    0.4407 |    0.4435 |     -0.0028 |
|    4 | log_loss          |    0.4036 |    0.3975 |      0.0061 |
|    5 | log_loss          |    0.4217 |    0.4212 |      0.0006 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                           3 |                      5 |         2 |           2 |    1 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-023/e93f59f057da/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-023/e93f59f057da/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-023/e93f59f057da/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-023/e93f59f057da/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Почему получился такой результат:
- Какие ошибки исправлены / добавлены:
- Что видно по кривым обучения:
- Следующий контролируемый эксперимент:
