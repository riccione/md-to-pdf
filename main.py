import argparse
import sys

from markdown_it import MarkdownIt
from weasyprint import HTML

CSS_STYLES = """
@page {
    size: letter;
    margin: 1.5cm 1.5cm 1.5cm 1.5cm;
    @bottom-right {
        content: "Page " counter(page);
        font-size: 9pt;
        color: #666;
    }
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.35;
    color: #222;
}

h1 {
    text-align: center;
    font-size: 16pt;
    font-weight: 700;
    margin: 0 0 2pt 0;
    color: #1a1a1a;
    letter-spacing: 1pt;
}

h1 + p {
    text-align: left;
    font-size: 9pt;
    color: #444;
    margin-bottom: 12pt;
    line-height: 1.5;
}

h1 + p a {
    color: #2563eb;
    text-decoration: none;
}

h2 {
    font-size: 11pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1pt;
    color: #1a1a1a;
    border-bottom: 1px solid #dddddd;
    padding-bottom: 2pt;
    margin: 12pt 0 6pt 0;
    page-break-after: avoid;
    break-after: avoid;
}

h3 {
    font-size: 10pt;
    font-weight: 700;
    color: #1a1a1a;
    margin: 8pt 0 2pt 0;
    page-break-after: avoid;
    break-after: avoid;
}

p {
    margin: 0 0 4pt 0;
    text-align: justify;
}

ul {
    margin: 2pt 0 5pt 1.4em;
    padding: 0;
}

li {
    margin-bottom: 1pt;
}

strong {
    font-weight: 700;
}

a {
    color: #2563eb;
    text-decoration: none;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 8pt 0;
}

em {
    font-style: italic;
}
"""


def build_html(markdown_text: str) -> str:
    md = MarkdownIt("commonmark")
    body_html = md.render(markdown_text)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>{CSS_STYLES}</style>
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
    html_document = build_html(markdown_text)

    print("Generating PDF...")
    try:
        HTML(string=html_document).write_pdf(args.output)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

    print(f"PDF successfully exported to {args.output}!")


if __name__ == "__main__":
    main()
