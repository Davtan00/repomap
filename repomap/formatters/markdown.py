"""Markdown formatter for repository structure."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

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
    def format_entry(prefix: str, name: str, is_dir: bool, is_last: bool, stats: Optional[Dict] = None) -> str:
        """Format a single entry in the tree."""
        connector = '└── ' if is_last else '├── '
        suffix = '/' if is_dir else ''
        entry = f"{prefix}{connector}{name}{suffix}"
        if stats and not is_dir:
            size = stats.get('size', 0)
            if size < 1024:
                size_str = f"{size}B"
            elif size < 1024 * 1024:
                size_str = f"{size/1024:.1f}KB"
            else:
                size_str = f"{size/(1024*1024):.1f}MB"
            entry += f" ({size_str})"
        return entry
