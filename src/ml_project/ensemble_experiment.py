"""Reproducible soft-voting experiment across diverse Titanic models."""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold

from . import config as project_config
from .baseline_config import BASELINE
from .mlp_experiment import run_mlp_cv
from .modeling.contracts import ModelGroupSettings
from .modeling.screening import (
    build_screening_candidate_pipeline,
    prepare_screening_context,
)


@dataclass(frozen=True)
class EnsembleSpec:
    """Immutable choices for one probability-averaging experiment."""

    experiment_id: str = "ENS-001"
    title: str = "Probability averaging of five diverse models"
    feature_reference_module: str = "ml_project.experiments.exp_013_tt_comb"
    mlp_module: str = "ml_project.mlp_experiments.mlp_024_dpoutmedium"
    members: tuple[str, ...] = (
        "logistic_regression",
        "random_forest",
        "xgboost",
        "catboost",
        "mlp_024",
    )
    n_splits: int = 5
    random_state: int = 42
    threshold: float = 0.5
    artifact_dir: Path = Path("artifacts/ensembles/ENS-001")
    note_path: Path = Path("ensembles/ENS-001 Probability averaging.md")


SPEC = EnsembleSpec()

SPEC_002 = EnsembleSpec(
    experiment_id="ENS-002",
    title="Probability averaging of XGBoost, LightGBM, CatBoost and MLP-024",
    members=("xgboost", "lightgbm", "catboost", "mlp_024"),
    artifact_dir=Path("artifacts/ensembles/ENS-002"),
    note_path=Path("ensembles/ENS-002 Strong models averaging.md"),
)


@dataclass(frozen=True)
class WeightedEnsembleSpec(EnsembleSpec):
    """Nested-CV contract for weights learned without outer-fold leakage."""

    inner_n_splits: int = 4
    weight_objective: str = "log_loss"


SPEC_003 = WeightedEnsembleSpec(
    experiment_id="ENS-003",
    title="Nested-CV learned weights for four strong models",
    members=("xgboost", "lightgbm", "catboost", "mlp_024"),
    artifact_dir=Path("artifacts/ensembles/ENS-003"),
    note_path=Path("ensembles/ENS-003 Learned weights.md"),
)

# These are copied from the Obsidian-recorded screening runs. Keeping the
# values here makes ENS-001 independent of later edits to model_screening_config.py.
MODEL_SOURCES: Mapping[str, str] = {
    "logistic_regression": "EXP-013 feature champion",
    "random_forest": "MS-002",
    "xgboost": "MS-005",
    "lightgbm": "MS-005",
    "catboost": "MS-006",
    "mlp_024": "MLP-024",
}

MODEL_PARAMETERS: Mapping[str, Mapping[str, Any]] = {
    "random_forest": {
        "n_estimators": 400,
        "max_depth": 7,
        "min_samples_leaf": 3,
        "max_features": "sqrt",
    },
    "xgboost": {
        "n_estimators": 350,
        "learning_rate": 0.04,
        "max_depth": 3,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
    },
    "lightgbm": {
        "n_estimators": 350,
        "learning_rate": 0.04,
        "num_leaves": 15,
        "max_depth": 5,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
    },
    "catboost": {
        "iterations": 400,
        "learning_rate": 0.04,
        "depth": 5,
        "l2_leaf_reg": 5.0,
    },
}

MODEL_GROUPS_FROZEN: Mapping[str, ModelGroupSettings] = {
    "tree_bagging": ModelGroupSettings(
        group_id="tree_bagging",
        title="ENS-001 tree preprocessing",
        preprocessing_profile="unscaled_sparse",
        models=(),
    ),
    "external_boosting": ModelGroupSettings(
        group_id="external_boosting",
        title="ENS-001 boosting preprocessing",
        preprocessing_profile="unscaled_sparse",
        models=(),
    ),
    "native_categorical": ModelGroupSettings(
        group_id="native_categorical",
        title="ENS-001 CatBoost preprocessing",
        preprocessing_profile="native_categorical",
        models=(),
    ),
}


@dataclass
class EnsembleResult:
    """OOF predictions and diagnostics produced by the common CV run."""

    oof_predictions: pd.DataFrame
    fold_metrics: pd.DataFrame
    summary: pd.DataFrame
    probability_correlations: pd.DataFrame
    prediction_disagreements: pd.DataFrame
    error_overlap: pd.DataFrame
    cv_splits: tuple[tuple[np.ndarray, np.ndarray], ...]
    learned_weights: pd.DataFrame | None = None


def _positive_probability(model: Any, frame: pd.DataFrame) -> np.ndarray:
    probabilities = np.asarray(model.predict_proba(frame), dtype=float)
    if probabilities.ndim != 2 or probabilities.shape[1] != 2:
        raise ValueError("Every ENS-001 member must return two-class probabilities")
    classes = np.asarray(getattr(model, "classes_", [0, 1]))
    positive = np.flatnonzero(classes == 1)
    if len(positive) != 1:
        raise ValueError("Every ENS-001 member must expose class 1")
    return probabilities[:, int(positive[0])]


def _metric_values(y_true: np.ndarray, probability: np.ndarray, threshold: float) -> dict[str, float]:
    prediction = (probability >= threshold).astype("int64")
    return {
        "accuracy": accuracy_score(y_true, prediction),
        "balanced_accuracy": balanced_accuracy_score(y_true, prediction),
        "precision": precision_score(y_true, prediction, zero_division=0),
        "recall": recall_score(y_true, prediction, zero_division=0),
        "f1": f1_score(y_true, prediction, zero_division=0),
        "roc_auc": roc_auc_score(y_true, probability),
        "log_loss": log_loss(y_true, probability, labels=[0, 1]),
    }


def _screening_pipeline(context: Any, group_name: str, model_id: str) -> Any:
    group = MODEL_GROUPS_FROZEN[group_name]
    return build_screening_candidate_pipeline(
        context,
        group,
        model_id,
        MODEL_PARAMETERS[model_id],
    )


def run_probability_ensemble(
    project_root: str | Path,
    train: pd.DataFrame,
    *,
    spec: EnsembleSpec = SPEC,
) -> EnsembleResult:
    """Fit all members on identical outer folds and average their OOF probabilities."""

    root = Path(project_root).resolve()
    context = prepare_screening_context(
        root,
        train,
        project_config.FEATURE_GROUPS,
        target=project_config.TARGET,
        key=project_config.KEY,
        initial_settings=BASELINE,
        feature_reference_module=spec.feature_reference_module,
    )
    y = context.data.y.to_numpy(dtype="int64")
    splitter = StratifiedKFold(
        n_splits=spec.n_splits,
        shuffle=True,
        random_state=spec.random_state,
    )
    splits = tuple(
        (np.asarray(train_idx), np.asarray(valid_idx))
        for train_idx, valid_idx in splitter.split(np.zeros(len(y)), y)
    )

    supported = set(MODEL_SOURCES)
    unknown = set(spec.members) - supported
    if unknown:
        raise ValueError(f"Unknown ensemble members: {sorted(unknown)}")
    if len(spec.members) < 2 or len(spec.members) != len(set(spec.members)):
        raise ValueError("Ensemble members must contain at least two unique models")

    pipeline_builders = {
        "logistic_regression": lambda: clone(context.reference_pipeline),
        "random_forest": lambda: _screening_pipeline(context, "tree_bagging", "random_forest"),
        "xgboost": lambda: _screening_pipeline(context, "external_boosting", "xgboost"),
        "lightgbm": lambda: _screening_pipeline(context, "external_boosting", "lightgbm"),
        "catboost": lambda: _screening_pipeline(context, "native_categorical", "catboost"),
    }
    pipelines = {
        model_id: pipeline_builders[model_id]()
        for model_id in spec.members
        if model_id != "mlp_024"
    }
    probabilities = {
        model_id: np.full(len(y), np.nan, dtype=float)
        for model_id in spec.members
    }
    folds = np.zeros(len(y), dtype="int64")
    for fold, (train_idx, valid_idx) in enumerate(splits, start=1):
        folds[valid_idx] = fold
        for model_id, pipeline in pipelines.items():
            fitted = clone(pipeline).fit(
                context.data.X.iloc[train_idx],
                context.data.y.iloc[train_idx],
            )
            probabilities[model_id][valid_idx] = _positive_probability(
                fitted,
                context.data.X.iloc[valid_idx],
            )

    if "mlp_024" in spec.members:
        mlp_module = importlib.reload(importlib.import_module(spec.mlp_module))
        prepared_mlp = mlp_module.prepare_features(train.copy(deep=True))
        mlp_result = run_mlp_cv(
            prepared_mlp,
            target=project_config.TARGET,
            key=project_config.KEY,
            build_network=mlp_module.build_network,
            spec=mlp_module.EXPERIMENT,
            build_fold_transformer=getattr(mlp_module, "build_fold_transformer", None),
            cv_splits=splits,
        )
        probabilities["mlp_024"] = mlp_result.oof_predictions["probability"].to_numpy()

    if any(not np.isfinite(values).all() for values in probabilities.values()):
        raise RuntimeError("At least one ensemble member produced incomplete OOF probabilities")
    probabilities["ensemble_mean"] = np.column_stack(list(probabilities.values())).mean(axis=1)

    oof = pd.DataFrame(
        {
            project_config.KEY: train[project_config.KEY].to_numpy(),
            "fold": folds,
            "target": y,
            **{f"probability_{key}": value for key, value in probabilities.items()},
        }
    )
    for model_id, probability in probabilities.items():
        oof[f"prediction_{model_id}"] = (probability >= spec.threshold).astype("int64")

    fold_rows: list[dict[str, Any]] = []
    for fold in range(1, spec.n_splits + 1):
        mask = folds == fold
        for model_id, probability in probabilities.items():
            fold_rows.append(
                {
                    "fold": fold,
                    "model": model_id,
                    **_metric_values(y[mask], probability[mask], spec.threshold),
                }
            )
    fold_metrics = pd.DataFrame(fold_rows)
    metric_columns = [
        "accuracy", "balanced_accuracy", "precision", "recall", "f1", "roc_auc", "log_loss"
    ]
    summary = (
        fold_metrics.groupby("model", sort=False)[metric_columns]
        .agg(["mean", "std"])
    )
    summary.columns = [f"{metric}_{stat}" for metric, stat in summary.columns]
    summary = summary.reset_index().sort_values("accuracy_mean", ascending=False, ignore_index=True)

    member_ids = [key for key in probabilities if key != "ensemble_mean"]
    probability_frame = pd.DataFrame({key: probabilities[key] for key in member_ids})
    correlations = probability_frame.corr()
    predictions = probability_frame.ge(spec.threshold).astype("int64")
    disagreements = pd.DataFrame(index=member_ids, columns=member_ids, dtype=float)
    errors = predictions.ne(y, axis=0)
    overlaps = pd.DataFrame(index=member_ids, columns=member_ids, dtype=float)
    for left in member_ids:
        for right in member_ids:
            disagreements.loc[left, right] = float((predictions[left] != predictions[right]).mean())
            union = errors[left] | errors[right]
            overlaps.loc[left, right] = float((errors[left] & errors[right]).sum() / max(1, union.sum()))

    return EnsembleResult(oof, fold_metrics, summary, correlations, disagreements, overlaps, splits)


def _subset_mlp_features(prepared: Any, indices: np.ndarray) -> Any:
    """Create an index-clean MLPFeatureData view for one outer-train partition."""

    from .mlp_experiment import MLPFeatureData

    return MLPFeatureData(
        frame=prepared.frame.iloc[indices].reset_index(drop=True),
        numeric_features=prepared.numeric_features,
        categorical_features=prepared.categorical_features,
        fold_generated_features=prepared.fold_generated_features,
    )


def _learn_simplex_weights(
    probability_matrix: np.ndarray,
    target: np.ndarray,
) -> np.ndarray:
    """Minimize log loss under non-negative weights constrained to sum to one."""

    from scipy.optimize import minimize

    n_models = probability_matrix.shape[1]
    start = np.full(n_models, 1.0 / n_models)

    def objective(weights: np.ndarray) -> float:
        probability = np.clip(probability_matrix @ weights, 1e-7, 1 - 1e-7)
        return float(log_loss(target, probability, labels=[0, 1]))

    fitted = minimize(
        objective,
        start,
        method="SLSQP",
        bounds=[(0.0, 1.0)] * n_models,
        constraints={"type": "eq", "fun": lambda weights: float(weights.sum() - 1.0)},
        options={"maxiter": 500, "ftol": 1e-10},
    )
    if not fitted.success:
        raise RuntimeError(f"Weight optimization failed: {fitted.message}")
    weights = np.clip(np.asarray(fitted.x, dtype=float), 0.0, 1.0)
    return weights / weights.sum()


def run_nested_weighted_ensemble(
    project_root: str | Path,
    train: pd.DataFrame,
    *,
    spec: WeightedEnsembleSpec = SPEC_003,
) -> EnsembleResult:
    """Learn fold-specific simplex weights on inner OOF predictions."""

    root = Path(project_root).resolve()
    base_result = run_probability_ensemble(root, train, spec=spec)
    context = prepare_screening_context(
        root,
        train,
        project_config.FEATURE_GROUPS,
        target=project_config.TARGET,
        key=project_config.KEY,
        initial_settings=BASELINE,
        feature_reference_module=spec.feature_reference_module,
    )
    pipeline_builders = {
        "xgboost": lambda: _screening_pipeline(context, "external_boosting", "xgboost"),
        "lightgbm": lambda: _screening_pipeline(context, "external_boosting", "lightgbm"),
        "catboost": lambda: _screening_pipeline(context, "native_categorical", "catboost"),
    }
    mlp_module = importlib.reload(importlib.import_module(spec.mlp_module))
    prepared_mlp = mlp_module.prepare_features(train.copy(deep=True))
    y = context.data.y.to_numpy(dtype="int64")
    weighted_probability = np.full(len(y), np.nan, dtype=float)
    weight_rows: list[dict[str, Any]] = []

    for outer_fold, (outer_train, outer_valid) in enumerate(base_result.cv_splits, start=1):
        inner_splitter = StratifiedKFold(
            n_splits=spec.inner_n_splits,
            shuffle=True,
            random_state=spec.random_state + outer_fold,
        )
        y_outer = y[outer_train]
        inner_splits = tuple(
            (np.asarray(inner_train), np.asarray(inner_valid))
            for inner_train, inner_valid in inner_splitter.split(
                np.zeros(len(outer_train)), y_outer
            )
        )
        inner_probabilities = {
            model_id: np.full(len(outer_train), np.nan, dtype=float)
            for model_id in spec.members
        }
        for inner_train_local, inner_valid_local in inner_splits:
            train_indices = outer_train[inner_train_local]
            valid_indices = outer_train[inner_valid_local]
            for model_id in spec.members:
                if model_id == "mlp_024":
                    continue
                fitted = clone(pipeline_builders[model_id]()).fit(
                    context.data.X.iloc[train_indices],
                    context.data.y.iloc[train_indices],
                )
                inner_probabilities[model_id][inner_valid_local] = _positive_probability(
                    fitted,
                    context.data.X.iloc[valid_indices],
                )

        if "mlp_024" in spec.members:
            outer_prepared = _subset_mlp_features(prepared_mlp, outer_train)
            inner_mlp_spec = replace(mlp_module.EXPERIMENT, n_splits=spec.inner_n_splits)
            inner_mlp = run_mlp_cv(
                outer_prepared,
                target=project_config.TARGET,
                key=project_config.KEY,
                build_network=mlp_module.build_network,
                spec=inner_mlp_spec,
                build_fold_transformer=getattr(mlp_module, "build_fold_transformer", None),
                cv_splits=inner_splits,
            )
            inner_probabilities["mlp_024"] = inner_mlp.oof_predictions[
                "probability"
            ].to_numpy()

        matrix = np.column_stack([inner_probabilities[name] for name in spec.members])
        if not np.isfinite(matrix).all():
            raise RuntimeError(f"Inner OOF probabilities are incomplete in fold {outer_fold}")
        weights = _learn_simplex_weights(matrix, y_outer)
        outer_matrix = np.column_stack(
            [
                base_result.oof_predictions.loc[
                    outer_valid, f"probability_{name}"
                ].to_numpy()
                for name in spec.members
            ]
        )
        weighted_probability[outer_valid] = outer_matrix @ weights
        weight_rows.append(
            {
                "fold": outer_fold,
                **{name: float(weight) for name, weight in zip(spec.members, weights, strict=True)},
            }
        )

    oof = base_result.oof_predictions.copy()
    oof["probability_ensemble_mean"] = weighted_probability
    oof["prediction_ensemble_mean"] = (
        weighted_probability >= spec.threshold
    ).astype("int64")
    member_metrics = base_result.fold_metrics[
        ~base_result.fold_metrics["model"].eq("ensemble_mean")
    ].copy()
    ensemble_rows = []
    folds = oof["fold"].to_numpy()
    for fold in range(1, spec.n_splits + 1):
        mask = folds == fold
        ensemble_rows.append(
            {
                "fold": fold,
                "model": "ensemble_mean",
                **_metric_values(y[mask], weighted_probability[mask], spec.threshold),
            }
        )
    fold_metrics = pd.concat(
        [member_metrics, pd.DataFrame(ensemble_rows)], ignore_index=True
    )
    metric_columns = [
        "accuracy", "balanced_accuracy", "precision", "recall", "f1", "roc_auc", "log_loss"
    ]
    summary = fold_metrics.groupby("model", sort=False)[metric_columns].agg(["mean", "std"])
    summary.columns = [f"{metric}_{stat}" for metric, stat in summary.columns]
    summary = summary.reset_index().sort_values("accuracy_mean", ascending=False, ignore_index=True)
    return EnsembleResult(
        oof,
        fold_metrics,
        summary,
        base_result.probability_correlations,
        base_result.prediction_disagreements,
        base_result.error_overlap,
        base_result.cv_splits,
        pd.DataFrame(weight_rows),
    )


def save_ensemble_run(
    project_root: str | Path,
    result: EnsembleResult,
    *,
    spec: EnsembleSpec = SPEC,
) -> tuple[Path, Path]:
    """Save reviewable artifacts and update the ENS-001 Obsidian card."""

    root = Path(project_root).resolve()
    run_dir = root / spec.artifact_dir
    run_dir.mkdir(parents=True, exist_ok=True)
    result.oof_predictions.to_csv(run_dir / "oof_predictions.csv", index=False)
    result.fold_metrics.to_csv(run_dir / "fold_metrics.csv", index=False)
    result.summary.to_csv(run_dir / "summary.csv", index=False)
    result.probability_correlations.to_csv(run_dir / "probability_correlations.csv")
    result.prediction_disagreements.to_csv(run_dir / "prediction_disagreements.csv")
    result.error_overlap.to_csv(run_dir / "error_overlap.csv")
    if result.learned_weights is not None:
        result.learned_weights.to_csv(run_dir / "learned_weights.csv", index=False)
    metadata = {
        "experiment_id": spec.experiment_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "feature_reference_module": spec.feature_reference_module,
        "mlp_module": spec.mlp_module,
        "n_splits": spec.n_splits,
        "random_state": spec.random_state,
        "threshold": spec.threshold,
        "members": {name: MODEL_SOURCES[name] for name in spec.members},
        "parameters": {
            name: MODEL_PARAMETERS[name]
            for name in spec.members
            if name in MODEL_PARAMETERS
        },
        "weighting": (
            {
                "strategy": "nested_cv_simplex",
                "objective": getattr(spec, "weight_objective", "log_loss"),
                "inner_n_splits": getattr(spec, "inner_n_splits", None),
            }
            if result.learned_weights is not None
            else {"strategy": "equal_mean"}
        ),
    }
    (run_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    ensemble_row = result.summary.loc[result.summary["model"].eq("ensemble_mean")].iloc[0]
    best_single = result.summary.loc[~result.summary["model"].eq("ensemble_mean")].iloc[0]
    note_path = root / spec.note_path
    note_path.parent.mkdir(parents=True, exist_ok=True)
    members = "\n".join(
        f"- `{name}` — {MODEL_SOURCES[name]}" for name in spec.members
    )
    note = f"""---
id: {spec.experiment_id}
type: ensemble-experiment
status: completed
decision: pending
primary_metric: accuracy
---

# {spec.experiment_id} — {spec.title}

## Гипотеза

Модели разных семейств совершают разные ошибки, поэтому среднее их OOF-вероятностей может быть точнее лучшей одиночной модели.

## Состав

{members}

Все модели переобучены на одних и тех же пяти `StratifiedKFold` (`shuffle=True`, `seed=42`). {f'Веса обучены отдельно внутри каждого outer train fold на {getattr(spec, "inner_n_splits", 4)} внутренних OOF folds по log loss.' if result.learned_weights is not None else f'Итоговая вероятность — простое среднее {len(spec.members)} вероятностей.'} Порог — `0.5`.

## Результат

- Ensemble accuracy: **{ensemble_row['accuracy_mean']:.4f} ± {ensemble_row['accuracy_std']:.4f}**
- Лучший одиночный участник этого же запуска: **{best_single['model']}**, {best_single['accuracy_mean']:.4f} ± {best_single['accuracy_std']:.4f}
- Разница ensemble: **{ensemble_row['accuracy_mean'] - best_single['accuracy_mean']:+.4f}**
- Ensemble ROC-AUC: **{ensemble_row['roc_auc_mean']:.4f}**; лучший одиночный ROC-AUC: **{result.summary.loc[~result.summary['model'].eq('ensemble_mean'), 'roc_auc_mean'].max():.4f}**.
- Ensemble log loss: **{ensemble_row['log_loss_mean']:.4f}**; лучший одиночный log loss: **{result.summary.loc[~result.summary['model'].eq('ensemble_mean'), 'log_loss_mean'].min():.4f}**.
- Решение оставлено `pending`: сначала проверить таблицы разнообразия и только затем выбрать `adopt` или `reject`.

## Артефакты

- [[{spec.artifact_dir.as_posix()}/summary.csv|summary.csv]]
- [[{spec.artifact_dir.as_posix()}/fold_metrics.csv|fold_metrics.csv]]
- [[{spec.artifact_dir.as_posix()}/oof_predictions.csv|oof_predictions.csv]]
- [[{spec.artifact_dir.as_posix()}/probability_correlations.csv|probability_correlations.csv]]
- [[{spec.artifact_dir.as_posix()}/prediction_disagreements.csv|prediction_disagreements.csv]]
- [[{spec.artifact_dir.as_posix()}/error_overlap.csv|error_overlap.csv]]
{f'- [[{spec.artifact_dir.as_posix()}/learned_weights.csv|learned_weights.csv]]' if result.learned_weights is not None else ''}
- [[{spec.artifact_dir.as_posix()}/metadata.json|metadata.json]]
"""
    note_path.write_text(note, encoding="utf-8")
    return run_dir, note_path


__all__ = [
    "EnsembleResult",
    "EnsembleSpec",
    "WeightedEnsembleSpec",
    "MODEL_PARAMETERS",
    "MODEL_GROUPS_FROZEN",
    "MODEL_SOURCES",
    "SPEC",
    "SPEC_002",
    "SPEC_003",
    "run_probability_ensemble",
    "run_nested_weighted_ensemble",
    "save_ensemble_run",
]
