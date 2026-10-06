"""Generate the reproducible notebook for one versioned MLP experiment."""

from __future__ import annotations

import json
import re
from pathlib import Path


ID_PATTERN = re.compile(r"MLP-\d{3,}")
SLUG_PATTERN = re.compile(r"[a-z][a-z0-9_]*")


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


def notebook_path(project_root: Path, experiment_id: str, slug: str) -> Path:
    """Построить путь к notebook выбранного MLP-эксперимента."""
    normalized_id = experiment_id.upper()
    normalized_slug = slug.lower().replace("-", "_")
    if not ID_PATTERN.fullmatch(normalized_id):
        raise ValueError("experiment_id must look like MLP-001")
    if not SLUG_PATTERN.fullmatch(normalized_slug):
        raise ValueError("slug must contain lowercase letters, digits, underscores")
    return (
        Path(project_root).resolve()
        / "notebooks/mlp-experiments"
        / f"{normalized_id}_{normalized_slug}.ipynb"
    )


def build_notebook(
    experiment_id: str,
    title: str,
    slug: str,
    module_name: str,
) -> dict[str, object]:
    """Собрать содержимое воспроизводимого Jupyter notebook."""
    cells = [
        _markdown(
            "mlp-top",
            f"""# {experiment_id} — {title}

Воспроизводимый PyTorch MLP-эксперимент. Источник истины — модуль
`{module_name}`: в нём редактируются признаки, типы заполнения пропусков,
гиперпараметры и архитектура. Этот notebook загружает модуль, проверяет контракт,
выполняет честный внешний CV и сохраняет OOF-результаты.

Рабочий цикл: **одна гипотеза → изменение модуля → Restart Kernel → Run All → вывод**.

Внешний validation fold никогда не участвует в preprocessing, early stopping или
выборе эпохи. Внутри каждого outer train fold создаётся свой inner validation split.
""",
        ),
        _markdown(
            "mlp-edit-md",
            f"""## 1. Что редактировать

Открой `src/ml_project/mlp_experiments/{module_name.rsplit('.', 1)[-1]}.py`.

- `prepare_features(frame)` — только признаки, вычисляемые отдельно для каждой строки.
- `build_fold_transformer()` — обучаемые групповые признаки и статистики train fold.
- `numeric_features` и `categorical_features` — явные роли всех входов.
- `MLPTrainingConfig` — imputation, scaling, batch size, learning rate, epochs.
- `build_network(input_dim)` — любое строение на `nn.Module`, выдающее один логит на строку.

Если новый признак использует статистику нескольких строк — среднее, частоту,
группировку, target encoding — его нельзя заранее считать на всей таблице.
Создавайте его через `build_fold_transformer`: runtime отдельно вызовет `fit`
на train fold и `transform` на validation/test.
""",
        ),
        _code(
            "mlp-setup",
            f"""from pathlib import Path
import importlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.metrics import ConfusionMatrixDisplay

CURRENT_DIR = Path.cwd().resolve()
PROJECT_ROOT = next(
    p for p in (CURRENT_DIR, *CURRENT_DIR.parents)
    if (p / "README.md").is_file() and (p / "src").is_dir()
)
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ml_project import DataCatalog
import ml_project.config as project_config
import ml_project.mlp_experiment as mlp_tools

EXPERIMENT_MODULE = {module_name!r}
mlp_tools = importlib.reload(mlp_tools)
experiment_module = mlp_tools.load_mlp_experiment(EXPERIMENT_MODULE)
spec = experiment_module.EXPERIMENT

print("Project:", PROJECT_ROOT)
print("Experiment:", spec.experiment_id, spec.title)
print("Module:", EXPERIMENT_MODULE)
print("Hypothesis:", spec.hypothesis)
print("Controlled change:", spec.change_description)
print("Reference:", spec.parent_mlp_module or spec.sklearn_reference_module or "logistic baseline")
display(pd.Series(vars(spec.training), name="value").to_frame())
""",
        ),
        _markdown(
            "mlp-data-md",
            """## 2. Данные и feature contract

`prepare_features` вызывается отдельно для train и inference. Исходные таблицы
должны остаться неизменными, порядок строк, key и target сохраняются.
Заполнение пропусков и one-hot здесь ещё не выполняются — они fit-ятся внутри folds.
""",
        ),
        _code(
            "mlp-data",
            """catalog = DataCatalog(PROJECT_ROOT, project_config.RAW_DIR, project_config.DATASETS)
catalog.validate()
raw_train = catalog.load(project_config.TRAIN_DATASET)
raw_test = catalog.load(project_config.INFERENCE_DATASET)
train_snapshot = raw_train.copy(deep=True)
test_snapshot = raw_test.copy(deep=True)

prepared = experiment_module.prepare_features(raw_train.copy(deep=True))
prepared_test = experiment_module.prepare_features(raw_test.copy(deep=True))
pd.testing.assert_frame_equal(raw_train, train_snapshot)
pd.testing.assert_frame_equal(raw_test, test_snapshot)
mlp_tools.validate_feature_data(
    prepared, raw_train, target=project_config.TARGET, key=project_config.KEY,
)

if project_config.TARGET in prepared_test.frame:
    raise ValueError("Inference data must not acquire target")
if not prepared_test.frame.index.equals(raw_test.index):
    raise ValueError("prepare_features changed inference row index/order")
if prepared.numeric_features != prepared_test.numeric_features:
    raise ValueError("Train/test numeric feature declarations differ")
if prepared.categorical_features != prepared_test.categorical_features:
    raise ValueError("Train/test categorical feature declarations differ")
missing_test = [
    name for name in prepared.features
    if name not in prepared_test.frame and name not in prepared.fold_generated_features
]
if missing_test:
    raise KeyError(f"Inference is missing features: {missing_test}")

feature_report = pd.DataFrame({
    "role": ["numeric"] * len(prepared.numeric_features)
            + ["categorical"] * len(prepared.categorical_features),
    "feature": list(prepared.features),
}).set_index("feature")
train_feature_view = prepared.frame.reindex(columns=list(prepared.features))
test_feature_view = prepared_test.frame.reindex(columns=list(prepared.features))
feature_report["dtype"] = train_feature_view.dtypes.astype(str)
feature_report["missing_train"] = train_feature_view.isna().sum()
feature_report["missing_test"] = test_feature_view.isna().sum()
display(feature_report)
display(
    prepared.frame.reindex(
        columns=[project_config.KEY, *prepared.features, project_config.TARGET]
    ).head()
)
""",
        ),
        _markdown(
            "mlp-preview-md",
            """## 3. Preview preprocessing и сети

Preview нужен для формы и количества параметров. Официальные метрики ниже заново
создают и fit-ят preprocessing только на train-части каждого fold.
""",
        ),
        _code(
            "mlp-preview",
            """preview_transformer_builder = getattr(experiment_module, "build_fold_transformer", None)
preview_transformer = preview_transformer_builder() if preview_transformer_builder else None
preview_frame = prepared.frame.copy(deep=True)
if preview_transformer is not None:
    preview_transformer.fit(preview_frame)
    preview_frame = preview_transformer.transform(preview_frame)
preview_preprocessor = mlp_tools.build_preprocessor(prepared, spec.training)
preview_x = preview_preprocessor.fit_transform(
    preview_frame.loc[:, list(prepared.features)]
)
input_dim = preview_x.shape[1]
preview_model = experiment_module.build_network(input_dim)
parameter_count = sum(p.numel() for p in preview_model.parameters() if p.requires_grad)
print("Raw features:", len(prepared.features))
print("Inputs after preprocessing:", input_dim)
print("Trainable parameters:", parameter_count)
print(preview_model)
""",
        ),
        _markdown(
            "mlp-cv-md",
            """## 4. Outer CV

Каждый outer fold создаёт новый preprocessor и новую сеть. Внутри outer-train
выделяется inner validation только для early stopping. OOF-предсказание каждой
строки сделано моделью, которая эту строку не видела.
""",
        ),
        _code(
            "mlp-cv",
            """result = mlp_tools.run_mlp_cv(
    prepared,
    target=project_config.TARGET,
    key=project_config.KEY,
    build_network=experiment_module.build_network,
    spec=spec,
    build_fold_transformer=getattr(experiment_module, "build_fold_transformer", None),
)
display(result.fold_metrics.round(4))
display(result.summary.round(4))
print("Encoded input dimensions by fold:", result.input_dims)
""",
        ),
        _code(
            "mlp-curves",
            """figure = mlp_tools.plot_training_histories(result)
display(figure)
plt.close(figure)
""",
        ),
        _markdown(
            "mlp-reference-md",
            """## 5. Reference champion и paired-сравнение

Reference заново обучается на тех же outer folds. Для первого MLP это последний
принятый sklearn-чемпион; для следующих опытов — последний MLP с
`decision: adopt`. Положительный `improvement` всегда означает улучшение,
включая `log_loss`, где меньше — лучше.
""",
        ),
        _code(
            "mlp-reference",
            """if spec.parent_mlp_module:
    reference = mlp_tools.run_mlp_parent_reference(
        raw_train,
        module_name=spec.parent_mlp_module,
        target=project_config.TARGET,
        key=project_config.KEY,
        cv_splits=result.cv_splits,
    )
else:
    reference = mlp_tools.run_sklearn_champion_reference(
        PROJECT_ROOT,
        raw_train,
        module_name=spec.sklearn_reference_module,
        target=project_config.TARGET,
        key=project_config.KEY,
        feature_groups=project_config.FEATURE_GROUPS,
        cv_splits=result.cv_splits,
    )

comparison = mlp_tools.compare_mlp_with_reference(result, reference, spec)
display(comparison.summary.round(4))
display(comparison.criteria.round(4))
display(
    comparison.paired_deltas[
        comparison.paired_deltas["metric"].eq(spec.primary_metric)
    ].round(4)
)
""",
        ),
        _code(
            "mlp-oof",
            """oof = result.oof_predictions
ConfusionMatrixDisplay.from_predictions(
    oof["target"], oof["prediction"], labels=[0, 1],
    display_labels=["Not survived", "Survived"], cmap="Blues", colorbar=False,
)
plt.title(f"{spec.experiment_id}: OOF confusion matrix")
plt.tight_layout()
plt.show()

analysis = raw_train[[project_config.KEY, "Sex", "Pclass", "Name"]].merge(
    oof, on=project_config.KEY, validate="one_to_one"
)
segment_metrics = analysis.groupby("Sex", observed=True).apply(
    lambda part: pd.Series({
        "rows": len(part),
        "accuracy": (part["target"] == part["prediction"]).mean(),
        "mean_probability": part["probability"].mean(),
    }),
    include_groups=False,
)
display(segment_metrics)
display(
    analysis.assign(confidence=lambda x: np.maximum(x.probability, 1-x.probability))
    .query("target != prediction")
    .sort_values("confidence", ascending=False)
    .head(15)
)

candidate_oof = result.oof_predictions.set_index(project_config.KEY)
reference_oof = reference.oof_predictions.set_index(project_config.KEY)
error_changes = candidate_oof[["target", "prediction", "probability"]].join(
    reference_oof[["prediction", "probability"]].rename(columns={
        "prediction": "reference_prediction",
        "probability": "reference_probability",
    }),
    validate="one_to_one",
)
print("Исправлено ошибок reference:", int((
    (error_changes.prediction == error_changes.target)
    & (error_changes.reference_prediction != error_changes.target)
).sum()))
print("Добавлено новых ошибок:", int((
    (error_changes.prediction != error_changes.target)
    & (error_changes.reference_prediction == error_changes.target)
).sum()))
""",
        ),
        _markdown(
            "mlp-conclusion-md",
            """## 6. Вывод до финального fit

- Гипотеза подтвердилась / не подтвердилась: …
- Основная OOF-метрика, paired Δ и fold wins/losses: …
- Что видно по train curves: …
- Ошибки по мужчинам и женщинам: …
- Единственное изменение следующего эксперимента: …

Не подбирайте архитектуру по Kaggle test: там нет target. Новый набор признаков,
imputer, hidden layer, dropout или learning rate оформляйте новым `MLP-xxx`.
""",
        ),
        _markdown(
            "mlp-save-md",
            """## 7. Сохранить результат и Obsidian-карточку

Сохраняются fold metrics, OOF, paired Δ, история эпох и hashes. Затем создаются
карточка `mlp-experiments/MLP-xxx ...md`, CSV-реестр, индекс и блок в README.
Ручной анализ карточки и поле `decision` при перезапуске сохраняются.
""",
        ),
        _code(
            "mlp-save",
            """run_dir = None
if spec.save_artifacts:
    dataset_path = catalog.path(project_config.TRAIN_DATASET)
    run_dir = mlp_tools.save_mlp_run(
        PROJECT_ROOT, experiment_module, prepared, result,
        target=project_config.TARGET, key=project_config.KEY,
        dataset_path=dataset_path,
        comparison=comparison,
    )
    print("Artifacts:", run_dir.relative_to(PROJECT_ROOT))
    if spec.sync_docs:
        note_path = mlp_tools.sync_mlp_report(
            PROJECT_ROOT,
            experiment_module,
            prepared,
            result,
            comparison,
            run_dir,
            dataset_path=dataset_path,
        )
        print("Obsidian card:", note_path.relative_to(PROJECT_ROOT))
else:
    print("Artifact saving is disabled in EXPERIMENT.")
""",
        ),
        _markdown(
            "mlp-final-md",
            """## 8. Финальная модель и Kaggle preview

Финальная сеть обучается на всей размеченной таблице; внутри неё остаётся inner
split для выбора эпохи. Это отдельный fit после оценки CV. `SAVE_FINAL_MODEL`
управляет записью весов, preprocessor и CSV. Сначала изучите CV и только затем
включайте сохранение.
""",
        ),
        _code(
            "mlp-final",
            """SAVE_FINAL_MODEL = False

if SAVE_FINAL_MODEL:
    if run_dir is None:
        raise RuntimeError("Enable spec.save_artifacts before final model saving")
    final_model = mlp_tools.fit_final_mlp(
        prepared,
        target=project_config.TARGET,
        build_network=experiment_module.build_network,
        spec=spec,
        build_fold_transformer=getattr(experiment_module, "build_fold_transformer", None),
    )
    test_probability = mlp_tools.predict_prepared_mlp(final_model, prepared_test)
    submission = pd.DataFrame({
        project_config.KEY: prepared_test.frame[project_config.KEY].to_numpy(),
        project_config.TARGET: (
            test_probability >= spec.training.threshold
        ).astype("int64"),
    })
    if len(submission) != len(raw_test) or not submission[project_config.KEY].equals(raw_test[project_config.KEY]):
        raise ValueError("Submission row/key contract failed")
    mlp_tools.save_final_mlp(run_dir, final_model)
    submission.to_csv(run_dir / "submission.csv", index=False)
    pd.DataFrame({
        project_config.KEY: prepared_test.frame[project_config.KEY],
        "probability": test_probability,
    }).to_csv(run_dir / "test_probabilities.csv", index=False)
    display(submission.head())
    print("Final model and submission saved to:", run_dir.relative_to(PROJECT_ROOT))
else:
    print("Final fit is disabled. Set SAVE_FINAL_MODEL = True after accepting CV result.")
""",
        ),
        _markdown(
            "mlp-next-md",
            """## 9. Решение и следующий эксперимент

После анализа измените в карточке только `decision:` на `adopt`, `reject`,
`iterate` или `inconclusive`, затем выполните:

```powershell
.\\sync-MLPexperiment-state.cmd
```

Из корня проекта:

```powershell
.\\new-MLPexperiment.cmd
```

Команда создаст следующий `MLP-xxx`, отдельный модуль и notebook. Старый модуль
после измеренного запуска не редактируйте: он фиксирует точное определение опыта.
""",
        ),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python (titanik-ml)",
                "language": "python",
                "name": "titanik-ml",
            },
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def create_notebook(
    project_root: Path,
    experiment_id: str,
    title: str,
    *,
    slug: str,
    module_name: str,
    overwrite: bool = False,
) -> Path:
    """Создать воспроизводимый Jupyter notebook на диске."""
    path = notebook_path(project_root, experiment_id, slug)
    if path.exists() and not overwrite:
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            build_notebook(experiment_id, title, slug, module_name),
            ensure_ascii=False,
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


__all__ = ["build_notebook", "create_notebook", "notebook_path"]
