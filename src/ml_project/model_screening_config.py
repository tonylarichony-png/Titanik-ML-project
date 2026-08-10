"""Редактируемый конфиг группового screening моделей для notebook 06."""

from pathlib import Path

from .modeling.contracts import (
    ModelGroupSettings,
    ModelScreeningSettings,
    ScreeningModelSpec,
)


# Все значения ниже — стартовые screening-параметры, а не результат tuning.
# Внутри одного MS-запуска параметры не меняются: так сравнение остаётся честным.
MODEL_GROUPS = {
    "classic_scaled": ModelGroupSettings(
        group_id="classic_scaled",
        title="Масштабируемые классические модели",
        preprocessing_profile="scaled_dense",
        purpose="Проверить линейную границу и локальную геометрию KNN.",
        models=(
            ScreeningModelSpec(
                model_id="linear_reference",
                label="Logistic regression — альтернативная регуляризация",
                params={"C": 0.5, "solver": "liblinear"},
            ),
            ScreeningModelSpec(
                model_id="knn",
                label="K-nearest neighbors",
                params={"n_neighbors": 15, "weights": "distance", "p": 2},
            ),
        ),
    ),
    "tree_bagging": ModelGroupSettings(
        group_id="tree_bagging",
        title="Деревья и bagging",
        preprocessing_profile="unscaled_sparse",
        purpose="Проверить нелинейные зависимости и устойчивые ансамбли деревьев.",
        models=(
            ScreeningModelSpec(
                model_id="decision_tree",
                label="Decision tree",
                params={"max_depth": 5, "min_samples_leaf": 8},
            ),
            ScreeningModelSpec(
                model_id="random_forest",
                label="Random forest",
                params={
                    "n_estimators": 400,
                    "max_depth": 7,
                    "min_samples_leaf": 3,
                    "max_features": "sqrt",
                },
            ),
            ScreeningModelSpec(
                model_id="extra_trees",
                label="Extra Trees",
                params={
                    "n_estimators": 400,
                    "max_depth": 8,
                    "min_samples_leaf": 3,
                    "max_features": "sqrt",
                },
            ),
        ),
    ),
    "sklearn_boosting": ModelGroupSettings(
        group_id="sklearn_boosting",
        title="Boosting из scikit-learn",
        preprocessing_profile="unscaled_dense",
        purpose="Быстрый boosting-screen без внешних библиотек.",
        models=(
            ScreeningModelSpec(
                model_id="hist_gradient_boosting",
                label="Histogram gradient boosting",
                params={"learning_rate": 0.04,
                        "max_iter": 250,
                        "max_leaf_nodes": 15,
                        "early_stopping": True,
                        "n_iter_no_change": 10,
                        "validation_fraction": 0.1,
                        },
            ),
            ScreeningModelSpec(
                model_id="gradient_boosting",
                label="Gradient boosting",
                params={"n_estimators": 300,
                        "learning_rate": 0.03,
                        "max_depth": 2
                        },
            ),
        ),
    ),
    "external_boosting": ModelGroupSettings(
        group_id="external_boosting",
        title="XGBoost и LightGBM",
        preprocessing_profile="unscaled_sparse",
        purpose="Сравнить две внешние реализации градиентного boosting.",
        models=(
            ScreeningModelSpec(
                model_id="xgboost",
                label="XGBoost",
                params={
                    "n_estimators": 350,
                    "learning_rate": 0.04,
                    "max_depth": 3,
                    "subsample": 0.85,
                    "colsample_bytree": 0.85,
                },
            ),
            ScreeningModelSpec(
                model_id="lightgbm",
                label="LightGBM",
                params={
                    "n_estimators": 350,
                    "learning_rate": 0.04,
                    "num_leaves": 15,
                    "max_depth": 5,
                    "subsample": 0.85,
                    "colsample_bytree": 0.85,
                },
            ),
        ),
    ),
    "native_categorical": ModelGroupSettings(
        group_id="native_categorical",
        title="CatBoost с нативными категориями",
        preprocessing_profile="native_categorical",
        purpose="Проверить категории без one-hot encoding.",
        models=(
            ScreeningModelSpec(
                model_id="catboost",
                label="CatBoost",
                params={
                    "iterations": 400,
                    "learning_rate": 0.04,
                    "depth": 5,
                    "l2_leaf_reg": 5.0,
                },
            ),
        ),
    ),
}


SCREENING = ModelScreeningSettings(
    # Новый ID нужен для каждого официально сохранённого группового прогона.
    screening_id="MS-004",
    screening_title="sklearn_boosting with early stopping and validation on EXP-013 TT-combined features",
    screening_note=Path("model-screening/MS-004 sklearn_boosting.md"),

    # Feature set фиксируется модулем принятого чемпиона; EXP-003 включает
    # также всю принятую parent-цепочку EXP-001 → EXP-002 → EXP-003.
    feature_reference_module="ml_project.experiments.exp_013_tt_comb",

    # Для следующей группы меняются active_group, ID, title, note и run_name.
    active_group="sklearn_boosting",
    groups=MODEL_GROUPS,
    reference_model_id="feature_champion",

    # Эта модель получает отдельный график агрегированной importance.
    diagnostic_model_id="hist_gradient_boosting",
    shortlist_size=2,

    run_name="ms_004_sklearn_boosting_v1",
    artifact_dir=Path("artifacts/model-screening"),
    results_registry=Path("model-screening/results.csv"),
    save_artifacts=True,
    save_figures=True,
    figure_dpi=160,
    sync_screening_note=True,
    sync_registry=True,
    allow_overwrite=True,
)


__all__ = ["MODEL_GROUPS", "SCREENING"]
