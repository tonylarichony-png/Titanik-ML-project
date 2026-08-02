"""Reusable, leakage-safe utilities for the first tabular ML baseline.

The notebook orchestrates these functions; it does not define preprocessing,
validation or evaluation logic itself. scikit-learn imports are intentionally
local so the earlier Data/EDA notebooks remain usable before modeling
dependencies are installed.
"""

from __future__ import annotations

import inspect
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from .docsync import MarkdownDocument, dataframe_to_markdown
from .profiling import FEATURE_GROUP_NAMES, validate_feature_groups


CLASSIFICATION_TASKS = {
    "binary_classification",
    "multiclass_classification",
}
SUPPORTED_TASKS = {*CLASSIFICATION_TASKS, "regression"}
SUPPORTED_CV_STRATEGIES = {
    "auto",
    "stratified_kfold",
    "kfold",
    "group_kfold",
    "time_series",
}
SUPPORTED_MODEL_FEATURE_GROUPS = {
    "numeric",
    "count",
    "categorical",
    "ordinal",
}


@dataclass(frozen=True)
class BaselineSettings:
    """Normalized values loaded from ``baseline_config.py``."""

    task_type: str | None
    model_feature_groups: tuple[str, ...]
    include_features: tuple[str, ...]
    exclude_features: tuple[str, ...]
    require_inference_features: bool
    primary_scorer: Any
    secondary_scorers: Mapping[str, Any]
    cv_strategy: str
    n_splits: int
    shuffle: bool
    random_state: int | None
    group_column: str | None
    time_column: str | None
    n_jobs: int | None
    error_score: str | float
    return_train_score: bool
    numeric_imputer: str
    numeric_fill_value: Any
    add_numeric_missing_indicator: bool
    numeric_scaler: str
    categorical_imputer: str
    categorical_fill_value: Any
    onehot_handle_unknown: str
    onehot_min_frequency: int | float | None
    onehot_max_categories: int | None
    onehot_sparse_output: bool
    column_transformer_sparse_threshold: float
    run_dummy_baseline: bool
    dummy_strategy: str
    dummy_params: Mapping[str, Any]
    model_name: str
    model_params: Mapping[str, Any]
    experiment_id: str
    experiment_title: str
    experiment_note: Path
    run_name: str
    artifact_dir: Path
    save_artifacts: bool
    save_metric_figures: bool
    metric_figure_dpi: int
    save_final_model: bool
    sync_docs: bool
    sync_experiment_note: bool
    allow_overwrite: bool


@dataclass(frozen=True)
class FeaturePlan:
    """Explicit model columns and the reason every other column is excluded."""

    numeric: tuple[str, ...]
    categorical: tuple[str, ...]
    excluded: tuple[str, ...]
    group_by_feature: Mapping[str, str]
    exclusion_reason: Mapping[str, str]
    warnings: tuple[str, ...] = ()

    @property
    def model_features(self) -> tuple[str, ...]:
        return (*self.numeric, *self.categorical)

    def to_frame(self) -> pd.DataFrame:
        rows: list[dict[str, str]] = []
        selected = set(self.model_features)
        for feature, group in self.group_by_feature.items():
            if feature in selected:
                role = "numeric" if feature in self.numeric else "categorical"
                rows.append(
                    {
                        "feature": feature,
                        "config_group": group,
                        "model_role": role,
                        "status": "used",
                        "reason": "",
                    }
                )
            else:
                rows.append(
                    {
                        "feature": feature,
                        "config_group": group,
                        "model_role": "—",
                        "status": "excluded",
                        "reason": self.exclusion_reason.get(
                            feature, "not selected for the baseline"
                        ),
                    }
                )
        return pd.DataFrame(rows)


@dataclass(frozen=True)
class PreparedData:
    """Train matrix, target and optional split-control groups."""

    X: pd.DataFrame
    y: pd.Series
    groups: pd.Series | None
    row_index: pd.Index


@dataclass(frozen=True)
class ScoringPlan:
    """Contract metric plus sklearn scoring implementations."""

    contract_metric: str
    scorers: Mapping[str, Any]
    labels: Mapping[str, str]
    directions: Mapping[str, str]
    negated: Mapping[str, bool]

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "role": "primary" if key == "primary" else "secondary",
                    "report_name": self.labels[key],
                    "sklearn_scorer": _display_value(scorer),
                    "direction": self.directions[key],
                }
                for key, scorer in self.scorers.items()
            ]
        )


@dataclass(frozen=True)
class CVEvaluation:
    """Fold-level and aggregated results for comparable model pipelines."""

    fold_scores: pd.DataFrame
    summary: pd.DataFrame
    raw_results: Mapping[str, Mapping[str, Any]]

    def primary_summary(self) -> pd.DataFrame:
        return self.summary[
            (self.summary["metric_key"] == "primary")
            & (self.summary["split"] == "validation")
        ].reset_index(drop=True)


@dataclass(frozen=True)
class SavedBaselineRun:
    """Paths created by an explicit baseline save action."""

    run_dir: Path
    fold_scores_path: Path
    summary_path: Path
    metadata_path: Path
    model_path: Path | None = None
    metric_figure_paths: Mapping[str, Path] | None = None


def settings_from_module(module: ModuleType) -> BaselineSettings:
    """Read the editable config module without caching its values."""

    return BaselineSettings(
        task_type=getattr(module, "TASK_TYPE"),
        model_feature_groups=tuple(getattr(module, "MODEL_FEATURE_GROUPS")),
        include_features=tuple(getattr(module, "INCLUDE_FEATURES")),
        exclude_features=tuple(getattr(module, "EXCLUDE_FEATURES")),
        require_inference_features=bool(
            getattr(module, "REQUIRE_INFERENCE_FEATURES")
        ),
        primary_scorer=getattr(module, "PRIMARY_SCORER"),
        secondary_scorers=dict(getattr(module, "SECONDARY_SCORERS")),
        cv_strategy=str(getattr(module, "CV_STRATEGY")).lower(),
        n_splits=int(getattr(module, "N_SPLITS")),
        shuffle=bool(getattr(module, "SHUFFLE")),
        random_state=getattr(module, "RANDOM_STATE"),
        group_column=getattr(module, "GROUP_COLUMN"),
        time_column=getattr(module, "TIME_COLUMN"),
        n_jobs=getattr(module, "N_JOBS"),
        error_score=getattr(module, "ERROR_SCORE"),
        return_train_score=bool(getattr(module, "RETURN_TRAIN_SCORE")),
        numeric_imputer=str(getattr(module, "NUMERIC_IMPUTER")).lower(),
        numeric_fill_value=getattr(module, "NUMERIC_FILL_VALUE"),
        add_numeric_missing_indicator=bool(
            getattr(module, "ADD_NUMERIC_MISSING_INDICATOR")
        ),
        numeric_scaler=str(getattr(module, "NUMERIC_SCALER")).lower(),
        categorical_imputer=str(
            getattr(module, "CATEGORICAL_IMPUTER")
        ).lower(),
        categorical_fill_value=getattr(module, "CATEGORICAL_FILL_VALUE"),
        onehot_handle_unknown=str(
            getattr(module, "ONEHOT_HANDLE_UNKNOWN")
        ),
        onehot_min_frequency=getattr(module, "ONEHOT_MIN_FREQUENCY"),
        onehot_max_categories=getattr(module, "ONEHOT_MAX_CATEGORIES"),
        onehot_sparse_output=bool(
            getattr(module, "ONEHOT_SPARSE_OUTPUT")
        ),
        column_transformer_sparse_threshold=float(
            getattr(module, "COLUMN_TRANSFORMER_SPARSE_THRESHOLD")
        ),
        run_dummy_baseline=bool(getattr(module, "RUN_DUMMY_BASELINE")),
        dummy_strategy=str(getattr(module, "DUMMY_STRATEGY")).lower(),
        dummy_params=dict(getattr(module, "DUMMY_PARAMS")),
        model_name=str(getattr(module, "MODEL_NAME")).lower(),
        model_params=dict(getattr(module, "MODEL_PARAMS")),
        experiment_id=str(getattr(module, "EXPERIMENT_ID")),
        experiment_title=str(getattr(module, "EXPERIMENT_TITLE")),
        experiment_note=Path(getattr(module, "EXPERIMENT_NOTE")),
        run_name=str(getattr(module, "RUN_NAME")),
        artifact_dir=Path(getattr(module, "ARTIFACT_DIR")),
        save_artifacts=bool(getattr(module, "SAVE_ARTIFACTS")),
        save_metric_figures=bool(getattr(module, "SAVE_METRIC_FIGURES")),
        metric_figure_dpi=int(getattr(module, "METRIC_FIGURE_DPI")),
        save_final_model=bool(getattr(module, "SAVE_FINAL_MODEL")),
        sync_docs=bool(getattr(module, "SYNC_DOCS")),
        sync_experiment_note=bool(getattr(module, "SYNC_EXPERIMENT_NOTE")),
        allow_overwrite=bool(getattr(module, "ALLOW_OVERWRITE")),
    )


def validate_baseline_settings(settings: BaselineSettings) -> list[str]:
    """Fail on unsafe/ambiguous values and return non-blocking warnings."""

    errors: list[str] = []
    warnings: list[str] = []

    if settings.task_type not in SUPPORTED_TASKS:
        errors.append(
            "TASK_TYPE must be one of: " + ", ".join(sorted(SUPPORTED_TASKS))
        )
    if settings.cv_strategy not in SUPPORTED_CV_STRATEGIES:
        errors.append(
            "CV_STRATEGY must be one of: "
            + ", ".join(sorted(SUPPORTED_CV_STRATEGIES))
        )
    if settings.n_splits < 2:
        errors.append("N_SPLITS must be at least 2")
    if settings.n_jobs == 0:
        errors.append("N_JOBS cannot be 0")
    if settings.cv_strategy == "group_kfold" and not settings.group_column:
        errors.append("GROUP_COLUMN is required for group_kfold")
    if settings.cv_strategy == "time_series" and not settings.time_column:
        errors.append("TIME_COLUMN is required for time_series")
    if settings.cv_strategy == "auto":
        warnings.append(
            "CV_STRATEGY='auto' удобна для первого запуска; после описания "
            "production-сценария зафиксируйте явную стратегию."
        )

    unknown_feature_groups = sorted(
        set(settings.model_feature_groups) - set(FEATURE_GROUP_NAMES)
    )
    unsupported_feature_groups = sorted(
        set(settings.model_feature_groups) - SUPPORTED_MODEL_FEATURE_GROUPS
    )
    if unknown_feature_groups:
        errors.append(
            "Unknown MODEL_FEATURE_GROUPS: "
            + ", ".join(unknown_feature_groups)
        )
    if unsupported_feature_groups:
        errors.append(
            "The first tabular baseline has no transformer for groups: "
            + ", ".join(unsupported_feature_groups)
        )
    overlap = sorted(set(settings.include_features) & set(settings.exclude_features))
    if overlap:
        errors.append(
            "Features cannot be both included and excluded: " + ", ".join(overlap)
        )

    if settings.numeric_imputer not in {
        "median",
        "mean",
        "most_frequent",
        "constant",
    }:
        errors.append("Unsupported NUMERIC_IMPUTER")
    if settings.numeric_scaler not in {"standard", "robust", "minmax", "none"}:
        errors.append("Unsupported NUMERIC_SCALER")
    if settings.categorical_imputer not in {"most_frequent", "constant"}:
        errors.append("Unsupported CATEGORICAL_IMPUTER")
    if not 0 <= settings.column_transformer_sparse_threshold <= 1:
        errors.append("COLUMN_TRANSFORMER_SPARSE_THRESHOLD must be between 0 and 1")

    if settings.model_name not in {"auto", "logistic_regression", "ridge"}:
        errors.append(
            "MODEL_NAME must be auto, logistic_regression or ridge for the "
            "reference baseline"
        )
    if (
        settings.task_type in CLASSIFICATION_TASKS
        and settings.model_name == "ridge"
    ):
        errors.append("ridge is a regression baseline, not a classifier")
    if settings.task_type == "regression" and settings.model_name == "logistic_regression":
        errors.append("logistic_regression cannot be used for regression")

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", settings.run_name):
        errors.append(
            "RUN_NAME must contain only letters, digits, dot, underscore or dash"
        )
    if settings.artifact_dir.is_absolute():
        errors.append("ARTIFACT_DIR must be relative to the project root")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", settings.experiment_id):
        errors.append(
            "EXPERIMENT_ID must contain only letters, digits, dot, underscore or dash"
        )
    if not settings.experiment_title.strip():
        errors.append("EXPERIMENT_TITLE cannot be empty")
    if settings.experiment_note.is_absolute():
        errors.append("EXPERIMENT_NOTE must be relative to the project root")
    if settings.experiment_note.suffix.lower() != ".md":
        errors.append("EXPERIMENT_NOTE must point to a Markdown (.md) file")
    if settings.metric_figure_dpi < 72:
        errors.append("METRIC_FIGURE_DPI must be at least 72")

    if errors:
        raise ValueError(
            "Invalid src/ml_project/baseline_config.py:\n"
            + "\n".join(f"- {error}" for error in errors)
        )
    return warnings


def settings_report(settings: BaselineSettings) -> pd.DataFrame:
    """Compact, human-readable report of the settings that change results."""

    rows = [
        ("task", "TASK_TYPE", settings.task_type),
        ("features", "MODEL_FEATURE_GROUPS", settings.model_feature_groups),
        ("features", "INCLUDE_FEATURES", settings.include_features or "all"),
        ("features", "EXCLUDE_FEATURES", settings.exclude_features or "none"),
        ("metric", "PRIMARY_SCORER", settings.primary_scorer or "from 00_problem"),
        ("metric", "SECONDARY_SCORERS", settings.secondary_scorers or "none"),
        ("validation", "CV_STRATEGY", settings.cv_strategy),
        ("validation", "N_SPLITS", settings.n_splits),
        ("validation", "SHUFFLE", settings.shuffle),
        ("validation", "RANDOM_STATE", settings.random_state),
        ("preprocessing", "NUMERIC_IMPUTER", settings.numeric_imputer),
        ("preprocessing", "NUMERIC_SCALER", settings.numeric_scaler),
        ("preprocessing", "CATEGORICAL_IMPUTER", settings.categorical_imputer),
        ("preprocessing", "ONEHOT_HANDLE_UNKNOWN", settings.onehot_handle_unknown),
        ("model", "RUN_DUMMY_BASELINE", settings.run_dummy_baseline),
        ("model", "MODEL_NAME", settings.model_name),
        ("model", "MODEL_PARAMS", settings.model_params or "defaults"),
        ("write", "EXPERIMENT_ID", settings.experiment_id),
        ("write", "EXPERIMENT_NOTE", settings.experiment_note),
        ("write", "RUN_NAME", settings.run_name),
        ("write", "SAVE_ARTIFACTS", settings.save_artifacts),
        ("write", "SAVE_METRIC_FIGURES", settings.save_metric_figures),
        ("write", "SAVE_FINAL_MODEL", settings.save_final_model),
        ("write", "SYNC_DOCS", settings.sync_docs),
        ("write", "SYNC_EXPERIMENT_NOTE", settings.sync_experiment_note),
        ("write", "ALLOW_OVERWRITE", settings.allow_overwrite),
    ]
    return pd.DataFrame(rows, columns=["section", "parameter", "value"])


def resolve_feature_plan(
    frame: pd.DataFrame,
    feature_groups: Mapping[str, Sequence[str]],
    *,
    target: str | None,
    key: str | None,
    settings: BaselineSettings,
) -> FeaturePlan:
    """Resolve explicit feature groups into model columns without dtype guessing."""

    if target is None:
        raise ValueError("TARGET is not configured in src/ml_project/config.py")
    if target not in frame.columns:
        raise KeyError(f"TARGET {target!r} is absent from the train dataset")

    normalized = validate_feature_groups(frame, feature_groups, target=target)
    group_by_feature = {
        feature: group
        for group, features in normalized.items()
        for feature in features
    }

    unknown_include = sorted(set(settings.include_features) - set(frame.columns))
    unknown_exclude = sorted(set(settings.exclude_features) - set(frame.columns))
    if unknown_include or unknown_exclude:
        messages = []
        if unknown_include:
            messages.append("INCLUDE_FEATURES absent from train: " + ", ".join(unknown_include))
        if unknown_exclude:
            messages.append("EXCLUDE_FEATURES absent from train: " + ", ".join(unknown_exclude))
        raise ValueError("\n".join(messages))

    forbidden_include = sorted(
        set(settings.include_features) & {value for value in (target, key) if value}
    )
    if forbidden_include:
        raise ValueError(
            "TARGET/KEY cannot be model features: " + ", ".join(forbidden_include)
        )

    enabled_groups = set(settings.model_feature_groups)
    group_candidates = {
        feature
        for group in enabled_groups
        for feature in normalized[group]
    }
    if settings.include_features:
        requested = set(settings.include_features)
        unsupported_requested = sorted(requested - group_candidates)
        if unsupported_requested:
            raise ValueError(
                "INCLUDE_FEATURES contains columns outside MODEL_FEATURE_GROUPS: "
                + ", ".join(unsupported_requested)
            )
        selected = requested
    else:
        selected = group_candidates

    selected -= set(settings.exclude_features)
    selected.discard(target)
    if key:
        selected.discard(key)

    numeric_groups = {"numeric", "count"}
    categorical_groups = {"categorical", "ordinal"}
    numeric = tuple(
        column
        for column in frame.columns
        if column in selected and group_by_feature.get(column) in numeric_groups
    )
    categorical = tuple(
        column
        for column in frame.columns
        if column in selected and group_by_feature.get(column) in categorical_groups
    )
    if not numeric and not categorical:
        raise ValueError(
            "The baseline has no model features. Fill FEATURE_GROUPS or adjust "
            "MODEL_FEATURE_GROUPS/INCLUDE_FEATURES."
        )

    exclusion_reason: dict[str, str] = {}
    warnings: list[str] = []
    for feature, group in group_by_feature.items():
        if feature in selected:
            continue
        if feature == key:
            reason = "project key / identifier"
        elif feature in settings.exclude_features:
            reason = "explicit EXCLUDE_FEATURES"
        elif settings.include_features and feature not in settings.include_features:
            reason = "outside INCLUDE_FEATURES whitelist"
        elif group not in enabled_groups:
            reason = f"group {group!r} is not enabled for this baseline"
        else:
            reason = "not selected"
        exclusion_reason[feature] = reason

    unsupported = [
        feature
        for feature, group in group_by_feature.items()
        if group in {"text", "datetime"} and feature not in selected
    ]
    if unsupported:
        warnings.append(
            "Текстовые и временные признаки намеренно исключены из первого "
            "табличного baseline: " + ", ".join(unsupported)
        )

    excluded = tuple(
        column
        for column in frame.columns
        if column != target and column not in selected
    )
    return FeaturePlan(
        numeric=numeric,
        categorical=categorical,
        excluded=excluded,
        group_by_feature=group_by_feature,
        exclusion_reason=exclusion_reason,
        warnings=tuple(warnings),
    )


def validate_inference_schema(
    inference: pd.DataFrame,
    plan: FeaturePlan,
    *,
    strict: bool = True,
) -> list[str]:
    """Check that inference can receive the exact training feature contract."""

    missing = [feature for feature in plan.model_features if feature not in inference]
    if missing and strict:
        raise ValueError(
            "Inference dataset lacks baseline features: " + ", ".join(missing)
        )
    return [
        "Inference dataset lacks baseline features: " + ", ".join(missing)
    ] if missing else []


def resolve_cv_strategy(settings: BaselineSettings) -> str:
    """Resolve the convenient ``auto`` strategy deterministically."""

    if settings.cv_strategy != "auto":
        return settings.cv_strategy
    return (
        "stratified_kfold"
        if settings.task_type in CLASSIFICATION_TASKS
        else "kfold"
    )


def prepare_training_data(
    frame: pd.DataFrame,
    *,
    target: str,
    plan: FeaturePlan,
    settings: BaselineSettings,
) -> PreparedData:
    """Prepare rows for CV without fitting any preprocessing statistic."""

    if frame[target].isna().any():
        raise ValueError("TARGET contains missing values; define an explicit policy")

    strategy = resolve_cv_strategy(settings)
    ordered = frame
    if strategy == "time_series":
        time_column = settings.time_column
        if not time_column or time_column not in frame:
            raise KeyError("Configured TIME_COLUMN is absent from train")
        if frame[time_column].isna().any():
            raise ValueError("TIME_COLUMN contains missing values")
        ordered = frame.sort_values(time_column, kind="stable")

    y = ordered[target].copy()
    if settings.task_type in CLASSIFICATION_TASKS:
        classes = y.value_counts(dropna=False)
        minimum_classes = 2 if settings.task_type == "binary_classification" else 3
        if len(classes) < minimum_classes:
            raise ValueError(
                f"{settings.task_type} requires at least {minimum_classes} target classes"
            )
        if strategy == "stratified_kfold" and int(classes.min()) < settings.n_splits:
            raise ValueError(
                "The rarest target class has fewer rows than N_SPLITS; reduce "
                "N_SPLITS or choose another validated protocol."
            )
    elif not pd.api.types.is_numeric_dtype(y):
        raise TypeError("Regression TARGET must be numeric")

    groups: pd.Series | None = None
    if strategy == "group_kfold":
        group_column = settings.group_column
        if not group_column or group_column not in ordered:
            raise KeyError("Configured GROUP_COLUMN is absent from train")
        if ordered[group_column].isna().any():
            raise ValueError("GROUP_COLUMN contains missing values")
        groups = ordered[group_column].copy()
        if groups.nunique() < settings.n_splits:
            raise ValueError("GROUP_COLUMN has fewer unique groups than N_SPLITS")

    return PreparedData(
        X=ordered.loc[:, list(plan.model_features)].copy(),
        y=y,
        groups=groups,
        row_index=ordered.index.copy(),
    )


def build_cv_splitter(settings: BaselineSettings, y: pd.Series) -> tuple[Any, str]:
    """Construct the configured sklearn splitter."""

    try:
        from sklearn.model_selection import (
            GroupKFold,
            KFold,
            StratifiedKFold,
            TimeSeriesSplit,
        )
    except ImportError as error:  # pragma: no cover - environment dependent
        raise _sklearn_import_error() from error

    strategy = resolve_cv_strategy(settings)
    if strategy == "stratified_kfold":
        class_counts = y.value_counts()
        if class_counts.empty or int(class_counts.min()) < settings.n_splits:
            raise ValueError("Each class must contain at least N_SPLITS rows")
        splitter = StratifiedKFold(
            n_splits=settings.n_splits,
            shuffle=settings.shuffle,
            random_state=settings.random_state if settings.shuffle else None,
        )
    elif strategy == "kfold":
        splitter = KFold(
            n_splits=settings.n_splits,
            shuffle=settings.shuffle,
            random_state=settings.random_state if settings.shuffle else None,
        )
    elif strategy == "group_kfold":
        splitter = GroupKFold(n_splits=settings.n_splits)
    elif strategy == "time_series":
        splitter = TimeSeriesSplit(n_splits=settings.n_splits)
    else:  # guarded by validate_baseline_settings
        raise ValueError(f"Unsupported CV strategy: {strategy}")
    return splitter, strategy


def cv_protocol_description(settings: BaselineSettings, strategy: str) -> str:
    """Create a compact protocol label for notebook and Markdown reports."""

    if strategy in {"group_kfold", "time_series"}:
        detail = (
            f", group={settings.group_column}"
            if strategy == "group_kfold"
            else f", time={settings.time_column}"
        )
        return f"{strategy}(n_splits={settings.n_splits}{detail})"
    return (
        f"{strategy}(n_splits={settings.n_splits}, "
        f"shuffle={settings.shuffle}, seed={settings.random_state})"
    )


def read_inline_field(path: Path, field: str) -> str:
    """Read one Dataview inline field such as ``(primary_metric:: accuracy)``."""

    text = Path(path).read_text(encoding="utf-8")
    pattern = re.compile(
        rf"[\[(]\s*{re.escape(field)}\s*::\s*(.*?)[\])]",
        flags=re.IGNORECASE,
    )
    matches = [match.strip() for match in pattern.findall(text)]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one ({field}:: value) field in {path}; "
            f"found {len(matches)}"
        )
    value = matches[0].strip().strip("`")
    if not value or value.upper() in {"TBD", "TODO", "NONE", "N/A"}:
        raise ValueError(f"Fill ({field}:: ...) in {path} before baseline")
    return value


def resolve_scoring_plan(
    project_root: Path,
    settings: BaselineSettings,
    *,
    problem_doc: Path = Path("docs/00_problem.md"),
) -> ScoringPlan:
    """Resolve the Problem metric contract into validated sklearn scorers."""

    try:
        from sklearn.metrics import get_scorer
    except ImportError as error:  # pragma: no cover - environment dependent
        raise _sklearn_import_error() from error

    contract = read_inline_field(Path(project_root) / problem_doc, "primary_metric")
    primary = settings.primary_scorer or _metric_alias(contract)
    scorer_items: list[tuple[str, str, Any]] = [("primary", contract, primary)]
    scorer_items.extend(
        (f"secondary_{index}", str(label), scorer)
        for index, (label, scorer) in enumerate(
            settings.secondary_scorers.items(), start=1
        )
    )

    scorers: dict[str, Any] = {}
    labels: dict[str, str] = {}
    directions: dict[str, str] = {}
    negated: dict[str, bool] = {}
    for key, label, scorer in scorer_items:
        if isinstance(scorer, str):
            try:
                get_scorer(scorer)
            except ValueError as error:
                raise ValueError(
                    f"{scorer!r} is not a valid scikit-learn scorer. "
                    "Use PRIMARY_SCORER/SECONDARY_SCORERS for the technical "
                    "implementation while keeping the metric contract in "
                    "docs/00_problem.md."
                ) from error
        elif not callable(scorer):
            raise TypeError(f"Scorer for {label!r} must be a name or callable")
        is_negated = isinstance(scorer, str) and scorer.startswith("neg_")
        scorers[key] = scorer
        labels[key] = label
        directions[key] = "minimize" if is_negated else "maximize"
        negated[key] = is_negated

    return ScoringPlan(
        contract_metric=contract,
        scorers=scorers,
        labels=labels,
        directions=directions,
        negated=negated,
    )


def build_tabular_preprocessor(settings: BaselineSettings, plan: FeaturePlan) -> Any:
    """Build fold-fitted numeric/categorical preprocessing."""

    try:
        from sklearn.compose import ColumnTransformer
        from sklearn.impute import SimpleImputer
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import (
            MinMaxScaler,
            OneHotEncoder,
            RobustScaler,
            StandardScaler,
        )
    except ImportError as error:  # pragma: no cover - environment dependent
        raise _sklearn_import_error() from error

    transformers: list[tuple[str, Any, list[str]]] = []
    if plan.numeric:
        numeric_imputer_kwargs: dict[str, Any] = {
            "strategy": settings.numeric_imputer,
            "add_indicator": settings.add_numeric_missing_indicator,
        }
        if settings.numeric_imputer == "constant":
            numeric_imputer_kwargs["fill_value"] = settings.numeric_fill_value
        if "keep_empty_features" in inspect.signature(SimpleImputer).parameters:
            numeric_imputer_kwargs["keep_empty_features"] = True

        numeric_steps: list[tuple[str, Any]] = [
            ("imputer", SimpleImputer(**numeric_imputer_kwargs))
        ]
        scaler = {
            "standard": StandardScaler(),
            "robust": RobustScaler(),
            "minmax": MinMaxScaler(),
            "none": None,
        }[settings.numeric_scaler]
        if scaler is not None:
            numeric_steps.append(("scaler", scaler))
        transformers.append(
            ("numeric", Pipeline(numeric_steps), list(plan.numeric))
        )

    if plan.categorical:
        categorical_imputer_kwargs: dict[str, Any] = {
            "strategy": settings.categorical_imputer,
        }
        if settings.categorical_imputer == "constant":
            categorical_imputer_kwargs["fill_value"] = (
                settings.categorical_fill_value
            )
        if "keep_empty_features" in inspect.signature(SimpleImputer).parameters:
            categorical_imputer_kwargs["keep_empty_features"] = True

        encoder_kwargs: dict[str, Any] = {
            "handle_unknown": settings.onehot_handle_unknown,
        }
        encoder_signature = inspect.signature(OneHotEncoder).parameters
        if "sparse_output" in encoder_signature:
            encoder_kwargs["sparse_output"] = settings.onehot_sparse_output
        else:  # scikit-learn < 1.2
            encoder_kwargs["sparse"] = settings.onehot_sparse_output
        if settings.onehot_min_frequency is not None:
            encoder_kwargs["min_frequency"] = settings.onehot_min_frequency
        if settings.onehot_max_categories is not None:
            encoder_kwargs["max_categories"] = settings.onehot_max_categories

        categorical_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(**categorical_imputer_kwargs)),
                ("onehot", OneHotEncoder(**encoder_kwargs)),
            ]
        )
        transformers.append(
            ("categorical", categorical_pipeline, list(plan.categorical))
        )

    return ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        sparse_threshold=settings.column_transformer_sparse_threshold,
        verbose_feature_names_out=True,
    )


def preprocessing_report(
    settings: BaselineSettings,
    plan: FeaturePlan,
) -> pd.DataFrame:
    """Explain the transformations before any model is fitted."""

    rows: list[dict[str, Any]] = []
    if plan.numeric:
        rows.append(
            {
                "model_role": "numeric",
                "features": len(plan.numeric),
                "imputation": settings.numeric_imputer,
                "representation": settings.numeric_scaler,
                "unknown_policy": "—",
            }
        )
    if plan.categorical:
        rows.append(
            {
                "model_role": "categorical",
                "features": len(plan.categorical),
                "imputation": settings.categorical_imputer,
                "representation": "one-hot",
                "unknown_policy": settings.onehot_handle_unknown,
            }
        )
    return pd.DataFrame(rows)


def build_dummy_estimator(settings: BaselineSettings) -> Any:
    """Build a no-skill floor appropriate for the task."""

    try:
        from sklearn.dummy import DummyClassifier, DummyRegressor
    except ImportError as error:  # pragma: no cover - environment dependent
        raise _sklearn_import_error() from error

    params = dict(settings.dummy_params)
    if settings.task_type in CLASSIFICATION_TASKS:
        strategy = "prior" if settings.dummy_strategy == "auto" else settings.dummy_strategy
        params.setdefault("strategy", strategy)
        if strategy in {"stratified", "uniform"}:
            params.setdefault("random_state", settings.random_state)
        return DummyClassifier(**params)
    strategy = "mean" if settings.dummy_strategy == "auto" else settings.dummy_strategy
    params.setdefault("strategy", strategy)
    return DummyRegressor(**params)


def build_simple_estimator(settings: BaselineSettings) -> Any:
    """Build the intentionally simple, interpretable reference estimator."""

    try:
        from sklearn.linear_model import LogisticRegression, Ridge
    except ImportError as error:  # pragma: no cover - environment dependent
        raise _sklearn_import_error() from error

    model_name = settings.model_name
    if model_name == "auto":
        model_name = (
            "logistic_regression"
            if settings.task_type in CLASSIFICATION_TASKS
            else "ridge"
        )
    params = dict(settings.model_params)
    if model_name == "logistic_regression":
        params.setdefault("max_iter", 1000)
        params.setdefault("random_state", settings.random_state)
        return LogisticRegression(**params)
    if model_name == "ridge":
        return Ridge(**params)
    raise ValueError(f"Unsupported simple baseline model: {model_name}")


def resolved_model_name(settings: BaselineSettings) -> str:
    if settings.model_name != "auto":
        return settings.model_name
    return (
        "logistic_regression"
        if settings.task_type in CLASSIFICATION_TASKS
        else "ridge"
    )


def build_model_pipeline(preprocessor: Any, estimator: Any) -> Any:
    """Combine preprocessing and estimator into the leakage boundary."""

    try:
        from sklearn.base import clone
        from sklearn.pipeline import Pipeline
    except ImportError as error:  # pragma: no cover - environment dependent
        raise _sklearn_import_error() from error

    return Pipeline(
        [
            ("preprocess", clone(preprocessor)),
            ("model", estimator),
        ]
    )


def evaluate_models_cv(
    models: Mapping[str, Any],
    data: PreparedData,
    *,
    cv: Any,
    scoring: ScoringPlan,
    settings: BaselineSettings,
) -> CVEvaluation:
    """Evaluate every full pipeline on the same folds and scoring contract."""

    try:
        from sklearn.model_selection import cross_validate
    except ImportError as error:  # pragma: no cover - environment dependent
        raise _sklearn_import_error() from error

    if not models:
        raise ValueError("At least one model pipeline is required")

    fold_rows: list[dict[str, Any]] = []
    raw_results: dict[str, Mapping[str, Any]] = {}
    for model_name, pipeline in models.items():
        result = cross_validate(
            pipeline,
            data.X,
            data.y,
            groups=data.groups,
            cv=cv,
            scoring=dict(scoring.scorers),
            n_jobs=settings.n_jobs,
            return_train_score=settings.return_train_score,
            error_score=settings.error_score,
        )
        raw_results[model_name] = result
        n_folds = len(result["fit_time"])
        for metric_key in scoring.scorers:
            for split, result_prefix in (("validation", "test"), ("train", "train")):
                score_key = f"{result_prefix}_{metric_key}"
                if score_key not in result:
                    continue
                values = np.asarray(result[score_key], dtype=float)
                if scoring.negated[metric_key]:
                    values = -values
                for fold_index in range(n_folds):
                    fold_rows.append(
                        {
                            "model": model_name,
                            "fold": fold_index + 1,
                            "split": split,
                            "metric_key": metric_key,
                            "metric": scoring.labels[metric_key],
                            "direction": scoring.directions[metric_key],
                            "value": float(values[fold_index]),
                            "fit_seconds": float(result["fit_time"][fold_index]),
                            "score_seconds": float(result["score_time"][fold_index]),
                        }
                    )

    fold_scores = pd.DataFrame(fold_rows)
    summary = (
        fold_scores.groupby(
            ["model", "split", "metric_key", "metric", "direction"],
            sort=False,
            as_index=False,
        )
        .agg(
            mean=("value", "mean"),
            std=("value", "std"),
            min=("value", "min"),
            max=("value", "max"),
            folds=("value", "size"),
            fit_seconds_mean=("fit_seconds", "mean"),
            score_seconds_mean=("score_seconds", "mean"),
        )
    )
    return CVEvaluation(
        fold_scores=fold_scores,
        summary=summary,
        raw_results=raw_results,
    )


def metric_figure_filename(metric_key: str, metric_label: str) -> str:
    """Return a stable, filesystem-safe filename for one metric chart."""

    slug = re.sub(r"[^a-z0-9]+", "-", metric_label.lower()).strip("-")
    slug = slug or "metric"
    return f"metric-{metric_key}-{slug}.png"


def build_metric_figures(
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
) -> dict[str, Any]:
    """Build one fold-by-fold validation chart for every configured metric."""

    try:
        import matplotlib.pyplot as plt
    except ImportError as error:  # pragma: no cover - environment dependent
        raise ImportError(
            "Metric figures require matplotlib. Install project dependencies "
            "with: python -m pip install -r requirements.txt"
        ) from error

    validation = evaluation.fold_scores[
        evaluation.fold_scores["split"] == "validation"
    ]
    figures: dict[str, Any] = {}
    for metric_key in scoring.scorers:
        metric_rows = validation[validation["metric_key"] == metric_key]
        if metric_rows.empty:
            continue

        label = scoring.labels[metric_key]
        direction = scoring.directions[metric_key]
        figure, axis = plt.subplots(figsize=(8.5, 4.8))
        for model_name in metric_rows["model"].drop_duplicates():
            model_rows = metric_rows[
                metric_rows["model"] == model_name
            ].sort_values("fold")
            mean = float(model_rows["value"].mean())
            std = float(model_rows["value"].std())
            line, = axis.plot(
                model_rows["fold"],
                model_rows["value"],
                marker="o",
                linewidth=2,
                label=f"{model_name}: {mean:.4f} ± {std:.4f}",
            )
            axis.axhline(
                mean,
                color=line.get_color(),
                linestyle=":",
                linewidth=1.2,
                alpha=0.65,
            )

        folds = sorted(int(value) for value in metric_rows["fold"].unique())
        axis.set_xticks(folds)
        axis.set_xlabel("CV fold")
        axis.set_ylabel(label)
        axis.set_title(f"{label} по validation folds ({direction})")
        axis.grid(True, alpha=0.25)
        axis.legend(title="Модель: mean ± std", frameon=False)
        figure.tight_layout()
        figures[metric_key] = figure
    return figures


def _cleanup_generated_run_files(run_dir: Path) -> None:
    """Remove only files owned by the baseline generator, never manual files."""

    known_files = {
        "cv_fold_scores.csv",
        "cv_summary.csv",
        "metadata.json",
        "model.joblib",
    }
    for path in run_dir.iterdir():
        generated_metric_figure = (
            path.is_file()
            and path.name.startswith("metric-")
            and path.suffix.lower() == ".png"
        )
        if path.is_file() and (path.name in known_files or generated_metric_figure):
            path.unlink()


def save_baseline_run(
    project_root: Path,
    settings: BaselineSettings,
    evaluation: CVEvaluation,
    plan: FeaturePlan,
    scoring: ScoringPlan,
    *,
    dataset_version: str,
    cv_description: str,
    final_pipeline: Any | None = None,
    data: PreparedData | None = None,
    metric_figures: Mapping[str, Any] | None = None,
) -> SavedBaselineRun:
    """Save reports, metric figures and optionally a final all-train pipeline.

    With ``ALLOW_OVERWRITE=True`` repeated execution refreshes only files owned
    by this generator. Unknown files in the run directory are preserved.
    """

    root = Path(project_root).resolve()
    base_dir = (root / settings.artifact_dir).resolve()
    try:
        base_dir.relative_to(root)
    except ValueError as error:
        raise ValueError("ARTIFACT_DIR resolves outside the project root") from error

    run_dir = (base_dir / settings.run_name).resolve()
    try:
        run_dir.relative_to(base_dir)
    except ValueError as error:
        raise ValueError("RUN_NAME resolves outside ARTIFACT_DIR") from error
    if run_dir.exists() and any(run_dir.iterdir()) and not settings.allow_overwrite:
        raise FileExistsError(
            f"Baseline run already exists: {run_dir}. Change RUN_NAME or set "
            "ALLOW_OVERWRITE=True deliberately."
        )
    run_dir.mkdir(parents=True, exist_ok=True)
    if settings.allow_overwrite:
        _cleanup_generated_run_files(run_dir)

    fold_scores_path = run_dir / "cv_fold_scores.csv"
    summary_path = run_dir / "cv_summary.csv"
    metadata_path = run_dir / "metadata.json"
    evaluation.fold_scores.to_csv(fold_scores_path, index=False)
    evaluation.summary.to_csv(summary_path, index=False)

    metadata = {
        "experiment_id": settings.experiment_id,
        "experiment_title": settings.experiment_title,
        "experiment_note": settings.experiment_note.as_posix(),
        "run_name": settings.run_name,
        "task_type": settings.task_type,
        "dataset_version": dataset_version,
        "cv": cv_description,
        "primary_metric": scoring.contract_metric,
        "primary_scorer": _display_value(scoring.scorers["primary"]),
        "model": resolved_model_name(settings),
        "model_params": dict(settings.model_params),
        "numeric_features": list(plan.numeric),
        "categorical_features": list(plan.categorical),
        "excluded_features": list(plan.excluded),
        "metric_figures": {
            key: metric_figure_filename(key, scoring.labels[key])
            for key in scoring.scorers
        } if settings.save_metric_figures else {},
        "settings": _json_safe(asdict(settings)),
    }
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )

    figure_paths: dict[str, Path] = {}
    if settings.save_metric_figures:
        figures = dict(metric_figures or build_metric_figures(evaluation, scoring))
        missing = [key for key in scoring.scorers if key not in figures]
        if missing:
            raise ValueError(
                "Metric figures are missing for: " + ", ".join(missing)
            )
        for metric_key in scoring.scorers:
            figure_path = run_dir / metric_figure_filename(
                metric_key, scoring.labels[metric_key]
            )
            figures[metric_key].savefig(
                figure_path,
                dpi=settings.metric_figure_dpi,
                bbox_inches="tight",
            )
            figure_paths[metric_key] = figure_path

    model_path: Path | None = None
    if settings.save_final_model:
        if final_pipeline is None or data is None:
            raise ValueError(
                "final_pipeline and data are required when SAVE_FINAL_MODEL=True"
            )
        try:
            from joblib import dump
            from sklearn.base import clone
        except ImportError as error:  # pragma: no cover - environment dependent
            raise _sklearn_import_error() from error
        fitted = clone(final_pipeline).fit(data.X, data.y)
        model_path = run_dir / "model.joblib"
        dump(fitted, model_path)

    return SavedBaselineRun(
        run_dir=run_dir,
        fold_scores_path=fold_scores_path,
        summary_path=summary_path,
        metadata_path=metadata_path,
        model_path=model_path,
        metric_figure_paths=figure_paths,
    )


def _vault_relative(project_root: Path, path: Path) -> str:
    root = Path(project_root).resolve()
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError(f"Path resolves outside the project root: {path}") from error


def _wikilink(project_root: Path, path: Path, alias: str | None = None) -> str:
    relative = _vault_relative(project_root, path)
    return f"[[{relative}|{alias}]]" if alias else f"[[{relative}]]"


def build_baseline_experiment_report(
    project_root: Path,
    settings: BaselineSettings,
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    saved_run: SavedBaselineRun,
    *,
    dataset_version: str,
    cv_description: str,
    model_name: str = "simple_model",
) -> str:
    """Render an Obsidian-native report with charts and readable CV tables."""

    overview = pd.DataFrame(
        [
            ("Эксперимент", f"{settings.experiment_id} — {settings.experiment_title}"),
            ("Run", settings.run_name),
            ("Версия данных", dataset_version),
            ("Validation", cv_description),
            ("Основная метрика", scoring.contract_metric),
            ("Основная модель", resolved_model_label(model_name)),
        ],
        columns=["Поле", "Значение"],
    )

    validation_summary = evaluation.summary[
        evaluation.summary["split"] == "validation"
    ].copy()
    validation_summary["mean ± std"] = validation_summary.apply(
        lambda row: f"{row['mean']:.4f} ± {row['std']:.4f}", axis=1
    )
    comparison = validation_summary[
        ["model", "metric", "direction", "mean ± std", "min", "max", "folds"]
    ].rename(
        columns={
            "model": "Модель",
            "metric": "Метрика",
            "direction": "Направление",
            "min": "Min",
            "max": "Max",
            "folds": "Folds",
        }
    )

    sections = [
        "## Сводка запуска\n\n" + dataframe_to_markdown(overview),
        "## Сравнение всех метрик\n\n" + dataframe_to_markdown(comparison, float_digits=4),
    ]

    figure_paths = dict(saved_run.metric_figure_paths or {})
    validation_folds = evaluation.fold_scores[
        evaluation.fold_scores["split"] == "validation"
    ]
    for metric_key in scoring.scorers:
        label = scoring.labels[metric_key]
        metric_summary = validation_summary[
            validation_summary["metric_key"] == metric_key
        ][["model", "mean", "std", "min", "max", "folds", "direction"]].rename(
            columns={
                "model": "Модель",
                "mean": "Mean",
                "std": "Std",
                "min": "Min",
                "max": "Max",
                "folds": "Folds",
                "direction": "Направление",
            }
        )
        metric_folds = validation_folds[
            validation_folds["metric_key"] == metric_key
        ].pivot(index="fold", columns="model", values="value")
        metric_folds = metric_folds.reset_index().rename(columns={"fold": "Fold"})

        metric_parts = [f"## Метрика: {label}"]
        if metric_key in figure_paths:
            figure_link = _vault_relative(project_root, figure_paths[metric_key])
            metric_parts.append(f"![[{figure_link}]]")
        metric_parts.extend(
            [
                "### Сводка по моделям\n\n"
                + dataframe_to_markdown(metric_summary, float_digits=4),
                "### Значения по folds\n\n"
                + dataframe_to_markdown(metric_folds, float_digits=4),
            ]
        )
        sections.append("\n\n".join(metric_parts))

    artifact_lines = [
        f"- Полная таблица folds: {_wikilink(project_root, saved_run.fold_scores_path, 'cv_fold_scores.csv')}",
        f"- Полная сводка: {_wikilink(project_root, saved_run.summary_path, 'cv_summary.csv')}",
        f"- Конфигурация запуска: {_wikilink(project_root, saved_run.metadata_path, 'metadata.json')}",
    ]
    if saved_run.model_path is not None:
        artifact_lines.append(
            f"- Финальная модель: {_wikilink(project_root, saved_run.model_path, 'model.joblib')}"
        )
    sections.append("## Артефакты\n\n" + "\n".join(artifact_lines))
    return "\n\n".join(sections)


def sync_baseline_experiment_note(
    project_root: Path,
    settings: BaselineSettings,
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    saved_run: SavedBaselineRun,
    *,
    dataset_version: str,
    cv_description: str,
    model_name: str = "simple_model",
) -> list[str]:
    """Create/update the generated block while preserving manual analysis."""

    root = Path(project_root).resolve()
    note_path = (root / settings.experiment_note).resolve()
    _vault_relative(root, note_path)
    note_path.parent.mkdir(parents=True, exist_ok=True)
    if not note_path.exists():
        note_path.write_text(
            "---\n"
            f"id: {settings.experiment_id}\n"
            "type: experiment\n"
            "experiment_type: baseline\n"
            "status: completed\n"
            "---\n\n"
            f"# {settings.experiment_id} — {settings.experiment_title}\n\n"
            "> [!info] Автоматический отчёт\n"
            "> Перезапуск notebook обновляет только блок ниже. Ручные выводы "
            "после него сохраняются.\n\n"
            "<!-- auto:baseline-experiment-report:start -->\n\n"
            "Отчёт появится после сохранения baseline.\n\n"
            "<!-- auto:baseline-experiment-report:end -->\n\n"
            "## Анализ и выводы\n\n"
            "- Что показало сравнение с dummy:\n"
            "- Насколько результат стабилен между folds:\n"
            "- Какие метрики расходятся и почему это важно:\n"
            "- Что проверить следующим экспериментом:\n",
            encoding="utf-8",
        )

    report = build_baseline_experiment_report(
        root,
        settings,
        evaluation,
        scoring,
        saved_run,
        dataset_version=dataset_version,
        cv_description=cv_description,
        model_name=model_name,
    )
    return MarkdownDocument(note_path).update_blocks(
        {"baseline-experiment-report": report}
    )


def build_validation_baseline_block(
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    *,
    dataset_version: str,
    cv_description: str,
) -> str:
    """Render the comparable primary scores for Validation."""

    primary = evaluation.primary_summary().copy()
    report = pd.DataFrame(
        {
            "Baseline": primary["model"],
            "Версия данных": dataset_version,
            "Протокол": cv_description,
            "Метрика": scoring.contract_metric,
            "Значение": primary.apply(
                lambda row: f"{row['mean']:.4f} ± {row['std']:.4f}", axis=1
            ),
        }
    )
    return dataframe_to_markdown(report)


def build_current_baseline_block(
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    *,
    dataset_version: str,
    cv_description: str,
    model_name: str = "simple_model",
    experiment_note: Path | None = None,
) -> str:
    """Render the selected simple reference model for Experiments."""

    primary = evaluation.primary_summary()
    row = primary[primary["model"] == model_name]
    if row.empty:
        row = primary.tail(1)
    record = row.iloc[0]
    rows: list[tuple[str, Any]] = [
            ("Эксперимент / версия", "Baseline / " + model_name),
            ("Данные", dataset_version),
            ("Модель", resolved_model_label(model_name)),
            ("Validation", cv_description),
            ("Основная метрика", scoring.contract_metric),
            ("Значение", f"{record['mean']:.4f} ± {record['std']:.4f}"),
            ("Стоимость / latency", "см. cv_summary.csv"),
    ]
    if experiment_note is not None:
        rows.insert(
            1,
            (
                "Карточка",
                f"[[{experiment_note.as_posix()}|подробный baseline-отчёт]]",
            ),
        )
    report = pd.DataFrame(
        rows,
        columns=["Поле", "Значение"],
    )
    return dataframe_to_markdown(report)


def sync_baseline_docs(
    project_root: Path,
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    *,
    dataset_version: str,
    cv_description: str,
    model_name: str = "simple_model",
    experiment_note: Path | None = None,
) -> dict[str, list[str]]:
    """Update only explicit baseline auto-blocks in stage documents."""

    root = Path(project_root)
    validation_blocks = MarkdownDocument(root / "docs/03_validation.md").update_blocks(
        {
            "baseline-results": build_validation_baseline_block(
                evaluation,
                scoring,
                dataset_version=dataset_version,
                cv_description=cv_description,
            )
        }
    )
    experiment_blocks = MarkdownDocument(root / "docs/05_experiments.md").update_blocks(
        {
            "current-baseline": build_current_baseline_block(
                evaluation,
                scoring,
                dataset_version=dataset_version,
                cv_description=cv_description,
                model_name=model_name,
                experiment_note=experiment_note,
            )
        }
    )
    return {
        "docs/03_validation.md": validation_blocks,
        "docs/05_experiments.md": experiment_blocks,
    }


def resolved_model_label(model_name: str) -> str:
    return model_name.replace("_", " ")


def _metric_alias(metric: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", metric.lower()).strip("_")
    aliases = {
        "acc": "accuracy",
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "f1_score": "f1",
        "f1": "f1",
        "f1_macro": "f1_macro",
        "f1_micro": "f1_micro",
        "roc_auc": "roc_auc",
        "auc_roc": "roc_auc",
        "pr_auc": "average_precision",
        "average_precision": "average_precision",
        "r2": "r2",
        "mae": "neg_mean_absolute_error",
        "mean_absolute_error": "neg_mean_absolute_error",
        "mse": "neg_mean_squared_error",
        "mean_squared_error": "neg_mean_squared_error",
        "rmse": "neg_root_mean_squared_error",
        "root_mean_squared_error": "neg_root_mean_squared_error",
        "log_loss": "neg_log_loss",
        "logloss": "neg_log_loss",
    }
    return aliases.get(normalized, normalized)


def _display_value(value: Any) -> str:
    if isinstance(value, Path):
        return value.as_posix()
    if callable(value) and not isinstance(value, str):
        return getattr(value, "__name__", repr(value))
    return str(value)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    if callable(value):
        return _display_value(value)
    return value


def _sklearn_import_error() -> ImportError:
    return ImportError(
        "03_baseline requires scikit-learn and joblib. Install project "
        "dependencies from the project root: "
        "python -m pip install -r requirements.txt"
    )


__all__ = [
    "BaselineSettings",
    "CVEvaluation",
    "FeaturePlan",
    "PreparedData",
    "SavedBaselineRun",
    "ScoringPlan",
    "build_current_baseline_block",
    "build_cv_splitter",
    "build_dummy_estimator",
    "build_baseline_experiment_report",
    "build_metric_figures",
    "build_model_pipeline",
    "build_simple_estimator",
    "build_tabular_preprocessor",
    "build_validation_baseline_block",
    "cv_protocol_description",
    "evaluate_models_cv",
    "prepare_training_data",
    "preprocessing_report",
    "read_inline_field",
    "resolve_cv_strategy",
    "resolve_feature_plan",
    "resolve_scoring_plan",
    "resolved_model_name",
    "save_baseline_run",
    "settings_from_module",
    "settings_report",
    "sync_baseline_docs",
    "sync_baseline_experiment_note",
    "validate_baseline_settings",
    "validate_inference_schema",
]
