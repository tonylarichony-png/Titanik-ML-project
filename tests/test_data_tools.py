from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from ml_project import (
    DataCatalog,
    DatasetProfiler,
    MarkdownDocument,
    build_field_descriptions_template,
)
from ml_project.docsync import dataframe_to_markdown


class DatasetProfilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = pd.DataFrame(
            {
                "id": [1, 2, 2],
                "target": [0, 1, 1],
                "value": [10.0, None, 30.0],
            }
        )
        self.profile = DatasetProfiler(
            self.frame,
            name="train",
            key="id",
            target="target",
        )

    def test_schema_and_missing_are_separate_reports(self) -> None:
        schema = self.profile.schema_report()
        missing = self.profile.missing_report()

        self.assertEqual(schema.columns.tolist(), ["field", "dtype"])
        self.assertEqual(missing["field"].tolist(), ["value"])
        self.assertEqual(int(missing.iloc[0]["missing"]), 1)

    def test_duplicate_and_target_reports(self) -> None:
        duplicate = self.profile.duplicate_report().iloc[0]
        target = self.profile.target_report()

        self.assertEqual(int(duplicate["key_duplicates"]), 1)
        self.assertEqual(target["count"].tolist(), [1, 2])


class DataCatalogTests(unittest.TestCase):
    def test_file_report_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "data" / "raw"
            raw.mkdir(parents=True)
            pd.DataFrame({"id": [1, 2]}).to_csv(raw / "train.csv", index=False)

            catalog = DataCatalog(
                root,
                Path("data/raw"),
                {
                    "train": {
                        "filename": "train.csv",
                        "role": "train",
                        "required": True,
                    }
                },
            )
            report = catalog.file_report().iloc[0]

            self.assertEqual(int(report["rows"]), 2)
            self.assertEqual(int(report["columns"]), 1)
            self.assertEqual(len(str(report["sha256"])), 64)

            template = build_field_descriptions_template(
                catalog,
                {"id": "Идентификатор строки."},
            )
            self.assertEqual(template.count("'id':"), 1)
            self.assertIn("'id': 'Идентификатор строки.'", template)


class MarkdownDocumentTests(unittest.TestCase):
    def test_markdown_table_is_padded_and_numeric_columns_are_aligned(self) -> None:
        table = dataframe_to_markdown(
            pd.DataFrame(
                {
                    "Название": ["короткое", "длинное значение"],
                    "Строки": [9, 125],
                }
            )
        )
        lines = table.splitlines()

        self.assertEqual(len({len(line) for line in lines}), 1)
        self.assertIn("---:", lines[1])

    def test_only_generated_block_is_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            path.write_text(
                "Manual before\n"
                "<!-- auto:test:start -->\n"
                "old\n"
                "<!-- auto:test:end -->\n"
                "Manual after\n",
                encoding="utf-8",
            )

            MarkdownDocument(path).update_blocks({"test": "new"})
            result = path.read_text(encoding="utf-8")

            self.assertIn("Manual before", result)
            self.assertIn("Manual after", result)
            self.assertIn(
                "<!-- auto:test:start -->\n\nnew\n\n<!-- auto:test:end -->",
                result,
            )
            self.assertNotIn("\nold\n", result)


if __name__ == "__main__":
    unittest.main()
