"""Markdown formatter for repository structure."""

from datetime import datetime
from pathlib import Path
from typing import List

class MarkdownFormatter:
    """Format repository structure as markdown."""
    
    @staticmethod
    def format_header(root_name: str, max_depth: int) -> List[str]:
        """Generate the header section of the markdown document."""
        return [
            "# Project Structure\n",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"Max depth: {max_depth}\n\n```\n{root_name}/"
        ]
    
    @staticmethod
    def format_entry(prefix: str, name: str, is_dir: bool, is_last: bool) -> str:
        """Format a single entry in the tree."""
        connector = '└── ' if is_last else '├── '
        suffix = '/' if is_dir else ''
        return f"{prefix}{connector}{name}{suffix}"
