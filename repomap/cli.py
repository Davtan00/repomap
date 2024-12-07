"""Command-line interface for RepoMap."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from .core import ProjectStructureGenerator

console = Console()

@click.command()
@click.option(
    '--path',
    '-p',
    default='.',
    help='Path to the repository root directory.',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path)
)
@click.option(
    '--max-depth',
    '-d',
    default=5,
    help='Maximum depth to traverse.',
    type=int
)
@click.option(
    '--output',
    '-o',
    default='project_structure.md',
    help='Output file name.',
    type=str
)
def main(path: Path, max_depth: int, output: str) -> None:
    """Generate a markdown file containing the repository structure."""
    try:
        console.print(
            Panel.fit(
                "[bold blue]RepoMap[/bold blue] - Repository Structure Generator",
                border_style="blue"
            )
        )
        
        generator = ProjectStructureGenerator(root_path=path, max_depth=max_depth)
        output_path = generator.save_to_file(output)
        
        console.print(f"\n✨ Project structure has been saved to: [green]{output_path}[/green]")
        
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    main()
