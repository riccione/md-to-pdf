import argparse
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from weasyprint import HTML


def build_html(markdown_text: str, css_path: str = "styles.css") -> str:
    css = Path(css_path).read_text(encoding="utf-8")
    md = MarkdownIt("commonmark")
    body_html = md.render(markdown_text)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
{body_html}
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file into a polished PDF."
    )
    parser.add_argument(
        "input",
        help="Path to the input Markdown file",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="Destination path for the generated PDF (default: output.pdf)",
    )
    parser.add_argument(
        "--header",
        help="Path to an optional header Markdown file prepended to the input",
    )
    args = parser.parse_args()

    print("Reading markdown...")
    header = ""
    if args.header:
        try:
            with open(args.header, encoding="utf-8") as f:
                header = f.read().rstrip() + "\n\n"
        except FileNotFoundError:
            print(f"Error: Header file not found: {args.header}")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied reading: {args.header}")
            sys.exit(1)
        except OSError as e:
            print(f"Error reading header file: {e}")
            sys.exit(1)

    try:
        with open(args.input, encoding="utf-8") as f:
            body = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading: {args.input}")
        sys.exit(1)
    except OSError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    markdown_text = header + body

    print("Compiling styles...")
    try:
        html_document = build_html(markdown_text)
    except FileNotFoundError:
        print("Error: styles.css not found")
        sys.exit(1)
    except PermissionError:
        print("Error: Permission denied reading: styles.css")
        sys.exit(1)
    except OSError as e:
        print(f"Error reading styles.css: {e}")
        sys.exit(1)

    print("Generating PDF...")
    try:
        HTML(string=html_document).write_pdf(args.output)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

    print(f"PDF successfully exported to {args.output}!")


if __name__ == "__main__":
    main()
