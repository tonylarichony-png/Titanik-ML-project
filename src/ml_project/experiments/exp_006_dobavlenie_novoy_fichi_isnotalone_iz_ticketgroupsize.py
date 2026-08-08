"""EXP-006: Добавление новой Фичи IsnotAlone из TicketGroupSize."""

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
    experiment_id='EXP-006',
    experiment_title='Добавление новой Фичи IsnotAlone из TicketGroupSize',
    experiment_note=Path(
        "experiments/EXP-006 Dobavlenie Novoy Fichi Isnotalone Iz Ticketgroupsize.md"
    ),
    hypothesis="  if добавится фича notAlone, then метрики должны улучшиться, because станет более понятно кто действительно едет в одиночестве ...",
    change_description="Добавить фичу IsnotAlone, которая будет определять едет ли пассажир один или с кем-то относительно EXP005 больше ничего не менять" ,
    success_criterion=(
        "Primary improvement >= +0.0050; "
        "add explicit metric guardrails below."
    ),
    primary_improvement_min=0.005,
    metric_guardrails={},
    reference_model='champion_reference',
    primary_candidate="candidate",
    experiment_parameters={
            "source_features": ["SibSp", "Parch","TicketGroupSize"],
            "derived_feature": "IsnotAlone",
            "formula": "true if TicketGroupSize>1 AND SibSp==0 AND Parch==0 else false",
            "categories": ["0", "1"],
            "representation": "categorical_one_hot",
            "replaces_features": [],
            "parent_experiment": "EXP-003",

            # "important_parameter": "...",
        },
    decision="pending",
    run_name="exp_006_v1",
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
    TicketGroupSize = (
        frame.groupby("Ticket")["Ticket"]
        .transform("size")
)
    frame["IsnotAlone"] = (
    (TicketGroupSize > 1) &
    (frame["FamilySizeGroup"] == 0)
).astype(int)
    groups["categorical"] = [
            *groups.get("categorical", []),
            "IsnotAlone",
        ]
    # reference_settings — настройки сравниваемой модели: исходного
    # baseline либо принятого parent-чемпиона. Не изменяйте объект
    # напрямую: ModelingSettings immutable.
    #
    # Если гипотеза меняет признаки, preprocessing или estimator,
    # создайте candidate_settings = replace(reference_settings, ...).
    # Validation contract наследуется: его смена требует нового протокола.
    candidate_settings = reference_settings

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
