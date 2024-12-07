# RepoMap

A powerful Python tool for generating repository structure documentation.

## Features

- Generate repository structure documentation in multiple formats
- Respect .gitignore patterns
- Smart directory filtering
- Configurable depth control
- Cross-platform compatibility

## Installation

```bash
pip install repomap
```

## Usage

Basic usage:
```bash
repomap
```

With options:
```bash
repomap --path /path/to/repo --max-depth 3 --output custom_structure.md
```

## Development

This project uses Poetry for dependency management. To set up the development environment:

1. Install Poetry (if not already installed)
2. Clone the repository
3. Run `poetry install`
4. Run tests with `poetry run pytest`

## License

MIT License
