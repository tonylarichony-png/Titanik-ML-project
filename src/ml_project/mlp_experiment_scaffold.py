"""Create a versioned PyTorch MLP experiment module and notebook."""

from __future__ import annotations

import argparse
import ast
import re
import sys
import textwrap
from pathlib import Path

try:
    from .experiment_scaffold import find_adopted_champion_module, slug_from_title
    from .mlp_experiment_notebook import create_notebook, notebook_path
except ImportError:
    from experiment_scaffold import find_adopted_champion_module, slug_from_title
    from mlp_experiment_notebook import create_notebook, notebook_path


ID_PATTERN = re.compile(r"MLP-\d{3,}")
SLUG_PATTERN = re.compile(r"[a-z][a-z0-9_]*")


def find_next_id(project_root: Path) -> str:
    """Найти следующий свободный идентификатор MLP-эксперимента."""
    package = Path(project_root) / "src/ml_project/mlp_experiments"
    numbers = [0]
    if package.exists():
        for path in package.glob("mlp_*.py"):
            match = re.search(
                r'''(?m)^\s*experiment_id\s*=\s*["']MLP-(\d+)["']''',
                path.read_text(encoding="utf-8"),
            )
            if match:
                numbers.append(int(match.group(1)))
    return f"MLP-{max(numbers) + 1:03d}"


def find_adopted_mlp_module(project_root: Path) -> str | None:
    """Return the latest MLP module whose Obsidian card says decision: adopt."""

    adopted: list[tuple[int, str]] = []
    for path in (Path(project_root) / "mlp-experiments").glob("MLP-*.md"):
        text = path.read_text(encoding="utf-8")
        id_match = re.search(r"(?m)^id:\s*MLP-(\d+)\s*$", text)
        decision = re.search(r"(?m)^decision:\s*adopt\s*$", text)
        module = re.search(r"(?m)^implementation_module:\s*([^\s]+)\s*$", text)
        if id_match and decision and module:
            adopted.append((int(id_match.group(1)), module.group(1)))
    return max(adopted)[1] if adopted else None


def _prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def module_source(
    experiment_id: str,
    title: str,
    *,
    parent_mlp_module: str | None,
    sklearn_reference_module: str | None,
) -> str:
    """Сформировать исходный код нового MLP-эксперимента."""
    note_title = re.sub(r"[^A-Za-z0-9А-Яа-яЁё _-]+", "", title).strip()
    return textwrap.dedent(
        f'''\
        """{experiment_id}: {title}."""

        from __future__ import annotations

        from pathlib import Path

        import pandas as pd
        from sklearn.base import BaseEstimator, TransformerMixin
        from torch import nn

        from ml_project.mlp_experiment import (
            MLPExperimentSpec,
            MLPFeatureData,
            MLPTrainingConfig,
        )


        EXPERIMENT = MLPExperimentSpec(
            experiment_id={experiment_id!r},
            title={title!r},
            hypothesis="CHANGE ME — if ..., then ..., because ...",
            change_description="CHANGE ME — exactly one controlled change",
            experiment_note=Path("mlp-experiments/{experiment_id} {note_title}.md"),
            n_splits=5,
            primary_metric="accuracy",
            primary_improvement_min=0.0,
            metric_guardrails={{
                "balanced_accuracy": 0.0,
                "recall": -0.01,
                "f1": 0.0,
            }},
            parent_mlp_module={parent_mlp_module!r},
            sklearn_reference_module={sklearn_reference_module!r},
            save_artifacts=True,
            sync_docs=True,
            training=MLPTrainingConfig(
                # Fold-safe preprocessing. Change one choice per experiment.
                numeric_imputer="median",       # mean | median | most_frequent
                categorical_imputer="most_frequent",  # most_frequent | constant
                numeric_scaler="standard",      # standard | none

                # Optimization.
                batch_size=32,
                learning_rate=1e-3,
                weight_decay=0.0,
                max_epochs=100,
                patience=12,
                min_delta=1e-4,
                inner_validation_fraction=0.15,
                threshold=0.5,
                random_state=42,
                device="cpu",
            ),
        )


        def prepare_features(frame: pd.DataFrame) -> MLPFeatureData:
            """Create row-local features and declare their preprocessing roles."""

            result = frame.copy(deep=True)

            # EDIT HERE — deterministic row-local feature engineering.
            # Examples:
            # result["FamilySize"] = result["SibSp"] + result["Parch"] + 1
            # result["IsAlone"] = (result["FamilySize"] == 1).astype("int64")
            # result["Title"] = result["Name"].str.extract(r",\\s*([^.]*)\\.", expand=False)

            numeric_features = (
                "Age",
                "Fare",
                "SibSp",
                "Parch",
                # "FamilySize",
            )
            categorical_features = (
                "Sex",
                "Embarked",
                "Pclass",
                # "IsAlone",
                # "Title",
            )
            return MLPFeatureData(
                frame=result,
                numeric_features=numeric_features,
                categorical_features=categorical_features,
                # Признаки, которые создаст build_fold_transformer:
                fold_generated_features=(),
            )


        def build_fold_transformer():
            """Return a fresh fitted-per-fold transformer, or None."""

            # EDIT HERE для признаков, которым нужны статистики других строк.
            # Transformer должен реализовать fit(DataFrame) и transform(DataFrame),
            # вернуть DataFrame с тем же index и создать все признаки из
            # fold_generated_features. Пример TicketGroupSize:
            #
            # class TicketGroupSize(BaseEstimator, TransformerMixin):
            #     def fit(self, frame, y=None):
            #         self.counts_ = frame["Ticket"].value_counts().to_dict()
            #         return self
            #     def transform(self, frame):
            #         result = frame.copy(deep=True)
            #         result["TicketGroupSize"] = (
            #             result["Ticket"].map(self.counts_).fillna(1).astype("int64")
            #         )
            #         return result
            # return TicketGroupSize()
            return None


        def build_network(input_dim: int) -> nn.Module:
            """Return one fresh network that emits one raw logit per passenger."""

            # EDIT HERE — add/remove hidden layers, activations or Dropout.
            # Keep input_dim on the first Linear and one output on the last Linear.
            return nn.Sequential(
                nn.Linear(input_dim, 32),
                nn.ReLU(),
                nn.Linear(32, 1),
            )


        __all__ = [
            "EXPERIMENT",
            "build_fold_transformer",
            "build_network",
            "prepare_features",
        ]
        '''
    )


def module_source_from_parent(
    project_root: Path,
    parent_module: str,
    experiment_id: str,
    title: str,
) -> str:
    """Copy an adopted MLP implementation and reset only the child contract."""

    root = Path(project_root).resolve()
    parent_path = root / "src" / (parent_module.replace(".", "/") + ".py")
    if not parent_path.is_file():
        raise FileNotFoundError(f"Adopted MLP module not found: {parent_path}")
    source = parent_path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(parent_path))
    experiment_call = None
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "EXPERIMENT"
                for target in node.targets
            )
            and isinstance(node.value, ast.Call)
        ):
            experiment_call = node.value
            break
    if experiment_call is None:
        raise ValueError(f"Cannot find EXPERIMENT assignment in {parent_path}")

    note_title = re.sub(r"[^A-Za-z0-9А-Яа-яЁё _-]+", "", title).strip()
    values = {
        "experiment_id": repr(experiment_id),
        "title": repr(title),
        "hypothesis": repr("CHANGE ME — if ..., then ..., because ..."),
        "change_description": repr("CHANGE ME — exactly one controlled change"),
        "experiment_note": (
            f"Path({f'mlp-experiments/{experiment_id} {note_title}.md'!r})"
        ),
        "parent_mlp_module": repr(parent_module),
        "sklearn_reference_module": "None",
    }
    keywords = {
        keyword.arg: keyword
        for keyword in experiment_call.keywords
        if keyword.arg is not None
    }
    missing = sorted(set(values).difference(keywords))
    if missing:
        raise ValueError(
            f"Adopted MLP contract is missing fields required for cloning: {missing}"
        )

    lines = source.splitlines(keepends=True)
    replacements: list[tuple[int, int, str]] = []
    for name, value in values.items():
        keyword = keywords[name]
        start = keyword.lineno - 1
        end = keyword.end_lineno
        indent = re.match(r"\s*", lines[start]).group(0)
        replacements.append((start, end, f"{indent}{name}={value},\n"))

    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        doc = tree.body[0]
        replacements.append(
            (
                doc.lineno - 1,
                doc.end_lineno,
                f'"""{experiment_id}: {title}."""\n',
            )
        )

    for start, end, replacement in sorted(replacements, reverse=True):
        lines[start:end] = [replacement]
    return "".join(lines)


def scaffold(
    project_root: Path,
    experiment_id: str,
    title: str,
    *,
    slug: str,
) -> tuple[Path, Path, str]:
    """Создать versioned-модуль и связанный notebook эксперимента."""
    root = Path(project_root).resolve()
    normalized_id = experiment_id.upper()
    normalized_slug = slug.lower().replace("-", "_")
    if not ID_PATTERN.fullmatch(normalized_id):
        raise ValueError("experiment_id must look like MLP-001")
    if not SLUG_PATTERN.fullmatch(normalized_slug):
        raise ValueError("slug must contain lowercase letters, digits, underscores")
    if not title.strip():
        raise ValueError("title cannot be empty")
    package = root / "src/ml_project/mlp_experiments"
    package.mkdir(parents=True, exist_ok=True)
    init = package / "__init__.py"
    if not init.exists():
        init.write_text('"""Versioned PyTorch MLP experiments."""\n', encoding="utf-8")
    stem = f"mlp_{normalized_id.split('-')[1]}_{normalized_slug}"
    module_path = package / f"{stem}.py"
    planned_notebook = notebook_path(root, normalized_id, normalized_slug)
    if module_path.exists() or planned_notebook.exists():
        existing = module_path if module_path.exists() else planned_notebook
        raise FileExistsError(existing)
    for existing in package.glob("mlp_*.py"):
        if re.search(
            rf'''(?m)^\s*experiment_id\s*=\s*["']{re.escape(normalized_id)}["']''',
            existing.read_text(encoding="utf-8"),
        ):
            raise FileExistsError(f"{normalized_id} already exists in {existing}")
    parent_mlp_module = find_adopted_mlp_module(root)
    sklearn_reference_module = (
        None if parent_mlp_module else find_adopted_champion_module(root)
    )
    source = (
        module_source_from_parent(
            root,
            parent_mlp_module,
            normalized_id,
            title.strip(),
        )
        if parent_mlp_module
        else module_source(
            normalized_id,
            title.strip(),
            parent_mlp_module=None,
            sklearn_reference_module=sklearn_reference_module,
        )
    )
    module_path.write_text(
        source,
        encoding="utf-8",
    )
    module_name = f"ml_project.mlp_experiments.{stem}"
    notebook = create_notebook(
        root,
        normalized_id,
        title.strip(),
        slug=normalized_slug,
        module_name=module_name,
    )
    return module_path, notebook, module_name


def main(argv: list[str] | None = None) -> int:
    """Запустить команду модуля из командной строки."""
    parser = argparse.ArgumentParser(
        description="Create a reproducible PyTorch MLP experiment and notebook."
    )
    parser.add_argument("experiment_id", nargs="?", help="Example: MLP-001")
    parser.add_argument("--title")
    parser.add_argument("--slug")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    interactive = args.experiment_id is None or args.title is None or args.slug is None
    if interactive and not sys.stdin.isatty():
        parser.error("provide experiment_id, --title and --slug in non-interactive mode")
    experiment_id = args.experiment_id or find_next_id(root)
    title = args.title or _prompt("Название MLP-эксперимента")
    slug = args.slug or _prompt("Техническое имя", slug_from_title(title))
    if interactive:
        print("\nБудет создан MLP-эксперимент:")
        print("  ID:", experiment_id)
        print("  Название:", title)
        print("  Модуль: src/ml_project/mlp_experiments/")
        print("  Notebook: notebooks/mlp-experiments/")
        if not args.yes:
            answer = input("Создать? [y/N]: ").strip().casefold()
            if answer not in {"y", "yes", "д", "да"}:
                print("Отменено: файлы не изменены.")
                return 0
    try:
        module_path, notebook, module_name = scaffold(
            root, experiment_id, title, slug=slug
        )
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    print("Created module:", module_path)
    print("Created notebook:", notebook)
    print("Module name:", module_name)
    adopted_parent = find_adopted_mlp_module(root)
    if adopted_parent:
        print("Copied implementation from adopted MLP:", adopted_parent)
        print("Comparison reference:", adopted_parent)
    else:
        print("Copied implementation from: clean MLP template")
        print("Reference: adopted sklearn champion", find_adopted_champion_module(root) or "baseline")
    print("Next: edit the module, then Restart Kernel and Run All in the notebook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
