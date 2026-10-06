from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from ml_project.mlp_experiment import (
    MLPExperimentSpec,
    MLPFeatureData,
    MLPTrainingConfig,
    build_preprocessor,
    fit_mlp,
    run_mlp_cv,
    validate_feature_data,
    validate_training_config,
)
from ml_project.mlp_experiment_scaffold import find_next_id, scaffold
from ml_project.mlp_tuning import (
    BASELINE_PARAMETERS,
    PHASE2_BASELINE_PARAMETERS,
    build_network_factory,
    build_phase2_network_factory,
    training_from_parameters,
)


class MLPScaffoldTests(unittest.TestCase):
    def test_scaffold_creates_versioned_module_and_bound_notebook(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            module, notebook, module_name = scaffold(
                root, "MLP-001", "Small net", slug="small_net"
            )
            self.assertTrue(module.is_file())
            self.assertTrue(notebook.is_file())
            self.assertEqual(
                module_name,
                "ml_project.mlp_experiments.mlp_001_small_net",
            )
            self.assertIn(module_name, notebook.read_text(encoding="utf-8"))
            self.assertIn("def prepare_features", module.read_text(encoding="utf-8"))
            self.assertEqual(find_next_id(root), "MLP-002")
            with self.assertRaises(FileExistsError):
                scaffold(root, "MLP-001", "Duplicate", slug="duplicate")

    def test_scaffold_copies_latest_adopted_mlp_implementation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src/ml_project/mlp_experiments"
            package.mkdir(parents=True)
            parent = package / "mlp_007_parent.py"
            parent.write_text(
                '"""MLP-007: Parent."""\n\n'
                "from pathlib import Path\n\n"
                "EXPERIMENT = MLPExperimentSpec(\n"
                "    experiment_id='MLP-007',\n"
                "    title='Parent',\n"
                "    hypothesis='old hypothesis',\n"
                "    change_description='old change',\n"
                "    experiment_note=Path('mlp-experiments/MLP-007 Parent.md'),\n"
                "    parent_mlp_module=None,\n"
                "    sklearn_reference_module='old.sklearn',\n"
                ")\n\n"
                "CUSTOM_FEATURE_MARKER = 'copied from champion'\n\n"
                "def build_network(input_dim):\n"
                "    return ('hidden', input_dim, 7)\n",
                encoding="utf-8-sig",
            )
            cards = root / "mlp-experiments"
            cards.mkdir()
            (cards / "MLP-007 Parent.md").write_text(
                "---\n"
                "id: MLP-007\n"
                "decision: adopt\n"
                "implementation_module: ml_project.mlp_experiments.mlp_007_parent\n"
                "---\n",
                encoding="utf-8",
            )

            module, notebook, _ = scaffold(
                root,
                "MLP-008",
                "Child experiment",
                slug="child_experiment",
            )
            source = module.read_text(encoding="utf-8")

            self.assertTrue(notebook.is_file())
            self.assertIn("CUSTOM_FEATURE_MARKER = 'copied from champion'", source)
            self.assertIn("return ('hidden', input_dim, 7)", source)
            self.assertIn("experiment_id='MLP-008'", source)
            self.assertIn("title='Child experiment'", source)
            self.assertIn(
                "parent_mlp_module='ml_project.mlp_experiments.mlp_007_parent'",
                source,
            )
            self.assertIn("sklearn_reference_module=None", source)
            self.assertIn("CHANGE ME — exactly one controlled change", source)
            self.assertNotIn("hypothesis='old hypothesis'", source)


class MLPTuningTests(unittest.TestCase):
    def test_baseline_parameters_reproduce_mlp_024_shape(self) -> None:
        from torch import nn

        model = build_network_factory(BASELINE_PARAMETERS)(12)
        linear_layers = [layer for layer in model if isinstance(layer, nn.Linear)]
        dropout_layers = [layer for layer in model if isinstance(layer, nn.Dropout)]

        self.assertEqual(
            [(layer.in_features, layer.out_features) for layer in linear_layers],
            [(12, 16), (16, 16), (16, 16), (16, 1)],
        )
        self.assertEqual(len(dropout_layers), 1)
        self.assertAlmostEqual(dropout_layers[0].p, 0.2)

    def test_trial_parameters_only_replace_optimizer_settings(self) -> None:
        base = MLPTrainingConfig(max_epochs=77, patience=9, min_delta=1e-5)
        tuned = training_from_parameters(base, BASELINE_PARAMETERS)

        self.assertEqual(tuned.batch_size, 32)
        self.assertEqual(tuned.learning_rate, 1e-3)
        self.assertEqual(tuned.weight_decay, 0.0)
        self.assertEqual(tuned.max_epochs, 77)
        self.assertEqual(tuned.patience, 9)
        self.assertEqual(tuned.min_delta, 1e-5)

    def test_phase2_baseline_builds_four_layer_relu_network(self) -> None:
        from torch import nn

        model = build_phase2_network_factory(PHASE2_BASELINE_PARAMETERS)(12)
        linear_layers = [layer for layer in model if isinstance(layer, nn.Linear)]
        activations = [layer for layer in model if isinstance(layer, nn.ReLU)]

        self.assertEqual(
            [(layer.in_features, layer.out_features) for layer in linear_layers],
            [(12, 8), (8, 8), (8, 8), (8, 8), (8, 1)],
        )
        self.assertEqual(len(activations), 4)

    def test_phase2_builds_requested_activation_per_hidden_layer(self) -> None:
        from torch import nn

        parameters = {
            **PHASE2_BASELINE_PARAMETERS,
            "n_layers": 3,
            "activation": "leaky_relu",
            "negative_slope": 0.05,
        }
        model = build_phase2_network_factory(parameters)(12)
        activations = [
            layer for layer in model if isinstance(layer, nn.LeakyReLU)
        ]

        self.assertEqual(len(activations), 3)
        self.assertTrue(
            all(layer.negative_slope == 0.05 for layer in activations)
        )


class MLPSchedulerTests(unittest.TestCase):
    def test_cosine_scheduler_steps_once_per_epoch(self) -> None:
        from torch import nn

        rng = np.random.default_rng(19)
        x = rng.normal(size=(80, 3)).astype("float32")
        y = np.tile(np.array([0, 1], dtype="int64"), 40)
        config = MLPTrainingConfig(
            batch_size=8,
            learning_rate=1e-3,
            max_epochs=4,
            patience=10,
            scheduler="cosine",
            scheduler_eta_min=1e-5,
            random_state=7,
        )

        fitted = fit_mlp(
            x,
            y,
            build_network=lambda input_dim: nn.Sequential(
                nn.Linear(input_dim, 4),
                nn.ReLU(),
                nn.Linear(4, 1),
            ),
            config=config,
            seed=7,
        )

        expected = np.array(
            [
                config.scheduler_eta_min
                + 0.5
                * (config.learning_rate - config.scheduler_eta_min)
                * (1 + np.cos(np.pi * step / config.max_epochs))
                for step in range(config.max_epochs)
            ]
        )
        np.testing.assert_allclose(
            fitted.history["learning_rate"].to_numpy(),
            expected,
            rtol=1e-7,
            atol=1e-12,
        )

    def test_scheduler_settings_are_validated(self) -> None:
        with self.assertRaisesRegex(ValueError, "scheduler must be"):
            validate_training_config(MLPTrainingConfig(scheduler="cosin"))
        with self.assertRaisesRegex(ValueError, "lower than learning_rate"):
            validate_training_config(
                MLPTrainingConfig(
                    scheduler="cosine",
                    learning_rate=1e-3,
                    scheduler_eta_min=1e-3,
                )
            )


class MLPEmbeddingTests(unittest.TestCase):
    def test_ordinal_preprocessor_reserves_minus_one_for_unknown(self) -> None:
        train = pd.DataFrame(
            {
                "number": [1.0, 2.0, 3.0],
                "category": ["a", "b", "a"],
            }
        )
        prepared = MLPFeatureData(
            frame=train,
            numeric_features=("number",),
            categorical_features=("category",),
        )
        config = MLPTrainingConfig(
            numeric_scaler="none",
            categorical_encoding="ordinal",
        )
        preprocessor = build_preprocessor(prepared, config)
        preprocessor.fit(train)

        transformed = preprocessor.transform(
            pd.DataFrame({"number": [4.0], "category": ["unseen"]})
        )

        self.assertEqual(transformed.shape, (1, 2))
        self.assertEqual(float(transformed[0, 1]), -1.0)

    def test_titanic_embedding_network_emits_one_logit_per_row(self) -> None:
        import torch

        from ml_project.mlp_experiments.mlp_045_embeddings import build_network

        model = build_network(9)
        values = torch.zeros((7, 9), dtype=torch.float32)
        logits = model(values)

        self.assertEqual(tuple(logits.shape), (7,))
        self.assertEqual(len(model.embeddings), 6)


class MLPRuntimeTests(unittest.TestCase):
    def test_outer_cv_produces_one_oof_prediction_per_row(self) -> None:
        from torch import nn
        from sklearn.base import BaseEstimator, TransformerMixin

        rng = np.random.default_rng(7)
        rows = 90
        frame = pd.DataFrame(
            {
                "id": np.arange(rows),
                "value": rng.normal(size=rows),
                "category": np.where(np.arange(rows) % 2, "a", "b"),
            }
        )
        frame.loc[::11, "value"] = np.nan
        frame["target"] = (
            frame["value"].fillna(0).to_numpy() + (frame["category"] == "a") * 0.5 > 0
        ).astype("int64")
        prepared = MLPFeatureData(
            frame,
            ("value", "category_frequency"),
            ("category",),
            ("category_frequency",),
        )
        validate_feature_data(prepared, frame, target="target", key="id")

        class CategoryFrequency(BaseEstimator, TransformerMixin):
            def fit(self, values, y=None):
                self.frequencies_ = values["category"].value_counts().to_dict()
                return self

            def transform(self, values):
                result = values.copy(deep=True)
                result["category_frequency"] = (
                    result["category"].map(self.frequencies_).fillna(0)
                )
                return result

        def build_network(input_dim: int):
            return nn.Sequential(nn.Linear(input_dim, 4), nn.ReLU(), nn.Linear(4, 1))

        spec = MLPExperimentSpec(
            experiment_id="MLP-999",
            title="test",
            hypothesis="test",
            change_description="test",
            n_splits=3,
            save_artifacts=False,
            training=MLPTrainingConfig(
                max_epochs=4,
                patience=2,
                batch_size=16,
                random_state=3,
            ),
        )
        result = run_mlp_cv(
            prepared,
            target="target",
            key="id",
            build_network=build_network,
            spec=spec,
            build_fold_transformer=CategoryFrequency,
        )
        self.assertEqual(len(result.fold_metrics), 3)
        self.assertEqual(len(result.oof_predictions), rows)
        self.assertTrue(result.oof_predictions["probability"].between(0, 1).all())
        self.assertEqual(result.oof_predictions["id"].nunique(), rows)
        self.assertEqual(set(result.oof_predictions["fold"]), {1, 2, 3})


if __name__ == "__main__":
    unittest.main()
