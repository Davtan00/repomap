"""Command-line interface for RepoMap."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .core import ProjectStructureGenerator, OutputFormat

console = Console()

def print_stats(path: Path) -> None:
    """Print repository statistics."""
    total_files = len(list(path.rglob('*')))
    total_dirs = len([p for p in path.rglob('*') if p.is_dir()])
    
    table = Table(title="Repository Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Files", str(total_files))
    table.add_row("Total Directories", str(total_dirs))
    
    console.print(table)

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
    help='Output file name. If not provided, will use project_structure.[format]',
    type=str
)
@click.option(
    '--format',
    '-f',
    type=click.Choice(['markdown', 'ascii', 'json'], case_sensitive=False),
    default='markdown',
    help='Output format.'
)
@click.option(
    '--stats/--no-stats',
    default=True,
    help='Show repository statistics.'
)
def main(path: Path, max_depth: int, output: str, format: str, stats: bool) -> None:
    """Generate a structured view of your repository.
    
    RepoMap helps you create clear documentation of your project's structure,
    respecting .gitignore patterns and providing useful statistics.
    """
    try:
        console.print(
            Panel.fit(
                "[bold blue]RepoMap[/bold blue] - Repository Structure Generator",
                border_style="blue"
            )
        )
        
        if stats:
            print_stats(path)
        
        generator = ProjectStructureGenerator(
            root_path=path,
            max_depth=max_depth,
            output_format=format.lower()
        )
        
        output_path = generator.save_to_file(output)
        console.print(f"\n✨ Project structure has been saved to: [green]{output_path}[/green]")
        
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    main()
