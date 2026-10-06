"""Focused tests for automatic ensemble weighting."""

from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from ml_project.ensemble_experiment import SPEC_003, _learn_simplex_weights
from ml_project.ensemble_submission import _submission_frame


class EnsembleWeightTests(unittest.TestCase):
    def test_simplex_optimizer_prefers_better_probabilities(self) -> None:
        target = np.array([0, 0, 1, 1], dtype="int64")
        probabilities = np.column_stack(
            [
                np.array([0.05, 0.10, 0.90, 0.95]),
                np.array([0.90, 0.80, 0.20, 0.10]),
            ]
        )

        weights = _learn_simplex_weights(probabilities, target)

        self.assertAlmostEqual(float(weights.sum()), 1.0, places=8)
        self.assertTrue((weights >= 0).all())
        self.assertGreater(weights[0], 0.99)

    def test_ens003_uses_four_requested_members(self) -> None:
        self.assertEqual(
            SPEC_003.members,
            ("xgboost", "lightgbm", "catboost", "mlp_024"),
        )
        self.assertEqual(SPEC_003.inner_n_splits, 4)

    def test_submission_frame_aligns_predictions_by_passenger_id(self) -> None:
        inference = pd.DataFrame({"PassengerId": [20, 10]})
        sample = pd.DataFrame({"PassengerId": [10, 20], "Survived": [0, 0]})

        result = _submission_frame(inference, sample, np.array([1, 0]))

        self.assertEqual(result["PassengerId"].tolist(), [10, 20])
        self.assertEqual(result["Survived"].tolist(), [0, 1])


if __name__ == "__main__":
    unittest.main()
