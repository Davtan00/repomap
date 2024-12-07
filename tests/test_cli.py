"""Tests for the command-line interface."""

from pathlib import Path
import pytest
from click.testing import CliRunner
from repomap.cli import main


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def sample_repo(tmp_path):
    """Create a sample repository structure."""
    repo_dir = tmp_path / "sample_repo"
    repo_dir.mkdir()

    # Create some files
    (repo_dir / "file1.txt").write_text("content")
    (repo_dir / "file2.py").write_text("print('hello')")

    # Create a subdirectory
    sub_dir = repo_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "subfile.txt").write_text("subcontent")

    return repo_dir


def test_cli_defaults(runner, sample_repo):
    """Test CLI with default options."""
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["--path", str(sample_repo)])
        assert result.exit_code == 0
        assert "Project structure has been saved" in result.output

        output_file = sample_repo / "project_structure.md"
        assert output_file.exists()
        content = output_file.read_text()
        assert "Project Structure" in content
        assert "file1.txt" in content
        assert "file2.py" in content
        assert "subdir" in content


def test_cli_format_options(runner, sample_repo):
    """Test different output formats."""
    formats = ["markdown", "ascii", "json"]

    for fmt in formats:
        result = runner.invoke(main, ["--path", str(sample_repo), "--format", fmt])
        assert result.exit_code == 0

        ext = ".json" if fmt == "json" else ".md"
        output_file = sample_repo / f"project_structure{ext}"
        assert output_file.exists()


def test_cli_custom_depth(runner, sample_repo):
    """Test custom depth option."""
    result = runner.invoke(main, ["--path", str(sample_repo), "--max-depth", "1"])
    assert result.exit_code == 0

    output_file = sample_repo / "project_structure.md"
    content = output_file.read_text()
    assert "max depth reached" in content.lower()


def test_cli_stats_option(runner, sample_repo):
    """Test statistics display."""
    # Test with stats enabled
    result = runner.invoke(main, ["--path", str(sample_repo), "--stats"])
    assert result.exit_code == 0
    assert "Repository Statistics" in result.output
    assert "Total Files" in result.output

    # Test with stats disabled
    result = runner.invoke(main, ["--path", str(sample_repo), "--no-stats"])
    assert result.exit_code == 0
    assert "Repository Statistics" not in result.output


def test_cli_invalid_path(runner):
    """Test CLI with invalid path."""
    result = runner.invoke(main, ["--path", "nonexistent"])
    assert result.exit_code != 0
    assert "Error" in result.output
