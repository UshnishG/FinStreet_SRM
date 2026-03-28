"""
summarize.py — CLI tool to generate a resume-ready project summary.

Usage:
    python summarize.py                   # plain-text output (default)
    python summarize.py --format markdown # Markdown output
    python summarize.py --format plain    # plain-text output
"""

import argparse
import sys
from pathlib import Path

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.summarizer import ProjectSummarizer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a resume-ready project summary from the repository."
    )
    parser.add_argument(
        "--format",
        choices=["plain", "markdown"],
        default="plain",
        help="Output format: 'plain' (default) or 'markdown'",
    )
    args = parser.parse_args()

    summarizer = ProjectSummarizer()

    if args.format == "markdown":
        print(summarizer.format_markdown())
    else:
        print(summarizer.format_plain_text())


if __name__ == "__main__":
    main()
