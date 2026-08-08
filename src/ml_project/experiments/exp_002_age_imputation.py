"""EXP-002: fold-safe Age imputation by normalized Title and Pclass."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.pipeline import Pipeline
from sklearn.utils.validation import check_is_fitted

from ml_project.modeling import (
    ModelingSettings,
    ExperimentData,
    ExperimentSettings,
    build_simple_estimator,
)
from ml_project.transformers import AgeByTitlePclassImputer


EXPERIMENT = ExperimentSettings(
    experiment_id="EXP-002",
    experiment_title='Заполнение пропусков Age с помощью "Title" и "Pclass"',
    experiment_note=Path("experiments/EXP-002 AGE_Experiment.md"),
    hypothesis=(
        "Если заполнить Age медианой по Title и Pclass внутри каждого train-fold, "
        "то accuracy повысится, потому что эти признаки несут информацию о возрасте."
    ),
    change_description="Новый fold-safe способ заполнения пропусков Age",
    success_criterion=(
        "Legacy pre-registration: accuracy должна вырасти; минимальный эффект "
        "и guardrails до первого запуска не были зафиксированы."
    ),
    primary_improvement_min=0.0,
    metric_guardrails={},
    reference_model="baseline_reference",
    primary_candidate="candidate",
    experiment_parameters={
        "feature": "Age",
        "reference_strategy": "global_median",
        "candidate_strategy": "median_by_Title_and_Pclass",
        "title_groups": ["Mr", "Mrs", "Miss", "Master"],
        "fallback": ["Title", "global_median"],
    },
    decision="adopt",
    run_name="exp_002_v1",
    artifact_dir=Path("artifacts/experiments"),
    results_registry=Path("experiments/results.csv"),
    save_artifacts=True,
    save_metric_figures=True,
    metric_figure_dpi=160,
    save_final_model=False,
    sync_experiment_note=True,
    sync_docs=True,
    allow_overwrite=True,
)


def _normalized_titles(frame: pd.DataFrame) -> pd.Series:
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


class TitleExtractor(BaseEstimator, TransformerMixin):
    """Create deterministic normalized Title without learning fold statistics."""

    def __init__(
        self,
        name_column: str = "Name",
        sex_column: str = "Sex",
        output_column: str = "Title",
    ) -> None:
        self.name_column = name_column
        self.sex_column = sex_column
        self.output_column = output_column

    def _validate_frame(self, X: Any) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("TitleExtractor expects a pandas DataFrame")
        missing = sorted({self.name_column, self.sex_column}.difference(X.columns))
        if missing:
            raise KeyError(f"TitleExtractor missing columns: {missing}")
        return X

    def fit(self, X: pd.DataFrame, y: Any = None) -> "TitleExtractor":
        frame = self._validate_frame(X)
        self.feature_names_in_ = np.asarray(frame.columns, dtype=object)
        self.n_features_in_ = frame.shape[1]
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(self, "feature_names_in_")
        frame = self._validate_frame(X).copy()
        frame[self.output_column] = _normalized_titles(frame)
        return frame


def prepare_candidate_data(
    train: pd.DataFrame,
    feature_groups: Mapping[str, Any],
    reference_settings: ModelingSettings,
) -> ExperimentData:
    """Подготовить EXP-002 поверх настроек EXP-001 reference."""

    # reference_settings здесь взяты из BASELINE (EXP-001). EXP-002 не меняет
    # отбор признаков, CV или estimator: меняется только fold-safe Age pipeline.
    candidate_settings = reference_settings

    diagnostic_frame = train.copy(deep=True)
    diagnostic_frame["Title"] = _normalized_titles(diagnostic_frame)
    title_report = (
        diagnostic_frame["Title"]
        .value_counts(dropna=False)
        .rename_axis("Title")
        .reset_index(name="rows")
    )
    title_report["share"] = title_report["rows"] / len(diagnostic_frame)
    age_group_report = (
        diagnostic_frame.groupby(["Title", "Pclass"], dropna=False)
        .agg(
            rows=("PassengerId", "size"),
            age_known=("Age", "count"),
            age_missing=("Age", lambda values: values.isna().sum()),
            age_median=("Age", "median"),
        )
        .reset_index()
        .sort_values(["Title", "Pclass"])
    )
    return ExperimentData(
        frame=train.copy(deep=True),
        feature_groups=copy.deepcopy(feature_groups),
        settings=candidate_settings,
        diagnostics={
            "Распределение нормализованных Title": title_report,
            "Age по Title × Pclass": age_group_report,
        },
    )


def build_candidate_models(
    preprocessor: Any,
    candidate_settings: ModelingSettings,
    experiment_settings: ExperimentSettings,
) -> dict[str, Any]:
    """Собрать candidate с Age-imputer и остальными настройками reference."""

    candidate = Pipeline(
        steps=[
            ("title", TitleExtractor()),
            (
                "age_imputer",
                AgeByTitlePclassImputer(
                    age_column="Age",
                    title_column="Title",
                    class_column="Pclass",
                ),
            ),
            ("preprocess", clone(preprocessor)),
            ("model", build_simple_estimator(candidate_settings)),
        ]
    )
    return {experiment_settings.primary_candidate: candidate}


__all__ = [
    "EXPERIMENT",
    "TitleExtractor",
    "build_candidate_models",
    "prepare_candidate_data",
]
