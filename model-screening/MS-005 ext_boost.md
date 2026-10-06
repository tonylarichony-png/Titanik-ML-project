---
type: model-screening
id: MS-005
status: completed
decision: pending
feature_reference: EXP-013
model_group: external_boosting
selected_model:
---

# MS-005 — external_boosting  on EXP-013 TT-combined features

<!-- auto:model-screening-report:start -->

## Контракт screening

| Поле              | Значение                                                         |
| ----------------- | ---------------------------------------------------------------- |
| Feature reference | EXP-013                                                          |
| Feature module    | ml_project.experiments.exp_013_tt_comb                           |
| Dataset SHA-256   | 7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f |
| Группа            | XGBoost и LightGBM                                               |
| Preprocessing     | unscaled_sparse                                                  |
| Validation        | stratified_kfold(n_splits=5, shuffle=True, seed=42)              |
| Primary metric    | accuracy                                                         |
| Shortlist         | xgboost, lightgbm                                                |

## Результат группы

| Rank | Model            | Metric   | Mean ± std      | Δ vs champion |   Wins |   Ties | Losses | Shortlist |
| ---: | ---------------- | -------- | --------------- | ------------: | -----: | -----: | -----: | --------: |
|    1 | xgboost          | accuracy | 0.8417 ± 0.0176 |        0.0292 | 4.0000 | 1.0000 | 0.0000 |      True |
|    2 | lightgbm         | accuracy | 0.8417 ± 0.0157 |        0.0292 | 5.0000 | 0.0000 | 0.0000 |      True |
|    3 | feature_champion | accuracy | 0.8126 ± 0.0152 |        0.0000 | 0.0000 | 0.0000 | 0.0000 |     False |

> [!important]
> Screening ранжирует стартовые конфигурации. Он не доказывает, что
> первое место — окончательно лучшая модель: shortlist сначала проходит
> отдельный coarse tuning и диагностику на том же validation contract.

## Параметры запуска

| model_id         | label                      | role                | preprocessing   | params                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---------------- | -------------------------- | ------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| feature_champion | Feature champion (EXP-013) | fixed_reference     | champion_exact  | {"C": 1.0, "class_weight": null, "dual": false, "fit_intercept": true, "intercept_scaling": 1, "l1_ratio": 0.0, "max_iter": 1000, "n_jobs": null, "penalty": "deprecated", "random_state": 42, "solver": "lbfgs", "tol": 0.0001, "verbose": 0, "warm_start": false}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| xgboost          | XGBoost                    | screening_candidate | unscaled_sparse | {"base_score": null, "booster": null, "callbacks": null, "colsample_bylevel": null, "colsample_bynode": null, "colsample_bytree": 0.85, "device": null, "early_stopping_rounds": null, "enable_categorical": true, "eval_metric": "logloss", "feature_types": null, "feature_weights": null, "gamma": null, "grow_policy": null, "importance_type": null, "interaction_constraints": null, "learning_rate": 0.04, "max_bin": null, "max_cat_threshold": null, "max_cat_to_onehot": null, "max_delta_step": null, "max_depth": 3, "max_leaves": null, "min_child_weight": null, "missing": NaN, "monotone_constraints": null, "multi_strategy": null, "n_estimators": 350, "n_jobs": 1, "num_parallel_tree": null, "objective": "binary:logistic", "random_state": 42, "reg_alpha": null, "reg_lambda": null, "sampling_method": null, "scale_pos_weight": null, "subsample": 0.85, "tree_method": "hist", "validate_parameters": null, "verbosity": null} |
| lightgbm         | LightGBM                   | screening_candidate | unscaled_sparse | {"boosting_type": "gbdt", "class_weight": null, "colsample_bytree": 0.85, "importance_type": "split", "learning_rate": 0.04, "max_depth": 5, "min_child_samples": 20, "min_child_weight": 0.001, "min_split_gain": 0.0, "n_estimators": 350, "n_jobs": 1, "num_leaves": 15, "objective": null, "random_state": 42, "reg_alpha": 0.0, "reg_lambda": 0.0, "subsample": 0.85, "subsample_for_bin": 200000, "subsample_freq": 0, "verbosity": -1}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

## OOF-сравнение с feature champion

| model    | rows | agreement_share | candidate_accuracy | reference_accuracy | corrected_errors | new_errors |
| -------- | ---: | --------------: | -----------------: | -----------------: | ---------------: | ---------: |
| xgboost  |  891 |          0.9147 |             0.8418 |             0.8126 |               51 |         25 |
| lightgbm |  891 |          0.9057 |             0.8418 |             0.8126 |               55 |         29 |

## Графики

![[assets/model-screening/MS-005/metric-primary-accuracy.png]]

![[assets/model-screening/MS-005/metric-secondary_1-balanced-accuracy.png]]

![[assets/model-screening/MS-005/metric-secondary_2-precision.png]]

![[assets/model-screening/MS-005/metric-secondary_3-recall.png]]

![[assets/model-screening/MS-005/metric-secondary_4-f1.png]]

![[assets/model-screening/MS-005/metric-secondary_5-roc-auc.png]]

![[assets/model-screening/MS-005/ranking-primary.png]]

![[assets/model-screening/MS-005/paired-primary-delta.png]]

![[assets/model-screening/MS-005/importance-lightgbm.png]]

![[assets/model-screening/MS-005/boosting-log-loss.png]]

<!-- auto:model-screening-report:end -->

## Интерпретация

- Что устойчиво по folds:
- Где модель исправляет / создаёт ошибки:
- Какие параметры ещё не исследованы:

## Решение

- Какие модели переходят в coarse tuning:
- Почему:
- Что запускаем следующим:
