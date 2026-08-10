---
type: model-screening
id: MS-001
status: completed
decision: pending
feature_reference: EXP-003
model_group: tree_bagging
selected_model:
---

# MS-001 — Tree and bagging screening on EXP-003 features

<!-- auto:model-screening-report:start -->

## Контракт screening

| Поле              | Значение                                                         |
| ----------------- | ---------------------------------------------------------------- |
| Feature reference | EXP-003                                                          |
| Feature module    | ml_project.experiments.exp_003_family_size                       |
| Dataset SHA-256   | 7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f |
| Группа            | Деревья и bagging                                                |
| Preprocessing     | unscaled_sparse                                                  |
| Validation        | stratified_kfold(n_splits=5, shuffle=True, seed=42)              |
| Primary metric    | accuracy                                                         |
| Shortlist         | random_forest, extra_trees                                       |

## Результат группы

| Rank | Model            | Metric   | Mean ± std      | Δ vs champion |   Wins |   Ties | Losses | Shortlist |
| ---: | ---------------- | -------- | --------------- | ------------: | -----: | -----: | -----: | --------: |
|    1 | random_forest    | accuracy | 0.8227 ± 0.0123 |        0.0022 | 3.0000 | 0.0000 | 2.0000 |      True |
|    2 | feature_champion | accuracy | 0.8204 ± 0.0176 |        0.0000 | 0.0000 | 0.0000 | 0.0000 |     False |
|    3 | extra_trees      | accuracy | 0.8070 ± 0.0148 |       -0.0135 | 1.0000 | 1.0000 | 3.0000 |      True |
|    4 | decision_tree    | accuracy | 0.8036 ± 0.0225 |       -0.0168 | 0.0000 | 0.0000 | 5.0000 |     False |

> [!important]
> Screening ранжирует стартовые конфигурации. Он не доказывает, что
> первое место — окончательно лучшая модель: shortlist сначала проходит
> отдельный coarse tuning и диагностику на том же validation contract.

## Параметры запуска

| model_id         | label                      | role                | preprocessing   | params                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------------- | -------------------------- | ------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| feature_champion | Feature champion (EXP-003) | fixed_reference     | champion_exact  | {"C": 1.0, "class_weight": null, "dual": false, "fit_intercept": true, "intercept_scaling": 1, "l1_ratio": 0.0, "max_iter": 1000, "n_jobs": null, "penalty": "deprecated", "random_state": 42, "solver": "lbfgs", "tol": 0.0001, "verbose": 0, "warm_start": false}                                                                                                                                                      |
| decision_tree    | Decision tree              | screening_candidate | unscaled_sparse | {"ccp_alpha": 0.0, "class_weight": null, "criterion": "gini", "max_depth": 5, "max_features": null, "max_leaf_nodes": null, "min_impurity_decrease": 0.0, "min_samples_leaf": 8, "min_samples_split": 2, "min_weight_fraction_leaf": 0.0, "monotonic_cst": null, "random_state": 42, "splitter": "best"}                                                                                                                 |
| random_forest    | Random forest              | screening_candidate | unscaled_sparse | {"bootstrap": true, "ccp_alpha": 0.0, "class_weight": null, "criterion": "gini", "max_depth": 7, "max_features": "sqrt", "max_leaf_nodes": null, "max_samples": null, "min_impurity_decrease": 0.0, "min_samples_leaf": 3, "min_samples_split": 2, "min_weight_fraction_leaf": 0.0, "monotonic_cst": null, "n_estimators": 400, "n_jobs": 1, "oob_score": false, "random_state": 42, "verbose": 0, "warm_start": false}  |
| extra_trees      | Extra Trees                | screening_candidate | unscaled_sparse | {"bootstrap": false, "ccp_alpha": 0.0, "class_weight": null, "criterion": "gini", "max_depth": 8, "max_features": "sqrt", "max_leaf_nodes": null, "max_samples": null, "min_impurity_decrease": 0.0, "min_samples_leaf": 3, "min_samples_split": 2, "min_weight_fraction_leaf": 0.0, "monotonic_cst": null, "n_estimators": 400, "n_jobs": 1, "oob_score": false, "random_state": 42, "verbose": 0, "warm_start": false} |

## OOF-сравнение с feature champion

| model         | rows | agreement_share | candidate_accuracy | reference_accuracy | corrected_errors | new_errors |
| ------------- | ---: | --------------: | -----------------: | -----------------: | ---------------: | ---------: |
| decision_tree |  891 |          0.9091 |             0.8036 |             0.8204 |               33 |         48 |
| random_forest |  891 |          0.9349 |             0.8227 |             0.8204 |               30 |         28 |
| extra_trees   |  891 |          0.9282 |             0.8070 |             0.8204 |               26 |         38 |

## Графики

![[assets/model-screening/MS-001/metric-primary-accuracy.png]]

![[assets/model-screening/MS-001/metric-secondary_1-balanced-accuracy.png]]

![[assets/model-screening/MS-001/metric-secondary_2-precision.png]]

![[assets/model-screening/MS-001/metric-secondary_3-recall.png]]

![[assets/model-screening/MS-001/metric-secondary_4-f1.png]]

![[assets/model-screening/MS-001/metric-secondary_5-roc-auc.png]]

![[assets/model-screening/MS-001/ranking-primary.png]]

![[assets/model-screening/MS-001/paired-primary-delta.png]]

![[assets/model-screening/MS-001/importance-random_forest.png]]

<!-- auto:model-screening-report:end -->

## Интерпретация

- Что устойчиво по folds:
- Где модель исправляет / создаёт ошибки:
- Какие параметры ещё не исследованы:

## Решение

- Какие модели переходят в coarse tuning:
- Почему:
- Что запускаем следующим:
