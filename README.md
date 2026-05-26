# md-to-pdf

Convert Markdown files into polished PDFs.

## Description

`md-to-pdf` is a CLI tool that reads Markdown text and produces a professional PDF with clean typography and print-optimised layout — all in a single command.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run python main.py input.md -o output.pdf
```

- **`input.md`** — Path to the Markdown file (required)
- **`-o, --output`** — Output PDF path (default: `output.pdf`)

If a `header.md` file exists in the current directory, its content is automatically prepended.

### Example

```bash
uv run python main.py document.md -o document.pdf
```

## Development

```bash
uv run ruff check
uv run ruff format --check
```

## License

[MIT](LICENSE)
