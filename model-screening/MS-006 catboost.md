---
type: model-screening
id: MS-006
status: completed
decision: pending
feature_reference: EXP-013
model_group: native_categorical
selected_model:
---

# MS-006 — native_categorical on EXP-013 TT-combined features

<!-- auto:model-screening-report:start -->

## Контракт screening

| Поле              | Значение                                                         |
| ----------------- | ---------------------------------------------------------------- |
| Feature reference | EXP-013                                                          |
| Feature module    | ml_project.experiments.exp_013_tt_comb                           |
| Dataset SHA-256   | 7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f |
| Группа            | CatBoost с нативными категориями                                 |
| Preprocessing     | native_categorical                                               |
| Validation        | stratified_kfold(n_splits=5, shuffle=True, seed=42)              |
| Primary metric    | accuracy                                                         |
| Shortlist         | catboost                                                         |

## Результат группы

| Rank | Model            | Metric   | Mean ± std      | Δ vs champion |   Wins |   Ties | Losses | Shortlist |
| ---: | ---------------- | -------- | --------------- | ------------: | -----: | -----: | -----: | --------: |
|    1 | catboost         | accuracy | 0.8372 ± 0.0140 |        0.0247 | 5.0000 | 0.0000 | 0.0000 |      True |
|    2 | feature_champion | accuracy | 0.8126 ± 0.0152 |        0.0000 | 0.0000 | 0.0000 | 0.0000 |     False |

> [!important]
> Screening ранжирует стартовые конфигурации. Он не доказывает, что
> первое место — окончательно лучшая модель: shortlist сначала проходит
> отдельный coarse tuning и диагностику на том же validation contract.

## Параметры запуска

| model_id         | label                      | role                | preprocessing      | params                                                                                                                                                                                                                                                                         |
| ---------------- | -------------------------- | ------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| feature_champion | Feature champion (EXP-013) | fixed_reference     | champion_exact     | {"C": 1.0, "class_weight": null, "dual": false, "fit_intercept": true, "intercept_scaling": 1, "l1_ratio": 0.0, "max_iter": 1000, "n_jobs": null, "penalty": "deprecated", "random_state": 42, "solver": "lbfgs", "tol": 0.0001, "verbose": 0, "warm_start": false}            |
| catboost         | CatBoost                   | screening_candidate | native_categorical | {"params": {"allow_writing_files": false, "cat_features": ["Embarked", "FamilySizeGroup", "IsnotAlone", "CabinKnown", "Deck", "SexPclass"], "depth": 5, "iterations": 400, "l2_leaf_reg": 5.0, "learning_rate": 0.04, "random_seed": 42, "thread_count": 1, "verbose": false}} |

## OOF-сравнение с feature champion

| model    | rows | agreement_share | candidate_accuracy | reference_accuracy | corrected_errors | new_errors |
| -------- | ---: | --------------: | -----------------: | -----------------: | ---------------: | ---------: |
| catboost |  891 |          0.9237 |             0.8373 |             0.8126 |               45 |         23 |

## Графики

![[assets/model-screening/MS-006/metric-primary-accuracy.png]]

![[assets/model-screening/MS-006/metric-secondary_1-balanced-accuracy.png]]

![[assets/model-screening/MS-006/metric-secondary_2-precision.png]]

![[assets/model-screening/MS-006/metric-secondary_3-recall.png]]

![[assets/model-screening/MS-006/metric-secondary_4-f1.png]]

![[assets/model-screening/MS-006/metric-secondary_5-roc-auc.png]]

![[assets/model-screening/MS-006/ranking-primary.png]]

![[assets/model-screening/MS-006/paired-primary-delta.png]]

![[assets/model-screening/MS-006/importance-catboost.png]]

![[assets/model-screening/MS-006/boosting-log-loss.png]]

<!-- auto:model-screening-report:end -->

## Интерпретация

- Что устойчиво по folds:
- Где модель исправляет / создаёт ошибки:
- Какие параметры ещё не исследованы:

## Решение

- Какие модели переходят в coarse tuning:
- Почему:
- Что запускаем следующим:
