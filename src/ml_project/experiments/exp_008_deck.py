"""EXP-008: Добавление фичи-Deck- палуба по первой букве CABIN."""

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
    experiment_id='EXP-008',
    experiment_title='Добавление фичи-Deck- палуба по первой букве CABIN',
    experiment_note=Path(
        "experiments/EXP-008 Deck.md"
    ),
    hypothesis="— if палуба известна, then может повлиять на выживаемость, because палуба может быть связана с классом обслуживания и расположением каюты, что может влиять на шансы выживания.",
    change_description="взять признак Cabin, выделить первую букву и создать новый признак Deck, относительно EXP004 больше ничего не менять" ,
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
            "source_features": ["Сabin"],
            "derived_feature": "Deck",
            "formula": "Cabin.str[0]",
            "categories": ["ABC", "DE", "FG", "ABC_Unknown", "DE_Unknown", "FG_Unknown"],
            "representation": "categorical_one_hot",
            "replaces_features": [],
            "parent_experiment": "EXP-003",

            # "important_parameter": "...",
        },
    decision="pending",
    run_name="exp_008_v1",
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
    frame['Deck'] = frame['Cabin'].str[0]

    # 2. Объединяем известные палубы A, B, C в один топ-бин 'ABC'
    frame['Deck'] = frame['Deck'].replace(['A', 'B', 'C','T'], 'ABC')

    # 3. Находим строки, где палуба пропущена (NaN)
    is_nan = frame['Deck'].isna()

    # 4. Заполняем пропуски специальными бинами в зависимости от класса (Pclass)
    class_map = {1: 'ABC_Unknown', 2: 'DE_Unknown', 3: 'FG_Unknown'}
    frame.loc[is_nan, 'Deck'] = frame.loc[is_nan, 'Pclass'].map(class_map)
    groups["categorical"] = [
    *groups.get("categorical", []),
    "Deck",
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
