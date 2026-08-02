"""Project-specific sklearn transformers used by model pipelines.

Keep fitted statistics inside transformer instances so cross-validation learns
them only from each train fold. Transformers in this module must not mutate the
input frame.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

try:
    from sklearn.base import BaseEstimator, TransformerMixin
    from sklearn.utils.validation import check_is_fitted
except ImportError as error:  # pragma: no cover - environment dependent
    raise ImportError(
        "ml_project.transformers requires scikit-learn. Install project "
        "dependencies with: python -m pip install -r requirements.txt"
    ) from error


class AgeByTitlePclassImputer(BaseEstimator, TransformerMixin):
    """Fill missing ages using Title × Pclass, Title and global fallbacks.

    The three statistics are learned in ``fit``. Therefore the transformer must
    be placed before the ``ColumnTransformer`` inside the full sklearn Pipeline;
    fitting it on the complete dataset before cross-validation would leak
    validation-fold information.

    Parameters
    ----------
    age_column:
        Numeric column whose missing values are filled.
    title_column:
        Grouping column with a person's title or another age-related category.
    class_column:
        Second grouping column, normally a service/class category.
    """

    def __init__(
        self,
        age_column: str = "Age",
        title_column: str = "Title",
        class_column: str = "Pclass",
    ) -> None:
        self.age_column = age_column
        self.title_column = title_column
        self.class_column = class_column

    @property
    def required_columns(self) -> tuple[str, str, str]:
        return self.age_column, self.title_column, self.class_column

    def _validate_frame(self, X: Any) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError(
                "AgeByTitlePclassImputer expects a pandas DataFrame and must "
                "run before ColumnTransformer converts the data."
            )
        missing = sorted(set(self.required_columns).difference(X.columns))
        if missing:
            raise KeyError(f"Отсутствуют столбцы: {missing}")
        return X

    def fit(self, X: pd.DataFrame, y: Any = None) -> "AgeByTitlePclassImputer":
        frame = self._validate_frame(X)
        known_age = frame.loc[
            frame[self.age_column].notna(), list(self.required_columns)
        ]
        if known_age.empty:
            raise ValueError("Нет известных значений Age для обучения imputer.")

        self.group_medians_ = known_age.groupby(
            [self.title_column, self.class_column], observed=True
        )[self.age_column].median()
        self.title_medians_ = known_age.groupby(
            self.title_column, observed=True
        )[self.age_column].median()
        self.global_median_ = float(known_age[self.age_column].median())
        self.feature_names_in_ = np.asarray(frame.columns, dtype=object)
        self.n_features_in_ = frame.shape[1]
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(
            self,
            [
                "group_medians_",
                "title_medians_",
                "global_median_",
                "feature_names_in_",
            ],
        )
        frame = self._validate_frame(X)
        transformed = frame.copy()
        missing_age = transformed[self.age_column].isna()
        if not missing_age.any():
            return transformed

        missing_rows = transformed.loc[
            missing_age, [self.title_column, self.class_column]
        ]
        group_keys = pd.MultiIndex.from_frame(missing_rows)
        group_fill = pd.Series(
            self.group_medians_.reindex(group_keys).to_numpy(),
            index=missing_rows.index,
            dtype=float,
        )
        title_fill = missing_rows[self.title_column].map(self.title_medians_)
        fill_values = group_fill.fillna(title_fill).fillna(self.global_median_)
        transformed.loc[missing_age, self.age_column] = fill_values
        return transformed

    def get_feature_names_out(self, input_features: Any = None) -> np.ndarray:
        """Report unchanged output columns for sklearn pipeline introspection."""

        check_is_fitted(self, "feature_names_in_")
        if input_features is None:
            return self.feature_names_in_.copy()
        features = np.asarray(input_features, dtype=object)
        if len(features) != self.n_features_in_:
            raise ValueError(
                f"Expected {self.n_features_in_} feature names, got {len(features)}"
            )
        return features


__all__ = ["AgeByTitlePclassImputer"]
