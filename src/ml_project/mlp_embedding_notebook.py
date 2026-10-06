"""Generate the dedicated categorical-embedding experiment notebook."""

from __future__ import annotations

import json
from pathlib import Path

from .mlp_experiment_notebook import build_notebook


MODULE_NAME = "ml_project.mlp_experiments.mlp_045_embeddings"


def _replace_source(notebook: dict[str, object], cell_id: str, source: str) -> None:
    for cell in notebook["cells"]:
        if cell["id"] == cell_id:
            cell["source"] = source.splitlines(keepends=True)
            if cell["cell_type"] == "code":
                cell["execution_count"] = None
                cell["outputs"] = []
            return
    raise KeyError(f"Notebook cell not found: {cell_id}")


def build_embedding_notebook() -> dict[str, object]:
    """Собрать notebook для эксперимента с категориальными embeddings."""
    notebook = build_notebook(
        "MLP-045",
        "Embeddings",
        "embeddings",
        MODULE_NAME,
    )
    _replace_source(
        notebook,
        "mlp-top",
        """# MLP-045 — embeddings категориальных признаков

Этот эксперимент сравнивает принятую **MLP-024** с той же скрытой сетью, но
заменяет one-hot представление всех шести категориальных признаков на обучаемые
`nn.Embedding`.

Путь данных внутри каждого fold:

`train категории → OrdinalEncoder → индексы → nn.Embedding → объединение с числами → MLP`.

Словари категорий fit-ятся только на train-части fold. Индекс `0` зарезервирован
для категории, которая не встречалась при fit. `test.csv` не участвует в CV.
""",
    )
    _replace_source(
        notebook,
        "mlp-edit-md",
        f"""## 1. Контролируемое изменение

Источник истины: `src/ml_project/mlp_experiments/mlp_045_embeddings.py`.

В эксперименте зафиксированы признаки и скрытая часть MLP-024. Изменяется способ
представления категорий:

- `Embarked`: embedding dimension 2;
- `FamilySizeGroup`: embedding dimension 3;
- `IsnotAlone`: embedding dimension 1;
- `CabinKnown`: embedding dimension 1;
- `Deck`: embedding dimension 3;
- `SexPclass`: embedding dimension 3.

Даже бинарные `IsnotAlone` и `CabinKnown` проходят через embedding, чтобы
единственным изменением относительно MLP-024 была замена one-hot механизма.
Не создавайте словари категорий вручную по всей таблице: их строит fold-fitted
`OrdinalEncoder`.
""",
    )
    _replace_source(
        notebook,
        "mlp-data-md",
        """## 2. Данные и роли признаков

Числовые признаки заполняются и масштабируются внутри fold. Категориальные
признаки там же получают целочисленные индексы. Неизвестная validation/test
категория кодируется как `-1`, после чего модель сдвигает её в специальный
embedding-индекс `0`.
""",
    )
    _replace_source(
        notebook,
        "mlp-preview-md",
        """## 3. Preview индексов и embedding-слоёв

Эта диагностическая ячейка показывает изученные категории, их индексы, размеры
embedding-таблиц и форму входа. Официальный CV ниже создаёт всё заново отдельно
для каждого train fold.
""",
    )
    _replace_source(
        notebook,
        "mlp-preview",
        """preview_transformer_builder = getattr(
    experiment_module, "build_fold_transformer", None
)
preview_transformer = (
    preview_transformer_builder() if preview_transformer_builder else None
)
preview_frame = prepared.frame.copy(deep=True)
if preview_transformer is not None:
    preview_transformer.fit(preview_frame)
    preview_frame = preview_transformer.transform(preview_frame)

preview_preprocessor = mlp_tools.build_preprocessor(prepared, spec.training)
preview_x = np.asarray(
    preview_preprocessor.fit_transform(
        preview_frame.loc[:, list(prepared.features)]
    ),
    dtype=np.float32,
)
input_dim = preview_x.shape[1]
preview_model = experiment_module.build_network(input_dim)

ordinal_encoder = (
    preview_preprocessor.named_transformers_["categorical"]
    .named_steps["encoder"]
)
mapping_rows = []
for feature, categories in zip(
    prepared.categorical_features,
    ordinal_encoder.categories_,
    strict=True,
):
    mapping_rows.append({
        "feature": feature,
        "unknown_index": 0,
        "known_categories": list(categories),
        "model_indices": list(range(1, len(categories) + 1)),
    })
display(pd.DataFrame(mapping_rows))

parameter_count = sum(
    parameter.numel()
    for parameter in preview_model.parameters()
    if parameter.requires_grad
)
print("Numeric columns:", prepared.numeric_features)
print("Embedded columns:", prepared.categorical_features)
print("Preprocessed columns:", input_dim)
print("Combined numeric + embedding width:", 16)
print("Trainable parameters:", parameter_count)
print(preview_model)

with torch.no_grad():
    sample_logits = preview_model(
        torch.tensor(preview_x[:5], dtype=torch.float32)
    )
print("Five preview logits:", sample_logits.tolist())
""",
    )
    setup = next(cell for cell in notebook["cells"] if cell["id"] == "mlp-setup")
    setup_source = "".join(setup["source"])
    setup_source = setup_source.replace(
        "import pandas as pd\n",
        "import pandas as pd\nimport torch\n",
    )
    _replace_source(notebook, "mlp-setup", setup_source)
    _replace_source(
        notebook,
        "mlp-conclusion-md",
        """## 6. Вывод до сохранения

Запишите:

- победила ли MLP-045 по accuracy и guardrails;
- сколько folds она выиграла у MLP-024;
- исправленные и добавленные OOF-ошибки;
- поведение train/inner-validation loss;
- оправдалось ли обучение плотных представлений на категориях размером 3–8.

Не оценивайте embeddings по Kaggle test: у него нет target.
""",
    )
    return notebook


def create_notebook(project_root: Path) -> Path:
    """Создать воспроизводимый Jupyter notebook на диске."""
    path = (
        Path(project_root).resolve()
        / "notebooks/mlp-experiments/MLP-045_embeddings.ipynb"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_embedding_notebook(), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> int:
    """Запустить команду модуля из командной строки."""
    print("Created:", create_notebook(Path.cwd()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
