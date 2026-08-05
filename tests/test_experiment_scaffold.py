from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ml_project.experiment_scaffold import (
    find_next_experiment_id,
    main,
    parse_guardrails,
    scaffold_experiment,
    slug_from_title,
)


class ExperimentScaffoldTests(unittest.TestCase):
    def test_interactive_preview_can_be_cancelled_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            answers = ["Тест признака", "", "", "", "n"]
            with (
                patch("ml_project.experiment_scaffold.sys.stdin") as stdin,
                patch("builtins.input", side_effect=answers),
            ):
                stdin.isatty.return_value = True
                result = main(["--project-root", str(root)])

            self.assertEqual(result, 0)
            self.assertFalse((root / "src").exists())

    def test_next_id_slug_and_guardrail_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src/ml_project/experiments"
            package.mkdir(parents=True)
            (package / "exp_002_existing.py").write_text(
                'experiment_id = "EXP-002"\n',
                encoding="utf-8",
            )

            self.assertEqual(find_next_experiment_id(root), "EXP-003")
            self.assertEqual(
                slug_from_title("Возраст по титулу"),
                "vozrast_po_titulu",
            )
            self.assertEqual(
                parse_guardrails("Recall=-0.005, F1=-0.002"),
                {"Recall": -0.005, "F1": -0.002},
            )

    def test_scaffold_creates_immutable_module_and_selects_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src/ml_project/experiments"
            package.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            selector = root / "src/ml_project/experiment_config.py"
            selector.write_text(
                'EXPERIMENT_MODULE = "ml_project.experiments.old"\n',
                encoding="utf-8",
            )

            path, module_name = scaffold_experiment(
                root,
                "EXP-003",
                "Title feature",
                slug="title_feature",
                primary_improvement_min=0.01,
                metric_guardrails={"Recall": -0.005},
            )

            self.assertEqual(path.name, "exp_003_title_feature.py")
            self.assertEqual(
                module_name,
                "ml_project.experiments.exp_003_title_feature",
            )
            source = path.read_text(encoding="utf-8")
            self.assertIn("experiment_id='EXP-003'", source)
            self.assertIn("primary_improvement_min=0.01", source)
            self.assertIn("metric_guardrails={'Recall': -0.005}", source)
            self.assertIn("prepare_candidate_data", source)
            self.assertIn("build_candidate_models", source)
            self.assertIn(
                module_name,
                selector.read_text(encoding="utf-8"),
            )

            with self.assertRaises(FileExistsError):
                scaffold_experiment(
                    root,
                    "EXP-003",
                    "Duplicate",
                    slug="another_slug",
                )


if __name__ == "__main__":
    unittest.main()
