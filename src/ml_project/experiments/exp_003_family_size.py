"""EXP-003: Объединение SibSp и Parch в признак FamilySize."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping
from dataclasses import replace

import pandas as pd

import numpy as np

from ml_project.experiment import build_reference_pipeline
from ml_project.modeling import (
    ModelingSettings,
    ExperimentData,
    ExperimentSettings,
)


EXPERIMENT = ExperimentSettings(
    experiment_id='EXP-003',
    experiment_title='Объединение SibSp и Parch в признак FamilySizeGroup',
    experiment_note=Path(
        "experiments/EXP-003 Family Size.md"
    ),
    hypothesis=" if объединить признаки,и категоризировать then должен улучшиться accuracy, because потому, что данный признак будет лучше определять одиночек, либо семью так как зависимость нелинейная:1,2,3,4,>4 ",
    change_description="Взять признаки SibSp и Parch и объединить в FamilySize, относительно EXP002 больше ничего не менять" ,
    success_criterion=(
        "Primary improvement >= +0.0050; "
        "add explicit metric guardrails below."
    ),
    primary_improvement_min=0.005,
    metric_guardrails={"Balanced accuracy": 0.0,
    "Recall": -0.01,
    "F1": 0.0,},
    reference_model="champion_reference",
    primary_candidate="candidate",
    experiment_parameters={
        "source_features": ["SibSp", "Parch"],
        "derived_feature": "FamilySizeGroup",
        "formula": "SibSp + Parch + 1",
        "categories": ["1", "2", "3", "4", ">4"],
        "representation": "categorical_one_hot",
        "replaces_features": ["SibSp", "Parch"],
        "parent_experiment": "EXP-002",

        # "important_parameter": "...",
    },
    decision="adopt",
    run_name="exp_003_v1",
    artifact_dir=Path("artifacts/experiments"),
    results_registry=Path("experiments/results.csv"),
    save_artifacts=True,
    save_metric_figures=True,
    metric_figure_dpi=160,
    save_final_model=False,
    sync_experiment_note=True,
    sync_docs=True,
    allow_overwrite=True,
    parent_experiment_module=(
        "ml_project.experiments.exp_002_age_imputation"
    ),
)


def prepare_candidate_data(
    train: pd.DataFrame,
    feature_groups: Mapping[str, Any],
    reference_settings: ModelingSettings,
) -> ExperimentData:
    """Подготовить EXP-003 поверх настроек принятого EXP-002."""

    # reference_settings уже содержат рецепт чемпиона EXP-002:
    # TitleExtractor + fold-safe заполнение Age и исходный feature plan.
    # Ниже создаётся отдельная копия candidate_settings только с изменением
    # EXP-003: FamilySizeGroup заменяет SibSp и Parch во входе модели.

    frame = train.copy(deep=True)
    groups = copy.deepcopy(feature_groups)

    family_size = frame["SibSp"] + frame["Parch"] + 1
    frame["FamilySizeGroup"] = pd.cut(
        family_size,
        bins=[0, 1, 2, 3, 4, np.inf],
        labels=["1", "2", "3", "4", ">4"],
        include_lowest=True,
    ).astype("string")

    groups["categorical"] = [
        *groups.get("categorical", []),
        "FamilySizeGroup",
    ]

    candidate_settings = replace(
        reference_settings,
        exclude_features=(
            *reference_settings.exclude_features,
            "SibSp",
            "Parch",
        ),
    )

    return ExperimentData(
        frame=frame,
        feature_groups=groups,
        settings=candidate_settings,
        diagnostics={},
    )


def build_candidate_models(
    preprocessor: Any,
    candidate_settings: ModelingSettings,
    experiment_settings: ExperimentSettings,
) -> dict[str, Any]:
    """Собрать EXP-002 pipeline с новым preprocessor EXP-003."""

    # candidate_settings — настройки после единственного изменения EXP-003.
    # build_reference_pipeline сохраняет Title/Age шаги принятого EXP-002,
    # но подставляет preprocessor с FamilySizeGroup без SibSp и Parch.
    candidate = build_reference_pipeline(
        experiment_settings.parent_experiment_module,
        preprocessor,
        candidate_settings,
    )
    return {experiment_settings.primary_candidate: candidate}


__all__ = [
    "EXPERIMENT",
    "build_candidate_models",
    "prepare_candidate_data",
]
