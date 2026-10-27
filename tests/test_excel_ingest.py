import importlib.util
import tempfile
import unittest
from pathlib import Path

import pytest

pytest.importorskip("pandas")
openpyxl = pytest.importorskip("openpyxl")

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "ai-analyst" / "excel-ingest" / "scripts" / "excel_ingest.py"
spec = importlib.util.spec_from_file_location("excel_ingest", SCRIPT)
excel_ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(excel_ingest)


def _workbook(path, sheets):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, rows in sheets.items():
        ws = wb.create_sheet(name)
        for row in rows:
            ws.append(row)
    wb.save(path)


def _sales(n=30):
    return [["ACME Trading - Confidential"], [], ["region", "orders", "revenue"]] + [
        ["N" if i % 2 else "S", i + 1, (i + 1) * 10.5] for i in range(n)
    ]


class ExcelIngestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_header_below_banner_is_found_and_summary_is_flagged(self):
        book = self.tmp / "acme.xlsx"
        _workbook(book, {"Sales": _sales(), "Summary": [["metric", "value"], ["total", 1]]})
        info = {s["sheet"]: s for s in excel_ingest.enumerate_sheets(book)}
        self.assertEqual(2, info["Sales"]["header_row"])
        self.assertEqual("high", info["Sales"]["header_confidence"])
        self.assertEqual("data", info["Sales"]["looks_like"])
        self.assertEqual("summary", info["Summary"]["looks_like"])

    def test_convert_skips_the_banner_and_names_the_columns(self):
        book = self.tmp / "acme.xlsx"
        _workbook(book, {"Sales": _sales(), "Summary": [["metric", "value"], ["total", 1]]})
        (result,) = excel_ingest.convert(book, self.tmp / "out")
        self.assertEqual(30, result["loaded_rows"])
        header = Path(result["csv_path"]).read_text(encoding="utf-8").splitlines()[0]
        self.assertEqual("region,orders,revenue", header)

    def test_two_data_sheets_are_refused_not_guessed(self):
        book = self.tmp / "two.xlsx"
        _workbook(book, {"Q1": _sales(), "Q2": _sales()})
        with self.assertRaises(excel_ingest.ExcelIngestError) as ctx:
            excel_ingest.resolve_sheet(book)
        self.assertIn("does not guess", str(ctx.exception))

    def test_legacy_xls_is_refused(self):
        legacy = self.tmp / "old.xls"
        legacy.write_bytes(b"")
        with self.assertRaises(excel_ingest.ExcelIngestError):
            excel_ingest.enumerate_sheets(legacy)


if __name__ == "__main__":
    unittest.main()
