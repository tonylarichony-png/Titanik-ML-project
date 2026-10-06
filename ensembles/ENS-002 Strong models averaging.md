---
id: ENS-002
type: ensemble-experiment
status: completed
decision: pending
primary_metric: accuracy
---

# ENS-002 — Probability averaging of XGBoost, LightGBM, CatBoost and MLP-024

## Гипотеза

Модели разных семейств совершают разные ошибки, поэтому среднее их OOF-вероятностей может быть точнее лучшей одиночной модели.

## Состав

- `xgboost` — MS-005
- `lightgbm` — MS-005
- `catboost` — MS-006
- `mlp_024` — MLP-024

Все модели переобучены на одних и тех же пяти `StratifiedKFold` (`shuffle=True`, `seed=42`). Итоговая вероятность — простое среднее 4 вероятностей, порог — `0.5`.

## Результат

- Ensemble accuracy: **0.8294 ± 0.0207**
- Лучший одиночный участник этого же запуска: **xgboost**, 0.8417 ± 0.0176
- Разница ensemble: **-0.0124**
- Ensemble ROC-AUC: **0.8856**; лучший одиночный ROC-AUC: **0.8871**.
- Ensemble log loss: **0.3865**; лучший одиночный log loss: **0.3869**.
- Решение оставлено `pending`: сначала проверить таблицы разнообразия и только затем выбрать `adopt` или `reject`.

## Интерпретация

- Одинаковая accuracy XGBoost и LightGBM не означает одинаковые модели: их итоговые классы расходятся на **2.92%** строк.
- Корреляция их вероятностей очень высокая — **0.9873**, а Jaccard-пересечение ошибок — **0.8312**. Поэтому две модели вносят мало независимой информации.
- Усреднение предсказало класс `1` для 292 пассажиров; одиночные модели — для 293–305, при 342 фактических единицах. На пороге `0.5` ансамбль потерял recall и accuracy.
- Более низкий log loss показывает, что сами вероятности получились полезными. Подбор порога должен быть отдельным заранее заданным экспериментом или выполняться во вложенной validation, иначе возникнет оптимистичная подгонка по тем же OOF-ответам.

## Артефакты

- [[artifacts/ensembles/ENS-002/summary.csv|summary.csv]]
- [[artifacts/ensembles/ENS-002/fold_metrics.csv|fold_metrics.csv]]
- [[artifacts/ensembles/ENS-002/oof_predictions.csv|oof_predictions.csv]]
- [[artifacts/ensembles/ENS-002/probability_correlations.csv|probability_correlations.csv]]
- [[artifacts/ensembles/ENS-002/prediction_disagreements.csv|prediction_disagreements.csv]]
- [[artifacts/ensembles/ENS-002/error_overlap.csv|error_overlap.csv]]
- [[artifacts/ensembles/ENS-002/metadata.json|metadata.json]]
