from __future__ import annotations

import argparse
from pathlib import Path

from resumelens.pipeline import run_resume_pipeline


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser for the project."""

    parser = argparse.ArgumentParser(description="ResumeLens: formal-language-based résumé screening")
    parser.add_argument("resume_path", type=str, help="Path to the raw résumé text file")
    parser.add_argument("--profile", choices=["all", "FULL_STACK_DEVELOPER", "MACHINE_LEARNING_ENGINEER"], default="all")
    parser.add_argument("--output-html", type=str, default=None, help="Optional path to write the generated HTML report")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    text = Path(args.resume_path).read_text(encoding="utf-8")
    result = run_resume_pipeline(text, profile_name=args.profile if args.profile != "all" else None)
    print("Extracted skills:", result.normalized_tokens)
    print("Classification:", result.classification)
    if args.output_html:
        Path(args.output_html).write_text(result.html, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
