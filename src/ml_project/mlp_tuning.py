"""Optuna helpers for fold-safe MLP hyperparameter screening."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Callable, Mapping, Sequence

import numpy as np
from sklearn.model_selection import StratifiedKFold
from torch import nn

from .mlp_experiment import (
    MLPExperimentSpec,
    MLPFeatureData,
    MLPTrainingConfig,
    run_mlp_cv,
)


BASELINE_PARAMETERS: dict[str, Any] = {
    "batch_size": 32,
    "learning_rate": 1e-3,
    "weight_decay": 0.0,
    "dropout": 0.2,
    "n_layers": 3,
    "hidden_dim": 16,
}


PHASE2_BASELINE_PARAMETERS: dict[str, Any] = {
    "batch_size": 32,
    "learning_rate": 0.0017503534730658975,
    "weight_decay": 1e-4,
    "dropout": 0.3,
    "n_layers": 4,
    "hidden_dim": 8,
    "activation": "relu",
}


class SquaredReLU(nn.Module):
    """ReLU followed by element-wise squaring."""

    def forward(self, values: Any) -> Any:
        """Выполнить прямой проход сети и вернуть выходные значения."""
        return nn.functional.relu(values).square()


def suggest_parameters(trial: Any) -> dict[str, Any]:
    """Sample a deliberately small search space around MLP-024."""

    return {
        "batch_size": trial.suggest_categorical("batch_size", [16, 32, 64]),
        "learning_rate": trial.suggest_float(
            "learning_rate", 3e-4, 3e-3, log=True
        ),
        "weight_decay": trial.suggest_categorical(
            "weight_decay", [0.0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
        ),
        "dropout": trial.suggest_float("dropout", 0.1, 0.3, step=0.05),
        "n_layers": trial.suggest_int("n_layers", 2, 4),
        "hidden_dim": trial.suggest_categorical("hidden_dim", [8, 16, 24, 32]),
    }


def suggest_phase2_parameters(trial: Any) -> dict[str, Any]:
    """Sample the focused architecture-and-activation search space."""

    activation = trial.suggest_categorical(
        "activation",
        ["relu", "leaky_relu", "gelu", "silu", "squared_relu"],
    )
    parameters: dict[str, Any] = {
        "batch_size": trial.suggest_categorical("batch_size", [32, 64]),
        "learning_rate": trial.suggest_float(
            "learning_rate", 1.2e-3, 2.5e-3, log=True
        ),
        "weight_decay": trial.suggest_categorical(
            "weight_decay", [1e-7, 1e-6, 1e-5, 1e-4]
        ),
        "dropout": trial.suggest_float("dropout", 0.05, 0.3, step=0.05),
        "n_layers": trial.suggest_int("n_layers", 3, 5),
        "hidden_dim": trial.suggest_categorical(
            "hidden_dim", [4, 8, 12, 16]
        ),
        "activation": activation,
    }
    if activation == "leaky_relu":
        parameters["negative_slope"] = trial.suggest_categorical(
            "negative_slope", [0.01, 0.05, 0.1]
        )
    return parameters


def make_activation(
    name: str,
    *,
    negative_slope: float | None = None,
) -> nn.Module:
    """Create a fresh activation module for one hidden layer."""

    if name == "relu":
        return nn.ReLU()
    if name == "leaky_relu":
        return nn.LeakyReLU(
            negative_slope=0.01 if negative_slope is None else negative_slope
        )
    if name == "gelu":
        return nn.GELU()
    if name == "silu":
        return nn.SiLU()
    if name == "squared_relu":
        return SquaredReLU()
    raise ValueError(f"Unknown activation: {name}")


def build_network_factory(parameters: Mapping[str, Any]) -> Callable[[int], nn.Module]:
    """Return the build_network callback required by the MLP runtime."""

    hidden_dim = int(parameters["hidden_dim"])
    n_layers = int(parameters["n_layers"])
    dropout = float(parameters["dropout"])

    def build_network(input_dim: int) -> nn.Module:
        layers: list[nn.Module] = []
        current_dim = int(input_dim)
        for _ in range(n_layers):
            layers.extend((nn.Linear(current_dim, hidden_dim), nn.ReLU()))
            current_dim = hidden_dim
        layers.extend((nn.Dropout(dropout), nn.Linear(current_dim, 1)))
        return nn.Sequential(*layers)

    return build_network


def build_phase2_network_factory(
    parameters: Mapping[str, Any],
) -> Callable[[int], nn.Module]:
    """Return a network builder with a trial-selected activation."""

    hidden_dim = int(parameters["hidden_dim"])
    n_layers = int(parameters["n_layers"])
    dropout = float(parameters["dropout"])
    activation = str(parameters["activation"])
    negative_slope = parameters.get("negative_slope")

    def build_network(input_dim: int) -> nn.Module:
        layers: list[nn.Module] = []
        current_dim = int(input_dim)
        for _ in range(n_layers):
            layers.append(nn.Linear(current_dim, hidden_dim))
            layers.append(
                make_activation(
                    activation,
                    negative_slope=(
                        None
                        if negative_slope is None
                        else float(negative_slope)
                    ),
                )
            )
            current_dim = hidden_dim
        layers.extend((nn.Dropout(dropout), nn.Linear(current_dim, 1)))
        return nn.Sequential(*layers)

    return build_network


def training_from_parameters(
    base: MLPTrainingConfig,
    parameters: Mapping[str, Any],
) -> MLPTrainingConfig:
    """Apply sampled optimizer settings while preserving the training contract."""

    return replace(
        base,
        batch_size=int(parameters["batch_size"]),
        learning_rate=float(parameters["learning_rate"]),
        weight_decay=float(parameters["weight_decay"]),
    )


def make_stratified_splits(
    prepared: MLPFeatureData,
    *,
    target: str,
    n_splits: int = 3,
    random_state: int = 2026,
) -> tuple[tuple[np.ndarray, np.ndarray], ...]:
    """Create one fixed set of folds shared by every Optuna trial."""

    y = prepared.frame[target].to_numpy(dtype=np.int64)
    splitter = StratifiedKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )
    return tuple(
        (np.asarray(train_index), np.asarray(valid_index))
        for train_index, valid_index in splitter.split(np.zeros(len(y)), y)
    )


def make_objective(
    prepared: MLPFeatureData,
    *,
    target: str,
    key: str,
    base_spec: MLPExperimentSpec,
    cv_splits: Sequence[tuple[np.ndarray, np.ndarray]],
    build_fold_transformer: Callable[[], Any] | None,
) -> Callable[[Any], float]:
    """Build an Optuna objective that never writes official experiment artifacts."""

    fixed_splits = tuple(cv_splits)

    def objective(trial: Any) -> float:
        parameters = suggest_parameters(trial)
        spec = replace(
            base_spec,
            experiment_id=f"TUNE-{trial.number:04d}",
            title=f"Optuna trial {trial.number}",
            hypothesis="Automated hyperparameter screening",
            change_description="Parameters sampled by Optuna",
            training=training_from_parameters(base_spec.training, parameters),
            n_splits=len(fixed_splits),
            save_artifacts=False,
            sync_docs=False,
        )
        result = run_mlp_cv(
            prepared,
            target=target,
            key=key,
            build_network=build_network_factory(parameters),
            spec=spec,
            build_fold_transformer=build_fold_transformer,
            cv_splits=fixed_splits,
        )
        accuracy = float(result.summary.loc["accuracy", "mean"])
        trial.set_user_attr(
            "accuracy_std", float(result.summary.loc["accuracy", "std"])
        )
        trial.set_user_attr(
            "log_loss_mean", float(result.summary.loc["log_loss", "mean"])
        )
        trial.set_user_attr(
            "fold_accuracy", result.fold_metrics["accuracy"].tolist()
        )
        return accuracy

    return objective


def make_phase2_objective(
    prepared: MLPFeatureData,
    *,
    target: str,
    key: str,
    base_spec: MLPExperimentSpec,
    cv_splits: Sequence[tuple[np.ndarray, np.ndarray]],
    build_fold_transformer: Callable[[], Any] | None,
) -> Callable[[Any], float]:
    """Build the focused phase-two objective with activation selection."""

    fixed_splits = tuple(cv_splits)

    def objective(trial: Any) -> float:
        parameters = suggest_phase2_parameters(trial)
        spec = replace(
            base_spec,
            experiment_id=f"TUNE2-{trial.number:04d}",
            title=f"Optuna phase-two trial {trial.number}",
            hypothesis="Focused architecture and activation screening",
            change_description="Parameters sampled by Optuna phase two",
            training=training_from_parameters(base_spec.training, parameters),
            n_splits=len(fixed_splits),
            save_artifacts=False,
            sync_docs=False,
        )
        result = run_mlp_cv(
            prepared,
            target=target,
            key=key,
            build_network=build_phase2_network_factory(parameters),
            spec=spec,
            build_fold_transformer=build_fold_transformer,
            cv_splits=fixed_splits,
        )
        accuracy = float(result.summary.loc["accuracy", "mean"])
        trial.set_user_attr(
            "accuracy_std", float(result.summary.loc["accuracy", "std"])
        )
        trial.set_user_attr(
            "log_loss_mean", float(result.summary.loc["log_loss", "mean"])
        )
        trial.set_user_attr(
            "fold_accuracy", result.fold_metrics["accuracy"].tolist()
        )
        return accuracy

    return objective


__all__ = [
    "BASELINE_PARAMETERS",
    "PHASE2_BASELINE_PARAMETERS",
    "SquaredReLU",
    "build_network_factory",
    "build_phase2_network_factory",
    "make_activation",
    "make_objective",
    "make_phase2_objective",
    "make_stratified_splits",
    "suggest_parameters",
    "suggest_phase2_parameters",
    "training_from_parameters",
]
