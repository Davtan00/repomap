"""Test cases for formatters."""

import json
from pathlib import Path

import pytest

from repomap.formatters.ascii import ASCIIFormatter
from repomap.formatters.html import HTMLFormatter
from repomap.formatters.json import JSONFormatter
from repomap.formatters.markdown import MarkdownFormatter
from datetime import datetime


def test_markdown_formatter():
    """Test markdown formatter output."""
    formatter = MarkdownFormatter()

    # Test header formatting
    header = formatter.format_header("test_repo", 5)
    assert isinstance(header, list)
    assert any("Project Structure" in line for line in header)
    assert any("Max depth: 5" in line for line in header)

    # Test entry formatting
    entry = formatter.format_entry("    ", "test_file.py", False, True)
    assert entry == "    └── test_file.py"

    entry_dir = formatter.format_entry("    ", "test_dir", True, False)
    assert entry_dir == "    ├── test_dir/"


def test_ascii_formatter():
    """Test ASCII formatter output."""
    formatter = ASCIIFormatter()

    # Test header formatting
    header = formatter.format_header("test_repo", 5)
    assert isinstance(header, list)
    assert any("Repository Structure" in line for line in header)
    assert any("Max depth: 5" in line for line in header)

    # Test entry formatting with stats
    stats = {"size": 1024}  # 1KB
    entry = formatter.format_entry("    ", "test_file.py", False, True, stats)
    assert "test_file.py" in entry
    assert "1.0 KB" in entry

    # Test directory entry
    entry_dir = formatter.format_entry("    ", "test_dir", True, False)
    assert entry_dir == "    ├── test_dir/"


def test_json_formatter():
    """Test JSON formatter output."""
    formatter = JSONFormatter()

    # Test node creation
    stats = {"size": 2048, "last_modified": datetime.now()}

    node = formatter.create_node("test_file.py", False, stats)
    assert node["name"] == "test_file.py"
    assert node["type"] == "file"
    assert node["size_bytes"] == 2048
    assert "created_at" in node

    # Test tree formatting
    tree_data = {"name": "root", "type": "directory", "children": [node]}

    json_str = formatter.format_tree(Path("."), tree_data, 5)
    parsed = json.loads(json_str)

    assert "metadata" in parsed
    assert "tree" in parsed
    assert parsed["metadata"]["max_depth"] == 5
    assert parsed["tree"]["children"][0]["name"] == "test_file.py"


def test_json_formatter_parse():
    """Test JSON formatter parsing."""
    formatter = JSONFormatter()

    test_data = {"metadata": {"version": "1.0.0"}, "tree": {"name": "root"}}

    json_str = json.dumps(test_data)
    parsed = formatter.parse_tree(json_str)

    assert parsed["metadata"]["version"] == "1.0.0"
    assert parsed["tree"]["name"] == "root"


def test_html_formatter():
    """Test HTML formatter output."""
    formatter = HTMLFormatter()

    # Test header formatting
    header = formatter.format_header("test_repo", 5)
    assert "Repository Structure" in header
    assert "Max depth: 5" in header
    assert "expandAll" in header
    assert "collapseAll" in header

    # Test tree formatting
    test_tree = {
        "name": "root",
        "type": "directory",
        "children": [
            {
                "name": "test.py",
                "type": "file",
                "size_bytes": 1024,
                "last_modified": "2023-12-07T12:00:00",
            },
            {
                "name": "test_dir",
                "type": "directory",
                "children": [{"name": "nested.txt", "type": "file", "size_bytes": 512}],
            },
        ],
    }

    html = formatter.format_tree(Path("."), test_tree, 5)

    # Check for essential HTML elements
    assert "<!DOCTYPE html>" in html
    assert "<html" in html
    assert "<style>" in html
    assert "<script>" in html

    # Check for content
    assert "test.py" in html
    assert "test_dir" in html
    assert "nested.txt" in html
    assert "1.0 KB" in html  # File size formatting
    assert "2023-12-07" in html  # Modified date
