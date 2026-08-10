"""EXP-013: Train_test_combine."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import numpy as np
from ml_project.titanic_joint_data import load_joint_data, align_joint_features
from ml_project import config as project_config
from ml_project.experiment import build_reference_pipeline
from ml_project.modeling import (
    ModelingSettings,
    ExperimentData,
    ExperimentSettings,
)


EXPERIMENT = ExperimentSettings(
    experiment_id='EXP-013',
    experiment_title='Train_test_combine',
    experiment_note=Path(
        "experiments/EXP-013 Tt Comb.md"
    ),
    hypothesis=" if я объединю датасеты , then улучшу метрики, потому что групповые признаки буду давать более точное представление!, because станет больше наблюдений для формирования групп признаков...",
    change_description="ALL IN — применяем все изменения сразу+ объединяем train и test датасеты, относительно EXP012 больше ничего не менять",
    success_criterion=(
        "Primary improvement >= +0.0050; "
        "add explicit metric guardrails below."
    ),
    primary_improvement_min=0.005,
    metric_guardrails={
        "Balanced accuracy": 0.0,
        "Recall": -0.01,
        "F1": 0.0,
    },
    reference_model='champion_reference',
    primary_candidate="candidate",
    experiment_parameters={
        "source_features": ["Fare", "SibSp", "Parch", "Ticket", "Cabin"],
        "derived_feature": [
            "FarePerPerson",
            "FamilySizeGroup",
            "IsnotAlone",
            "CabinKnown",
            "Deck",
        ],
        "formula": "ALL IN",
        "categories": ["ALL IN"],
        "representation": ["categorical_one_hot", "num_normalized"],
        "replaces_features": ["Fare", "SibSp", "Parch", "Ticket", "Cabin"],
        "parent_experiment": "EXP-003",
    },
    run_name="exp_013_v1",
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

KEY = project_config.KEY
PROJECT_ROOT = next(
    parent for parent in Path(__file__).resolve().parents
    if (parent / "README.md").exists() and (parent / "src").exists()
)


def prepare_candidate_data(
    train: pd.DataFrame,
    feature_groups: Mapping[str, Any],
    reference_settings: ModelingSettings,
) -> ExperimentData:
    """Подготовить candidate поверх настроек baseline/чемпиона."""

    frame = train.copy(deep=True)
    groups = copy.deepcopy(feature_groups)
    joint = load_joint_data(PROJECT_ROOT)
    combined = joint.frame.copy(deep=True)
    featured_joint = combined.copy(deep=True)
    # 1. Размер группы по билету на объединённом train+test
    featured_joint["TicketGroupSize"] = (
        featured_joint
        .groupby("Ticket")["Ticket"]
        .transform("size")
        .astype("int64")
    )

    # 2. Fare per person + log1p
    featured_joint["FarePerPerson"] = np.log1p(
        featured_joint["Fare"] / featured_joint["TicketGroupSize"]
    )

    # 3. Не один ли человек "по факту билета", хотя SibSp/Parch == 0
    featured_joint["IsnotAlone"] = (
        (featured_joint["TicketGroupSize"] > 1)
        & (featured_joint["Parch"] == 0)
        & (featured_joint["SibSp"] == 0)
    ).astype(int)

    # 4. Известна ли каюта
    featured_joint["CabinKnown"] = (
        featured_joint["Cabin"]
        .notna()
        .astype(int)
    )

    # 5. Палуба
    featured_joint["Deck"] = featured_joint["Cabin"].str[0]

    featured_joint["Deck"] = featured_joint["Deck"].replace(
        ["A", "B", "C", "T"],
        "ABC",
    )

    is_nan = featured_joint["Deck"].isna()

    class_map = {
        1: "ABC_Unknown",
        2: "DE_Unknown",
        3: "FG_Unknown",
    }

    featured_joint.loc[is_nan, "Deck"] = (
        featured_joint.loc[is_nan, "Pclass"]
        .map(class_map)
    )

    # 6. Взаимодействие пола и класса билета.
    featured_joint["SexPclass"] = (
        featured_joint["Sex"].astype("string")
        + "_P"
        + featured_joint["Pclass"].astype("string")
    )

    # Возвращаем признаки из joint train+test обратно в текущий train-frame по PassengerId
    frame = align_joint_features(
        frame,
        featured_joint,
        features=[
            "TicketGroupSize",
            "FarePerPerson",
            "IsnotAlone",
            "CabinKnown",
            "Deck",
            "SexPclass",
        ],
        key=KEY,
    )

    groups["numeric"] = [
        *groups.get("numeric", []),
        "FarePerPerson",
    ]

    groups["count"] = [
        *groups.get("count", []),
        "TicketGroupSize",
    ]

    groups["categorical"] = [
        *groups.get("categorical", []),
        "IsnotAlone",
        "CabinKnown",
        "Deck",
        "SexPclass",
    ]

    candidate_settings = replace(
        reference_settings,
        exclude_features=tuple(dict.fromkeys((
            *reference_settings.exclude_features,
            "Sex",
            "Pclass",
        ))),
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
