"""Reproducible PyTorch MLP experiments for tabular binary classification."""

from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
import math
import random
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from .docsync import MarkdownDocument, dataframe_to_markdown


@dataclass(frozen=True)
class MLPTrainingConfig:
    """All choices that affect preprocessing and neural-network training."""

    numeric_imputer: str = "median"
    categorical_imputer: str = "most_frequent"
    numeric_scaler: str = "standard"
    categorical_encoding: str = "one_hot"
    batch_size: int = 32
    learning_rate: float = 1e-3
    weight_decay: float = 0.0
    max_epochs: int = 100
    patience: int = 12
    min_delta: float = 1e-4
    inner_validation_fraction: float = 0.15
    threshold: float = 0.5
    random_state: int = 42
    device: str = "cpu"
    scheduler: str = "none"
    scheduler_eta_min: float = 1e-5


@dataclass(frozen=True)
class MLPExperimentSpec:
    """Identity and validation contract for one immutable experiment module."""

    experiment_id: str
    title: str
    hypothesis: str
    change_description: str
    experiment_note: Path = Path("mlp-experiments/MLP-000 Draft.md")
    training: MLPTrainingConfig = field(default_factory=MLPTrainingConfig)
    n_splits: int = 5
    primary_metric: str = "accuracy"
    primary_improvement_min: float = 0.0
    metric_guardrails: Mapping[str, float] = field(
        default_factory=lambda: {
            "balanced_accuracy": 0.0,
            "recall": -0.01,
            "f1": 0.0,
        }
    )
    parent_mlp_module: str | None = None
    sklearn_reference_module: str | None = None
    save_artifacts: bool = True
    sync_docs: bool = True
    artifact_dir: Path = Path("artifacts/mlp-experiments")
    results_registry: Path = Path("mlp-experiments/results.csv")


@dataclass(frozen=True)
class MLPFeatureData:
    """Feature-engineering result and explicit preprocessing roles."""

    frame: pd.DataFrame
    numeric_features: tuple[str, ...]
    categorical_features: tuple[str, ...]
    fold_generated_features: tuple[str, ...] = ()

    @property
    def features(self) -> tuple[str, ...]:
        """Вернуть полный упорядоченный список признаков MLP."""
        return self.numeric_features + self.categorical_features


@dataclass
class FittedMLP:
    """Обученная MLP вместе с preprocessing и историей оптимизации."""
    model: Any
    preprocessor: ColumnTransformer
    history: pd.DataFrame
    best_epoch: int
    input_dim: int
    device: str
    feature_transformer: Any = None


@dataclass
class MLPCVResult:
    """Результаты внешней кросс-валидации MLP."""
    fold_metrics: pd.DataFrame
    summary: pd.DataFrame
    oof_predictions: pd.DataFrame
    histories: dict[int, pd.DataFrame]
    input_dims: dict[int, int]
    cv_splits: tuple[tuple[np.ndarray, np.ndarray], ...]


@dataclass
class MLPReferenceResult:
    """Метрики и OOF-предсказания референсной модели."""
    name: str
    source_module: str
    fold_metrics: pd.DataFrame
    oof_predictions: pd.DataFrame


@dataclass
class MLPComparison:
    """Парное сравнение MLP-кандидата с референсной моделью."""
    summary: pd.DataFrame
    paired_deltas: pd.DataFrame
    criteria: pd.DataFrame
    reference: MLPReferenceResult


def validate_training_config(config: MLPTrainingConfig) -> None:
    """Проверить параметры обучения PyTorch MLP."""
    if config.numeric_imputer not in {"mean", "median", "most_frequent"}:
        raise ValueError("numeric_imputer must be mean, median or most_frequent")
    if config.categorical_imputer not in {"most_frequent", "constant"}:
        raise ValueError("categorical_imputer must be most_frequent or constant")
    if config.numeric_scaler not in {"standard", "none"}:
        raise ValueError("numeric_scaler must be standard or none")
    if config.categorical_encoding not in {"one_hot", "ordinal"}:
        raise ValueError("categorical_encoding must be one_hot or ordinal")
    if config.batch_size < 1 or config.max_epochs < 1 or config.patience < 1:
        raise ValueError("batch_size, max_epochs and patience must be positive")
    if not 0 < config.inner_validation_fraction < 0.5:
        raise ValueError("inner_validation_fraction must be between 0 and 0.5")
    if not 0 < config.threshold < 1:
        raise ValueError("threshold must be between 0 and 1")
    for name in ("learning_rate", "min_delta"):
        value = float(getattr(config, name))
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a positive finite number")
    if not math.isfinite(config.weight_decay) or config.weight_decay < 0:
        raise ValueError("weight_decay must be a non-negative finite number")
    if config.scheduler not in {"none", "cosine"}:
        raise ValueError("scheduler must be none or cosine")
    if (
        not math.isfinite(config.scheduler_eta_min)
        or config.scheduler_eta_min < 0
    ):
        raise ValueError(
            "scheduler_eta_min must be a finite non-negative number"
        )
    if (
        config.scheduler == "cosine"
        and config.scheduler_eta_min >= config.learning_rate
    ):
        raise ValueError(
            "scheduler_eta_min must be lower than learning_rate"
        )
    if config.device != "cpu":
        raise ValueError("The reproducible project runner currently supports device='cpu'")


def validate_feature_data(
    prepared: MLPFeatureData,
    source: pd.DataFrame,
    *,
    target: str,
    key: str,
) -> None:
    """Проверить таблицу и роли признаков MLP перед обучением."""
    if not isinstance(prepared, MLPFeatureData):
        raise TypeError("prepare_features must return MLPFeatureData")
    if not prepared.frame.index.equals(source.index):
        raise ValueError("prepare_features changed row index or row order")
    if target not in prepared.frame or key not in prepared.frame:
        raise KeyError("prepare_features must preserve target and key")
    pd.testing.assert_series_equal(prepared.frame[target], source[target])
    pd.testing.assert_series_equal(prepared.frame[key], source[key])
    features = list(prepared.features)
    if not features:
        raise ValueError("At least one feature is required")
    duplicates = pd.Index(features)[pd.Index(features).duplicated()].unique().tolist()
    if duplicates:
        raise ValueError(f"Features must occur exactly once: {duplicates}")
    forbidden = [name for name in (target, key) if name in features]
    if forbidden:
        raise ValueError(f"Target/key cannot be model features: {forbidden}")
    unknown_generated = [
        name for name in prepared.fold_generated_features if name not in features
    ]
    if unknown_generated:
        raise ValueError(
            "fold_generated_features must also be numeric/categorical features: "
            f"{unknown_generated}"
        )
    missing = [
        name
        for name in features
        if name not in prepared.frame and name not in prepared.fold_generated_features
    ]
    if missing:
        raise KeyError(f"Declared features are absent from frame: {missing}")


def build_preprocessor(
    prepared: MLPFeatureData,
    config: MLPTrainingConfig,
) -> ColumnTransformer:
    """Build a fresh fold-fitted tabular preprocessor."""

    validate_training_config(config)
    numeric_steps: list[tuple[str, Any]] = [
        ("imputer", SimpleImputer(strategy=config.numeric_imputer))
    ]
    if config.numeric_scaler == "standard":
        numeric_steps.append(("scaler", StandardScaler()))
    categorical_imputer = (
        SimpleImputer(strategy="constant", fill_value="__MISSING__")
        if config.categorical_imputer == "constant"
        else SimpleImputer(strategy="most_frequent")
    )
    categorical_encoder = (
        OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        if config.categorical_encoding == "one_hot"
        else OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1,
            dtype=np.float32,
        )
    )
    return ColumnTransformer(
        [
            ("numeric", Pipeline(numeric_steps), list(prepared.numeric_features)),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", categorical_imputer),
                        (
                            "encoder",
                            categorical_encoder,
                        ),
                    ]
                ),
                list(prepared.categorical_features),
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


def _fit_feature_transformer(builder, frame: pd.DataFrame):
    transformer = builder() if builder is not None else None
    if transformer is None:
        return None, frame.copy(deep=True)
    if not hasattr(transformer, "fit") or not hasattr(transformer, "transform"):
        raise TypeError("build_fold_transformer must return fit/transform object or None")
    transformer.fit(frame.copy(deep=True))
    transformed = transformer.transform(frame.copy(deep=True))
    if not isinstance(transformed, pd.DataFrame):
        raise TypeError("Fold feature transformer must return pandas DataFrame")
    if not transformed.index.equals(frame.index):
        raise ValueError("Fold feature transformer changed row index/order")
    return transformer, transformed


def _transform_features(transformer, frame: pd.DataFrame) -> pd.DataFrame:
    if transformer is None:
        return frame.copy(deep=True)
    transformed = transformer.transform(frame.copy(deep=True))
    if not isinstance(transformed, pd.DataFrame):
        raise TypeError("Fold feature transformer must return pandas DataFrame")
    if not transformed.index.equals(frame.index):
        raise ValueError("Fold feature transformer changed row index/order")
    return transformed


def _require_model_features(frame: pd.DataFrame, prepared: MLPFeatureData) -> None:
    missing = [name for name in prepared.features if name not in frame]
    if missing:
        raise KeyError(f"Feature transformer did not create declared features: {missing}")


def _torch():
    try:
        import torch
        from torch import nn
        from torch.utils.data import DataLoader, TensorDataset
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(
            "PyTorch is required. Activate titanik-ml and install requirements.txt."
        ) from error
    return torch, nn, DataLoader, TensorDataset


def seed_everything(seed: int) -> None:
    """Зафиксировать генераторы случайных чисел для воспроизводимости."""
    torch, _, _, _ = _torch()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def _evaluate_arrays(model, x, y, loss_fn) -> tuple[float, np.ndarray]:
    torch, _, _, _ = _torch()
    model.eval()
    with torch.no_grad():
        logits = model(x).reshape(-1)
        loss = loss_fn(logits, y).item()
        probability = torch.sigmoid(logits).cpu().numpy()
    return float(loss), probability


def fit_mlp(
    x: np.ndarray,
    y: np.ndarray,
    *,
    build_network: Callable[[int], Any],
    config: MLPTrainingConfig,
    seed: int,
    validation_data: tuple[np.ndarray, np.ndarray] | None = None,
) -> FittedMLP:
    """Fit one MLP with an inner validation split for early stopping."""

    torch, nn, DataLoader, TensorDataset = _torch()
    seed_everything(seed)
    if validation_data is None:
        indices = np.arange(len(y))
        train_idx, inner_idx = train_test_split(
            indices,
            test_size=config.inner_validation_fraction,
            random_state=seed,
            stratify=y,
        )
        x_train_np, y_train_np = x[train_idx], y[train_idx]
        x_inner_np, y_inner_np = x[inner_idx], y[inner_idx]
    else:
        x_train_np, y_train_np = x, y
        x_inner_np, y_inner_np = validation_data
    x_train = torch.tensor(x_train_np, dtype=torch.float32)
    y_train = torch.tensor(y_train_np, dtype=torch.float32)
    x_inner = torch.tensor(x_inner_np, dtype=torch.float32)
    y_inner = torch.tensor(y_inner_np, dtype=torch.float32)
    device = torch.device(config.device)
    model = build_network(int(x.shape[1])).to(device)
    if not isinstance(model, nn.Module):
        raise TypeError("build_network(input_dim) must return torch.nn.Module")
    with torch.no_grad():
        probe = model(x_train[:2].to(device)).reshape(-1)
    if probe.shape != (min(2, len(x_train)),):
        raise ValueError("Network must return one logit per row")
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )
    scheduler = None

    if config.scheduler == "cosine":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=config.max_epochs,
            eta_min=config.scheduler_eta_min,
        )
    elif config.scheduler != "none":
        raise ValueError(
            f"Unknown scheduler: {config.scheduler}"
        )
    loader = DataLoader(
        TensorDataset(x_train, y_train),
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=0,
        generator=torch.Generator().manual_seed(seed),
    )
    x_train, y_train = x_train.to(device), y_train.to(device)
    x_inner, y_inner = x_inner.to(device), y_inner.to(device)
    history: list[dict[str, float | int]] = []
    best_loss = float("inf")
    best_epoch = 0
    best_state = None
    patience_reference = float("inf")
    stale_epochs = 0
    for epoch in range(1, config.max_epochs + 1):
        current_lr = float(optimizer.param_groups[0]["lr"])
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(xb).reshape(-1), yb)
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite training loss")
            loss.backward()
            optimizer.step()
        train_loss, _ = _evaluate_arrays(model, x_train, y_train, loss_fn)
        inner_loss, inner_probability = _evaluate_arrays(
            model, x_inner, y_inner, loss_fn
        )
        inner_true = y_inner.cpu().numpy().astype("int64")
        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "inner_val_loss": inner_loss,
                "inner_val_accuracy": accuracy_score(
                    inner_true,
                    inner_probability >= config.threshold,
                ),
                "learning_rate": current_lr,
            }
        )
        if scheduler is not None:
            scheduler.step()
        if inner_loss < best_loss:
            best_loss = inner_loss
            best_epoch = epoch
            best_state = copy.deepcopy(model.state_dict())
        if inner_loss < patience_reference - config.min_delta:
            patience_reference = inner_loss
            stale_epochs = 0
        else:
            stale_epochs += 1
        if stale_epochs >= config.patience:
            break
    if best_state is None:
        raise RuntimeError("Training did not produce a checkpoint")
    model.load_state_dict(best_state)
    model.eval()
    return FittedMLP(
        model=model,
        preprocessor=None,  # assigned by fit_prepared_mlp
        history=pd.DataFrame(history),
        best_epoch=best_epoch,
        input_dim=int(x.shape[1]),
        device=config.device,
    )


def _fit_fixed_epochs(
    x: np.ndarray,
    y: np.ndarray,
    *,
    build_network: Callable[[int], Any],
    config: MLPTrainingConfig,
    seed: int,
    epochs: int,
):
    """Fit a fresh model on all supplied rows for a fixed epoch budget."""

    torch, nn, DataLoader, TensorDataset = _torch()
    seed_everything(seed)
    device = torch.device(config.device)
    x_tensor = torch.tensor(x, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    model = build_network(int(x.shape[1])).to(device)
    if not isinstance(model, nn.Module):
        raise TypeError("build_network(input_dim) must return torch.nn.Module")
    optimizer = torch.optim.Adam(
        model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay
    )
    scheduler = None
    if config.scheduler == "cosine":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=config.max_epochs,
            eta_min=config.scheduler_eta_min,
        )
    elif config.scheduler != "none":
        raise ValueError(f"Unknown scheduler: {config.scheduler}")
    loss_fn = nn.BCEWithLogitsLoss()
    loader = DataLoader(
        TensorDataset(x_tensor, y_tensor),
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=0,
        generator=torch.Generator().manual_seed(seed),
    )
    for _ in range(epochs):
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(xb).reshape(-1), yb)
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite training loss")
            loss.backward()
            optimizer.step()
        if scheduler is not None:
            scheduler.step()
    model.eval()
    return model


def fit_prepared_mlp(
    prepared: MLPFeatureData,
    row_indices: Sequence[int],
    *,
    target: str,
    build_network: Callable[[int], Any],
    config: MLPTrainingConfig,
    seed: int,
    build_fold_transformer: Callable[[], Any] | None = None,
) -> FittedMLP:
    """Обучить MLP на выбранных строках с внутренней ранней остановкой."""
    rows = np.asarray(row_indices)
    full_frame = prepared.frame.iloc[rows]
    full_y = full_frame[target].to_numpy(dtype=np.int64)
    local_indices = np.arange(len(full_frame))
    optimization_idx, inner_idx = train_test_split(
        local_indices,
        test_size=config.inner_validation_fraction,
        random_state=seed,
        stratify=full_y,
    )

    # Epoch selection: the preprocessor sees optimization rows only.
    selection_transformer, optimization_frame = _fit_feature_transformer(
        build_fold_transformer,
        full_frame.iloc[optimization_idx],
    )
    inner_frame = _transform_features(
        selection_transformer,
        full_frame.iloc[inner_idx],
    )
    _require_model_features(optimization_frame, prepared)
    _require_model_features(inner_frame, prepared)
    selection_preprocessor = build_preprocessor(prepared, config)
    selection_preprocessor.fit(
        optimization_frame.loc[:, list(prepared.features)]
    )
    x_optimization = np.asarray(
        selection_preprocessor.transform(
            optimization_frame.loc[:, list(prepared.features)]
        ),
        dtype=np.float32,
    )
    x_inner = np.asarray(
        selection_preprocessor.transform(
            inner_frame.loc[:, list(prepared.features)]
        ),
        dtype=np.float32,
    )
    selection = fit_mlp(
        x_optimization,
        full_y[optimization_idx],
        build_network=build_network,
        config=config,
        seed=seed,
        validation_data=(x_inner, full_y[inner_idx]),
    )

    # Outer model: fresh preprocessing/model, all outer-train rows, fixed epochs.
    full_transformer, transformed_full_frame = _fit_feature_transformer(
        build_fold_transformer,
        full_frame,
    )
    _require_model_features(transformed_full_frame, prepared)
    full_preprocessor = build_preprocessor(prepared, config)
    full_x = np.asarray(
        full_preprocessor.fit_transform(
            transformed_full_frame.loc[:, list(prepared.features)]
        ),
        dtype=np.float32,
    )
    final_model = _fit_fixed_epochs(
        full_x,
        full_y,
        build_network=build_network,
        config=config,
        seed=seed + 100_000,
        epochs=selection.best_epoch,
    )
    return FittedMLP(
        model=final_model,
        preprocessor=full_preprocessor,
        history=selection.history,
        best_epoch=selection.best_epoch,
        input_dim=int(full_x.shape[1]),
        device=config.device,
        feature_transformer=full_transformer,
    )


def predict_prepared_mlp(
    fitted: FittedMLP,
    prepared: MLPFeatureData,
    row_indices: Sequence[int] | None = None,
) -> np.ndarray:
    """Рассчитать вероятности для подготовленных строк с помощью MLP."""
    torch, _, _, _ = _torch()
    frame = prepared.frame if row_indices is None else prepared.frame.iloc[np.asarray(row_indices)]
    frame = _transform_features(fitted.feature_transformer, frame)
    _require_model_features(frame, prepared)
    x = fitted.preprocessor.transform(frame.loc[:, list(prepared.features)])
    x_tensor = torch.tensor(np.asarray(x, dtype=np.float32), dtype=torch.float32)
    fitted.model.eval()
    with torch.no_grad():
        logits = fitted.model(x_tensor.to(fitted.device)).reshape(-1)
        return torch.sigmoid(logits).cpu().numpy()


def _metric_row(
    fold: int,
    y_true: np.ndarray,
    probability: np.ndarray,
    threshold: float,
) -> dict[str, float | int]:
    prediction = (probability >= threshold).astype("int64")
    return {
        "fold": fold,
        "accuracy": accuracy_score(y_true, prediction),
        "balanced_accuracy": balanced_accuracy_score(y_true, prediction),
        "precision": precision_score(y_true, prediction, zero_division=0),
        "recall": recall_score(y_true, prediction, zero_division=0),
        "f1": f1_score(y_true, prediction, zero_division=0),
        "roc_auc": roc_auc_score(y_true, probability),
        "log_loss": log_loss(y_true, probability, labels=[0, 1]),
    }


def run_mlp_cv(
    prepared: MLPFeatureData,
    *,
    target: str,
    key: str,
    build_network: Callable[[int], Any],
    spec: MLPExperimentSpec,
    build_fold_transformer: Callable[[], Any] | None = None,
    cv_splits: Sequence[tuple[np.ndarray, np.ndarray]] | None = None,
) -> MLPCVResult:
    """Run outer stratified CV; early stopping only sees an inner train split."""

    validate_feature_data(prepared, prepared.frame, target=target, key=key)
    validate_training_config(spec.training)
    y = prepared.frame[target].to_numpy(dtype=np.int64)
    if cv_splits is None:
        splitter = StratifiedKFold(
            n_splits=spec.n_splits,
            shuffle=True,
            random_state=spec.training.random_state,
        )
        splits = tuple(
            (np.asarray(train_idx), np.asarray(valid_idx))
            for train_idx, valid_idx in splitter.split(np.zeros(len(y)), y)
        )
    else:
        splits = tuple(
            (np.asarray(train_idx), np.asarray(valid_idx))
            for train_idx, valid_idx in cv_splits
        )
        if len(splits) != spec.n_splits:
            raise ValueError("Provided CV split count differs from spec.n_splits")
    oof_probability = np.full(len(y), np.nan, dtype=float)
    oof_fold = np.zeros(len(y), dtype=int)
    metrics: list[dict[str, float | int]] = []
    histories: dict[int, pd.DataFrame] = {}
    input_dims: dict[int, int] = {}
    for fold, (train_idx, valid_idx) in enumerate(
        splits, start=1
    ):
        fitted = fit_prepared_mlp(
            prepared,
            train_idx,
            target=target,
            build_network=build_network,
            config=spec.training,
            seed=spec.training.random_state + fold,
            build_fold_transformer=build_fold_transformer,
        )
        probability = predict_prepared_mlp(fitted, prepared, valid_idx)
        oof_probability[valid_idx] = probability
        oof_fold[valid_idx] = fold
        metrics.append(
            _metric_row(fold, y[valid_idx], probability, spec.training.threshold)
        )
        histories[fold] = fitted.history.assign(best_epoch=fitted.best_epoch)
        input_dims[fold] = fitted.input_dim
    if not np.isfinite(oof_probability).all() or (oof_fold == 0).any():
        raise RuntimeError("OOF predictions are incomplete")
    fold_metrics = pd.DataFrame(metrics)
    metric_columns = [column for column in fold_metrics if column != "fold"]
    summary = pd.DataFrame(
        {
            "mean": fold_metrics[metric_columns].mean(),
            "std": fold_metrics[metric_columns].std(ddof=1),
            "min": fold_metrics[metric_columns].min(),
            "max": fold_metrics[metric_columns].max(),
        }
    )
    oof = pd.DataFrame(
        {
            key: prepared.frame[key].to_numpy(),
            "fold": oof_fold,
            "target": y,
            "probability": oof_probability,
            "prediction": (oof_probability >= spec.training.threshold).astype("int64"),
        },
        index=prepared.frame.index,
    )
    return MLPCVResult(fold_metrics, summary, oof, histories, input_dims, splits)


def run_mlp_parent_reference(
    raw_train: pd.DataFrame,
    *,
    module_name: str,
    target: str,
    key: str,
    cv_splits: Sequence[tuple[np.ndarray, np.ndarray]],
) -> MLPReferenceResult:
    """Re-evaluate an adopted MLP parent on exactly the candidate folds."""

    module = load_mlp_experiment(module_name)
    source_path = Path(module.__file__).resolve()
    project_root = next(
        parent for parent in source_path.parents if (parent / "src/ml_project").is_dir()
    )
    decision = _frontmatter_value(project_root / module.EXPERIMENT.experiment_note, "decision")
    if decision != "adopt":
        raise ValueError(
            f"MLP parent {module.EXPERIMENT.experiment_id} must have decision: adopt; "
            f"found {decision or 'no card'}"
        )
    prepared = module.prepare_features(raw_train.copy(deep=True))
    validate_feature_data(prepared, raw_train, target=target, key=key)
    result = run_mlp_cv(
        prepared,
        target=target,
        key=key,
        build_network=module.build_network,
        build_fold_transformer=getattr(module, "build_fold_transformer", None),
        spec=module.EXPERIMENT,
        cv_splits=cv_splits,
    )
    return MLPReferenceResult(
        name=f"{module.EXPERIMENT.experiment_id}_reference",
        source_module=module_name,
        fold_metrics=result.fold_metrics,
        oof_predictions=result.oof_predictions,
    )


def run_sklearn_champion_reference(
    project_root: Path,
    raw_train: pd.DataFrame,
    *,
    module_name: str | None,
    target: str,
    key: str,
    feature_groups: Mapping[str, Sequence[str]],
    cv_splits: Sequence[tuple[np.ndarray, np.ndarray]],
) -> MLPReferenceResult:
    """Evaluate the accepted sklearn champion on the candidate's exact folds."""

    from sklearn.base import clone

    from . import baseline_config
    from . import experiment as experiment_tools
    from . import modeling as modeling_tools

    initial_settings = baseline_config.BASELINE
    reference_data = experiment_tools.prepare_reference_experiment_data(
        module_name,
        raw_train,
        feature_groups,
        initial_settings,
    )
    settings = reference_data.settings
    plan = modeling_tools.resolve_feature_plan(
        reference_data.frame,
        reference_data.feature_groups,
        target=target,
        key=key,
        settings=settings,
    )
    data = modeling_tools.prepare_training_data(
        reference_data.frame,
        target=target,
        plan=plan,
        settings=settings,
    )
    if not data.row_index.equals(raw_train.index):
        raise ValueError("sklearn reference changed row order; folds are not comparable")
    # Parent pipelines may begin with raw feature transformers (for example
    # TitleExtractor) that need columns excluded from the final model matrix.
    reference_x = reference_data.frame.loc[data.row_index].drop(columns=[target])
    preprocessor = modeling_tools.build_tabular_preprocessor(settings, plan)
    template = experiment_tools.build_reference_pipeline(
        module_name,
        preprocessor,
        settings,
    )
    y = data.y.to_numpy(dtype=np.int64)
    oof_probability = np.full(len(y), np.nan, dtype=float)
    oof_fold = np.zeros(len(y), dtype=int)
    metrics: list[dict[str, float | int]] = []
    for fold, (train_idx, valid_idx) in enumerate(cv_splits, start=1):
        pipeline = clone(template)
        pipeline.fit(reference_x.iloc[train_idx], data.y.iloc[train_idx])
        class_index = list(pipeline.classes_).index(1)
        probability = pipeline.predict_proba(reference_x.iloc[valid_idx])[:, class_index]
        oof_probability[valid_idx] = probability
        oof_fold[valid_idx] = fold
        metrics.append(_metric_row(fold, y[valid_idx], probability, 0.5))
    if not np.isfinite(oof_probability).all():
        raise RuntimeError("sklearn reference OOF predictions are incomplete")
    name = "sklearn_champion" if module_name else "logistic_baseline"
    oof = pd.DataFrame(
        {
            key: raw_train[key].to_numpy(),
            "fold": oof_fold,
            "target": y,
            "probability": oof_probability,
            "prediction": (oof_probability >= 0.5).astype("int64"),
        },
        index=raw_train.index,
    )
    return MLPReferenceResult(
        name=name,
        source_module=module_name or "ml_project.baseline_config.BASELINE",
        fold_metrics=pd.DataFrame(metrics),
        oof_predictions=oof,
    )


def compare_mlp_with_reference(
    candidate: MLPCVResult,
    reference: MLPReferenceResult,
    spec: MLPExperimentSpec,
) -> MLPComparison:
    """Build paired fold deltas where positive always means improvement."""

    metric_columns = [column for column in candidate.fold_metrics if column != "fold"]
    candidate_summary = candidate.fold_metrics[metric_columns].agg(
        ["mean", "std", "min", "max"]
    ).T.assign(model="mlp_candidate")
    reference_summary = reference.fold_metrics[metric_columns].agg(
        ["mean", "std", "min", "max"]
    ).T.assign(model=reference.name)
    summary = pd.concat([reference_summary, candidate_summary]).reset_index(
        names="metric"
    )[["model", "metric", "mean", "std", "min", "max"]]
    paired_rows: list[dict[str, Any]] = []
    for metric in metric_columns:
        merged = reference.fold_metrics[["fold", metric]].merge(
            candidate.fold_metrics[["fold", metric]],
            on="fold",
            suffixes=("_reference", "_candidate"),
            validate="one_to_one",
        )
        for row in merged.itertuples(index=False):
            raw_delta = getattr(row, f"{metric}_candidate") - getattr(
                row, f"{metric}_reference"
            )
            improvement = -raw_delta if metric == "log_loss" else raw_delta
            paired_rows.append(
                {
                    "fold": row.fold,
                    "metric": metric,
                    "reference": getattr(row, f"{metric}_reference"),
                    "candidate": getattr(row, f"{metric}_candidate"),
                    "improvement": improvement,
                }
            )
    paired = pd.DataFrame(paired_rows)
    thresholds = {spec.primary_metric: spec.primary_improvement_min, **dict(spec.metric_guardrails)}
    criteria_rows = []
    for metric, minimum in thresholds.items():
        rows = paired[paired["metric"].eq(metric)]
        if rows.empty:
            raise ValueError(f"Unknown MLP success metric: {metric}")
        observed = float(rows["improvement"].mean())
        criteria_rows.append(
            {
                "role": "primary" if metric == spec.primary_metric else "guardrail",
                "metric": metric,
                "observed_improvement": observed,
                "minimum_improvement": float(minimum),
                "passed": observed >= float(minimum),
            }
        )
    return MLPComparison(
        summary=summary,
        paired_deltas=paired,
        criteria=pd.DataFrame(criteria_rows),
        reference=reference,
    )


def plot_training_histories(result: MLPCVResult):
    """Построить кривые обучения по всем folds."""
    fig, ax = plt.subplots(figsize=(9, 5))
    for fold, history in result.histories.items():
        ax.plot(history["epoch"], history["inner_val_loss"], label=f"fold {fold}")
        best_epoch = int(history["best_epoch"].iloc[0])
        ax.scatter(
            [best_epoch],
            [history.loc[history["epoch"].eq(best_epoch), "inner_val_loss"].iloc[0]],
            s=25,
        )
    ax.set(title="Inner validation loss by outer fold", xlabel="Epoch", ylabel="BCE loss")
    ax.grid(alpha=0.2)
    ax.legend(ncol=2)
    fig.tight_layout()
    return fig


def load_mlp_experiment(module_name: str):
    """Загрузить versioned-модуль MLP-эксперимента."""
    module = importlib.import_module(module_name)
    required = ("EXPERIMENT", "prepare_features", "build_network")
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise AttributeError(f"MLP experiment module is missing: {missing}")
    if not isinstance(module.EXPERIMENT, MLPExperimentSpec):
        raise TypeError("EXPERIMENT must be MLPExperimentSpec")
    return module


def source_sha256(module: Any) -> str:
    """Рассчитать SHA-256 исходного файла Python-модуля."""
    path = Path(inspect.getsourcefile(module) or "")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_mlp_run(
    project_root: Path,
    module: Any,
    prepared: MLPFeatureData,
    result: MLPCVResult,
    *,
    target: str,
    key: str,
    dataset_path: Path,
    comparison: MLPComparison | None = None,
) -> Path:
    """Save exact inputs, OOF outputs and configuration for one CV run."""

    spec: MLPExperimentSpec = module.EXPERIMENT
    module_hash = source_sha256(module)
    run_dir = (
        Path(project_root)
        / spec.artifact_dir
        / spec.experiment_id
        / module_hash[:12]
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    result.fold_metrics.to_csv(run_dir / "fold_metrics.csv", index=False)
    result.summary.to_csv(run_dir / "summary.csv", index_label="metric")
    result.oof_predictions.to_csv(run_dir / "oof_predictions.csv", index=False)
    histories = pd.concat(
        [history.assign(fold=fold) for fold, history in result.histories.items()],
        ignore_index=True,
    )
    histories.to_csv(run_dir / "training_history.csv", index=False)
    if comparison is not None:
        comparison.summary.to_csv(run_dir / "comparison_summary.csv", index=False)
        comparison.paired_deltas.to_csv(run_dir / "paired_deltas.csv", index=False)
        comparison.criteria.to_csv(run_dir / "success_criteria.csv", index=False)
        comparison.reference.oof_predictions.to_csv(
            run_dir / "reference_oof_predictions.csv", index=False
        )
    figure = plot_training_histories(result)
    figure.savefig(run_dir / "training_history.png", dpi=160, bbox_inches="tight")
    plt.close(figure)
    metadata = {
        "experiment": {
            **asdict(spec),
            "artifact_dir": str(spec.artifact_dir),
        },
        "module": module.__name__,
        "module_sha256": module_hash,
        "dataset": str(dataset_path.relative_to(project_root)),
        "dataset_sha256": hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
        "target": target,
        "key": key,
        "numeric_features": list(prepared.numeric_features),
        "categorical_features": list(prepared.categorical_features),
        "fold_generated_features": list(prepared.fold_generated_features),
        "input_dims": result.input_dims,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if comparison is not None:
        metadata.update(
            {
                "reference_name": comparison.reference.name,
                "reference_module": comparison.reference.source_module,
                "criteria_passed": bool(comparison.criteria["passed"].all()),
                "success_criteria": comparison.criteria.to_dict(orient="records"),
            }
        )
    (run_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return run_dir


def _frontmatter_value(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    match = re.search(
        rf'''(?m)^{re.escape(key)}:\s*["']?([^\n"']+)["']?\s*$''',
        path.read_text(encoding="utf-8"),
    )
    return match.group(1).strip() if match else None


def _ensure_mlp_overview_files(project_root: Path) -> None:
    directory = project_root / "mlp-experiments"
    directory.mkdir(parents=True, exist_ok=True)
    index = directory / "_index.md"
    if not index.exists():
        index.write_text(
            "# PyTorch MLP experiments\n\n"
            "<!-- auto:mlp-experiment-registry:start -->\n\n"
            "Результаты появятся после первого запуска.\n\n"
            "<!-- auto:mlp-experiment-registry:end -->\n",
            encoding="utf-8",
        )


def _refresh_mlp_overviews(project_root: Path, registry: pd.DataFrame) -> None:
    _ensure_mlp_overview_files(project_root)
    public = registry.copy()
    if public.empty:
        block = "Результаты появятся после первого запуска."
    else:
        public["Эксперимент"] = public.apply(
            lambda row: f"[[{row['note']}|{row['experiment_id']} — {row['title']}]]",
            axis=1,
        )
        public["Результат"] = public.apply(
            lambda row: f"{float(row['candidate_score']):.4f} ± {float(row['candidate_std']):.4f}",
            axis=1,
        )
        public["Δ"] = public["improvement"].map(lambda value: f"{float(value):+.4f}")
        public = public.rename(
            columns={"reference": "Reference", "decision": "Решение"}
        )[["Эксперимент", "Reference", "Результат", "Δ", "Решение"]]
        block = dataframe_to_markdown(public)
    MarkdownDocument(project_root / "mlp-experiments/_index.md").update_blocks(
        {"mlp-experiment-registry": block}
    )
    readme = project_root / "README.md"
    if readme.exists() and "<!-- auto:mlp-results:start -->" in readme.read_text(encoding="utf-8"):
        MarkdownDocument(readme).update_blocks({"mlp-results": block})


def sync_mlp_report(
    project_root: Path,
    module: Any,
    prepared: MLPFeatureData,
    result: MLPCVResult,
    comparison: MLPComparison,
    run_dir: Path,
    *,
    dataset_path: Path,
) -> Path:
    """Create/update the Obsidian card, MLP registry and README summary."""

    root = Path(project_root).resolve()
    spec: MLPExperimentSpec = module.EXPERIMENT
    note_path = root / spec.experiment_note
    note_path.parent.mkdir(parents=True, exist_ok=True)
    decision = _frontmatter_value(note_path, "decision") or "pending"
    if decision not in {"pending", "adopt", "reject", "iterate", "inconclusive"}:
        raise ValueError(f"Unknown MLP decision in {note_path}: {decision}")
    if not note_path.exists():
        note_path.write_text(
            "---\n"
            f"id: {spec.experiment_id}\n"
            "type: mlp-experiment\n"
            "status: completed\n"
            f"decision: {decision}\n"
            f"implementation_module: {module.__name__}\n"
            "---\n\n"
            f"# {spec.experiment_id} — {spec.title}\n\n"
            "← [[mlp-experiments/_index.md|Реестр MLP]]\n\n"
            "> [!info] Автоматическая часть\n"
            "> Повторный запуск заменяет только отчёт между маркерами.\n\n"
            "<!-- auto:mlp-experiment-report:start -->\n\n"
            "Отчёт появится после запуска notebook.\n\n"
            "<!-- auto:mlp-experiment-report:end -->\n\n"
            "## Анализ и решение\n\n"
            "- Почему получился такой результат:\n"
            "- Какие ошибки исправлены / добавлены:\n"
            "- Что видно по кривым обучения:\n"
            "- Следующий контролируемый эксперимент:\n",
            encoding="utf-8",
        )
    primary_rows = comparison.summary[
        comparison.summary["metric"].eq(spec.primary_metric)
    ].set_index("model")
    candidate_row = primary_rows.loc["mlp_candidate"]
    reference_row = primary_rows.loc[comparison.reference.name]
    primary_paired = comparison.paired_deltas[
        comparison.paired_deltas["metric"].eq(spec.primary_metric)
    ]
    wins = int((primary_paired["improvement"] > 0).sum())
    losses = int((primary_paired["improvement"] < 0).sum())
    ties = int((primary_paired["improvement"] == 0).sum())
    candidate_oof = result.oof_predictions.set_index(result.oof_predictions.columns[0])
    reference_oof = comparison.reference.oof_predictions.set_index(
        comparison.reference.oof_predictions.columns[0]
    )
    aligned = candidate_oof[["target", "prediction"]].join(
        reference_oof[["prediction"]].rename(columns={"prediction": "reference_prediction"}),
        how="inner",
        validate="one_to_one",
    )
    corrected = int(
        ((aligned["prediction"] == aligned["target"]) &
         (aligned["reference_prediction"] != aligned["target"])).sum()
    )
    introduced = int(
        ((aligned["prediction"] != aligned["target"]) &
         (aligned["reference_prediction"] == aligned["target"])).sum()
    )
    overview = pd.DataFrame(
        [
            ("Эксперимент", f"{spec.experiment_id} — {spec.title}"),
            ("Гипотеза", spec.hypothesis),
            ("Одно изменение", spec.change_description),
            ("Решение", decision),
            ("Reference", f"{comparison.reference.name}: {comparison.reference.source_module}"),
            ("Validation", f"stratified_kfold(n_splits={spec.n_splits}, shuffle=True, seed={spec.training.random_state})"),
            ("Основная метрика", spec.primary_metric),
            ("Критерии", "passed" if comparison.criteria["passed"].all() else "failed"),
            ("Код", module.__name__),
            ("Hash кода", source_sha256(module)[:12] + "…"),
        ],
        columns=["Поле", "Значение"],
    )
    report = "\n\n".join(
        [
            "## Контракт эксперимента\n\n" + dataframe_to_markdown(overview),
            "## Проверка pre-registered criteria\n\n"
            + dataframe_to_markdown(comparison.criteria, float_digits=4),
            "## Сравнение всех метрик\n\n"
            + dataframe_to_markdown(comparison.summary, float_digits=4),
            "## Paired Δ по folds\n\n"
            + dataframe_to_markdown(comparison.paired_deltas, float_digits=4),
            "## OOF-изменения ошибок\n\n"
            + dataframe_to_markdown(
                pd.DataFrame(
                    [
                        {"Исправлено ошибок reference": corrected,
                         "Добавлено новых ошибок": introduced,
                         "Fold wins": wins, "Fold losses": losses, "Ties": ties}
                    ]
                )
            ),
            "## Артефакты\n\n"
            + "\n".join(
                [
                    f"- Run: [[{run_dir.relative_to(root).as_posix()}/metadata.json|metadata.json]]",
                    f"- OOF: [[{run_dir.relative_to(root).as_posix()}/oof_predictions.csv|oof_predictions.csv]]",
                    f"- Paired folds: [[{run_dir.relative_to(root).as_posix()}/paired_deltas.csv|paired_deltas.csv]]",
                    f"- Training history: [[{run_dir.relative_to(root).as_posix()}/training_history.png|training_history.png]]",
                ]
            ),
        ]
    )
    MarkdownDocument(note_path).update_blocks({"mlp-experiment-report": report})

    registry_path = root / spec.results_registry
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    if registry_path.exists() and registry_path.stat().st_size:
        registry = pd.read_csv(registry_path)
    else:
        registry = pd.DataFrame()
    row = {
        "experiment_id": spec.experiment_id,
        "title": spec.title,
        "note": spec.experiment_note.as_posix(),
        "hypothesis": spec.hypothesis,
        "change": spec.change_description,
        "primary_metric": spec.primary_metric,
        "reference": comparison.reference.name,
        "reference_module": comparison.reference.source_module,
        "reference_score": float(reference_row["mean"]),
        "reference_std": float(reference_row["std"]),
        "candidate_score": float(candidate_row["mean"]),
        "candidate_std": float(candidate_row["std"]),
        "improvement": float(primary_paired["improvement"].mean()),
        "criteria_passed": bool(comparison.criteria["passed"].all()),
        "decision": decision,
        "implementation_module": module.__name__,
        "implementation_sha256": source_sha256(module),
        "dataset_sha256": hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
        "artifact_dir": run_dir.relative_to(root).as_posix(),
    }
    if not registry.empty and "experiment_id" in registry:
        registry = registry[registry["experiment_id"] != spec.experiment_id]
    registry = pd.concat([registry, pd.DataFrame([row])], ignore_index=True)
    registry = registry.sort_values("experiment_id", kind="stable")
    registry.to_csv(registry_path, index=False)
    _refresh_mlp_overviews(root, registry)
    return note_path


def sync_mlp_state(project_root: Path) -> dict[str, int]:
    """Propagate manually edited card decisions without retraining."""

    root = Path(project_root).resolve()
    registry_path = root / "mlp-experiments/results.csv"
    if not registry_path.exists():
        return {"cards": 0, "updated_rows": 0}
    registry = pd.read_csv(registry_path)
    updated = 0
    cards = 0
    for note in (root / "mlp-experiments").glob("MLP-*.md"):
        experiment_id = _frontmatter_value(note, "id")
        decision = _frontmatter_value(note, "decision")
        if not experiment_id or not decision:
            continue
        cards += 1
        text = note.read_text(encoding="utf-8")
        updated_text = re.sub(
            r"(?m)^\| Решение\s*\|[^\n]*\|$",
            f"| Решение          | {decision} |",
            text,
            count=1,
        )
        if updated_text != text:
            note.write_text(updated_text, encoding="utf-8")
        mask = registry["experiment_id"].eq(experiment_id)
        if mask.any() and not registry.loc[mask, "decision"].eq(decision).all():
            registry.loc[mask, "decision"] = decision
            updated += int(mask.sum())
    registry.to_csv(registry_path, index=False)
    _refresh_mlp_overviews(root, registry)
    return {"cards": cards, "updated_rows": updated}


def fit_final_mlp(
    prepared: MLPFeatureData,
    *,
    target: str,
    build_network: Callable[[int], Any],
    spec: MLPExperimentSpec,
    build_fold_transformer: Callable[[], Any] | None = None,
) -> FittedMLP:
    """Обучить финальную MLP на всей размеченной выборке."""
    return fit_prepared_mlp(
        prepared,
        np.arange(len(prepared.frame)),
        target=target,
        build_network=build_network,
        config=spec.training,
        seed=spec.training.random_state + 10_000,
        build_fold_transformer=build_fold_transformer,
    )


def save_final_mlp(run_dir: Path, fitted: FittedMLP) -> None:
    """Сохранить веса, preprocessing и историю финальной MLP."""
    torch, _, _, _ = _torch()
    torch.save(
        {
            "state_dict": {
                key: value.detach().cpu().clone()
                for key, value in fitted.model.state_dict().items()
            },
            "input_dim": fitted.input_dim,
            "best_epoch": fitted.best_epoch,
        },
        Path(run_dir) / "final_model.pt",
    )
    joblib.dump(fitted.preprocessor, Path(run_dir) / "preprocessor.joblib")
    fitted.history.to_csv(Path(run_dir) / "final_training_history.csv", index=False)


__all__ = [
    "FittedMLP",
    "MLPCVResult",
    "MLPComparison",
    "MLPExperimentSpec",
    "MLPFeatureData",
    "MLPReferenceResult",
    "MLPTrainingConfig",
    "build_preprocessor",
    "compare_mlp_with_reference",
    "fit_final_mlp",
    "load_mlp_experiment",
    "plot_training_histories",
    "predict_prepared_mlp",
    "run_mlp_cv",
    "run_mlp_parent_reference",
    "run_sklearn_champion_reference",
    "save_final_mlp",
    "save_mlp_run",
    "sync_mlp_report",
    "sync_mlp_state",
    "validate_feature_data",
]
