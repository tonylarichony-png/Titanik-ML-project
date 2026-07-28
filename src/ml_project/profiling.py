"""Reusable dataframe profiling used by Data and EDA notebooks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class DatasetProfiler:
    """Profile one dataframe without embedding implementation in a notebook."""

    df: pd.DataFrame
    name: str
    key: str | None = None
    target: str | None = None

    def schema_report(self) -> pd.DataFrame:
        """Return structural metadata only; value quality lives in other reports."""
        return pd.DataFrame(
            {
                "field": self.df.columns,
                "dtype": [str(dtype) for dtype in self.df.dtypes],
            }
        )

    def missing_report(self, *, include_zero: bool = False) -> pd.DataFrame:
        """Return missing counts and shares, already filtered when requested."""
        report = pd.DataFrame(
            {
                "dataset": self.name,
                "field": self.df.columns,
                "missing": self.df.isna().sum().to_numpy(),
                "missing_share": self.df.isna().mean().to_numpy(),
            }
        )
        if not include_zero:
            report = report[report["missing"] > 0]
        return report.sort_values(
            ["missing_share", "field"],
            ascending=[False, True],
        ).reset_index(drop=True)

    def duplicate_report(self) -> pd.DataFrame:
        """Return full-row and configured-key duplicate checks."""
        key_exists = self.key is not None and self.key in self.df.columns
        return pd.DataFrame(
            [
                {
                    "dataset": self.name,
                    "rows": len(self.df),
                    "full_row_duplicates": int(self.df.duplicated().sum()),
                    "key": self.key or "not configured",
                    "key_missing": (
                        int(self.df[self.key].isna().sum()) if key_exists else np.nan
                    ),
                    "key_duplicates": (
                        int(self.df[self.key].duplicated().sum())
                        if key_exists
                        else np.nan
                    ),
                    "key_unique": (
                        bool(self.df[self.key].is_unique) if key_exists else np.nan
                    ),
                }
            ]
        )

    def target_report(self) -> pd.DataFrame:
        """Return counts and shares for the configured target."""
        if self.target is None:
            raise ValueError(f"Target is not configured for dataset {self.name!r}.")
        if self.target not in self.df.columns:
            raise KeyError(
                f"Target {self.target!r} is absent from dataset {self.name!r}."
            )

        counts = self.df[self.target].value_counts(dropna=False).sort_index()
        report = counts.rename("count").to_frame()
        report["share"] = report["count"] / len(self.df)
        report.index = report.index.map(lambda value: "<NA>" if pd.isna(value) else value)
        report.index.name = self.target
        return report.reset_index()

    def numeric_report(self) -> pd.DataFrame:
        """Return descriptive statistics for numeric columns."""
        columns = self.df.select_dtypes(include="number").columns.tolist()
        if not columns:
            return pd.DataFrame()
        return self.df[columns].describe().T.reset_index(names="field")

    def categorical_report(self, *, max_unique: int = 30) -> pd.DataFrame:
        """Return compact cardinality and mode information."""
        columns = [
            column
            for column in self.df.columns
            if self.df[column].nunique(dropna=True) <= max_unique
            and column != self.target
        ]
        rows: list[dict[str, object]] = []
        for column in columns:
            mode = self.df[column].mode(dropna=True)
            counts = self.df[column].value_counts(dropna=True)
            rows.append(
                {
                    "field": column,
                    "unique": int(self.df[column].nunique(dropna=True)),
                    "most_frequent": mode.iloc[0] if not mode.empty else np.nan,
                    "frequency": int(counts.iloc[0]) if not counts.empty else 0,
                }
            )
        return pd.DataFrame(rows)

    def plot_target(self):
        """Plot the configured target distribution."""
        import seaborn as sns

        if self.target is None or self.target not in self.df.columns:
            raise KeyError(f"Configured target is unavailable in {self.name!r}.")
        axis = sns.countplot(data=self.df, x=self.target)
        axis.set(
            title=f"Target distribution — {self.name}",
            ylabel="Rows",
        )
        return axis

    def plot_numeric_histograms(self, *, bins: int = 25):
        """Plot numeric features, excluding configured key and target."""
        import matplotlib.pyplot as plt

        excluded = {value for value in (self.key, self.target) if value}
        columns = [
            column
            for column in self.df.select_dtypes(include="number").columns
            if column not in excluded
        ]
        if not columns:
            return None
        axes = self.df[columns].hist(figsize=(12, 8), bins=bins)
        plt.suptitle(f"Numeric distributions — {self.name}", y=1.02)
        plt.tight_layout()
        return axes

    @staticmethod
    def compare_missing(*profiles: "DatasetProfiler") -> pd.DataFrame:
        """Compare missing-value shares across multiple datasets."""
        if not profiles:
            return pd.DataFrame()
        series = {
            profile.name: profile.df.isna().mean()
            for profile in profiles
        }
        report = pd.DataFrame(series).fillna(0)
        report = report[(report > 0).any(axis=1)]
        report.index.name = "field"
        return report.reset_index()
