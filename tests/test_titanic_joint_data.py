from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from ml_project.titanic_joint_data import (
    INFERENCE_ROLE,
    TRAIN_ROLE,
    align_joint_features,
    combine_train_inference,
    load_joint_data,
)


def train_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "PassengerId": [1, 2],
            "Ticket": ["A", "B"],
            "Fare": [30.0, 10.0],
            "Survived": [1, 0],
        },
        index=[10, 11],
    )


def inference_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "PassengerId": [3, 4],
            "Ticket": ["A", "A"],
            "Fare": [30.0, 30.0],
        },
        index=[20, 21],
    )


class TitanicJointDataTests(unittest.TestCase):
    def test_combine_marks_roles_and_preserves_inputs(self) -> None:
        train = train_frame()
        inference = inference_frame()
        train_snapshot = train.copy(deep=True)
        inference_snapshot = inference.copy(deep=True)

        joint = combine_train_inference(
            train,
            inference,
            key="PassengerId",
            target="Survived",
            dataset_versions={"train": "train-sha", "inference": "test-sha"},
        )

        pd.testing.assert_frame_equal(train, train_snapshot)
        pd.testing.assert_frame_equal(inference, inference_snapshot)
        self.assertEqual(len(joint.frame), 4)
        self.assertEqual(
            joint.frame["__dataset_role"].tolist(),
            [TRAIN_ROLE, TRAIN_ROLE, INFERENCE_ROLE, INFERENCE_ROLE],
        )
        self.assertEqual(joint.frame["__original_order"].tolist(), [0, 1, 0, 1])
        report = joint.report().set_index("dataset_role")
        self.assertEqual(int(report.loc[TRAIN_ROLE, "target_known"]), 2)
        self.assertEqual(int(report.loc[INFERENCE_ROLE, "target_missing"]), 2)

    def test_notebook_features_align_by_passenger_id_and_split_back(self) -> None:
        train = train_frame()
        inference = inference_frame()
        joint = combine_train_inference(
            train,
            inference,
            key="PassengerId",
            target="Survived",
        )
        featured = joint.frame.copy(deep=True)
        featured["TicketGroupSize"] = (
            featured.groupby("Ticket")["Ticket"].transform("size")
        )
        featured["FarePerPerson"] = (
            featured["Fare"] / featured["TicketGroupSize"]
        )

        prepared_train = align_joint_features(
            train,
            featured,
            features=["TicketGroupSize", "FarePerPerson"],
            key="PassengerId",
        )
        prepared_inference = align_joint_features(
            inference,
            featured,
            features=["TicketGroupSize", "FarePerPerson"],
            key="PassengerId",
        )

        self.assertEqual(prepared_train["TicketGroupSize"].tolist(), [3, 1])
        self.assertEqual(prepared_inference["TicketGroupSize"].tolist(), [3, 3])
        self.assertEqual(prepared_train.index.tolist(), [10, 11])
        self.assertEqual(prepared_inference.index.tolist(), [20, 21])

        split_train, split_inference = joint.split(featured)
        self.assertEqual(split_train["PassengerId"].tolist(), [1, 2])
        self.assertEqual(split_inference["PassengerId"].tolist(), [3, 4])
        self.assertNotIn("Survived", split_inference)
        self.assertIn("TicketGroupSize", split_train)

    def test_invalid_keys_and_schema_are_rejected(self) -> None:
        duplicate = inference_frame().copy()
        duplicate["PassengerId"] = [3, 3]
        with self.assertRaisesRegex(ValueError, "must be unique"):
            combine_train_inference(
                train_frame(),
                duplicate,
                key="PassengerId",
                target="Survived",
            )

        wrong_schema = inference_frame().drop(columns="Fare")
        with self.assertRaisesRegex(ValueError, "feature schemas differ"):
            combine_train_inference(
                train_frame(),
                wrong_schema,
                key="PassengerId",
                target="Survived",
            )

    def test_loader_uses_project_config_and_records_both_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "data" / "raw"
            raw.mkdir(parents=True)
            train = train_frame().reset_index(drop=True)
            inference = inference_frame().reset_index(drop=True)
            for column in (
                "Pclass",
                "Name",
                "Sex",
                "Age",
                "SibSp",
                "Parch",
                "Cabin",
                "Embarked",
            ):
                train[column] = 0
                inference[column] = 0
            train.to_csv(raw / "train.csv", index=False)
            inference.to_csv(raw / "test.csv", index=False)

            joint = load_joint_data(root)

            self.assertEqual(len(joint.frame), 4)
            self.assertEqual(len(joint.dataset_versions[TRAIN_ROLE]), 64)
            self.assertEqual(len(joint.dataset_versions[INFERENCE_ROLE]), 64)


if __name__ == "__main__":
    unittest.main()
