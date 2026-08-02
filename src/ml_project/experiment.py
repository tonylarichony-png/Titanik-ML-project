"""Reusable orchestration for controlled experiments after the baseline."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any, Mapping

import numpy as np
import pandas as pd

from . import baseline as baseline_tools
from .baseline import (
    BaselineSettings,
    CVEvaluation,
    FeaturePlan,
    PreparedData,
    SavedBaselineRun,
    ScoringPlan,
)
from .docsync import MarkdownDocument, dataframe_to_markdown


DECISIONS = {"pending", "adopt", "reject", "iterate", "inconclusive"}


@dataclass(frozen=True)
class ExperimentSettings:
    experiment_id: str
    experiment_title: str
    experiment_note: Path
    hypothesis: str
    change_description: str
    success_criterion: str
    reference_model: str
    primary_candidate: str
    experiment_parameters: Mapping[str, Any]
    decision: str
    run_name: str
    artifact_dir: Path
    results_registry: Path
    save_artifacts: bool
    save_metric_figures: bool
    metric_figure_dpi: int
    save_final_model: bool
    sync_experiment_note: bool
    sync_docs: bool
    allow_overwrite: bool


def settings_from_module(module: ModuleType) -> ExperimentSettings:
    """Reload the editable experiment config without cached values."""

    return ExperimentSettings(
        experiment_id=str(getattr(module, "EXPERIMENT_ID")),
        experiment_title=str(getattr(module, "EXPERIMENT_TITLE")),
        experiment_note=Path(getattr(module, "EXPERIMENT_NOTE")),
        hypothesis=str(getattr(module, "HYPOTHESIS")),
        change_description=str(getattr(module, "CHANGE_DESCRIPTION")),
        success_criterion=str(getattr(module, "SUCCESS_CRITERION")),
        reference_model=str(getattr(module, "REFERENCE_MODEL")),
        primary_candidate=str(getattr(module, "PRIMARY_CANDIDATE")),
        experiment_parameters=dict(getattr(module, "EXPERIMENT_PARAMETERS")),
        decision=str(getattr(module, "DECISION")).lower(),
        run_name=str(getattr(module, "RUN_NAME")),
        artifact_dir=Path(getattr(module, "ARTIFACT_DIR")),
        results_registry=Path(getattr(module, "RESULTS_REGISTRY")),
        save_artifacts=bool(getattr(module, "SAVE_ARTIFACTS")),
        save_metric_figures=bool(getattr(module, "SAVE_METRIC_FIGURES")),
        metric_figure_dpi=int(getattr(module, "METRIC_FIGURE_DPI")),
        save_final_model=bool(getattr(module, "SAVE_FINAL_MODEL")),
        sync_experiment_note=bool(getattr(module, "SYNC_EXPERIMENT_NOTE")),
        sync_docs=bool(getattr(module, "SYNC_DOCS")),
        allow_overwrite=bool(getattr(module, "ALLOW_OVERWRITE")),
    )


def validate_settings(settings: ExperimentSettings) -> None:
    errors: list[str] = []
    name_pattern = r"[A-Za-z0-9][A-Za-z0-9._-]*"
    if not re.fullmatch(name_pattern, settings.experiment_id):
        errors.append("EXPERIMENT_ID contains unsupported characters")
    if not re.fullmatch(name_pattern, settings.run_name):
        errors.append("RUN_NAME contains unsupported characters")
    for label, value in (
        ("EXPERIMENT_TITLE", settings.experiment_title),
        ("HYPOTHESIS", settings.hypothesis),
        ("CHANGE_DESCRIPTION", settings.change_description),
        ("SUCCESS_CRITERION", settings.success_criterion),
        ("REFERENCE_MODEL", settings.reference_model),
        ("PRIMARY_CANDIDATE", settings.primary_candidate),
    ):
        if not value.strip() or "CHANGE ME" in value.upper():
            errors.append(f"Fill {label} before running the experiment")
    if settings.reference_model == settings.primary_candidate:
        errors.append("REFERENCE_MODEL and PRIMARY_CANDIDATE must be different")
    if settings.decision not in DECISIONS:
        errors.append("DECISION must be one of: " + ", ".join(sorted(DECISIONS)))
    for label, path, suffix in (
        ("EXPERIMENT_NOTE", settings.experiment_note, ".md"),
        ("RESULTS_REGISTRY", settings.results_registry, ".csv"),
    ):
        if path.is_absolute():
            errors.append(f"{label} must be relative to the project root")
        if path.suffix.lower() != suffix:
            errors.append(f"{label} must end with {suffix}")
    if settings.artifact_dir.is_absolute():
        errors.append("ARTIFACT_DIR must be relative to the project root")
    if settings.metric_figure_dpi < 72:
        errors.append("METRIC_FIGURE_DPI must be at least 72")
    if errors:
        raise ValueError(
            "Invalid src/ml_project/experiment_config.py:\n"
            + "\n".join(f"- {error}" for error in errors)
        )


def settings_report(settings: ExperimentSettings) -> pd.DataFrame:
    rows = [
        ("identity", "EXPERIMENT_ID", settings.experiment_id),
        ("identity", "EXPERIMENT_TITLE", settings.experiment_title),
        ("pre-registration", "HYPOTHESIS", settings.hypothesis),
        ("pre-registration", "CHANGE_DESCRIPTION", settings.change_description),
        ("pre-registration", "SUCCESS_CRITERION", settings.success_criterion),
        ("comparison", "REFERENCE_MODEL", settings.reference_model),
        ("comparison", "PRIMARY_CANDIDATE", settings.primary_candidate),
        ("comparison", "DECISION", settings.decision),
        ("write", "RUN_NAME", settings.run_name),
        ("write", "SAVE_ARTIFACTS", settings.save_artifacts),
        ("write", "SAVE_METRIC_FIGURES", settings.save_metric_figures),
        ("write", "SAVE_FINAL_MODEL", settings.save_final_model),
        ("write", "SYNC_EXPERIMENT_NOTE", settings.sync_experiment_note),
        ("write", "SYNC_DOCS", settings.sync_docs),
        ("write", "ALLOW_OVERWRITE", settings.allow_overwrite),
    ]
    return pd.DataFrame(rows, columns=["section", "parameter", "value"])


def prepare_experiment_data(
    reference_data: PreparedData,
    experiment_frame: pd.DataFrame,
    *,
    target: str,
) -> PreparedData:
    """Align candidate columns to exactly the rows/target used by the reference."""

    missing_rows = reference_data.row_index.difference(experiment_frame.index)
    if len(missing_rows):
        raise ValueError("experiment_frame lost rows from the reference dataset")
    if target not in experiment_frame:
        raise KeyError(f"TARGET {target!r} is absent from experiment_frame")
    aligned = experiment_frame.loc[reference_data.row_index]
    candidate_y = aligned[target]
    if not np.array_equal(candidate_y.to_numpy(), reference_data.y.to_numpy()):
        raise ValueError(
            "The experiment changed TARGET values or row order. Start a new "
            "validation contract instead of comparing this run to the baseline."
        )
    changed_reference_features = [
        column
        for column in reference_data.X.columns
        if column not in aligned
        or not aligned[column].equals(reference_data.X[column])
    ]
    if changed_reference_features:
        raise ValueError(
            "Do not overwrite raw baseline features in experiment_frame. "
            "Create a new feature or transform it inside the candidate Pipeline: "
            + ", ".join(changed_reference_features)
        )
    return PreparedData(
        X=aligned.drop(columns=[target]),
        y=reference_data.y,
        groups=reference_data.groups,
        row_index=reference_data.row_index,
    )


def validate_model_contract(
    candidate_models: Mapping[str, Any],
    settings: ExperimentSettings,
) -> None:
    if not candidate_models:
        raise ValueError(
            "The candidate_models dictionary is empty. Fill the editable "
            "experiment cell before continuing."
        )
    if settings.reference_model in candidate_models:
        raise ValueError("candidate_models must not overwrite REFERENCE_MODEL")
    if settings.primary_candidate not in candidate_models:
        raise ValueError(
            f"PRIMARY_CANDIDATE={settings.primary_candidate!r} is absent from "
            "candidate_models"
        )


def comparison_summary(
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    *,
    reference_model: str,
) -> pd.DataFrame:
    """Add deltas where positive always means improvement over the reference."""

    summary = evaluation.summary[
        evaluation.summary["split"] == "validation"
    ].copy()
    reference = summary[summary["model"] == reference_model][
        ["metric_key", "mean"]
    ].rename(columns={"mean": "reference_mean"})
    if set(reference["metric_key"]) != set(scoring.scorers):
        raise ValueError(f"Reference model {reference_model!r} has incomplete metrics")
    result = summary.merge(reference, on="metric_key", how="left")
    raw_delta = result["mean"] - result["reference_mean"]
    result["improvement"] = np.where(
        result["direction"].eq("maximize"), raw_delta, -raw_delta
    )
    result["mean ± std"] = result.apply(
        lambda row: f"{row['mean']:.4f} ± {row['std']:.4f}", axis=1
    )
    return result


def _effective_baseline_settings(
    baseline_settings: BaselineSettings,
    experiment_settings: ExperimentSettings,
) -> BaselineSettings:
    return replace(
        baseline_settings,
        experiment_id=experiment_settings.experiment_id,
        experiment_title=experiment_settings.experiment_title,
        experiment_note=experiment_settings.experiment_note,
        run_name=experiment_settings.run_name,
        artifact_dir=experiment_settings.artifact_dir,
        save_artifacts=experiment_settings.save_artifacts,
        save_metric_figures=experiment_settings.save_metric_figures,
        metric_figure_dpi=experiment_settings.metric_figure_dpi,
        save_final_model=experiment_settings.save_final_model,
        sync_docs=experiment_settings.sync_docs,
        sync_experiment_note=experiment_settings.sync_experiment_note,
        allow_overwrite=experiment_settings.allow_overwrite,
    )


def save_experiment_run(
    project_root: Path,
    experiment_settings: ExperimentSettings,
    baseline_settings: BaselineSettings,
    evaluation: CVEvaluation,
    candidate_plan: FeaturePlan,
    scoring: ScoringPlan,
    *,
    dataset_version: str,
    cv_description: str,
    models: Mapping[str, Any],
    data: PreparedData,
    metric_figures: Mapping[str, Any] | None = None,
) -> SavedBaselineRun:
    """Save generic experiment outputs using the proven baseline artifact layer."""

    validate_model_contract(
        {key: value for key, value in models.items() if key != experiment_settings.reference_model},
        experiment_settings,
    )
    effective = _effective_baseline_settings(baseline_settings, experiment_settings)
    saved = baseline_tools.save_baseline_run(
        project_root,
        effective,
        evaluation,
        candidate_plan,
        scoring,
        dataset_version=dataset_version,
        cv_description=cv_description,
        final_pipeline=models[experiment_settings.primary_candidate],
        data=data,
        metric_figures=metric_figures,
    )
    metadata = json.loads(saved.metadata_path.read_text(encoding="utf-8"))
    metadata.update(
        {
            "run_kind": "controlled_experiment",
            "hypothesis": experiment_settings.hypothesis,
            "change_description": experiment_settings.change_description,
            "success_criterion": experiment_settings.success_criterion,
            "reference_model": experiment_settings.reference_model,
            "primary_candidate": experiment_settings.primary_candidate,
            "evaluated_models": list(models),
            "experiment_parameters": dict(experiment_settings.experiment_parameters),
            "decision": experiment_settings.decision,
        }
    )
    saved.metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    return saved


def _vault_relative(project_root: Path, path: Path) -> str:
    root = Path(project_root).resolve()
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError(f"Path resolves outside project root: {path}") from error


def build_experiment_report(
    project_root: Path,
    settings: ExperimentSettings,
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    saved: SavedBaselineRun,
    *,
    dataset_version: str,
    cv_description: str,
) -> str:
    comparison = comparison_summary(
        evaluation, scoring, reference_model=settings.reference_model
    )
    overview = pd.DataFrame(
        [
            ("Эксперимент", f"{settings.experiment_id} — {settings.experiment_title}"),
            ("Гипотеза", settings.hypothesis),
            ("Одно изменение", settings.change_description),
            ("Критерий успеха", settings.success_criterion),
            ("Решение", settings.decision),
            ("Run", settings.run_name),
            ("Версия данных", dataset_version),
            ("Validation", cv_description),
            ("Reference", settings.reference_model),
            ("Основной кандидат", settings.primary_candidate),
            ("Основная метрика", scoring.contract_metric),
        ],
        columns=["Поле", "Значение"],
    )
    compact = comparison[
        ["model", "metric", "direction", "mean ± std", "reference_mean", "improvement"]
    ].rename(
        columns={
            "model": "Модель",
            "metric": "Метрика",
            "direction": "Направление",
            "reference_mean": "Reference",
            "improvement": "Δ к reference",
        }
    )
    sections = [
        "## Контракт эксперимента\n\n" + dataframe_to_markdown(overview),
        "> [!note] Как читать Δ\n> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.",
        "## Сравнение всех метрик\n\n" + dataframe_to_markdown(compact, float_digits=4),
    ]
    fold_scores = evaluation.fold_scores[evaluation.fold_scores["split"] == "validation"]
    figures = dict(saved.metric_figure_paths or {})
    for metric_key in scoring.scorers:
        label = scoring.labels[metric_key]
        metric_summary = comparison[comparison["metric_key"] == metric_key][
            ["model", "mean", "std", "min", "max", "reference_mean", "improvement"]
        ].rename(
            columns={
                "model": "Модель", "mean": "Mean", "std": "Std",
                "min": "Min", "max": "Max", "reference_mean": "Reference",
                "improvement": "Δ к reference",
            }
        )
        folds = fold_scores[fold_scores["metric_key"] == metric_key].pivot(
            index="fold", columns="model", values="value"
        ).reset_index().rename(columns={"fold": "Fold"})
        parts = [f"## Метрика: {label}"]
        if metric_key in figures:
            parts.append(f"![[{_vault_relative(project_root, figures[metric_key])}]]")
        parts.extend(
            [
                "### Сводка\n\n" + dataframe_to_markdown(metric_summary, float_digits=4),
                "### Значения по folds\n\n" + dataframe_to_markdown(folds, float_digits=4),
            ]
        )
        sections.append("\n\n".join(parts))
    run_rel = _vault_relative(project_root, saved.run_dir)
    artifact_lines = [
        f"- [[{run_rel}/cv_fold_scores.csv|cv_fold_scores.csv]]",
        f"- [[{run_rel}/cv_summary.csv|cv_summary.csv]]",
        f"- [[{run_rel}/metadata.json|metadata.json]]",
    ]
    if saved.model_path is not None:
        artifact_lines.append(f"- [[{run_rel}/model.joblib|model.joblib]]")
    sections.append("## Артефакты\n\n" + "\n".join(artifact_lines))
    return "\n\n".join(sections)


def _update_note_frontmatter(path: Path, fields: Mapping[str, str]) -> None:
    """Update generated scalar fields without touching the note body."""

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Experiment note has no YAML frontmatter: {path}")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError(f"Experiment note has invalid YAML frontmatter: {path}")
    frontmatter = text[4:closing]
    for key, value in fields.items():
        rendered = f"{key}: {value}"
        pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
        if pattern.search(frontmatter):
            frontmatter = pattern.sub(rendered, frontmatter, count=1)
        else:
            frontmatter = frontmatter.rstrip() + "\n" + rendered
    path.write_text(
        "---\n" + frontmatter.rstrip() + text[closing:], encoding="utf-8"
    )


def sync_experiment_note(
    project_root: Path,
    settings: ExperimentSettings,
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    saved: SavedBaselineRun,
    *,
    dataset_version: str,
    cv_description: str,
) -> list[str]:
    root = Path(project_root).resolve()
    note_path = (root / settings.experiment_note).resolve()
    _vault_relative(root, note_path)
    note_path.parent.mkdir(parents=True, exist_ok=True)
    if not note_path.exists():
        yaml_string = lambda value: json.dumps(value, ensure_ascii=False)
        note_path.write_text(
            "---\n"
            f"id: {settings.experiment_id}\n"
            "type: experiment\n"
            "experiment_type: hypothesis-test\n"
            "status: completed\n"
            f"created: {date.today().isoformat()}\n"
            f"hypothesis: {yaml_string(settings.hypothesis)}\n"
            f"primary_metric: {yaml_string(scoring.contract_metric)}\n"
            f"decision: {settings.decision}\n"
            "---\n\n"
            f"# {settings.experiment_id} — {settings.experiment_title}\n\n"
            "← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]\n\n"
            "> [!info] Автоматическая часть\n"
            "> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.\n\n"
            "<!-- auto:experiment-report:start -->\n\n"
            "Отчёт появится после сохранения запуска.\n\n"
            "<!-- auto:experiment-report:end -->\n\n"
            "## Анализ результата — заполнить вручную\n\n"
            "- **Что произошло:**\n"
            "- **Подтвердилась ли гипотеза:**\n"
            "- **Почему мог получиться такой результат:**\n"
            "- **Стабильность по folds / seeds:**\n"
            "- **Ограничения и возможный leakage:**\n\n"
            "## Решение — заполнить вручную\n\n"
            "- **Outcome:** adopt / reject / iterate / inconclusive.\n"
            "- **Следующий шаг:**\n",
            encoding="utf-8",
        )
    _update_note_frontmatter(
        note_path,
        {
            "status": "completed",
            "hypothesis": json.dumps(settings.hypothesis, ensure_ascii=False),
            "primary_metric": json.dumps(scoring.contract_metric, ensure_ascii=False),
            "decision": settings.decision,
        },
    )
    report = build_experiment_report(
        root, settings, evaluation, scoring, saved,
        dataset_version=dataset_version, cv_description=cv_description,
    )
    return MarkdownDocument(note_path).update_blocks({"experiment-report": report})


def _registry_row(
    settings: ExperimentSettings,
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    *,
    dataset_version: str,
) -> dict[str, Any]:
    comparison = comparison_summary(
        evaluation, scoring, reference_model=settings.reference_model
    )
    row = comparison[
        (comparison["metric_key"] == "primary")
        & (comparison["model"] == settings.primary_candidate)
    ]
    if row.empty:
        raise ValueError("Primary candidate has no primary metric result")
    record = row.iloc[0]
    return {
        "experiment_id": settings.experiment_id,
        "title": settings.experiment_title,
        "note": settings.experiment_note.as_posix(),
        "hypothesis": settings.hypothesis,
        "change": settings.change_description,
        "dataset_version": dataset_version,
        "run_name": settings.run_name,
        "candidate": settings.primary_candidate,
        "primary_metric": scoring.contract_metric,
        "direction": record["direction"],
        "reference_score": float(record["reference_mean"]),
        "candidate_score": float(record["mean"]),
        "improvement": float(record["improvement"]),
        "decision": settings.decision,
    }


def sync_experiment_docs(
    project_root: Path,
    settings: ExperimentSettings,
    evaluation: CVEvaluation,
    scoring: ScoringPlan,
    *,
    dataset_version: str,
) -> dict[str, Any]:
    """Upsert the registry and regenerate latest/leaderboard blocks in docs/05."""

    root = Path(project_root).resolve()
    registry_path = (root / settings.results_registry).resolve()
    _vault_relative(root, registry_path)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    row = _registry_row(
        settings, evaluation, scoring, dataset_version=dataset_version
    )
    if registry_path.exists():
        registry = pd.read_csv(registry_path)
        registry = registry[
            ~(
                registry["experiment_id"].astype(str).eq(settings.experiment_id)
                & registry["run_name"].astype(str).eq(settings.run_name)
            )
        ]
    else:
        registry = pd.DataFrame()
    registry = pd.concat([registry, pd.DataFrame([row])], ignore_index=True)
    registry.to_csv(registry_path, index=False)

    latest = pd.DataFrame(
        [
            ("Эксперимент", f"[[{row['note']}|{row['experiment_id']} — {row['title']}]]"),
            ("Гипотеза", row["hypothesis"]),
            ("Изменение", row["change"]),
            ("Метрика", row["primary_metric"]),
            ("Reference", f"{row['reference_score']:.4f}"),
            ("Кандидат", f"{row['candidate_score']:.4f}"),
            ("Δ к reference", f"{row['improvement']:+.4f}"),
            ("Решение", row["decision"]),
        ],
        columns=["Поле", "Значение"],
    )
    leaderboard = registry.copy()
    leaderboard["Experiment"] = leaderboard.apply(
        lambda item: f"[[{item['note']}|{item['experiment_id']}]]", axis=1
    )
    leaderboard = leaderboard[
        ["Experiment", "hypothesis", "change", "primary_metric", "reference_score", "candidate_score", "improvement", "decision"]
    ].rename(
        columns={
            "hypothesis": "Hypothesis", "change": "Change",
            "primary_metric": "Metric", "reference_score": "Reference",
            "candidate_score": "Result", "improvement": "Δ",
            "decision": "Decision",
        }
    )
    blocks = MarkdownDocument(root / "docs/05_experiments.md").update_blocks(
        {
            "latest-experiment": dataframe_to_markdown(latest, float_digits=4),
            "experiment-leaderboard": dataframe_to_markdown(leaderboard, float_digits=4),
        }
    )
    return {"registry": settings.results_registry.as_posix(), "blocks": blocks}


__all__ = [
    "ExperimentSettings",
    "build_experiment_report",
    "comparison_summary",
    "prepare_experiment_data",
    "save_experiment_run",
    "settings_from_module",
    "settings_report",
    "sync_experiment_docs",
    "sync_experiment_note",
    "validate_model_contract",
    "validate_settings",
]
