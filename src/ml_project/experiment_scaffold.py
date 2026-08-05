"""Create and select a versioned experiment module."""

from __future__ import annotations

import argparse
import math
import re
import sys
import textwrap
from pathlib import Path
from typing import Mapping


EXPERIMENT_ID_PATTERN = re.compile(r"EXP-\d{3,}")
SLUG_PATTERN = re.compile(r"[a-z][a-z0-9_]*")
CYRILLIC_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def find_next_experiment_id(project_root: Path) -> str:
    """Return the next free EXP ID declared by versioned experiment modules."""

    package_dir = Path(project_root).resolve() / "src/ml_project/experiments"
    numbers = [1]
    if package_dir.exists():
        for module_path in package_dir.glob("exp_*.py"):
            source = module_path.read_text(encoding="utf-8")
            match = re.search(
                r'''(?m)^\s*experiment_id\s*=\s*["']EXP-(\d+)["']''',
                source,
            )
            if match:
                numbers.append(int(match.group(1)))
    return f"EXP-{max(numbers) + 1:03d}"


def slug_from_title(title: str) -> str:
    """Build a readable Python slug from Latin or Russian text."""

    transliterated = "".join(
        CYRILLIC_TO_LATIN.get(character, character)
        for character in title.casefold()
    )
    slug = re.sub(r"[^a-z0-9]+", "_", transliterated).strip("_")
    if not slug or not slug[0].isalpha():
        slug = f"experiment_{slug}".rstrip("_")
    return slug


def parse_guardrails(value: str) -> dict[str, float]:
    """Parse ``Metric=min_delta`` pairs separated by commas."""

    if not value.strip():
        return {}
    result: dict[str, float] = {}
    for item in value.split(","):
        if "=" not in item:
            raise ValueError(
                "Guardrails must look like Recall=-0.005, F1=-0.002"
            )
        metric, raw_threshold = item.rsplit("=", 1)
        metric = metric.strip()
        if not metric:
            raise ValueError("Guardrail metric cannot be empty")
        try:
            threshold = float(raw_threshold.strip())
        except ValueError as error:
            raise ValueError(
                f"Guardrail threshold for {metric!r} must be a number"
            ) from error
        if not math.isfinite(threshold):
            raise ValueError(
                f"Guardrail threshold for {metric!r} must be finite"
            )
        if metric in result:
            raise ValueError(f"Duplicate guardrail metric: {metric!r}")
        result[metric] = threshold
    return result


def _prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def _confirmed() -> bool:
    answer = input("Создать эксперимент? [y/N]: ").strip().casefold()
    return answer in {"y", "yes", "д", "да"}


def _module_source(
    experiment_id: str,
    title: str,
    slug: str,
    primary_improvement_min: float,
    metric_guardrails: Mapping[str, float],
) -> str:
    module_run = experiment_id.lower().replace("-", "_")
    note_title = slug.replace("_", " ").title()
    return textwrap.dedent(
        f'''\
        """{experiment_id}: {title}."""

        from __future__ import annotations

        import copy
        from pathlib import Path
        from typing import Any, Mapping

        import pandas as pd

        from ml_project.modeling import (
            BaselineSettings,
            ExperimentData,
            ExperimentSettings,
        )


        EXPERIMENT = ExperimentSettings(
            experiment_id={experiment_id!r},
            experiment_title={title!r},
            experiment_note=Path(
                "experiments/{experiment_id} {note_title}.md"
            ),
            hypothesis="CHANGE ME — if ..., then ..., because ...",
            change_description="CHANGE ME — exactly one controlled change",
            success_criterion=(
                "Primary improvement >= {primary_improvement_min:+.4f}; "
                "add explicit metric guardrails below."
            ),
            primary_improvement_min={primary_improvement_min!r},
            metric_guardrails={dict(metric_guardrails)!r},
            reference_model="baseline_reference",
            primary_candidate="candidate",
            experiment_parameters={{
                # "important_parameter": "...",
            }},
            decision="pending",
            run_name="{module_run}_v1",
            artifact_dir=Path("artifacts/experiments"),
            results_registry=Path("experiments/results.csv"),
            save_artifacts=True,
            save_metric_figures=True,
            metric_figure_dpi=160,
            save_final_model=False,
            sync_experiment_note=True,
            sync_docs=True,
            allow_overwrite=True,
        )


        def prepare_candidate_data(
            train: pd.DataFrame,
            feature_groups: Mapping[str, Any],
            baseline_settings: BaselineSettings,
        ) -> ExperimentData:
            """Create candidate data without mutating baseline raw features."""

            frame = train.copy(deep=True)
            groups = copy.deepcopy(feature_groups)

            # CHANGE ME — add deterministic raw features here. Statistics learned
            # from data must live inside a transformer in build_candidate_models.

            return ExperimentData(
                frame=frame,
                feature_groups=groups,
                settings=baseline_settings,
                diagnostics={{}},
            )


        def build_candidate_models(
            preprocessor: Any,
            candidate_settings: BaselineSettings,
            experiment_settings: ExperimentSettings,
        ) -> dict[str, Any]:
            """Return candidates keyed by experiment_settings.primary_candidate."""

            raise NotImplementedError(
                "CHANGE ME — build one sklearn-compatible candidate Pipeline"
            )


        __all__ = [
            "EXPERIMENT",
            "build_candidate_models",
            "prepare_candidate_data",
        ]
        '''
    )


def scaffold_experiment(
    project_root: Path,
    experiment_id: str,
    title: str,
    *,
    slug: str,
    primary_improvement_min: float = 0.0,
    metric_guardrails: Mapping[str, float] | None = None,
    select: bool = True,
) -> tuple[Path, str]:
    """Create one experiment module and optionally select it for the notebook."""

    root = Path(project_root).resolve()
    normalized_id = experiment_id.upper()
    normalized_slug = slug.lower().replace("-", "_")
    if not EXPERIMENT_ID_PATTERN.fullmatch(normalized_id):
        raise ValueError("experiment_id must look like EXP-003")
    if not SLUG_PATTERN.fullmatch(normalized_slug):
        raise ValueError("slug must contain lowercase letters, digits, underscores")
    if not title.strip():
        raise ValueError("title cannot be empty")
    if not math.isfinite(primary_improvement_min):
        raise ValueError("primary_improvement_min must be finite")
    guardrails = dict(metric_guardrails or {})
    for metric, threshold in guardrails.items():
        if not str(metric).strip():
            raise ValueError("metric_guardrails contains an empty metric")
        if not math.isfinite(float(threshold)):
            raise ValueError(
                f"metric_guardrails[{metric!r}] must be finite"
            )

    package_dir = (root / "src/ml_project/experiments").resolve()
    package_dir.relative_to(root)
    package_dir.mkdir(parents=True, exist_ok=True)
    module_stem = f"{normalized_id.lower().replace('-', '_')}_{normalized_slug}"
    module_path = package_dir / f"{module_stem}.py"
    if module_path.exists():
        raise FileExistsError(f"Experiment module already exists: {module_path}")

    for existing in package_dir.glob("exp_*.py"):
        if re.search(
            rf'''(?m)^\s*experiment_id\s*=\s*["']{re.escape(normalized_id)}["']''',
            existing.read_text(encoding="utf-8"),
        ):
            raise FileExistsError(
                f"{normalized_id} is already declared in {existing.name}"
            )

    selector_path = root / "src/ml_project/experiment_config.py"
    selector = ""
    selector_pattern = re.compile(
        r'(?m)^EXPERIMENT_MODULE\s*=\s*["\'][^"\']+["\']\s*$'
    )
    if select:
        selector = selector_path.read_text(encoding="utf-8")
        if not selector_pattern.search(selector):
            raise ValueError(
                f"Cannot find EXPERIMENT_MODULE assignment in {selector_path}"
            )

    module_path.write_text(
        _module_source(
            normalized_id,
            title.strip(),
            normalized_slug,
            float(primary_improvement_min),
            guardrails,
        ),
        encoding="utf-8",
    )
    module_name = f"ml_project.experiments.{module_stem}"

    if select:
        replacement = f'EXPERIMENT_MODULE = "{module_name}"'
        selector_path.write_text(
            selector_pattern.sub(replacement, selector, count=1),
            encoding="utf-8",
        )
    return module_path, module_name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a versioned experiment module and select it."
    )
    parser.add_argument(
        "experiment_id",
        nargs="?",
        help="Stable ID, for example EXP-003; omitted in interactive mode",
    )
    parser.add_argument("--title", help="Human-readable title")
    parser.add_argument("--slug", help="Python-safe short slug")
    parser.add_argument(
        "--min-improvement",
        type=float,
        help="Minimum positive-direction primary delta",
    )
    parser.add_argument(
        "--guardrail",
        action="append",
        default=[],
        help="Metric=min_delta; repeat the option or separate pairs by commas",
    )
    parser.add_argument(
        "--no-select",
        action="store_true",
        help="Create the module without changing experiment_config.py",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root (default: current directory)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation when prompts are used",
    )
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    interactive = (
        args.experiment_id is None
        or args.title is None
        or args.slug is None
        or args.min_improvement is None
    )
    if interactive and not sys.stdin.isatty():
        parser.error(
            "missing arguments in a non-interactive terminal; provide "
            "experiment_id, --title, --slug and --min-improvement"
        )

    experiment_id = args.experiment_id or find_next_experiment_id(root)
    title = args.title or _prompt("Название эксперимента")
    if not title:
        parser.error("title cannot be empty")
    slug = args.slug or _prompt(
        "Техническое имя",
        slug_from_title(title),
    )
    raw_minimum = (
        str(args.min_improvement)
        if args.min_improvement is not None
        else _prompt("Минимальное улучшение основной метрики", "0.0")
    )
    try:
        primary_improvement_min = float(raw_minimum)
    except ValueError:
        parser.error("minimum improvement must be a number")

    guardrail_values = list(args.guardrail)
    if interactive and not guardrail_values:
        prompted = _prompt(
            "Guardrails (например Recall=-0.005, пусто = нет)",
            "",
        )
        if prompted:
            guardrail_values.append(prompted)
    try:
        guardrails = parse_guardrails(",".join(guardrail_values))
    except ValueError as error:
        parser.error(str(error))

    if interactive:
        module_stem = (
            f"{experiment_id.lower().replace('-', '_')}_"
            f"{slug.lower().replace('-', '_')}"
        )
        print("\nБудет создан эксперимент:")
        print(f"  ID: {experiment_id}")
        print(f"  Название: {title}")
        print(f"  Модуль: src/ml_project/experiments/{module_stem}.py")
        print(f"  Минимальное улучшение: {primary_improvement_min:+.4f}")
        print(f"  Guardrails: {guardrails or 'нет'}")
        print(f"  Выбрать для notebook: {not args.no_select}")
        if not args.yes and not _confirmed():
            print("Отменено: файлы не изменены.")
            return 0

    path, module_name = scaffold_experiment(
        root,
        experiment_id,
        title,
        slug=slug,
        primary_improvement_min=primary_improvement_min,
        metric_guardrails=guardrails,
        select=not args.no_select,
    )
    print(f"Created: {path}")
    print(f"Module: {module_name}")
    if not args.no_select:
        print("Selected in: src/ml_project/experiment_config.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
