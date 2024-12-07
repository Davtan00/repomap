# RepoMap

A powerful Python tool for generating repository structure documentation in multiple formats.

## ✨ Features

- 📝 **Multiple Output Formats**
  - Markdown for clean documentation
  - ASCII tree with file sizes
  - JSON structure with metadata
  - HTML with collapsible trees (coming soon!)

- 🎯 **Smart Filtering**
  - Respects .gitignore patterns
  - Intelligent directory filtering
  - Configurable depth control
  - Cross-platform compatibility

- 📊 **Repository Statistics**
  - File and directory counts
  - Size analysis
  - Last modified tracking

## 🚀 Installation

```bash
pip install repomap
```

## 📖 Usage

Basic usage:
```bash
repomap
```

With options:
```bash
# Generate markdown output (default)
repomap --path /path/to/repo --max-depth 3

# Generate ASCII tree with file sizes
repomap --format ascii --stats

# Generate JSON output
repomap --format json --output repo-structure.json
```

## 🛠️ Development

This project uses Poetry for dependency management. To set up the development environment:

1. Install Poetry (if not already installed):
   ```bash
   pip install poetry
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/repomap.git
   cd repomap
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Run tests:
   ```bash
   poetry run pytest
   ```

## 📋 Requirements

- Python >=3.8.1
- Click for CLI
- Rich for terminal formatting
- PyYAML for configuration (coming soon)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License
