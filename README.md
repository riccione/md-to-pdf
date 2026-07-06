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
- **`--header`** — Path to an optional header Markdown file prepended to the input

### Examples

No header:
```bash
uv run python main.py document.md -o document.pdf
```

With header:
```bash
uv run python main.py body.md --header header.md -o full.pdf
```

## Development

```bash
uv run ruff check
uv run ruff format --check
```

## License

[MIT](LICENSE)
