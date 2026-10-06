"""Generate the second Optuna notebook for MLP activations and architecture."""

from __future__ import annotations

import json
from pathlib import Path


def _markdown(cell_id: str, source: str) -> dict[str, object]:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def _code(cell_id: str, source: str) -> dict[str, object]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def build_notebook() -> dict[str, object]:
    """Собрать содержимое воспроизводимого Jupyter notebook."""
    cells = [
        _markdown(
            "intro",
            """# MLP-TUNE-002 — архитектура и функции активации

Это отдельное исследование после 140 trials `MLP-TUNE-001`. Оно не изменяет
первую SQLite study и не создаёт официальные `MLP-xxx` эксперименты.

Optuna подбирает архитектуру, функцию активации и параметры обучения. Первая
trial воспроизводит лучший screening-вариант №86 с `ReLU`. После screening
несколько кандидатов обязательно проверяются на пяти официальных folds.

`test.csv` здесь не используется. После работы завершите kernel через
**Kernel → Shut Down Kernel**, чтобы освободить память.
""",
        ),
        _markdown(
            "environment-md",
            """## 1. Ограничиваем потоки

Выполните эту ячейку первой. Trials идут последовательно, а библиотеки линейной
алгебры не создают лишние рабочие потоки.
""",
        ),
        _code(
            "environment",
            """import os

for variable in (
    "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "OMP_THREAD_LIMIT",
    "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
):
    os.environ[variable] = "1"
""",
        ),
        _markdown(
            "setup-md",
            """## 2. Данные и фиксированные screening folds

Используются те же признаки и fold-safe преобразования, что у принятой MLP-024.
Все trials видят одинаковые три folds с seed 2026, поэтому их можно сравнивать
между собой.
""",
        ),
        _code(
            "setup",
            """from dataclasses import replace
from pathlib import Path
import sys

import optuna
import pandas as pd
import torch
from IPython.display import display

torch.set_num_threads(1)

CURRENT_DIR = Path.cwd().resolve()
PROJECT_ROOT = next(
    path for path in (CURRENT_DIR, *CURRENT_DIR.parents)
    if (path / "README.md").is_file() and (path / "src").is_dir()
)
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ml_project import DataCatalog
import ml_project.config as project_config
import ml_project.mlp_experiment as mlp_tools
import ml_project.mlp_tuning as tuning

PARENT_MODULE = "ml_project.mlp_experiments.mlp_024_dpoutmedium"
parent = mlp_tools.load_mlp_experiment(PARENT_MODULE)

catalog = DataCatalog(PROJECT_ROOT, project_config.RAW_DIR, project_config.DATASETS)
raw_train = catalog.load(project_config.TRAIN_DATASET)
prepared = parent.prepare_features(raw_train.copy(deep=True))
mlp_tools.validate_feature_data(
    prepared, raw_train, target=project_config.TARGET, key=project_config.KEY
)

build_fold_transformer = getattr(parent, "build_fold_transformer", None)
screening_splits = tuning.make_stratified_splits(
    prepared,
    target=project_config.TARGET,
    n_splits=3,
    random_state=2026,
)

print("Project:", PROJECT_ROOT)
print("Parent:", parent.EXPERIMENT.experiment_id, parent.EXPERIMENT.title)
print("Rows:", len(prepared.frame))
print("Screening folds:", len(screening_splits))
""",
        ),
        _markdown(
            "space-md",
            """## 3. Что выбирает Optuna

Каждая сеть использует одну функцию активации во всех скрытых слоях:
`ReLU`, `LeakyReLU`, `GELU`, `SiLU` или `SquaredReLU`. Для `LeakyReLU`
дополнительно выбирается `negative_slope`.

Также меняются:

- `batch_size`: 32 или 64;
- `learning_rate`: от 0.0012 до 0.0025;
- `weight_decay`: от 1e-7 до 1e-4;
- `dropout`: от 0.05 до 0.30;
- число скрытых слоёв: от 3 до 5;
- общая ширина скрытых слоёв: 4, 8, 12 или 16.

Dropout остаётся после последнего скрытого слоя. BatchNorm не добавляется.
""",
        ),
        _code(
            "study",
            """STUDY_NAME = "titanic_mlp_tuning_002"
STUDY_DIR = PROJECT_ROOT / "artifacts/optuna"
STUDY_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = STUDY_DIR / f"{STUDY_NAME}.db"
STORAGE = f"sqlite:///{DATABASE_PATH.as_posix()}"

study = optuna.create_study(
    study_name=STUDY_NAME,
    storage=STORAGE,
    load_if_exists=True,
    direction="maximize",
    sampler=optuna.samplers.TPESampler(seed=43),
)

if not study.trials:
    study.enqueue_trial(tuning.PHASE2_BASELINE_PARAMETERS)

objective = tuning.make_phase2_objective(
    prepared,
    target=project_config.TARGET,
    key=project_config.KEY,
    base_spec=parent.EXPERIMENT,
    cv_splits=screening_splits,
    build_fold_transformer=build_fold_transformer,
)

print("Storage:", DATABASE_PATH.relative_to(PROJECT_ROOT))
print("Existing trials:", len(study.trials))
display(pd.Series(tuning.PHASE2_BASELINE_PARAMETERS, name="trial 86 + ReLU").to_frame())
""",
        ),
        _markdown(
            "run-md",
            """## 4. Запускаем небольшими этапами

Начните с 20 trials. Повторный запуск этой ячейки добавит ещё 20 в ту же study.
После 60–80 trials проверьте, продолжает ли улучшаться максимум и какие активации
встречаются среди лучших результатов.
""",
        ),
        _code(
            "run",
            """N_TRIALS = 20

study.optimize(
    objective,
    n_trials=N_TRIALS,
    n_jobs=1,
    gc_after_trial=True,
    show_progress_bar=True,
)
""",
        ),
        _markdown(
            "results-md",
            """## 5. Таблица результатов

`value` — средняя accuracy на трёх screening folds. Сохраняем таблицу в CSV,
чтобы результаты не зависели от состояния notebook.
""",
        ),
        _code(
            "results",
            """trials = study.trials_dataframe()
csv_path = STUDY_DIR / f"{STUDY_NAME}_trials.csv"
trials.to_csv(csv_path, index=False)

columns = [
    "number", "value", "state",
    "params_activation", "params_negative_slope",
    "params_batch_size", "params_learning_rate", "params_weight_decay",
    "params_dropout", "params_n_layers", "params_hidden_dim",
    "user_attrs_accuracy_std", "user_attrs_log_loss_mean",
]
available = [column for column in columns if column in trials]
complete = trials.loc[trials["state"].eq("COMPLETE"), available]
display(complete.sort_values("value", ascending=False).head(15))

print("Saved:", csv_path.relative_to(PROJECT_ROOT))
print("Best screening accuracy:", study.best_value)
print("Best parameters:", study.best_params)
""",
        ),
        _markdown(
            "activation-md",
            """## 6. Смотрим не только на одну лучшую trial

Одна trial может случайно удачно попасть в три folds. Здесь сравниваются число
попаданий каждой активации в top-20, её лучшая accuracy и медиана результатов.
""",
        ),
        _code(
            "activation-analysis",
            """complete_all = trials.loc[trials["state"].eq("COMPLETE")].copy()
top_20 = complete_all.nlargest(min(20, len(complete_all)), "value")

activation_summary = (
    complete_all.groupby("params_activation")
    .agg(
        trials=("number", "count"),
        best_accuracy=("value", "max"),
        median_accuracy=("value", "median"),
        mean_accuracy=("value", "mean"),
    )
    .sort_values("best_accuracy", ascending=False)
)
top_counts = top_20["params_activation"].value_counts().rename("top_20_count")
display(activation_summary.join(top_counts).fillna({"top_20_count": 0}))
""",
        ),
        _markdown(
            "official-md",
            """## 7. Официальная перепроверка трёх лучших trials

Эта ячейка ничего не сохраняет в реестр и не принимает решение `adopt`. Она
заново обучает MLP-024 и три лучших кандидата на пяти folds с seed 42. Запускайте
её после окончания screening.

Если несколько лучших trials почти одинаковы, замените `head(3)` на выбранные
номера, чтобы проверить разные активации.
""",
        ),
        _code(
            "official-check",
            """official_splits = tuning.make_stratified_splits(
    prepared,
    target=project_config.TARGET,
    n_splits=5,
    random_state=42,
)

reference_spec = replace(
    parent.EXPERIMENT,
    experiment_id="TUNE2-OFFICIAL-REFERENCE",
    title="MLP-024 official-fold reference",
    save_artifacts=False,
    sync_docs=False,
)
reference_result = mlp_tools.run_mlp_cv(
    prepared,
    target=project_config.TARGET,
    key=project_config.KEY,
    build_network=parent.build_network,
    spec=reference_spec,
    build_fold_transformer=build_fold_transformer,
    cv_splits=official_splits,
)

rows = [{
    "candidate": "MLP-024",
    "screening_trial": None,
    "accuracy": float(reference_result.summary.loc["accuracy", "mean"]),
    "accuracy_std": float(reference_result.summary.loc["accuracy", "std"]),
    "balanced_accuracy": float(reference_result.summary.loc["balanced_accuracy", "mean"]),
    "f1": float(reference_result.summary.loc["f1", "mean"]),
    "roc_auc": float(reference_result.summary.loc["roc_auc", "mean"]),
    "log_loss": float(reference_result.summary.loc["log_loss", "mean"]),
}]

selected_trials = sorted(
    (trial for trial in study.trials if trial.value is not None),
    key=lambda trial: trial.value,
    reverse=True,
)[:3]

for selected in selected_trials:
    parameters = selected.params
    candidate_spec = replace(
        parent.EXPERIMENT,
        experiment_id=f"TUNE2-OFFICIAL-{selected.number:04d}",
        title=f"Official-fold check of trial {selected.number}",
        training=tuning.training_from_parameters(parent.EXPERIMENT.training, parameters),
        save_artifacts=False,
        sync_docs=False,
    )
    result = mlp_tools.run_mlp_cv(
        prepared,
        target=project_config.TARGET,
        key=project_config.KEY,
        build_network=tuning.build_phase2_network_factory(parameters),
        spec=candidate_spec,
        build_fold_transformer=build_fold_transformer,
        cv_splits=official_splits,
    )
    rows.append({
        "candidate": f"trial {selected.number}: {parameters['activation']}",
        "screening_trial": selected.number,
        "accuracy": float(result.summary.loc["accuracy", "mean"]),
        "accuracy_std": float(result.summary.loc["accuracy", "std"]),
        "balanced_accuracy": float(result.summary.loc["balanced_accuracy", "mean"]),
        "f1": float(result.summary.loc["f1", "mean"]),
        "roc_auc": float(result.summary.loc["roc_auc", "mean"]),
        "log_loss": float(result.summary.loc["log_loss", "mean"]),
    })

official_comparison = pd.DataFrame(rows).sort_values("accuracy", ascending=False)
display(official_comparison)
""",
        ),
        _markdown(
            "decision-md",
            """## 8. Как принять решение

Победа на screening folds только выдвигает кандидата. Если он сохраняет улучшение
на пяти официальных folds, создайте обычный `new-MLPexperiment` на основе MLP-024,
перенесите выбранную архитектуру и выполните стандартный notebook. Только его
paired-сравнение и карточка используются для решения `adopt` или `reject`.

Не выбирайте seed как гиперпараметр: это поиск удачной случайности, а не модели.
""",
        ),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python (titanik-ml)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def create_notebook(project_root: Path) -> Path:
    """Создать воспроизводимый Jupyter notebook на диске."""
    path = (
        Path(project_root).resolve()
        / "notebooks/mlp-tuning/02_optuna_mlp_activations.ipynb"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_notebook(), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> int:
    """Запустить команду модуля из командной строки."""
    path = create_notebook(Path.cwd())
    print("Created:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
