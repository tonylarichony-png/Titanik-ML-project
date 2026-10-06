---
id: ENS-001
type: ensemble-experiment
status: completed
decision: pending
primary_metric: accuracy
---

# ENS-001 — Probability averaging of five diverse models

## Гипотеза

Модели разных семейств совершают разные ошибки, поэтому среднее их OOF-вероятностей может быть точнее лучшей одиночной модели.

## Состав

- `logistic_regression` — EXP-013 feature champion
- `random_forest` — MS-002
- `xgboost` — MS-005
- `catboost` — MS-006
- `mlp_024` — MLP-024

Все модели переобучены на одних и тех же пяти `StratifiedKFold` (`shuffle=True`, `seed=42`). Итоговая вероятность — простое среднее 5 вероятностей, порог — `0.5`.

## Результат

- Ensemble accuracy: **0.8395 ± 0.0232**
- Лучший одиночный участник этого же запуска: **xgboost**, 0.8417 ± 0.0176
- Разница ensemble: **-0.0023**
- Ensemble ROC-AUC: **0.8843**; лучший одиночный ROC-AUC: **0.8871**.
- Ensemble log loss: **0.3901**; лучший одиночный log loss: **0.3869**.
- Решение оставлено `pending`: сначала проверить таблицы разнообразия и только затем выбрать `adopt` или `reject`.

## Артефакты

- [[artifacts/ensembles/ENS-001/summary.csv|summary.csv]]
- [[artifacts/ensembles/ENS-001/fold_metrics.csv|fold_metrics.csv]]
- [[artifacts/ensembles/ENS-001/oof_predictions.csv|oof_predictions.csv]]
- [[artifacts/ensembles/ENS-001/probability_correlations.csv|probability_correlations.csv]]
- [[artifacts/ensembles/ENS-001/prediction_disagreements.csv|prediction_disagreements.csv]]
- [[artifacts/ensembles/ENS-001/error_overlap.csv|error_overlap.csv]]
- [[artifacts/ensembles/ENS-001/metadata.json|metadata.json]]
