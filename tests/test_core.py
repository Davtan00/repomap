"""Tests for the core functionality."""

import os
from pathlib import Path
import pytest
from repomap.core import ProjectStructureGenerator


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory with some files and subdirs."""
    # Create main project directory
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # Create some files and directories
    (project_dir / "file1.txt").touch()
    (project_dir / "file2.py").touch()

    # Create a subdirectory with files
    subdir = project_dir / "subdir"
    subdir.mkdir()
    (subdir / "subfile1.txt").touch()

    # Create a .gitignore file
    gitignore = project_dir / ".gitignore"
    gitignore.write_text("*.log\n__pycache__/\n")

    return project_dir


def test_project_structure_generator_init():
    """Test ProjectStructureGenerator initialization."""
    generator = ProjectStructureGenerator()
    assert generator.max_depth == 5
    assert generator.root_path == Path.cwd().resolve()


def test_gitignore_parsing(temp_project_dir):
    """Test .gitignore file parsing."""
    generator = ProjectStructureGenerator(root_path=str(temp_project_dir))
    assert "*.log" in generator.ignored_patterns
    assert "__pycache__/" in generator.ignored_patterns


def test_should_ignore(temp_project_dir):
    """Test ignore patterns functionality."""
    generator = ProjectStructureGenerator(root_path=str(temp_project_dir))

    # Test default ignore directory
    venv_dir = temp_project_dir / "venv"
    venv_dir.mkdir()
    assert generator._should_ignore(venv_dir)

    # Test .gitignore pattern
    log_file = temp_project_dir / "test.log"
    log_file.touch()
    assert generator._should_ignore(log_file)


def test_generate_tree(temp_project_dir):
    """Test tree generation."""
    generator = ProjectStructureGenerator(root_path=str(temp_project_dir))
    tree = generator.generate_tree()

    # Check for expected content
    assert "test_project/" in tree
    assert "file1.txt" in tree
    assert "file2.py" in tree
    assert "subdir/" in tree
