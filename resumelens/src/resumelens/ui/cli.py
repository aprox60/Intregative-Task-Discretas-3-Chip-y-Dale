import argparse

from resumelens.pipeline import run_resume_pipeline


def build_parser():
    parser = argparse.ArgumentParser(description="ResumeLens: formal language based resume screening")
    parser.add_argument("resume_path", help="Path to the resume text file")
    parser.add_argument("--output-html", default=None, help="Optional path to save the HTML report")
    return parser


def main():
    args = build_parser().parse_args()
    with open(args.resume_path, encoding="utf-8") as file:
        text = file.read()

    result = run_resume_pipeline(text)
    print("Normalized tokens:", result.normalized_tokens)
    for profile_name in result.sorted_by_profile:
        print(profile_name, result.sorted_by_profile[profile_name], "->", result.classification[profile_name])

    if args.output_html:
        with open(args.output_html, "w", encoding="utf-8") as file:
            file.write(result.html)
    return 0


if __name__ == "__main__":
    main()
