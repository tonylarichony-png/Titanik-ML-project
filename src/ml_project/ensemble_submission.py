"""Create final Titanic submissions for ENS-003 stacking and MLP-024."""

from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from . import config as project_config
from .baseline_config import BASELINE
from .data import DataCatalog
from .ensemble_experiment import (
    MODEL_SOURCES,
    SPEC_003,
    _learn_simplex_weights,
    _positive_probability,
    _screening_pipeline,
)
from .experiment import load_experiment, prepare_experiment_candidate
from .mlp_experiment import fit_final_mlp, predict_prepared_mlp, save_final_mlp
from .modeling.screening import prepare_screening_context
from .modeling.submission import _write_submission_index


@dataclass(frozen=True)
class CreatedSubmission:
    """Пути и краткая сводка созданного Kaggle submission."""
    submission_id: str
    candidate_id: str
    csv_path: Path
    note_path: Path
    prediction_distribution: dict[int, int]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _submission_frame(
    inference: pd.DataFrame,
    sample: pd.DataFrame,
    prediction: np.ndarray,
) -> pd.DataFrame:
    key = project_config.KEY
    target = project_config.TARGET
    if len(prediction) != len(inference):
        raise ValueError("Prediction length differs from inference rows")
    by_key = pd.Series(prediction, index=inference[key].to_numpy())
    frame = sample.copy()
    frame[target] = frame[key].map(by_key)
    if frame[target].isna().any() or not frame[key].is_unique:
        raise ValueError("Submission key alignment failed")
    if set(frame[key]) != set(inference[key]):
        raise ValueError("Submission and inference key sets differ")
    frame[target] = frame[target].astype("int64")
    return frame


def _write_card(
    root: Path,
    submission_id: str,
    candidate_id: str,
    model: str,
    cv_mean: float,
    cv_std: float,
    csv_path: Path,
    frame: pd.DataFrame,
    details: str,
) -> Path:
    note_path = root / "submissions" / f"{submission_id}.md"
    counts = frame[project_config.TARGET].value_counts().sort_index()
    distribution = "\n".join(
        f"| {int(label)} | {int(rows)} | {rows / len(frame):.4f} |"
        for label, rows in counts.items()
    )
    note_path.write_text(
        f"""---
type: kaggle-submission
id: {submission_id}
status: ready
candidate: {candidate_id}
source: {candidate_id.split('/')[0]}
model: {model}
kaggle_public_score:
kaggle_private_score:
---

# {submission_id} — {candidate_id}

## Контракт submission

- Candidate: `{candidate_id}`
- Model: `{model}`
- CV accuracy: **{cv_mean:.4f} ± {cv_std:.4f}**
- Rows: **{len(frame)}**
- CSV: [[{csv_path.relative_to(root).as_posix()}|{csv_path.name}]]
- CSV SHA-256: `{_sha256(csv_path)}`

{details}

## Распределение предсказаний

| prediction | rows | share |
|---:|---:|---:|
{distribution}

## Kaggle результат

- После загрузки заполнить `kaggle_public_score` и `kaggle_private_score` во frontmatter.
- Дата отправки:
- Наблюдение:
""",
        encoding="utf-8",
    )
    return note_path


def _update_registry(
    root: Path,
    rows: list[dict[str, Any]],
) -> None:
    registry_path = root / "submissions/results.csv"
    registry = pd.read_csv(registry_path) if registry_path.is_file() else pd.DataFrame()
    ids = {str(row["submission_id"]) for row in rows}
    if not registry.empty:
        registry = registry[~registry["submission_id"].astype(str).isin(ids)]
    registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    registry.to_csv(registry_path, index=False)
    _write_submission_index(root, registry)


def create_ensemble_and_mlp_submissions(
    project_root: str | Path,
    *,
    stacking_id: str = "SUB-009",
    mlp_id: str = "SUB-010",
) -> tuple[CreatedSubmission, CreatedSubmission]:
    """Fit full-train ENS-003/MLP-024 and save two Kaggle-ready CSV files."""

    root = Path(project_root).resolve()
    catalog = DataCatalog(root, project_config.RAW_DIR, project_config.DATASETS)
    catalog.validate()
    train = catalog.load(project_config.TRAIN_DATASET)
    inference = catalog.load(project_config.INFERENCE_DATASET)
    sample = (
        catalog.load("gender_submission")
        if "gender_submission" in catalog.available_names()
        else pd.DataFrame(
            {
                project_config.KEY: inference[project_config.KEY].to_numpy(),
                project_config.TARGET: np.zeros(len(inference), dtype="int64"),
            }
        )
    )
    report = catalog.file_report().set_index("dataset")
    dataset_versions = {
        "train": str(report.loc[project_config.TRAIN_DATASET, "sha256"]),
        "inference": str(report.loc[project_config.INFERENCE_DATASET, "sha256"]),
    }

    # Learn final meta-weights from cross-fitted train probabilities.
    oof_path = root / "artifacts/ensembles/ENS-002/oof_predictions.csv"
    if not oof_path.is_file():
        raise FileNotFoundError("Run ENS-002 first to create base OOF probabilities")
    oof = pd.read_csv(oof_path)
    members = list(SPEC_003.members)
    weight_matrix = oof[[f"probability_{name}" for name in members]].to_numpy()
    weights = _learn_simplex_weights(weight_matrix, oof["target"].to_numpy())

    context = prepare_screening_context(
        root,
        train,
        project_config.FEATURE_GROUPS,
        target=project_config.TARGET,
        key=project_config.KEY,
        initial_settings=BASELINE,
        feature_reference_module=SPEC_003.feature_reference_module,
    )
    definition = load_experiment(SPEC_003.feature_reference_module)
    prepared_inference = prepare_experiment_candidate(
        definition,
        inference,
        project_config.FEATURE_GROUPS,
        BASELINE,
    )
    # The versioned EXP pipeline begins with raw transformers (Title/Age), so
    # serving must retain the same raw-plus-derived input contract used in CV.
    inference_x = prepared_inference.frame.loc[:, list(context.data.X.columns)]
    pipeline_specs = {
        "xgboost": ("external_boosting", "xgboost"),
        "lightgbm": ("external_boosting", "lightgbm"),
        "catboost": ("native_categorical", "catboost"),
    }
    fitted_pipelines: dict[str, Any] = {}
    test_probabilities: dict[str, np.ndarray] = {}
    for model_id, (group, registry_id) in pipeline_specs.items():
        fitted = _screening_pipeline(context, group, registry_id)
        fitted.fit(context.data.X, context.data.y)
        fitted_pipelines[model_id] = fitted
        test_probabilities[model_id] = _positive_probability(fitted, inference_x)

    mlp_module = importlib.reload(importlib.import_module(SPEC_003.mlp_module))
    prepared_train_mlp = mlp_module.prepare_features(train.copy(deep=True))
    prepared_test_mlp = mlp_module.prepare_features(inference.copy(deep=True))
    final_mlp = fit_final_mlp(
        prepared_train_mlp,
        target=project_config.TARGET,
        build_network=mlp_module.build_network,
        spec=mlp_module.EXPERIMENT,
        build_fold_transformer=getattr(mlp_module, "build_fold_transformer", None),
    )
    test_probabilities["mlp_024"] = predict_prepared_mlp(
        final_mlp, prepared_test_mlp
    )

    stacking_probability = np.column_stack(
        [test_probabilities[name] for name in members]
    ) @ weights
    stacking_frame = _submission_frame(
        inference,
        sample,
        (stacking_probability >= SPEC_003.threshold).astype("int64"),
    )
    mlp_frame = _submission_frame(
        inference,
        sample,
        (test_probabilities["mlp_024"] >= mlp_module.EXPERIMENT.training.threshold).astype("int64"),
    )

    stacking_dir = root / "artifacts/submissions" / stacking_id
    mlp_dir = root / "artifacts/submissions" / mlp_id
    stacking_dir.mkdir(parents=True, exist_ok=True)
    mlp_dir.mkdir(parents=True, exist_ok=True)
    stacking_csv = stacking_dir / f"{stacking_id}_ENS-003_stacking.csv"
    mlp_csv = mlp_dir / f"{mlp_id}_MLP-024.csv"
    stacking_frame.to_csv(stacking_csv, index=False)
    mlp_frame.to_csv(mlp_csv, index=False)
    pd.DataFrame(
        {
            project_config.KEY: inference[project_config.KEY],
            **{f"probability_{name}": test_probabilities[name] for name in members},
            "probability_stacking": stacking_probability,
        }
    ).to_csv(stacking_dir / "test_probabilities.csv", index=False)
    pd.DataFrame(
        {
            project_config.KEY: inference[project_config.KEY],
            "probability": test_probabilities["mlp_024"],
        }
    ).to_csv(mlp_dir / "test_probabilities.csv", index=False)
    pd.DataFrame([dict(zip(members, weights, strict=True))]).to_csv(
        stacking_dir / "final_weights.csv", index=False
    )
    joblib.dump(fitted_pipelines, stacking_dir / "base_pipelines.joblib")
    save_final_mlp(stacking_dir, final_mlp)
    save_final_mlp(mlp_dir, final_mlp)

    common_metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_versions": dataset_versions,
        "feature_reference": SPEC_003.feature_reference_module,
        "mlp_module": SPEC_003.mlp_module,
    }
    (stacking_dir / "metadata.json").write_text(
        json.dumps(
            {
                **common_metadata,
                "submission_id": stacking_id,
                "candidate_id": "ENS-003/stacking",
                "members": {name: MODEL_SOURCES[name] for name in members},
                "final_weights": dict(zip(members, weights, strict=True)),
                "threshold": SPEC_003.threshold,
                "csv_sha256": _sha256(stacking_csv),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (mlp_dir / "metadata.json").write_text(
        json.dumps(
            {
                **common_metadata,
                "submission_id": mlp_id,
                "candidate_id": "MLP-024/candidate",
                "threshold": mlp_module.EXPERIMENT.training.threshold,
                "best_epoch": final_mlp.best_epoch,
                "csv_sha256": _sha256(mlp_csv),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    weight_text = ", ".join(
        f"{name}={weight:.4f}" for name, weight in zip(members, weights, strict=True)
    )
    stacking_note = _write_card(
        root,
        stacking_id,
        "ENS-003/stacking",
        "NestedWeightedSoftVoting",
        0.840606,
        0.021788,
        stacking_csv,
        stacking_frame,
        f"## Финальные веса\n\n`{weight_text}`\n\nВеса обучены по полным cross-fitted OOF-прогнозам train; test labels не использовались.",
    )
    mlp_note = _write_card(
        root,
        mlp_id,
        "MLP-024/candidate",
        "TitanicMLP",
        0.838365,
        0.011105,
        mlp_csv,
        mlp_frame,
        f"## Финальное обучение\n\nMLP-024 обучена на полном train после выбора числа эпох на внутреннем split. Выбрано эпох: **{final_mlp.best_epoch}**.",
    )

    rows = [
        {
            "submission_id": stacking_id,
            "note": stacking_note.relative_to(root).as_posix(),
            "candidate_id": "ENS-003/stacking",
            "source_type": "ensemble",
            "source_id": "ENS-003",
            "feature_reference": "EXP-013 + MLP-024",
            "model": "NestedWeightedSoftVoting",
            "cv_metric": "accuracy",
            "cv_mean": 0.840606,
            "cv_std": 0.021788,
            "original_decision": "pending",
            "rows": len(stacking_frame),
            "submission_file": stacking_csv.relative_to(root).as_posix(),
            "submission_sha256": _sha256(stacking_csv),
            "kaggle_public_score": "",
            "kaggle_private_score": "",
        },
        {
            "submission_id": mlp_id,
            "note": mlp_note.relative_to(root).as_posix(),
            "candidate_id": "MLP-024/candidate",
            "source_type": "mlp",
            "source_id": "MLP-024",
            "feature_reference": "MLP-024",
            "model": "TitanicMLP",
            "cv_metric": "accuracy",
            "cv_mean": 0.838365,
            "cv_std": 0.011105,
            "original_decision": "adopt",
            "rows": len(mlp_frame),
            "submission_file": mlp_csv.relative_to(root).as_posix(),
            "submission_sha256": _sha256(mlp_csv),
            "kaggle_public_score": "",
            "kaggle_private_score": "",
        },
    ]
    _update_registry(root, rows)

    return (
        CreatedSubmission(
            stacking_id,
            "ENS-003/stacking",
            stacking_csv,
            stacking_note,
            {int(k): int(v) for k, v in stacking_frame[project_config.TARGET].value_counts().items()},
        ),
        CreatedSubmission(
            mlp_id,
            "MLP-024/candidate",
            mlp_csv,
            mlp_note,
            {int(k): int(v) for k, v in mlp_frame[project_config.TARGET].value_counts().items()},
        ),
    )


__all__ = ["CreatedSubmission", "create_ensemble_and_mlp_submissions"]
