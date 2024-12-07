"""ASCII formatter for repository structure."""

from datetime import datetime
from typing import List, Optional


class ASCIIFormatter:
    """Format repository structure as ASCII tree."""

    @staticmethod
    def format_header(root_name: str, max_depth: int) -> List[str]:
        """Generate the header section of the ASCII tree."""
        return [
            "Repository Structure",
            "=" * 20,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Max depth: {max_depth}",
            "",
            root_name + "/",
        ]

    @staticmethod
    def format_entry(
        prefix: str,
        name: str,
        is_dir: bool,
        is_last: bool,
        stats: Optional[dict] = None,
    ) -> str:
        """Format a single entry in the tree with optional statistics."""
        connector = "└── " if is_last else "├── "
        suffix = "/" if is_dir else ""

        # Add size information for files if stats are provided
        if stats and not is_dir:
            size = stats.get("size", 0)
            if size < 1024:
                size_str = f" ({size} B)"
            elif size < 1024 * 1024:
                size_str = f" ({size/1024:.1f} KB)"
            else:
                size_str = f" ({size/(1024*1024):.1f} MB)"
        else:
            size_str = ""

        return f"{prefix}{connector}{name}{suffix}{size_str}"
