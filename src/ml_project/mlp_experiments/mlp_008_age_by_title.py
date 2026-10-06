"""MLP-008: fold-safe Age imputation by normalized passenger title."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
from torch import nn

from ml_project.mlp_experiment import (
    MLPExperimentSpec,
    MLPFeatureData,
    MLPTrainingConfig,
)


EXPERIMENT = MLPExperimentSpec(
    experiment_id='MLP-008',
    title="Заполнение Age медианой по Title",
    hypothesis=(
        "Если заполнять пропуски Age медианой возраста пассажиров с тем же "
        "нормализованным Title внутри train-fold, то MLP точнее учтёт возрастные "
        "различия между Mr, Mrs, Miss и Master."
    ),
    change_description=(
        "Относительно принятого MLP-002 изменяется только заполнение Age: "
        "медиана по Title с fallback на общую медиану train-fold."
    ),
    experiment_note=Path("mlp-experiments/MLP-008 Age median by Title.md"),
    n_splits=5,
    primary_metric="accuracy",
    primary_improvement_min=0.0,
    metric_guardrails={
        "balanced_accuracy": 0.0,
        "recall": -0.01,
        "f1": 0.0,
    },
    parent_mlp_module='ml_project.mlp_experiments.mlp_002_mlp_8neurons_feng',
    sklearn_reference_module=None,
    save_artifacts=True,
    sync_docs=True,
    training=MLPTrainingConfig(
        # Fold-safe preprocessing. Change one choice per experiment.
        numeric_imputer="median",       # mean | median | most_frequent
        categorical_imputer="most_frequent",  # most_frequent | constant
        numeric_scaler="standard",      # standard | none

        # Optimization.
        batch_size=32,
        learning_rate=1e-3,
        weight_decay=0.0,
        max_epochs=100,
        patience=12,
        min_delta=1e-4,
        inner_validation_fraction=0.15,
        threshold=0.5,
        random_state=42,
        device="cpu",
    ),
)


def normalized_titles(frame: pd.DataFrame) -> pd.Series:
    """Extract stable title groups using values from the same passenger only."""

    titles = (
        frame["Name"]
        .astype("string")
        .str.extract(r",\s*([^.]*)\.", expand=False)
        .str.strip()
    )
    main_titles = {"Mr", "Mrs", "Miss", "Master"}
    rare = ~titles.isin(main_titles)
    titles = titles.copy()
    titles.loc[rare & frame["Sex"].eq("male")] = "Mr"
    titles.loc[rare & frame["Sex"].eq("female")] = "Mrs"
    return titles.fillna("Unknown")


class AgeByTitleMedianImputer(BaseEstimator, TransformerMixin):
    """Learn Title-specific Age medians from one train fold."""

    def fit(self, frame: pd.DataFrame, y=None):
        known_age = frame.loc[frame["Age"].notna(), ["Title", "Age"]]
        if known_age.empty:
            raise ValueError("Нет известных значений Age для обучения imputer.")
        self.title_medians_ = known_age.groupby("Title", observed=True)["Age"].median()
        self.global_median_ = float(known_age["Age"].median())
        return self

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(self, ["title_medians_", "global_median_"])
        result = frame.copy(deep=True)
        missing_age = result["Age"].isna()
        if missing_age.any():
            fill_values = (
                result.loc[missing_age, "Title"]
                .map(self.title_medians_)
                .fillna(self.global_median_)
            )
            result.loc[missing_age, "Age"] = fill_values.astype(float)
        return result


def prepare_features(frame: pd.DataFrame) -> MLPFeatureData:
    """Create row-local features and declare their preprocessing roles."""

    result = frame.copy(deep=True)
    result["Title"] = normalized_titles(result)

    numeric_features = (
        "Age",
        "Fare",
        "SibSp",
        "Parch",
    )
    categorical_features = (
        "Sex",
        "Embarked",
        "Pclass",
    )
    return MLPFeatureData(
        frame=result,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        fold_generated_features=(),
    )


def build_fold_transformer():
    """Return a fresh imputer whose medians are fitted inside each train fold."""

    return AgeByTitleMedianImputer()


def build_network(input_dim: int) -> nn.Module:
    """Return one fresh network that emits one raw logit per passenger."""

    # EDIT HERE — add/remove hidden layers, activations or Dropout.
    # Keep input_dim on the first Linear and one output on the last Linear.
    return nn.Sequential(
        nn.Linear(input_dim, 8),
        nn.ReLU(),
        nn.Linear(8, 1),
    )


__all__ = [
    "AgeByTitleMedianImputer",
    "EXPERIMENT",
    "build_fold_transformer",
    "build_network",
    "normalized_titles",
    "prepare_features",
]
