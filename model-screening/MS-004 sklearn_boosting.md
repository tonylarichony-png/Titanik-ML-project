---
type: model-screening
id: MS-004
status: completed
decision: pending
feature_reference: EXP-013
model_group: sklearn_boosting
selected_model:
---

# MS-004 — sklearn_boosting with early stopping and validation on EXP-013 TT-combined features

<!-- auto:model-screening-report:start -->

## Контракт screening

| Поле              | Значение                                                         |
| ----------------- | ---------------------------------------------------------------- |
| Feature reference | EXP-013                                                          |
| Feature module    | ml_project.experiments.exp_013_tt_comb                           |
| Dataset SHA-256   | 7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f |
| Группа            | Boosting из scikit-learn                                         |
| Preprocessing     | unscaled_dense                                                   |
| Validation        | stratified_kfold(n_splits=5, shuffle=True, seed=42)              |
| Primary metric    | accuracy                                                         |
| Shortlist         | hist_gradient_boosting, gradient_boosting                        |

## Результат группы

| Rank | Model                  | Metric   | Mean ± std      | Δ vs champion |   Wins |   Ties | Losses | Shortlist |
| ---: | ---------------------- | -------- | --------------- | ------------: | -----: | -----: | -----: | --------: |
|    1 | hist_gradient_boosting | accuracy | 0.8350 ± 0.0213 |        0.0224 | 3.0000 | 1.0000 | 1.0000 |      True |
|    2 | gradient_boosting      | accuracy | 0.8350 ± 0.0199 |        0.0224 | 5.0000 | 0.0000 | 0.0000 |      True |
|    3 | feature_champion       | accuracy | 0.8126 ± 0.0152 |        0.0000 | 0.0000 | 0.0000 | 0.0000 |     False |

> [!important]
> Screening ранжирует стартовые конфигурации. Он не доказывает, что
> первое место — окончательно лучшая модель: shortlist сначала проходит
> отдельный coarse tuning и диагностику на том же validation contract.

## Параметры запуска

| model_id               | label                       | role                | preprocessing  | params                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------- | --------------------------- | ------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| feature_champion       | Feature champion (EXP-013)  | fixed_reference     | champion_exact | {"C": 1.0, "class_weight": null, "dual": false, "fit_intercept": true, "intercept_scaling": 1, "l1_ratio": 0.0, "max_iter": 1000, "n_jobs": null, "penalty": "deprecated", "random_state": 42, "solver": "lbfgs", "tol": 0.0001, "verbose": 0, "warm_start": false}                                                                                                                                                                                                           |
| hist_gradient_boosting | Histogram gradient boosting | screening_candidate | unscaled_dense | {"categorical_features": "from_dtype", "class_weight": null, "early_stopping": true, "interaction_cst": null, "l2_regularization": 0.0, "learning_rate": 0.04, "loss": "log_loss", "max_bins": 255, "max_depth": null, "max_features": 1.0, "max_iter": 250, "max_leaf_nodes": 15, "min_samples_leaf": 20, "monotonic_cst": null, "n_iter_no_change": 10, "random_state": 42, "scoring": "loss", "tol": 1e-07, "validation_fraction": 0.1, "verbose": 0, "warm_start": false} |
| gradient_boosting      | Gradient boosting           | screening_candidate | unscaled_dense | {"ccp_alpha": 0.0, "criterion": "deprecated", "init": null, "learning_rate": 0.03, "loss": "log_loss", "max_depth": 2, "max_features": null, "max_leaf_nodes": null, "min_impurity_decrease": 0.0, "min_samples_leaf": 1, "min_samples_split": 2, "min_weight_fraction_leaf": 0.0, "n_estimators": 300, "n_iter_no_change": null, "random_state": 42, "subsample": 1.0, "tol": 0.0001, "validation_fraction": 0.1, "verbose": 0, "warm_start": false}                         |

## OOF-сравнение с feature champion

| model                  | rows | agreement_share | candidate_accuracy | reference_accuracy | corrected_errors | new_errors |
| ---------------------- | ---: | --------------: | -----------------: | -----------------: | ---------------: | ---------: |
| hist_gradient_boosting |  891 |          0.9192 |             0.8350 |             0.8126 |               46 |         26 |
| gradient_boosting      |  891 |          0.9349 |             0.8350 |             0.8126 |               39 |         19 |

## Графики

![[assets/model-screening/MS-004/metric-primary-accuracy.png]]

![[assets/model-screening/MS-004/metric-secondary_1-balanced-accuracy.png]]

![[assets/model-screening/MS-004/metric-secondary_2-precision.png]]

![[assets/model-screening/MS-004/metric-secondary_3-recall.png]]

![[assets/model-screening/MS-004/metric-secondary_4-f1.png]]

![[assets/model-screening/MS-004/metric-secondary_5-roc-auc.png]]

![[assets/model-screening/MS-004/ranking-primary.png]]

![[assets/model-screening/MS-004/paired-primary-delta.png]]

![[assets/model-screening/MS-004/boosting-log-loss.png]]

<!-- auto:model-screening-report:end -->

## Интерпретация

- Что устойчиво по folds:
- Где модель исправляет / создаёт ошибки:
- Какие параметры ещё не исследованы:

## Решение

- Какие модели переходят в coarse tuning:
- Почему:
- Что запускаем следующим:
