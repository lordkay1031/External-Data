"""Tests for json_to_csv.py"""

import csv
import json
import os
import tempfile
import pytest

from json_to_csv import json_to_csv


def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def read_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestJsonToCsv:
    def test_basic_conversion(self, tmp_path):
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Los Angeles"},
        ]
        input_file = str(tmp_path / "input.json")
        output_file = str(tmp_path / "output.csv")
        write_json(input_file, data)

        json_to_csv(input_file, output_file)

        rows = read_csv(output_file)
        assert len(rows) == 2
        assert rows[0] == {"name": "Alice", "age": "30", "city": "New York"}
        assert rows[1] == {"name": "Bob", "age": "25", "city": "Los Angeles"}

    def test_selected_columns(self, tmp_path):
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Los Angeles"},
        ]
        input_file = str(tmp_path / "input.json")
        output_file = str(tmp_path / "output.csv")
        write_json(input_file, data)

        json_to_csv(input_file, output_file, columns=["name", "city"])

        rows = read_csv(output_file)
        assert len(rows) == 2
        # 'age' should not be present
        assert list(rows[0].keys()) == ["name", "city"]
        assert rows[0]["name"] == "Alice"
        assert rows[0]["city"] == "New York"

    def test_column_order(self, tmp_path):
        data = [{"a": 1, "b": 2, "c": 3}]
        input_file = str(tmp_path / "input.json")
        output_file = str(tmp_path / "output.csv")
        write_json(input_file, data)

        json_to_csv(input_file, output_file, columns=["c", "a"])

        with open(output_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
        assert header == ["c", "a"]

    def test_empty_list(self, tmp_path):
        input_file = str(tmp_path / "input.json")
        output_file = str(tmp_path / "output.csv")
        write_json(input_file, [])

        json_to_csv(input_file, output_file)

        assert os.path.exists(output_file)
        with open(output_file, encoding="utf-8") as f:
            content = f.read()
        assert content == ""

    def test_empty_list_with_columns(self, tmp_path):
        input_file = str(tmp_path / "input.json")
        output_file = str(tmp_path / "output.csv")
        write_json(input_file, [])

        json_to_csv(input_file, output_file, columns=["name", "age"])

        with open(output_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
        assert header == ["name", "age"]

    def test_not_a_list_raises(self, tmp_path):
        input_file = str(tmp_path / "input.json")
        output_file = str(tmp_path / "output.csv")
        write_json(input_file, {"key": "value"})

        with pytest.raises(ValueError, match="list of objects"):
            json_to_csv(input_file, output_file)

    def test_header_written(self, tmp_path):
        data = [{"x": 1, "y": 2}]
        input_file = str(tmp_path / "input.json")
        output_file = str(tmp_path / "output.csv")
        write_json(input_file, data)

        json_to_csv(input_file, output_file)

        with open(output_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
        assert header == ["x", "y"]
