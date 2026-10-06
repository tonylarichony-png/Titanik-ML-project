"""MLP-026: Dpoutlight 1layer."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from torch import nn

from ml_project.mlp_experiment import (
    MLPExperimentSpec,
    MLPFeatureData,
    MLPTrainingConfig,
)
from ml_project.transformers import AgeByTitlePclassImputer


EXPERIMENT = MLPExperimentSpec(
    experiment_id='MLP-026',
    title='Dpoutlight 1layer',
    hypothesis='CHANGE ME — if ..., then ..., because ...',
    change_description='CHANGE ME — exactly one controlled change',
    experiment_note=Path('mlp-experiments/MLP-026 Dpoutlight 1layer.md'),
    n_splits=5,
    primary_metric="accuracy",
    primary_improvement_min=0.0,
    metric_guardrails={
        "balanced_accuracy": 0.0,
        "recall": -0.01,
        "f1": 0.0,
    },
    parent_mlp_module='ml_project.mlp_experiments.mlp_024_dpoutmedium',
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
    """Extract the same normalized Title groups used in EXP-002."""

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


class AllInFoldTransformer(BaseEstimator, TransformerMixin):
    """Learn Age medians and ticket counts using only the current train fold."""

    def fit(self, frame: pd.DataFrame, y=None):
        self.age_imputer_ = AgeByTitlePclassImputer(
            age_column="Age",
            title_column="Title",
            class_column="Pclass",
        ).fit(frame)
        self.ticket_counts_ = frame["Ticket"].value_counts().to_dict()
        return self

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = self.age_imputer_.transform(frame)
        result["TicketGroupSize"] = (
            result["Ticket"]
            .map(self.ticket_counts_)
            .fillna(1)
            .astype("int64")
        )
        result["FarePerPerson"] = np.log1p(
            result["Fare"] / result["TicketGroupSize"]
        )
        result["IsnotAlone"] = (
            (result["TicketGroupSize"] > 1)
            & result["Parch"].eq(0)
            & result["SibSp"].eq(0)
        ).astype("int64")
        return result


def prepare_features(frame: pd.DataFrame) -> MLPFeatureData:
    """Create every deterministic row-local feature from the sklearn chain."""

    result = frame.copy(deep=True)
    result["Title"] = normalized_titles(result)

    family_size = result["SibSp"] + result["Parch"] + 1
    result["FamilySizeGroup"] = pd.cut(
        family_size,
        bins=[0, 1, 2, 3, 4, np.inf],
        labels=["1", "2", "3", "4", ">4"],
        include_lowest=True,
    ).astype("string")

    result["CabinKnown"] = result["Cabin"].notna().astype("int64")
    result["Deck"] = result["Cabin"].str[0]
    result["Deck"] = result["Deck"].replace(["A", "B", "C", "T"], "ABC")
    missing_deck = result["Deck"].isna()
    deck_for_unknown = {
        1: "ABC_Unknown",
        2: "DE_Unknown",
        3: "FG_Unknown",
    }
    result.loc[missing_deck, "Deck"] = (
        result.loc[missing_deck, "Pclass"].map(deck_for_unknown)
    )

    result["SexPclass"] = (
        result["Sex"].astype("string")
        + "_P"
        + result["Pclass"].astype("string")
    )

    numeric_features = (
        "Age",
        "TicketGroupSize",
        "FarePerPerson",
    )
    categorical_features = (
        "Embarked",
        "FamilySizeGroup",
        "IsnotAlone",
        "CabinKnown",
        "Deck",
        "SexPclass",
    )
    return MLPFeatureData(
        frame=result,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        fold_generated_features=(
            "TicketGroupSize",
            "FarePerPerson",
            "IsnotAlone",
        ),
    )


def build_fold_transformer():
    """Return a fresh all-in transformer fitted inside each train fold."""

    return AllInFoldTransformer()


def build_network(input_dim: int) -> nn.Module:
    """Return one fresh network that emits one raw logit per passenger."""

    # EDIT HERE — add/remove hidden layers, activations or Dropout.
    # Keep input_dim on the first Linear and one output on the last Linear.
    return nn.Sequential(
        nn.Linear(input_dim, 16),
        nn.ReLU(),
        nn.Dropout(p=0.1),
        nn.Linear(16, 16),
        nn.ReLU(),
        nn.Linear(16, 16),
        nn.ReLU(),

        nn.Linear(16, 1),
    )


__all__ = [
    "AllInFoldTransformer",
    "EXPERIMENT",
    "build_fold_transformer",
    "build_network",
    "normalized_titles",
    "prepare_features",
]
