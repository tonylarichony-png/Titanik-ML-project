"""EXP-010: Объединение признака pcclass и Sex  в один."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from ml_project.experiment import build_reference_pipeline
from ml_project.modeling import (
    ModelingSettings,
    ExperimentData,
    ExperimentSettings,
)


EXPERIMENT = ExperimentSettings(
    experiment_id='EXP-010',
    experiment_title='Объединение признака pcclass и Sex  в один',
    experiment_note=Path(
        "experiments/EXP-010 Pclassxsex.md"
    ),
    hypothesis=" if сделаю категориальный признак SexPclass, then модели будет удобнее работать, because данный признак будет лучше отражать действительно так как зависимость нелинейная ",
    change_description="Объединить признаки Pclass и Sex в один приз",
    success_criterion=(
        "Primary improvement >= +0.0050; "
        "add explicit metric guardrails below."
    ),
    primary_improvement_min=0.005,
    metric_guardrails={"Balanced accuracy": 0.0,
        "Recall": -0.01,
        "F1": 0.0,},
    reference_model='champion_reference',
    primary_candidate="candidate",
    experiment_parameters={
            "source_features": ["Pclass", "Sex"],
            "derived_feature": "SexPclass",
            "formula": "Sex+'_P'+Pclass",
            "categories": ["male_P1", "male_P2", "male_P3", "female_P1", "female P2", "female_P3"],
            "representation": "categorical_one_hot",
            "replaces_features": ["Pclass", "Sex"],
            "parent_experiment": "EXP-003",

            # "important_parameter": "...",
        },
    decision="pending",
    run_name="exp_010_v1",
    artifact_dir=Path("artifacts/experiments"),
    results_registry=Path("experiments/results.csv"),
    save_artifacts=True,
    save_metric_figures=True,
    metric_figure_dpi=160,
    save_final_model=False,
    sync_experiment_note=True,
    sync_docs=True,
    allow_overwrite=True,
    parent_experiment_module='ml_project.experiments.exp_003_family_size',
)


def prepare_candidate_data(
    train: pd.DataFrame,
    feature_groups: Mapping[str, Any],
    reference_settings: ModelingSettings,
) -> ExperimentData:
    """Подготовить candidate поверх настроек baseline/чемпиона."""

    frame = train.copy(deep=True)
    groups = copy.deepcopy(feature_groups)


    frame["SexPclass"] = (
    frame["Sex"].astype("string")
    + "_P"
    + frame["Pclass"].astype("string")
)
    # EDIT HERE — зарегистрируйте каждый новый model-ready признак ровно
    # в одной группе:
    groups["categorical"] = [*groups.get("categorical", []), "SexPclass"]

    # EDIT HERE — если меняются настройки относительно reference:
    candidate_settings = replace(
        reference_settings,
        exclude_features=(*reference_settings.exclude_features, "Sex","Pclass"),
    )

    # reference_settings — настройки сравниваемой модели: исходного
    # baseline либо принятого parent-чемпиона. Не изменяйте объект
    # напрямую: ModelingSettings immutable.
    #
    # Если гипотеза меняет признаки, preprocessing или estimator,
    # создайте candidate_settings = replace(reference_settings, ...).
    # Validation contract наследуется: его смена требует нового протокола.


    # CHANGE ME — создавайте здесь только детерминированные raw-признаки.
    # Обучаемая статистика должна жить в sklearn transformer внутри
    # build_candidate_models, чтобы fit выполнялся отдельно на fold.

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
    """Собрать candidate с подготовленными candidate_settings."""

    # Для feature-only изменения поверх принятого чемпиона:
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
