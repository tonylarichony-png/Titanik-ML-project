"""EXP-009: ALLIN."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import numpy as np
from ml_project.experiment import build_reference_pipeline
from ml_project.modeling import (
    ModelingSettings,
    ExperimentData,
    ExperimentSettings,
)


EXPERIMENT = ExperimentSettings(
    experiment_id='EXP-009',
    experiment_title='ALLIN',
    experiment_note=Path(
        "experiments/EXP-009 Allin.md"
    ),
    hypothesis=" — if я все изменения применю одновременнор, then может получится увеличить метрики, because модель может найти скрытые зависимости между признаками, которые не видны при поочередном применении изменений",
    change_description="ALL IN — применяем все изменения сразу, относительно EXP008 больше ничего не менять" ,
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
            "source_features": ["Fare", "SibSp", "Parch", "Ticket", "Cabin"],
            "derived_feature": ["FarpPer", "FamilySizeGroup", "IsnotAlone", "CabinKnown", "Deck"],
            "formula": "ALL IN",
            "categories": ["ALL IN"],
            "representation": ["categorical_one_hot", "num_normalized"],
            "replaces_features": ["Fare", "SibSp", "Parch", "Ticket", "Cabin"],
            "parent_experiment": "EXP-002",

            # "important_parameter": "...",
        },
    decision="pending",
    run_name="exp_009_v1",
    artifact_dir=Path("artifacts/experiments"),
    results_registry=Path("experiments/frames.csv"),
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
    ticket_group_size = (
        frame.groupby("Ticket")["Ticket"]
        .transform("size")
    )

    # 1. Цена билета на человека
    frame["FarpPer"] = np.log1p(
        frame["Fare"] / ticket_group_size
    )

    # 2. Путешествует не один,
    # но SibSp/Parch этого не показывают
    frame["IsnotAlone"] = (
        (ticket_group_size > 1)
        & (frame["Parch"] == 0)
        & (frame["SibSp"] == 0)
    ).astype(int)

    # 3. Известна ли каюта
    frame["CabinKnown"] = (
        frame["Cabin"]
        .notna()
        .astype(int)
    )

    # 4. Палуба
    frame["Deck"] = frame["Cabin"].str[0]

    # A/B/C/T объединяем
    frame["Deck"] = frame["Deck"].replace(
        ["A", "B", "C", "T"],
        "ABC"
    )

    # Неизвестную палубу кодируем с учетом класса
    is_nan = frame["Deck"].isna()

    class_map = {
        1: "ABC_Unknown",
        2: "DE_Unknown",
        3: "FG_Unknown",
    }

    frame.loc[is_nan, "Deck"] = (
        frame.loc[is_nan, "Pclass"]
        .map(class_map)
    )

    groups["numeric"] = [
            *groups.get("numeric", []),
            "FarpPer",
        ]
    groups["categorical"] = [
    *groups.get("categorical", []),
    "IsnotAlone","CabinKnown","Deck"
]
    # reference_settings — настройки сравниваемой модели: исходного
    # baseline либо принятого parent-чемпиона. Не изменяйте объект
    # напрямую: ModelingSettings immutable.
    #
    # Если гипотеза меняет признаки, preprocessing или estimator,
    # создайте candidate_settings = replace(reference_settings, ...).
    # Validation contract наследуется: его смена требует нового протокола.
    candidate_settings = replace(
    reference_settings,
    exclude_features=(
        *reference_settings.exclude_features,
        "Fare",
    ),
)

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
