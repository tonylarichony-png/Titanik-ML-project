"""Titanic-only joint train/inference context for notebook experiments.

Модуль намеренно не входит в универсальный шаблон. Он только объединяет
канонические raw train/test и помогает вернуть созданные в notebook признаки
к исходным строкам по PassengerId. Сами формулы признаков остаются внутри
конкретного эксперимента.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd

from . import config as project_config
from .data import DataCatalog


ROLE_COLUMN = "__dataset_role"
ORDER_COLUMN = "__original_order"
TRAIN_ROLE = "train"
INFERENCE_ROLE = "inference"


@dataclass(frozen=True)
class JointData:
    """Объединённые raw train/test с явным источником каждой строки."""

    frame: pd.DataFrame
    key: str
    target: str
    dataset_versions: Mapping[str, str]
    role_column: str = ROLE_COLUMN
    order_column: str = ORDER_COLUMN

    def report(self) -> pd.DataFrame:
        """Показать размер частей и заполненность target после объединения."""

        rows: list[dict[str, object]] = []
        for role, part in self.frame.groupby(self.role_column, sort=False):
            target_known = (
                int(part[self.target].notna().sum())
                if self.target in part
                else 0
            )
            rows.append(
                {
                    "dataset_role": role,
                    "rows": len(part),
                    "unique_keys": int(part[self.key].nunique()),
                    "target_known": target_known,
                    "target_missing": len(part) - target_known,
                }
            )
        return pd.DataFrame(rows)

    def split(
        self,
        frame: pd.DataFrame | None = None,
        *,
        drop_inference_target: bool = True,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Разделить joint-frame обратно, сохранив исходный порядок строк."""

        source = self.frame if frame is None else frame
        return split_joint_frame(
            source,
            target=self.target,
            role_column=self.role_column,
            order_column=self.order_column,
            drop_inference_target=drop_inference_target,
        )


def _validate_input_frames(
    train: pd.DataFrame,
    inference: pd.DataFrame,
    *,
    key: str,
    target: str,
    role_column: str,
    order_column: str,
) -> None:
    if not isinstance(train, pd.DataFrame) or not isinstance(
        inference, pd.DataFrame
    ):
        raise TypeError("train and inference must be pandas DataFrames")
    reserved = {role_column, order_column}
    collisions = sorted(reserved.intersection(train.columns).union(
        reserved.intersection(inference.columns)
    ))
    if collisions:
        raise ValueError(
            "Input frames already contain reserved joint columns: "
            + ", ".join(collisions)
        )
    if key not in train or key not in inference:
        raise KeyError(f"KEY {key!r} must exist in train and inference")
    if target not in train:
        raise KeyError(f"TARGET {target!r} must exist in train")
    if train[key].isna().any() or inference[key].isna().any():
        raise ValueError(f"KEY {key!r} must not contain missing values")
    if train[key].duplicated().any() or inference[key].duplicated().any():
        raise ValueError(f"KEY {key!r} must be unique inside each dataset")
    overlap = pd.Index(train[key]).intersection(pd.Index(inference[key]))
    if len(overlap):
        preview = ", ".join(map(str, overlap[:10]))
        raise ValueError(
            f"Train and inference KEY values overlap: {preview}"
        )
    train_features = set(train.columns).difference({target})
    inference_features = set(inference.columns).difference({target})
    if train_features != inference_features:
        missing_in_inference = sorted(train_features - inference_features)
        missing_in_train = sorted(inference_features - train_features)
        details: list[str] = []
        if missing_in_inference:
            details.append(
                "missing in inference: " + ", ".join(missing_in_inference)
            )
        if missing_in_train:
            details.append("missing in train: " + ", ".join(missing_in_train))
        raise ValueError("Train/inference feature schemas differ; " + "; ".join(details))


def combine_train_inference(
    train: pd.DataFrame,
    inference: pd.DataFrame,
    *,
    key: str,
    target: str,
    dataset_versions: Mapping[str, str] | None = None,
    role_column: str = ROLE_COLUMN,
    order_column: str = ORDER_COLUMN,
) -> JointData:
    """Объединить две выборки без изменения переданных DataFrame."""

    _validate_input_frames(
        train,
        inference,
        key=key,
        target=target,
        role_column=role_column,
        order_column=order_column,
    )
    train_part = train.copy(deep=True)
    inference_part = inference.copy(deep=True)
    train_part[role_column] = TRAIN_ROLE
    inference_part[role_column] = INFERENCE_ROLE
    train_part[order_column] = range(len(train_part))
    inference_part[order_column] = range(len(inference_part))
    combined = pd.concat(
        [train_part, inference_part],
        ignore_index=True,
        sort=False,
    )
    return JointData(
        frame=combined,
        key=key,
        target=target,
        dataset_versions=dict(dataset_versions or {}),
        role_column=role_column,
        order_column=order_column,
    )


def load_joint_data(project_root: str | Path) -> JointData:
    """Загрузить и объединить канонические Titanic train/test из config.py."""

    root = Path(project_root).resolve()
    inference_name = project_config.INFERENCE_DATASET
    if not inference_name:
        raise ValueError("config.INFERENCE_DATASET is required for joint data")
    catalog = DataCatalog(
        root,
        project_config.RAW_DIR,
        project_config.DATASETS,
    )
    catalog.validate()
    if inference_name not in catalog.available_names():
        raise FileNotFoundError(catalog.path(inference_name))
    train = catalog.load(project_config.TRAIN_DATASET)
    inference = catalog.load(inference_name)
    file_report = catalog.file_report().set_index("dataset")
    versions = {
        TRAIN_ROLE: str(
            file_report.loc[project_config.TRAIN_DATASET, "sha256"]
        ),
        INFERENCE_ROLE: str(file_report.loc[inference_name, "sha256"]),
    }
    return combine_train_inference(
        train,
        inference,
        key=project_config.KEY,
        target=project_config.TARGET,
        dataset_versions=versions,
    )


def split_joint_frame(
    frame: pd.DataFrame,
    *,
    target: str,
    role_column: str = ROLE_COLUMN,
    order_column: str = ORDER_COLUMN,
    drop_inference_target: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Разделить произвольную featured-копию joint-frame по явной роли."""

    missing = [
        column
        for column in (role_column, order_column)
        if column not in frame
    ]
    if missing:
        raise KeyError("Joint frame lacks service columns: " + ", ".join(missing))
    roles = set(frame[role_column].dropna().astype(str))
    expected_roles = {TRAIN_ROLE, INFERENCE_ROLE}
    if roles != expected_roles:
        raise ValueError(
            "Joint frame roles must be exactly: "
            + ", ".join(sorted(expected_roles))
        )

    def select(role: str) -> pd.DataFrame:
        selected = (
            frame.loc[frame[role_column].eq(role)]
            .sort_values(order_column, kind="stable")
            .drop(columns=[role_column, order_column])
            .reset_index(drop=True)
        )
        return selected

    train = select(TRAIN_ROLE)
    inference = select(INFERENCE_ROLE)
    if drop_inference_target and target in inference:
        inference = inference.drop(columns=target)
    return train, inference


def align_joint_features(
    base_frame: pd.DataFrame,
    featured_joint: pd.DataFrame,
    *,
    features: Iterable[str],
    key: str = project_config.KEY,
) -> pd.DataFrame:
    """Добавить выбранные joint-признаки в текущий frame по стабильному KEY."""

    feature_names = tuple(features)
    if not feature_names:
        raise ValueError("features must contain at least one column")
    if len(set(feature_names)) != len(feature_names):
        raise ValueError("features contains duplicate column names")
    if key not in base_frame or key not in featured_joint:
        raise KeyError(f"KEY {key!r} must exist in both frames")
    if base_frame[key].duplicated().any():
        raise ValueError(f"Base frame KEY {key!r} must be unique")
    if featured_joint[key].duplicated().any():
        raise ValueError(f"Joint frame KEY {key!r} must be globally unique")
    missing_features = [
        feature for feature in feature_names if feature not in featured_joint
    ]
    if missing_features:
        raise KeyError(
            "Joint frame lacks requested features: "
            + ", ".join(missing_features)
        )
    lookup = featured_joint.set_index(key, drop=False)
    missing_keys = pd.Index(base_frame[key]).difference(lookup.index)
    if len(missing_keys):
        preview = ", ".join(map(str, missing_keys[:10]))
        raise KeyError(f"Base frame contains keys absent from joint data: {preview}")

    aligned = lookup.loc[base_frame[key], list(feature_names)]
    result = base_frame.copy(deep=True)
    for feature in feature_names:
        result[feature] = pd.Series(
            aligned[feature].array,
            index=result.index,
            name=feature,
        )
    return result


__all__ = [
    "INFERENCE_ROLE",
    "JointData",
    "ORDER_COLUMN",
    "ROLE_COLUMN",
    "TRAIN_ROLE",
    "align_joint_features",
    "combine_train_inference",
    "load_joint_data",
    "split_joint_frame",
]
