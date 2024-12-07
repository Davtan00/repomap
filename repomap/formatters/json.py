"""JSON formatter for repository structure."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class JSONFormatter:
    """Format repository structure as JSON."""

    @staticmethod
    def create_node(
        name: str, is_dir: bool, stats: Optional[dict] = None
    ) -> Dict[str, Any]:
        """Create a JSON node for a file or directory."""
        node = {
            "name": name,
            "type": "directory" if is_dir else "file",
            "created_at": datetime.now().isoformat(),
        }

        if stats:
            if "size" in stats:
                node["size_bytes"] = stats["size"]
            if "last_modified" in stats:
                node["last_modified"] = stats["last_modified"].isoformat()

        return node

    @staticmethod
    def format_tree(root_path: Path, tree_data: Dict[str, Any], max_depth: int) -> str:
        """Format the entire tree as a JSON string."""
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "root_path": str(root_path),
            "max_depth": max_depth,
            "version": "1.0.0",
        }

        full_data = {"metadata": metadata, "tree": tree_data}

        return json.dumps(full_data, indent=2, ensure_ascii=False)

    @staticmethod
    def parse_tree(json_str: str) -> Dict[str, Any]:
        """Parse a JSON tree string back into a dictionary."""
        return json.loads(json_str)
