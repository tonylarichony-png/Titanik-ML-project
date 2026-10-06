"""MLP-009: TABDDPM."""

from __future__ import annotations
import numpy as np
import torch

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.validation import check_is_fitted
from torch.utils.data import DataLoader, TensorDataset
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
    experiment_id='MLP-009',
    title='TABDDPM',
    hypothesis="Если восстанавливать Age условной диффузионной моделью по Title, Sex, "
    "Pclass, Fare, SibSp, Parch и Embarked, то более информативное заполнение "
    "Age улучшит качество принятого MLP-002.",
    change_description="CHANGE ME — exactly one controlled change",
    experiment_note=Path("mlp-experiments/MLP-009 TABDDPM.md"),
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
class AgeNoisePredictor(nn.Module):
    def __init__(
        self,
        condition_dim: int,
        diffusion_steps: int,
        time_dim: int = 16,
        hidden_dim: int = 64,
    ):
        super().__init__()

        self.time_embedding = nn.Embedding(
            diffusion_steps,
            time_dim,
        )

        self.network = nn.Sequential(
            nn.Linear(1 + condition_dim + time_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(
        self,
        noisy_age: torch.Tensor,
        condition: torch.Tensor,
        timestep: torch.Tensor,
    ) -> torch.Tensor:
        time_features = self.time_embedding(timestep)

        inputs = torch.cat(
            [noisy_age, condition, time_features],
            dim=1,
        )

        return self.network(inputs)


class ConditionalAgeDDPMImputer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        diffusion_steps: int = 50,
        epochs: int = 80,
        batch_size: int = 128,
        learning_rate: float = 1e-3,
        n_samples: int = 16,
        random_state: int = 42,
    ):
        self.diffusion_steps = diffusion_steps
        self.epochs = epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.n_samples = n_samples
        self.random_state = random_state

    def _build_condition_preprocessor(self):
        numeric = [
            "Fare",
            "SibSp",
            "Parch",
            "Pclass",
        ]

        categorical = [
            "Title",
            "Sex",
            "Embarked",
        ]

        return ColumnTransformer(
            transformers=[
                (
                    "numeric",
                    Pipeline(
                        steps=[
                            (
                                "imputer",
                                SimpleImputer(strategy="median"),
                            ),
                            (
                                "scaler",
                                StandardScaler(),
                            ),
                        ]
                    ),
                    numeric,
                ),
                (
                    "categorical",
                    Pipeline(
                        steps=[
                            (
                                "imputer",
                                SimpleImputer(
                                    strategy="most_frequent"
                                ),
                            ),
                            (
                                "onehot",
                                OneHotEncoder(
                                    handle_unknown="ignore",
                                    sparse_output=False,
                                ),
                            ),
                        ]
                    ),
                    categorical,
                ),
            ],
            sparse_threshold=0.0,
        )

    def fit(self, frame: pd.DataFrame, y=None):
        torch.manual_seed(self.random_state)
        np.random.seed(self.random_state)

        known = frame.loc[frame["Age"].notna()].copy()

        if known.empty:
            raise ValueError(
                "Нет известных Age для обучения DDPM."
            )

        self.condition_preprocessor_ = (
            self._build_condition_preprocessor()
        )

        conditions = np.asarray(
            self.condition_preprocessor_.fit_transform(known),
            dtype=np.float32,
        )

        known_age = known["Age"].to_numpy(dtype=np.float32)

        self.age_mean_ = float(known_age.mean())
        self.age_std_ = max(float(known_age.std()), 1e-6)
        self.age_min_ = float(known_age.min())
        self.age_max_ = float(known_age.max())

        normalized_age = (
            (known_age - self.age_mean_) / self.age_std_
        ).reshape(-1, 1)

        self.betas_ = torch.linspace(
            1e-4,
            0.02,
            self.diffusion_steps,
            dtype=torch.float32,
        )

        self.alphas_ = 1.0 - self.betas_
        self.alpha_bars_ = torch.cumprod(
            self.alphas_,
            dim=0,
        )

        self.model_ = AgeNoisePredictor(
            condition_dim=conditions.shape[1],
            diffusion_steps=self.diffusion_steps,
        )

        optimizer = torch.optim.Adam(
            self.model_.parameters(),
            lr=self.learning_rate,
        )

        age_tensor = torch.tensor(
            normalized_age,
            dtype=torch.float32,
        )

        condition_tensor = torch.tensor(
            conditions,
            dtype=torch.float32,
        )

        generator = torch.Generator().manual_seed(
            self.random_state
        )

        loader = DataLoader(
            TensorDataset(age_tensor, condition_tensor),
            batch_size=self.batch_size,
            shuffle=True,
            generator=generator,
        )

        self.training_loss_ = []

        self.model_.train()

        for epoch in range(self.epochs):
            epoch_losses = []

            for age_0, condition in loader:
                timestep = torch.randint(
                    low=0,
                    high=self.diffusion_steps,
                    size=(len(age_0),),
                    generator=generator,
                )

                noise = torch.randn(
                    age_0.shape,
                    generator=generator,
                )

                alpha_bar = self.alpha_bars_[
                    timestep
                ].reshape(-1, 1)

                noisy_age = (
                    torch.sqrt(alpha_bar) * age_0
                    + torch.sqrt(1.0 - alpha_bar) * noise
                )

                predicted_noise = self.model_(
                    noisy_age,
                    condition,
                    timestep,
                )

                loss = torch.mean(
                    (predicted_noise - noise) ** 2
                )

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_losses.append(float(loss.detach()))

            self.training_loss_.append(
                float(np.mean(epoch_losses))
            )

        self.model_.eval()
        return self

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(
            self,
            [
                "model_",
                "condition_preprocessor_",
                "age_mean_",
                "age_std_",
                "alpha_bars_",
            ],
        )

        result = frame.copy(deep=True)
        missing_age = result["Age"].isna()

        if not missing_age.any():
            return result

        missing_rows = result.loc[missing_age]

        conditions = np.asarray(
            self.condition_preprocessor_.transform(
                missing_rows
            ),
            dtype=np.float32,
        )

        condition_tensor = torch.tensor(
            conditions,
            dtype=torch.float32,
        )

        repeated_conditions = (
            condition_tensor.repeat_interleave(
                self.n_samples,
                dim=0,
            )
        )

        generator = torch.Generator().manual_seed(
            self.random_state + 1
        )

        generated_age = torch.randn(
            (
                len(missing_rows) * self.n_samples,
                1,
            ),
            generator=generator,
        )

        self.model_.eval()

        with torch.no_grad():
            for step in reversed(
                range(self.diffusion_steps)
            ):
                timestep = torch.full(
                    (len(generated_age),),
                    step,
                    dtype=torch.long,
                )

                predicted_noise = self.model_(
                    generated_age,
                    repeated_conditions,
                    timestep,
                )

                beta = self.betas_[step]
                alpha = self.alphas_[step]
                alpha_bar = self.alpha_bars_[step]

                reverse_mean = (
                    generated_age
                    - (
                        beta
                        / torch.sqrt(1.0 - alpha_bar)
                    )
                    * predicted_noise
                ) / torch.sqrt(alpha)

                if step > 0:
                    previous_alpha_bar = (
                        self.alpha_bars_[step - 1]
                    )

                    posterior_variance = (
                        beta
                        * (1.0 - previous_alpha_bar)
                        / (1.0 - alpha_bar)
                    )

                    reverse_noise = torch.randn(
                        generated_age.shape,
                        generator=generator,
                    )

                    generated_age = (
                        reverse_mean
                        + torch.sqrt(
                            posterior_variance
                        )
                        * reverse_noise
                    )
                else:
                    generated_age = reverse_mean

        generated_age = (
            generated_age.reshape(
                len(missing_rows),
                self.n_samples,
            )
            * self.age_std_
            + self.age_mean_
        )

        imputed_age = (
            generated_age.median(dim=1).values
            .clamp(self.age_min_, self.age_max_)
            .cpu()
            .numpy()
        )

        result.loc[missing_age, "Age"] = imputed_age

        return result


def normalized_titles(frame: pd.DataFrame) -> pd.Series:
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

def prepare_features(frame: pd.DataFrame) -> MLPFeatureData:
    """Create row-local features and declare their preprocessing roles."""

    result = frame.copy(deep=True)
    result["Title"] = normalized_titles(result)
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
    return ConditionalAgeDDPMImputer(
        diffusion_steps=50,
        epochs=80,
        batch_size=128,
        learning_rate=1e-3,
        n_samples=16,
        random_state=42,
    )


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
    "EXPERIMENT",
    "build_fold_transformer",
    "build_network",
    "prepare_features",
]
