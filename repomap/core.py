"""Core functionality for the RepoMap package."""

import fnmatch
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .formatters.ascii import ASCIIFormatter
from .formatters.html import HTMLFormatter
from .formatters.json import JSONFormatter
from .formatters.markdown import MarkdownFormatter


class OutputFormat:
    """Supported output formats."""

    MARKDOWN = "markdown"
    ASCII = "ascii"
    JSON = "json"
    HTML = "html"


class ProjectStructureGenerator:
    # Common directories that should be ignored by default
    DEFAULT_IGNORE_DIRS: Set[str] = {
        "venv",
        ".venv",
        "env",
        ".env",
        "node_modules",
        ".git",
        ".github",
        ".idea",
        ".vscode",
        "__pycache__",
        "build",
        "dist",
        ".pytest_cache",
        ".mypy_cache",
        ".coverage",
        "coverage",
        "htmlcov",
    }

    def __init__(
        self, root_path: str = ".", max_depth: int = 5, output_format: str = OutputFormat.MARKDOWN
    ) -> None:
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.ignored_patterns = self._read_gitignore()
        self.output_format = output_format
        self._formatter = self._get_formatter()

    def _get_formatter(self):
        """Get the appropriate formatter based on output format."""
        formatters = {
            OutputFormat.MARKDOWN: MarkdownFormatter(),
            OutputFormat.ASCII: ASCIIFormatter(),
            OutputFormat.JSON: JSONFormatter(),
            OutputFormat.HTML: HTMLFormatter(),
        }
        return formatters.get(self.output_format, MarkdownFormatter())

    def _read_gitignore(self) -> List[str]:
        """Read .gitignore file and return list of patterns to ignore."""
        gitignore_path = self.root_path / ".gitignore"
        patterns: List[str] = []
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        return patterns

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored based on .gitignore patterns and default ignore dirs."""
        if path.name in self.DEFAULT_IGNORE_DIRS:
            return True

        rel_path = str(path.relative_to(self.root_path))
        for pattern in self.ignored_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(path.name, pattern):
                return True
        return False

    def _get_file_stats(self, path: Path) -> Dict[str, Any]:
        """Get file statistics."""
        stat = path.stat()
        return {"size": stat.st_size, "last_modified": datetime.fromtimestamp(stat.st_mtime)}

    def generate_tree(self) -> str:
        """Generate the directory tree structure in the specified format."""
        if self.output_format == OutputFormat.JSON:
            tree_data = self._generate_json_tree(self.root_path, current_depth=0)
            return self._formatter.format_tree(self.root_path, tree_data, self.max_depth)

        lines = self._formatter.format_header(self.root_path.name, self.max_depth)
        self._generate_tree(self.root_path, "", lines, is_last=True, current_depth=0)

        if self.output_format == OutputFormat.MARKDOWN:
            lines.append("```")
        return "\n".join(lines)

    def _generate_json_tree(self, path: Path, current_depth: int) -> Dict[str, Any]:
        """Generate JSON tree structure."""
        if self._should_ignore(path):
            return {}

        node = self._formatter.create_node(
            path.name, path.is_dir(), self._get_file_stats(path) if path.is_file() else None
        )

        if path.is_dir() and current_depth < self.max_depth:
            children = []
            entries = sorted(
                [x for x in path.iterdir() if not self._should_ignore(x)],
                key=lambda x: (x.is_file(), x.name.lower()),
            )

            for entry in entries:
                child = self._generate_json_tree(entry, current_depth + 1)
                if child:
                    children.append(child)

            if children:
                node["children"] = children

        return node

    def _generate_tree(
        self, path: Path, prefix: str, lines: List[str], is_last: bool, current_depth: int
    ) -> None:
        """Recursively generate tree structure with depth limit."""
        if self._should_ignore(path):
            return

        if current_depth >= self.max_depth:
            if path.is_dir() and any(True for _ in path.iterdir()):
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}... (max depth reached)")
            return

        entries = sorted(
            [x for x in path.iterdir() if not self._should_ignore(x)],
            key=lambda x: (x.is_file(), x.name.lower()),
        )

        for i, entry in enumerate(entries):
            is_last_entry = i == len(entries) - 1
            stats = self._get_file_stats(entry) if entry.is_file() else None

            lines.append(
                self._formatter.format_entry(
                    prefix, entry.name, entry.is_dir(), is_last_entry, stats
                )
            )

            if entry.is_dir():
                self._generate_tree(
                    entry,
                    prefix + ("    " if is_last_entry else "│   "),
                    lines,
                    is_last_entry,
                    current_depth + 1,
                )

    def save_to_file(self, output_file: Optional[str] = None) -> Path:
        """Generate and save the tree structure to a file."""
        if output_file is None:
            ext = {OutputFormat.JSON: ".json", OutputFormat.HTML: ".html"}.get(
                self.output_format, ".md"
            )
            output_file = f"project_structure{ext}"

        tree_content = self.generate_tree()
        output_path = self.root_path / output_file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(tree_content)
        return output_path
