from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from ml_project.transformers import AgeByTitlePclassImputer

try:
    from sklearn.base import clone
except ImportError:  # pragma: no cover - local dependency state
    SKLEARN_AVAILABLE = False
else:
    SKLEARN_AVAILABLE = True


@unittest.skipUnless(SKLEARN_AVAILABLE, "scikit-learn is not installed")
class AgeByTitlePclassImputerTests(unittest.TestCase):
    def training_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Age": [20.0, 40.0, 50.0, 30.0, np.nan, np.nan, np.nan],
                "Title": ["Mr", "Mr", "Mr", "Mrs", "Mr", "Mr", "Dr"],
                "Pclass": [1, 1, 2, 1, 1, 3, 3],
                "Other": range(7),
            }
        )

    def test_hierarchical_fallbacks_and_input_immutability(self) -> None:
        frame = self.training_frame()
        original = frame.copy(deep=True)

        transformed = AgeByTitlePclassImputer().fit_transform(frame)

        # Exact Mr × class 1 median.
        self.assertEqual(transformed.loc[4, "Age"], 30.0)
        # Unseen Mr × class 3 falls back to the Mr median.
        self.assertAlmostEqual(transformed.loc[5, "Age"], 40.0)
        # Unseen title falls back to the global median.
        self.assertEqual(transformed.loc[6, "Age"], 35.0)
        pd.testing.assert_frame_equal(frame, original)
        self.assertEqual(list(transformed.columns), list(frame.columns))

    def test_estimator_is_cloneable_and_reports_unchanged_feature_names(self) -> None:
        transformer = AgeByTitlePclassImputer(
            age_column="age", title_column="title", class_column="class"
        )
        cloned = clone(transformer)
        self.assertEqual(cloned.get_params(), transformer.get_params())

        frame = self.training_frame()
        fitted = AgeByTitlePclassImputer().fit(frame)
        self.assertEqual(
            fitted.get_feature_names_out().tolist(), frame.columns.tolist()
        )

    def test_clear_errors_for_wrong_input_and_missing_training_age(self) -> None:
        with self.assertRaisesRegex(TypeError, "pandas DataFrame"):
            AgeByTitlePclassImputer().fit(np.zeros((3, 3)))
        with self.assertRaisesRegex(KeyError, "Title"):
            AgeByTitlePclassImputer().fit(
                pd.DataFrame({"Age": [20.0], "Pclass": [1]})
            )
        with self.assertRaisesRegex(ValueError, "Нет известных значений Age"):
            AgeByTitlePclassImputer().fit(
                pd.DataFrame(
                    {"Age": [np.nan], "Title": ["Mr"], "Pclass": [1]}
                )
            )


if __name__ == "__main__":
    unittest.main()
