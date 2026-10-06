---
id: ENS-003
type: ensemble-experiment
status: completed
decision: pending
primary_metric: accuracy
---

# ENS-003 — Nested-CV learned weights for four strong models

## Гипотеза

Модели разных семейств совершают разные ошибки, поэтому среднее их OOF-вероятностей может быть точнее лучшей одиночной модели.

## Состав

- `xgboost` — MS-005
- `lightgbm` — MS-005
- `catboost` — MS-006
- `mlp_024` — MLP-024

Все модели переобучены на одних и тех же пяти `StratifiedKFold` (`shuffle=True`, `seed=42`). Веса обучены отдельно внутри каждого outer train fold на 4 внутренних OOF folds по log loss. Порог — `0.5`.

## Результат

- Ensemble accuracy: **0.8406 ± 0.0218**
- Лучший одиночный участник этого же запуска: **xgboost**, 0.8417 ± 0.0176
- Разница ensemble: **-0.0011**
- Ensemble ROC-AUC: **0.8847**; лучший одиночный ROC-AUC: **0.8871**.
- Ensemble log loss: **0.3869**; лучший одиночный log loss: **0.3869**.
- Решение оставлено `pending`: сначала проверить таблицы разнообразия и только затем выбрать `adopt` или `reject`.

## Обученные веса

| Outer fold | XGBoost | LightGBM | CatBoost | MLP-024 |
|---:|---:|---:|---:|---:|
| 1 | 0.422 | 0.000 | 0.369 | 0.209 |
| 2 | 0.000 | 0.000 | 0.668 | 0.332 |
| 3 | 0.668 | 0.066 | 0.087 | 0.179 |
| 4 | 0.165 | 0.000 | 0.407 | 0.429 |
| 5 | 0.000 | 0.000 | 0.675 | 0.325 |

## Интерпретация

- Оптимизатор почти полностью исключил LightGBM: его вес равен нулю в четырёх folds и только `0.066` в третьем. Это согласуется с высокой корреляцией LightGBM и XGBoost: отдельной информации мало.
- MLP-024 получила устойчивый ненулевой вес `0.179–0.429`. Значит, её отличающиеся ошибки действительно полезны, хотя равный вес `0.25` в ENS-002 работал плохо.
- Веса XGBoost и CatBoost сильно меняются между folds. На 891 строке точное соотношение между похожими бустингами определяется нестабильно.
- Nested weighting восстановил accuracy ENS-002 с `0.8294` до `0.8406`, но не превзошёл одиночный XGBoost `0.8417`. Преимущество learned stacking по основной метрике пока не подтверждено.

## Артефакты

- [[artifacts/ensembles/ENS-003/summary.csv|summary.csv]]
- [[artifacts/ensembles/ENS-003/fold_metrics.csv|fold_metrics.csv]]
- [[artifacts/ensembles/ENS-003/oof_predictions.csv|oof_predictions.csv]]
- [[artifacts/ensembles/ENS-003/probability_correlations.csv|probability_correlations.csv]]
- [[artifacts/ensembles/ENS-003/prediction_disagreements.csv|prediction_disagreements.csv]]
- [[artifacts/ensembles/ENS-003/error_overlap.csv|error_overlap.csv]]
- [[artifacts/ensembles/ENS-003/learned_weights.csv|learned_weights.csv]]
- [[artifacts/ensembles/ENS-003/metadata.json|metadata.json]]
