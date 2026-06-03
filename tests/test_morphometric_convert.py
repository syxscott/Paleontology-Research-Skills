"""Tests for paleo-morphometric-convert format parsers and writers."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPT_DIR = _HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "paleo-morphometric-convert" / "scripts"
sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "scripts"))

import convert  # noqa: E402


class TestTpsParser(unittest.TestCase):

    def test_single_specimen(self):
        text = "LM=3\n1.0 2.0\n3.0 4.0\n5.0 6.0\nID=spec1\nSCALE=1.5\n"
        result = convert._parse_tps(text)
        self.assertEqual(len(result), 1)
        s = result[0]
        self.assertEqual(s["specimen_id"], "spec1")
        self.assertEqual(s["scale"], 1.5)
        self.assertEqual(len(s["landmarks"]), 3)
        self.assertEqual(s["landmarks"][0]["x"], 1.0)
        self.assertEqual(s["landmarks"][2]["y"], 6.0)

    def test_multi_specimen(self):
        text = ("LM=2\n1.0 2.0\n3.0 4.0\nID=a\nSCALE=1.0\n\n"
                "LM=2\n5.0 6.0\n7.0 8.0\nID=b\nSCALE=2.0\n")
        result = convert._parse_tps(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["specimen_id"], "a")
        self.assertEqual(result[1]["specimen_id"], "b")
        self.assertEqual(result[1]["scale"], 2.0)

    def test_garbage_returns_empty(self):
        result = convert._parse_tps("not a tps file at all")
        self.assertEqual(result, [])


class TestCsvParser(unittest.TestCase):

    def test_long_format(self):
        text = ("specimen_id,landmark_id,x,y,type,name\n"
                "a,1,1.0,2.0,semilandmark,LM01\n"
                "a,2,3.0,4.0,semilandmark,LM02\n"
                "b,1,5.0,6.0,fixed,APEX\n")
        result = convert._parse_csv(text)
        self.assertEqual(len(result), 2)
        names = {s["specimen_id"] for s in result}
        self.assertEqual(names, {"a", "b"})
        a = next(s for s in result if s["specimen_id"] == "a")
        self.assertEqual(len(a["landmarks"]), 2)

    def test_missing_columns_returns_empty(self):
        text = "specimen_id,landmark_id\na,1\n"
        result = convert._parse_csv(text)
        self.assertTrue(all(len(s["landmarks"]) == 0 for s in result))


class TestRoundTrip(unittest.TestCase):

    def test_tps_csv_tps(self):
        original = [{
            "specimen_id": "spec1",
            "scale": 1.0,
            "image_path": None,
            "num_landmarks": 3,
            "landmarks": [
                {"id": 1, "x": 1.0, "y": 2.0, "type": "semilandmark", "name": "LM01"},
                {"id": 2, "x": 3.0, "y": 4.0, "type": "semilandmark", "name": "LM02"},
                {"id": 3, "x": 5.0, "y": 6.0, "type": "semilandmark", "name": "LM03"},
            ],
        }]
        with tempfile.TemporaryDirectory() as td:
            tps_path = Path(td) / "a.tps"
            csv_path = Path(td) / "a.csv"
            tps_path2 = Path(td) / "b.tps"
            convert._write_tps(original, tps_path)
            text = tps_path.read_text(encoding="utf-8")
            parsed_back = convert._parse_tps(text)
            self.assertEqual(parsed_back[0]["specimen_id"], "spec1")
            convert._write_csv(parsed_back, csv_path)
            parsed_csv = convert._parse_csv(csv_path.read_text(encoding="utf-8"))
            self.assertEqual(len(parsed_csv[0]["landmarks"]), 3)
            convert._write_tps(parsed_csv, tps_path2)
            self.assertIn("LM=3", tps_path2.read_text(encoding="utf-8"))


class TestValidation(unittest.TestCase):

    def test_all_same_count(self):
        specimens = [
            {"specimen_id": "a", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 5},
            {"specimen_id": "b", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 5},
        ]
        v = convert._validate(specimens)
        self.assertTrue(v["all_same_count"])
        self.assertEqual(v["specimens_count"], 2)

    def test_inconsistent_count_warning(self):
        specimens = [
            {"specimen_id": "a", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 3},
            {"specimen_id": "b", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 5},
        ]
        v = convert._validate(specimens)
        self.assertFalse(v["all_same_count"])
        self.assertTrue(any("Inconsistent" in w for w in v["warnings"]))

    def test_empty(self):
        v = convert._validate([])
        self.assertEqual(v["specimens_count"] if "specimens_count" in v else 0, 0)


if __name__ == "__main__":
    unittest.main()
