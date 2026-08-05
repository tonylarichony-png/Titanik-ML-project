from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

import ml_project.baseline_config as baseline_config
import ml_project.experiment_config as experiment_config
from ml_project import baseline as baseline_tools
from ml_project import experiment as experiment_tools

try:
    import matplotlib  # noqa: F401
    import sklearn  # noqa: F401
except ImportError:  # pragma: no cover - local dependency state
    DEPENDENCIES_AVAILABLE = False
else:
    DEPENDENCIES_AVAILABLE = True


FEATURE_GROUPS = {
    "numeric": ["numeric"],
    "count": [],
    "categorical": ["category"],
    "ordinal": [],
    "text": [],
    "datetime": [],
    "identifier": ["id"],
    "ignored": [],
}


def frame() -> pd.DataFrame:
    size = 30
    return pd.DataFrame(
        {
            "id": range(size),
            "numeric": np.linspace(0, 10, size),
            "category": ["a", "b", "c"] * 10,
            "target": [0, 1] * 15,
        }
    )


def configured_baseline():
    settings = baseline_config.BASELINE
    return replace(
        settings,
        task_type="binary_classification",
        model_feature_groups=("numeric", "count", "categorical", "ordinal"),
        include_features=(),
        exclude_features=(),
        secondary_scorers={"F1": "f1"},
        cv_strategy="stratified_kfold",
        n_splits=3,
        n_jobs=1,
        model_name="logistic_regression",
        save_artifacts=False,
        save_metric_figures=False,
        save_final_model=False,
        sync_docs=False,
        sync_experiment_note=False,
    )


def configured_experiment(**changes: object):
    settings = experiment_tools.load_experiment(
        experiment_config.EXPERIMENT_MODULE,
        reload_module=False,
    ).settings
    defaults = {
        "experiment_id": "EXP-002",
        "experiment_title": "Regularization test",
        "experiment_note": Path("experiments/EXP-002 Regularization.md"),
        "hypothesis": "Regularization improves validation accuracy",
        "change_description": "Change only logistic C",
        "success_criterion": "Accuracy improvement is positive",
        "primary_improvement_min": 0.005,
        "metric_guardrails": {},
        "reference_model": "baseline_reference",
        "primary_candidate": "candidate",
        "decision": "pending",
        "run_name": "exp_002_v1",
        "artifact_dir": Path("artifacts/experiments"),
        "results_registry": Path("experiments/results.csv"),
        "save_artifacts": True,
        "save_metric_figures": True,
        "metric_figure_dpi": 100,
        "save_final_model": False,
        "sync_experiment_note": True,
        "sync_docs": True,
        "allow_overwrite": True,
    }
    defaults.update(changes)
    settings = replace(settings, **defaults)
    experiment_tools.validate_settings(settings)
    return settings


class ExperimentDocumentSyncTests(unittest.TestCase):
    def test_registry_refreshes_readme_with_link_and_delta(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "experiments").mkdir()
            (root / "docs/05_experiments.md").write_text(
                "<!-- auto:latest-experiment:start -->\nold\n"
                "<!-- auto:latest-experiment:end -->\n"
                "<!-- auto:experiment-leaderboard:start -->\nold\n"
                "<!-- auto:experiment-leaderboard:end -->\n"
                "<!-- auto:best-measured-result:start -->\nold\n"
                "<!-- auto:best-measured-result:end -->\n",
                encoding="utf-8",
            )
            (root / "experiments/_index.md").write_text(
                "<!-- auto:experiment-registry:start -->\nold\n"
                "<!-- auto:experiment-registry:end -->\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text(
                "<!-- auto:key-results:start -->\nold\n"
                "<!-- auto:key-results:end -->\n",
                encoding="utf-8",
            )
            scoring = baseline_tools.ScoringPlan(
                contract_metric="accuracy",
                scorers={"primary": "accuracy"},
                labels={"primary": "accuracy"},
                directions={"primary": "maximize"},
                negated={"primary": False},
            )
            evaluation = baseline_tools.CVEvaluation(
                fold_scores=pd.DataFrame(
                    [
                        {
                            "model": model,
                            "split": "validation",
                            "fold": fold,
                            "metric_key": "primary",
                            "metric": "accuracy",
                            "direction": "maximize",
                            "value": value,
                        }
                        for model, values in (
                            ("baseline_reference", (0.79, 0.81)),
                            ("candidate", (0.80, 0.82)),
                        )
                        for fold, value in enumerate(values, start=1)
                    ]
                ),
                summary=pd.DataFrame(
                    [
                        {
                            "model": "baseline_reference",
                            "split": "validation",
                            "metric_key": "primary",
                            "metric": "accuracy",
                            "direction": "maximize",
                            "mean": 0.8,
                            "std": 0.02,
                            "min": 0.78,
                            "max": 0.82,
                            "folds": 5,
                        },
                        {
                            "model": "candidate",
                            "split": "validation",
                            "metric_key": "primary",
                            "metric": "accuracy",
                            "direction": "maximize",
                            "mean": 0.81,
                            "std": 0.01,
                            "min": 0.8,
                            "max": 0.82,
                            "folds": 5,
                        },
                    ]
                ),
                raw_results={},
            )
            experiment_tools.sync_experiment_docs(
                root,
                configured_experiment(),
                evaluation,
                scoring,
                dataset_version="abc123",
                baseline_settings=configured_baseline(),
            )

            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("EXP-001 Baseline.md", readme)
            self.assertIn("EXP-002 Regularization.md", readme)
            self.assertIn("+0.0100", readme)
            self.assertIn("pending", readme)
            self.assertIn("Criteria", (root / "docs/05_experiments.md").read_text(encoding="utf-8"))

            run_dir = root / "artifacts/experiments/exp_002_v1"
            saved = baseline_tools.SavedBaselineRun(
                run_dir=run_dir,
                fold_scores_path=run_dir / "cv_fold_scores.csv",
                summary_path=run_dir / "cv_summary.csv",
                metadata_path=run_dir / "metadata.json",
                metric_figure_paths={
                    "primary": (
                        root
                        / "assets/experiments/EXP-002/"
                        "metric-primary-accuracy.png"
                    )
                },
            )
            experiment = configured_experiment()
            experiment_tools.sync_experiment_note(
                root,
                experiment,
                evaluation,
                scoring,
                saved,
                dataset_version="abc123",
                cv_description="2-fold CV",
            )
            note = (root / experiment.experiment_note).read_text(encoding="utf-8")
            self.assertIn(
                "![[assets/experiments/EXP-002/metric-primary-accuracy.png]]",
                note,
            )
            self.assertIn(
                "[[artifacts/experiments/exp_002_v1/cv_summary.csv"
                "|cv_summary.csv]]",
                note,
            )


@unittest.skipUnless(DEPENDENCIES_AVAILABLE, "modeling dependencies unavailable")
class ExperimentTests(unittest.TestCase):
    def test_versioned_experiment_module_has_source_provenance(self) -> None:
        definition = experiment_tools.load_experiment(
            experiment_config.EXPERIMENT_MODULE
        )
        self.assertEqual(definition.settings.experiment_id, "EXP-002")
        self.assertTrue(definition.source_path.is_file())
        self.assertEqual(len(definition.source_sha256), 64)

    def test_structured_success_criteria_are_evaluated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/00_problem.md").write_text(
                "(primary_metric:: accuracy)\n", encoding="utf-8"
            )
            (
                _,
                experiment,
                _,
                _,
                scoring,
                _,
                _,
                evaluation,
            ) = self.build_run(root)
            criteria = experiment_tools.success_criteria_report(
                evaluation,
                scoring,
                replace(
                    experiment,
                    primary_improvement_min=-1.0,
                    metric_guardrails={"F1": -1.0},
                ),
            )
            self.assertEqual(criteria["passed"].tolist(), [True, True])

    def build_run(self, root: Path):
        baseline = configured_baseline()
        experiment = configured_experiment()
        data_frame = frame()
        plan = baseline_tools.resolve_feature_plan(
            data_frame,
            FEATURE_GROUPS,
            target="target",
            key="id",
            settings=baseline,
        )
        reference_data = baseline_tools.prepare_training_data(
            data_frame,
            target="target",
            plan=plan,
            settings=baseline,
        )
        prepared = experiment_tools.prepare_experiment_data(
            reference_data, data_frame.copy(), target="target"
        )
        preprocessor = baseline_tools.build_tabular_preprocessor(baseline, plan)
        reference = baseline_tools.build_model_pipeline(
            preprocessor, baseline_tools.build_simple_estimator(baseline)
        )
        from sklearn.linear_model import LogisticRegression

        candidate = baseline_tools.build_model_pipeline(
            preprocessor, LogisticRegression(C=0.5, max_iter=1000, random_state=42)
        )
        models = {"baseline_reference": reference, "candidate": candidate}
        scoring = baseline_tools.resolve_scoring_plan(root, baseline)
        cv, strategy = baseline_tools.build_cv_splitter(baseline, prepared.y)
        evaluation = baseline_tools.evaluate_models_cv(
            models, prepared, cv=cv, scoring=scoring, settings=baseline
        )
        return (
            baseline,
            experiment,
            plan,
            prepared,
            scoring,
            baseline_tools.cv_protocol_description(baseline, strategy),
            models,
            evaluation,
        )

    def test_changed_raw_reference_feature_is_rejected(self) -> None:
        data_frame = frame()
        baseline = configured_baseline()
        plan = baseline_tools.resolve_feature_plan(
            data_frame, FEATURE_GROUPS, target="target", key="id", settings=baseline
        )
        reference_data = baseline_tools.prepare_training_data(
            data_frame, target="target", plan=plan, settings=baseline
        )
        changed = data_frame.copy()
        changed["numeric"] = changed["numeric"] + 1
        with self.assertRaisesRegex(ValueError, "Do not overwrite"):
            experiment_tools.prepare_experiment_data(
                reference_data, changed, target="target"
            )

    def test_full_experiment_report_registry_and_safe_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "experiments").mkdir()
            (root / "docs/00_problem.md").write_text(
                "(primary_metric:: accuracy)\n", encoding="utf-8"
            )
            (root / "docs/05_experiments.md").write_text(
                "Manual before\n"
                "<!-- auto:latest-experiment:start -->\nold\n"
                "<!-- auto:latest-experiment:end -->\n"
                "<!-- auto:experiment-leaderboard:start -->\nold\n"
                "<!-- auto:experiment-leaderboard:end -->\n"
                "<!-- auto:best-measured-result:start -->\nold\n"
                "<!-- auto:best-measured-result:end -->\n"
                "Manual after\n",
                encoding="utf-8",
            )
            (root / "experiments/_index.md").write_text(
                "<!-- auto:experiment-registry:start -->\nold\n"
                "<!-- auto:experiment-registry:end -->\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text(
                "Manual dashboard\n"
                "<!-- auto:key-results:start -->\nold\n"
                "<!-- auto:key-results:end -->\n",
                encoding="utf-8",
            )
            (
                baseline,
                experiment,
                plan,
                prepared,
                scoring,
                description,
                models,
                evaluation,
            ) = self.build_run(root)
            figures = baseline_tools.build_metric_figures(evaluation, scoring)
            saved = experiment_tools.save_experiment_run(
                root,
                experiment,
                baseline,
                evaluation,
                plan,
                scoring,
                dataset_version="abc123",
                cv_description=description,
                models=models,
                data=prepared,
                metric_figures=figures,
            )
            experiment_tools.sync_experiment_note(
                root,
                experiment,
                evaluation,
                scoring,
                saved,
                dataset_version="abc123",
                cv_description=description,
            )
            experiment_tools.sync_experiment_docs(
                root,
                experiment,
                evaluation,
                scoring,
                dataset_version="abc123",
                baseline_settings=baseline,
            )

            note = (root / experiment.experiment_note).read_text(encoding="utf-8")
            docs = (root / "docs/05_experiments.md").read_text(encoding="utf-8")
            registry = pd.read_csv(root / experiment.results_registry)
            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("![[assets/experiments/EXP-002/metric-primary-accuracy.png]]", note)
            self.assertIn("Δ к reference", note)
            self.assertIn("EXP-002", docs)
            self.assertIn("EXP-001 Baseline.md", readme)
            self.assertIn("EXP-002", readme)
            self.assertIn("Manual before", docs)
            self.assertEqual(len(registry), 1)

            decided = replace(experiment, decision="adopt")
            experiment_tools.sync_experiment_note(
                root,
                decided,
                evaluation,
                scoring,
                saved,
                dataset_version="abc123",
                cv_description=description,
            )
            decided_note = (root / experiment.experiment_note).read_text(
                encoding="utf-8"
            )
            self.assertIn("\ndecision: adopt\n", decided_note)

            # Same run is idempotent and the registry row is upserted, not duplicated.
            experiment_tools.save_experiment_run(
                root,
                experiment,
                baseline,
                evaluation,
                plan,
                scoring,
                dataset_version="abc123",
                cv_description=description,
                models=models,
                data=prepared,
                metric_figures=figures,
            )
            experiment_tools.sync_experiment_docs(
                root,
                experiment,
                evaluation,
                scoring,
                dataset_version="abc123",
                baseline_settings=baseline,
            )
            self.assertEqual(len(pd.read_csv(root / experiment.results_registry)), 1)


if __name__ == "__main__":
    unittest.main()
