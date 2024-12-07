"""HTML formatter with collapsible tree structure."""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class HTMLFormatter:
    """Format repository structure as an interactive HTML document."""
    
    @staticmethod
    def _get_styles() -> str:
        """Return CSS styles for the HTML tree."""
        return """
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .tree {
                margin: 20px;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .header {
                margin-bottom: 20px;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 8px;
            }
            .caret {
                cursor: pointer;
                user-select: none;
            }
            .caret::before {
                content: "▶";
                color: black;
                display: inline-block;
                margin-right: 6px;
            }
            .caret-down::before {
                transform: rotate(90deg);
            }
            .nested {
                display: none;
                margin-left: 20px;
            }
            .active {
                display: block;
            }
            .file {
                margin-left: 20px;
            }
            .file-info {
                color: #666;
                font-size: 0.9em;
            }
            .directory {
                color: #2c3e50;
                font-weight: bold;
            }
            .file-name {
                color: #34495e;
            }
        </style>
        """
    
    @staticmethod
    def _get_scripts() -> str:
        """Return JavaScript for tree interactivity."""
        return """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var toggler = document.getElementsByClassName("caret");
                for (var i = 0; i < toggler.length; i++) {
                    toggler[i].addEventListener("click", function() {
                        this.parentElement.querySelector(".nested").classList.toggle("active");
                        this.classList.toggle("caret-down");
                    });
                }
                
                // Expand all button
                document.getElementById("expandAll").addEventListener("click", function() {
                    var elements = document.getElementsByClassName("nested");
                    var carets = document.getElementsByClassName("caret");
                    for (var i = 0; i < elements.length; i++) {
                        elements[i].classList.add("active");
                    }
                    for (var i = 0; i < carets.length; i++) {
                        carets[i].classList.add("caret-down");
                    }
                });
                
                // Collapse all button
                document.getElementById("collapseAll").addEventListener("click", function() {
                    var elements = document.getElementsByClassName("nested");
                    var carets = document.getElementsByClassName("caret");
                    for (var i = 0; i < elements.length; i++) {
                        elements[i].classList.remove("active");
                    }
                    for (var i = 0; i < carets.length; i++) {
                        carets[i].classList.remove("caret-down");
                    }
                });
            });
        </script>
        """
    
    @staticmethod
    def format_header(root_name: str, max_depth: int) -> str:
        """Generate the header section of the HTML document."""
        return f"""
        <div class="header">
            <h1>Repository Structure</h1>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Max depth: {max_depth}</p>
            <button id="expandAll">Expand All</button>
            <button id="collapseAll">Collapse All</button>
        </div>
        """
    
    def format_tree(self, root_path: Path, tree_data: Dict[str, Any], max_depth: int) -> str:
        """Format the entire tree as an HTML document."""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Repository Structure - {root_path.name}</title>
            {self._get_styles()}
        </head>
        <body>
            {self.format_header(root_path.name, max_depth)}
            <div class="tree">
                {self._format_node(tree_data)}
            </div>
            {self._get_scripts()}
        </body>
        </html>
        """
        return html_content
    
    def _format_node(self, node: Dict[str, Any], level: int = 0) -> str:
        """Format a single node in the tree."""
        is_dir = node['type'] == 'directory'
        name = node['name']
        
        if is_dir:
            has_children = 'children' in node and node['children']
            if has_children:
                children_html = '\n'.join(
                    self._format_node(child, level + 1)
                    for child in node['children']
                )
                return f"""
                <div>
                    <span class="caret directory">{name}/</span>
                    <div class="nested">
                        {children_html}
                    </div>
                </div>
                """
            return f'<div><span class="directory">{name}/</span></div>'
        
        # File node
        size_str = ""
        if 'size_bytes' in node:
            size = node['size_bytes']
            if size < 1024:
                size_str = f" ({size} B)"
            elif size < 1024 * 1024:
                size_str = f" ({size/1024:.1f} KB)"
            else:
                size_str = f" ({size/(1024*1024):.1f} MB)"
        
        modified_str = ""
        if 'last_modified' in node:
            modified_str = f" - Modified: {node['last_modified']}"
        
        return f"""
        <div class="file">
            <span class="file-name">{name}</span>
            <span class="file-info">{size_str}{modified_str}</span>
        </div>
        """
