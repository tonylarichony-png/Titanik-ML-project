"""MLP-001: First reproducible MLP baseline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from torch import nn

from ml_project.mlp_experiment import (
    MLPExperimentSpec,
    MLPFeatureData,
    MLPTrainingConfig,
)


EXPERIMENT = MLPExperimentSpec(
    experiment_id='MLP-001',
    title='First reproducible MLP baseline',
    hypothesis=(
        "Если обучить небольшой MLP на базовых Titanic-признаках, то получим "
        "воспроизводимую нейросетевую точку отсчёта для следующих изменений."
    ),
    change_description=(
        "Первый PyTorch baseline: 7 исходных признаков, один скрытый слой из "
        "32 нейронов и fold-safe preprocessing."
    ),
    experiment_note=Path("mlp-experiments/MLP-001 Baseline.md"),
    n_splits=5,
    primary_metric="accuracy",
    primary_improvement_min=0.0,
    metric_guardrails={
        "balanced_accuracy": 0.0,
        "recall": -0.01,
        "f1": 0.0,
    },
    parent_mlp_module=None,
    sklearn_reference_module="ml_project.experiments.exp_013_tt_comb",
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


def prepare_features(frame: pd.DataFrame) -> MLPFeatureData:
    """Create row-local features and declare their preprocessing roles."""

    result = frame.copy(deep=True)

    # EDIT HERE — deterministic row-local feature engineering.
    # Examples:
    # result["FamilySize"] = result["SibSp"] + result["Parch"] + 1
    # result["IsAlone"] = (result["FamilySize"] == 1).astype("int64")
    # result["Title"] = result["Name"].str.extract(r",\s*([^.]*)\.", expand=False)

    numeric_features = (
        "Age",
        "Fare",
        "SibSp",
        "Parch",
        # "FamilySize",
    )
    categorical_features = (
        "Sex",
        "Embarked",
        "Pclass",
        # "IsAlone",
        # "Title",
    )
    return MLPFeatureData(
        frame=result,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        # Признаки, которые создаст build_fold_transformer:
        fold_generated_features=(),
    )


def build_fold_transformer():
    """Return a fresh fitted-per-fold transformer, or None."""

    # EDIT HERE для признаков, которым нужны статистики других строк.
    # Transformer должен реализовать fit(DataFrame) и transform(DataFrame),
    # вернуть DataFrame с тем же index и создать все признаки из
    # fold_generated_features. Пример TicketGroupSize:
    #
    # class TicketGroupSize(BaseEstimator, TransformerMixin):
    #     def fit(self, frame, y=None):
    #         self.counts_ = frame["Ticket"].value_counts().to_dict()
    #         return self
    #     def transform(self, frame):
    #         result = frame.copy(deep=True)
    #         result["TicketGroupSize"] = (
    #             result["Ticket"].map(self.counts_).fillna(1).astype("int64")
    #         )
    #         return result
    # return TicketGroupSize()
    return None


def build_network(input_dim: int) -> nn.Module:
    """Return one fresh network that emits one raw logit per passenger."""

    # EDIT HERE — add/remove hidden layers, activations or Dropout.
    # Keep input_dim on the first Linear and one output on the last Linear.
    return nn.Sequential(
        nn.Linear(input_dim, 32),
        nn.ReLU(),
        nn.Linear(32, 1),
    )


__all__ = [
    "EXPERIMENT",
    "build_fold_transformer",
    "build_network",
    "prepare_features",
]
