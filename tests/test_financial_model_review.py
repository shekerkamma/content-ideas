"""Tests for the financial-model-review scripts: stdlib xlsx extraction, tidy
CSV melting, and the arithmetic integrity gate. No third-party deps — these
scripts exist precisely because openpyxl is unreliable on these hosts."""

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "skills" / "financial-model-review" / "scripts"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


extract_workbook = _load("extract_workbook")
sheets_to_csv = _load("sheets_to_csv")
check_model_integrity = _load("check_model_integrity")


SHEET_XML = """<?xml version="1.0"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>{rows}</sheetData></worksheet>"""

WORKBOOK_XML = """<?xml version="1.0"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="{name}" sheetId="1" state="visible" r:id="rId1"/></sheets>
</workbook>"""

RELS_XML = """<?xml version="1.0"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Target="worksheets/sheet1.xml"
 Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"/>
</Relationships>"""


def build_xlsx(path, sheet_name, grid):
    """Write a minimal .xlsx from a list of (row_number, {col_letter: value})."""
    rows = []
    for rnum, cells in grid:
        parts = []
        for col, val in cells.items():
            if isinstance(val, str):
                parts.append(
                    f'<c r="{col}{rnum}" t="inlineStr"><is><t>{val}</t></is></c>'
                )
            else:
                parts.append(f'<c r="{col}{rnum}"><v>{val}</v></c>')
        rows.append(f'<row r="{rnum}">{"".join(parts)}</row>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/workbook.xml", WORKBOOK_XML.format(name=sheet_name))
        z.writestr("xl/_rels/workbook.xml.rels", RELS_XML)
        z.writestr("xl/worksheets/sheet1.xml", SHEET_XML.format(rows="".join(rows)))


class TestPeriodDetection(unittest.TestCase):
    def test_bare_year_only_counts_inside_plausible_range(self):
        self.assertTrue(sheets_to_csv.is_period("2027"))
        self.assertTrue(sheets_to_csv.is_period("FY2027"))
        # Unit counts that merely look like years must not be treated as periods.
        self.assertFalse(sheets_to_csv.is_period("2200"))
        self.assertFalse(sheets_to_csv.is_period("8000"))

    def test_data_row_with_year_like_values_is_not_a_header(self):
        """Regression: a units row of 4-digit values was read as a header row,
        silently dropping every data row beneath it."""
        units_row = {1: "AD0 Smart Mirror", 4: 10, 5: 2200, 6: 8000,
                     7: 18000, 8: 34000, 9: 54000}
        self.assertFalse(sheets_to_csv.is_header_row(units_row))

    def test_header_row_with_trailing_annotation_column(self):
        """Regression: a trailing 'Share FY32' column made a real header fail."""
        header = {1: "Segment", 2: "FY2027", 3: "FY2028", 4: "FY2029",
                  5: "Share FY32"}
        self.assertTrue(sheets_to_csv.is_header_row(header))

    def test_header_row_with_leading_label_columns(self):
        header = {1: "Product", 2: "Commercial model", 3: "Launch",
                  4: "FY2027", 5: "FY2028"}
        self.assertTrue(sheets_to_csv.is_header_row(header))

    def test_single_period_is_not_a_header(self):
        self.assertFalse(sheets_to_csv.is_header_row({1: "Total", 2: "FY2027"}))


class TestExtractAndMelt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "model.xlsx"
        build_xlsx(
            self.path,
            "Detail",
            [
                (1, {"A": "ADAS Segment — Product Detail"}),
                (3, {"A": "Product", "B": "Commercial model", "C": "FY2027", "D": "FY2028"}),
                (4, {"A": "Truck kit", "B": "Product Sales", "C": 2.5, "D": 6.25}),
                (6, {"A": "Product — UNITS", "B": "FY2027", "C": "FY2028"}),
                (7, {"A": "Truck kit", "B": 100, "C": 2200}),
                (9, {"A": "GROSS PROFIT"}),
                (10, {"A": "Product", "B": "FY2027", "C": "FY2028"}),
                (11, {"A": "Truck kit", "B": 1.4, "C": 4.7}),
            ],
        )
        self.addCleanup(self.tmp.cleanup)

    def test_extract_reads_inline_strings_and_numbers(self):
        book = extract_workbook.extract(self.path)
        self.assertEqual(len(book["sheets"]), 1)
        self.assertEqual(book["sheets"][0]["name"], "Detail")
        first = book["sheets"][0]["rows"][0]
        self.assertEqual(first["cells"][1], "ADAS Segment — Product Detail")

    def test_melt_separates_repeated_line_item_by_section_and_block(self):
        book = extract_workbook.extract(self.path)
        rows = sheets_to_csv.tidy_sheet(book["sheets"][0])
        keys = {(r["section"], r["block"], r["period"]): r["value"]
                for r in rows if r["line_item"] == "Truck kit"}
        # Same line item appears three times; each must stay addressable.
        self.assertEqual(keys[("ADAS Segment — Product Detail", "Product", "FY2027")], 2.5)
        self.assertEqual(keys[("ADAS Segment — Product Detail", "Product — UNITS", "FY2028")], 2200)
        self.assertEqual(keys[("GROSS PROFIT", "Product", "FY2027")], 1.4)

    def test_units_row_survives_melting(self):
        """The 2200 unit value must appear as data, not be swallowed as a header."""
        book = extract_workbook.extract(self.path)
        rows = sheets_to_csv.tidy_sheet(book["sheets"][0])
        units = [r for r in rows if r["block"] == "Product — UNITS"]
        self.assertEqual(len(units), 2)

    def test_label_columns_are_preserved_as_attrs(self):
        """Regression: non-numeric label columns between the line item and the
        first period (Commercial model, Launch) were dropped by the melt,
        silently losing analytical dimensions like recurring-vs-one-time."""
        book = extract_workbook.extract(self.path)
        rows = sheets_to_csv.tidy_sheet(book["sheets"][0])
        rev = [r for r in rows if r["block"] == "Product" and r["line_item"] == "Truck kit"]
        self.assertTrue(rev)
        self.assertIn("Commercial model=Product Sales", rev[0]["attrs"])
        # blocks without label columns must not invent them
        units = [r for r in rows if r["block"] == "Product — UNITS"]
        self.assertEqual(units[0]["attrs"], "")

    def test_no_formula_workbook_is_flagged(self):
        book = extract_workbook.extract(self.path)
        self.assertIn("no formulas found", extract_workbook.to_markdown(book))


class TestIntegrityGate(unittest.TestCase):
    def _spec(self, net_income):
        return {
            "label": "t",
            "periods": ["FY2027", "FY2028"],
            "tolerance": 0.02,
            "series": {
                "EBT": [-2.29, 1.40],
                "Tax": [0.0, -0.22],
                "Net Income": net_income,
                "Revenue": [6.0, 41.17],
                "Gross Profit": [3.2, 30.36],
            },
            "identities": [
                {"name": "EBT - Tax = Net Income",
                 "terms": {"EBT": 1, "Tax": -1, "Net Income": -1}}
            ],
            "ratios": [{"name": "GM", "numerator": "Gross Profit",
                        "denominator": "Revenue", "percent": True}],
            "cagr": [{"name": "Revenue", "series": "Revenue"}],
        }

    def test_break_is_detected(self):
        res = check_model_integrity.run(self._spec([-2.29, -0.67]))
        statuses = [r["status"] for r in res["checks"][0]["results"]]
        self.assertIn(check_model_integrity.BREAK, statuses)
        _, breaks = check_model_integrity.report(res)
        self.assertEqual(breaks, 1)

    def test_clean_model_passes(self):
        res = check_model_integrity.run(self._spec([-2.29, 1.62]))
        _, breaks = check_model_integrity.report(res)
        self.assertEqual(breaks, 0)

    def test_rounding_drift_is_not_a_break(self):
        spec = self._spec([-2.29, 1.61])  # 0.01 off, inside tolerance
        res = check_model_integrity.run(spec)
        statuses = [r["status"] for r in res["checks"][0]["results"]]
        self.assertNotIn(check_model_integrity.BREAK, statuses)
        self.assertIn(check_model_integrity.ROUNDING, statuses)

    def test_sums_are_expanded_into_identities(self):
        spec = {
            "label": "t", "periods": ["FY1"], "tolerance": 0.01,
            "series": {"A": [1.0], "B": [2.0], "Total": [4.0]},
            "sums": [{"name": "A+B=Total", "of": ["A", "B"], "equals": "Total"}],
        }
        res = check_model_integrity.run(spec)
        self.assertEqual(res["checks"][0]["results"][0]["status"],
                         check_model_integrity.BREAK)

    def test_cagr_and_ratio_computed(self):
        res = check_model_integrity.run(self._spec([-2.29, 1.62]))
        self.assertAlmostEqual(res["ratios"][0]["values"][0], 53.33, places=1)
        self.assertGreater(res["cagr"][0]["cagr_pct"], 500)

    def test_missing_series_raises_clear_error(self):
        spec = {
            "label": "t", "periods": ["FY1"], "series": {"A": [1.0]},
            "identities": [{"name": "x", "terms": {"A": 1, "Ghost": -1}}],
        }
        with self.assertRaises(KeyError):
            check_model_integrity.run(spec)


if __name__ == "__main__":
    unittest.main()
