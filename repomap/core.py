"""Core functionality for the RepoMap package."""

import os
from datetime import datetime
from pathlib import Path
import fnmatch
from typing import List, Set, Optional

class ProjectStructureGenerator:
    # Common directories that should be ignored by default
    DEFAULT_IGNORE_DIRS: Set[str] = {
        'venv',
        '.venv',
        'env',
        '.env',
        'node_modules',
        '.git',
        '.github',
        '.idea',
        '.vscode',
        '__pycache__',
        'build',
        'dist',
        '.pytest_cache',
        '.mypy_cache',
        '.coverage',
        'coverage',
        'htmlcov'
    }

    def __init__(self, root_path: str = '.', max_depth: int = 5) -> None:
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.ignored_patterns = self._read_gitignore()
        
    def _read_gitignore(self) -> List[str]:
        """Read .gitignore file and return list of patterns to ignore."""
        gitignore_path = self.root_path / '.gitignore'
        patterns: List[str] = []
        if gitignore_path.exists():
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
        return patterns
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored based on .gitignore patterns and default ignore dirs."""
        # Check if the directory is in default ignore list
        if path.name in self.DEFAULT_IGNORE_DIRS:
            return True

        rel_path = str(path.relative_to(self.root_path))
        for pattern in self.ignored_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or \
               fnmatch.fnmatch(path.name, pattern):
                return True
        return False
    
    def generate_tree(self) -> str:
        """Generate the directory tree structure in markdown format."""
        lines = [f"# Project Structure\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                f"Max depth: {self.max_depth}\n\n```\n{self.root_path.name}/"]
        self._generate_tree(self.root_path, "", lines, is_last=True, current_depth=0)
        lines.append("```")
        return '\n'.join(lines)
    
    def _generate_tree(self, path: Path, prefix: str, lines: List[str], is_last: bool, current_depth: int) -> None:
        """Recursively generate tree structure with depth limit."""
        if self._should_ignore(path):
            return
            
        if current_depth >= self.max_depth:
            if path.is_dir() and any(True for _ in path.iterdir()):
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}... (max depth reached)")
            return

        entries = sorted([x for x in path.iterdir() if not self._should_ignore(x)],
                        key=lambda x: (x.is_file(), x.name.lower()))
        
        for i, entry in enumerate(entries):
            is_last_entry = i == len(entries) - 1
            if entry.is_dir():
                lines.append(f"{prefix}{'└── ' if is_last_entry else '├── '}{entry.name}/")
                self._generate_tree(
                    entry,
                    prefix + ('    ' if is_last_entry else '│   '),
                    lines,
                    is_last_entry,
                    current_depth + 1
                )
            else:
                lines.append(f"{prefix}{'└── ' if is_last_entry else '├── '}{entry.name}")
    
    def save_to_file(self, output_file: str = 'project_structure.md') -> Path:
        """Generate and save the tree structure to a markdown file."""
        tree_content = self.generate_tree()
        output_path = self.root_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(tree_content)
        return output_path
