"""Generate the step-by-step Optuna notebook for the adopted Titanic MLP."""

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
            "tune-intro",
            """# MLP-TUNE-001 — подбор гиперпараметров Optuna

Этот notebook не создаёт 30 официальных `MLP-xxx`. Он проводит screening вокруг
принятой **MLP-024**, сохраняет каждую trial в SQLite и показывает лучшие наборы.

Порядок: **фиксированные folds → trials → таблица результатов → проверка лучших
конфигураций → отдельный официальный MLP-эксперимент**.

`test.csv` в подборе не используется. Запускайте notebook в одном kernel и после
работы завершайте его через **Kernel → Shut Down Kernel**.
""",
        ),
        _markdown(
            "tune-env-md",
            """## 1. Ограничиваем вычислительные потоки

Эта ячейка должна выполняться первой. `n_jobs=1` означает, что Optuna не создаёт
параллельные trials, а ограничения BLAS не позволяют одному kernel резервировать
гигабайты памяти под множество потоков.
""",
        ),
        _code(
            "tune-env",
            """import os

for variable in (
    "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "OMP_THREAD_LIMIT",
    "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
):
    os.environ[variable] = "1"
""",
        ),
        _markdown(
            "tune-imports-md",
            """## 2. Импорты и источник данных

Да, здесь впервые появляется `import optuna`. Но сначала пакет должен быть частью
окружения (`requirements.txt` и `environment.yml` уже обновлены).
""",
        ),
        _code(
            "tune-imports",
            """from pathlib import Path
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
cv_splits = tuning.make_stratified_splits(
    prepared,
    target=project_config.TARGET,
    n_splits=3,
    random_state=2026,
)

print("Project:", PROJECT_ROOT)
print("Parent:", parent.EXPERIMENT.experiment_id, parent.EXPERIMENT.title)
print("Rows:", len(prepared.frame))
print("Screening folds:", len(cv_splits))
""",
        ),
        _markdown(
            "tune-space-md",
            """## 3. Пространство поиска

Optuna будет выбирать batch size, learning rate, weight decay, Dropout, глубину и
общую ширину скрытых слоёв. ReLU, положение Dropout, признаки и preprocessing
зафиксированы результатами ручных экспериментов.

Первая trial принудительно повторяет параметры MLP-024 и становится baseline на
новых screening folds. Её accuracy не обязана равняться официальным `0.8384`:
здесь используются три folds с другим seed. Все последующие trials сравниваются
именно с этой контрольной trial на тех же строках.
""",
        ),
        _code(
            "tune-study",
            """STUDY_NAME = "titanic_mlp_tuning_001"
STUDY_DIR = PROJECT_ROOT / "artifacts/optuna"
STUDY_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = STUDY_DIR / f"{STUDY_NAME}.db"
STORAGE = f"sqlite:///{DATABASE_PATH.as_posix()}"

study = optuna.create_study(
    study_name=STUDY_NAME,
    storage=STORAGE,
    load_if_exists=True,
    direction="maximize",
    sampler=optuna.samplers.TPESampler(seed=42),
)

if not study.trials:
    study.enqueue_trial(tuning.BASELINE_PARAMETERS)

objective = tuning.make_objective(
    prepared,
    target=project_config.TARGET,
    key=project_config.KEY,
    base_spec=parent.EXPERIMENT,
    cv_splits=cv_splits,
    build_fold_transformer=build_fold_transformer,
)

print("Storage:", DATABASE_PATH.relative_to(PROJECT_ROOT))
print("Existing trials:", len(study.trials))
display(pd.Series(tuning.BASELINE_PARAMETERS, name="MLP-024").to_frame())
""",
        ),
        _markdown(
            "tune-run-md",
            """## 4. Запуск trials

Для первого знакомства начните с 10 trials. Повторный запуск продолжит ту же
SQLite study. Когда всё понятно, измените `N_TRIALS` на 20–30.
""",
        ),
        _code(
            "tune-run",
            """N_TRIALS = 10

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
            "tune-results-md",
            """## 5. Результаты

`value` — средняя accuracy на трёх одинаковых screening folds. Эта таблица нужна
для отбора кандидатов, а не для объявления нового чемпиона.
""",
        ),
        _code(
            "tune-results",
            """trials = study.trials_dataframe()
trials.to_csv(STUDY_DIR / f"{STUDY_NAME}_trials.csv", index=False)

columns = [
    "number", "value", "state",
    "params_batch_size", "params_learning_rate", "params_weight_decay",
    "params_dropout", "params_n_layers", "params_hidden_dim",
    "user_attrs_accuracy_std", "user_attrs_log_loss_mean",
]
available = [column for column in columns if column in trials]
display(
    trials.loc[trials["state"].eq("COMPLETE"), available]
    .sort_values("value", ascending=False)
    .head(10)
)

print("Best screening accuracy:", study.best_value)
print("Best parameters:", study.best_params)
""",
        ),
        _markdown(
            "tune-next-md",
            """## 6. Что делать с победителем

1. Не помечать trial как `adopt`.
2. Взять 3–5 лучших конфигураций и проверить их на официальных пяти folds и
   нескольких seed.
3. Создать `new-MLPexperiment.cmd` на основе MLP-024.
4. Перенести только выбранные параметры и архитектуру.
5. Выполнить обычный notebook, получить paired-сравнение и только затем принять
   или отклонить кандидата.

SQLite и CSV находятся в `artifacts/optuna/`; повторный запуск продолжает study.
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
    path = Path(project_root).resolve() / "notebooks/mlp-tuning/01_optuna_mlp.ipynb"
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
