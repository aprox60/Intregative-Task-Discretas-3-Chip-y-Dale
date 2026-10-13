# Command line interface of ResumeLens.
#
# With a file:      python -m resumelens data/sample_resumes/wednesday_addams.txt
# Interactive menu: python -m resumelens

import argparse
import os

from resumelens.classification.classifier import AUTOMATA, status_text
from resumelens.classification.profiles import PROFILES
from resumelens.pipeline import run_resume_file, run_resume_pipeline

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SAMPLES_DIR = os.path.join(PROJECT_DIR, "data", "sample_resumes")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "data", "output")

LINE = "-" * 70


def title(text):
    return "\n" + LINE + "\n" + text + "\n" + LINE


def format_report(result, details=False):
    lines = []
    extraction = result.extraction

    lines.append(title("Stage 1 - Extraction (regular expressions)"))
    lines.append("Name:       " + (extraction.name or "(not found)"))
    lines.append("Email:      " + ", ".join(extraction.emails))
    lines.append("Phone:      " + ", ".join(extraction.phones))
    lines.append("Links:      " + ", ".join(extraction.links))
    for education in extraction.education:
        lines.append("Education:  " + education.degree + " in " + education.field + " " + education.institution)
    for experience in extraction.experience:
        lines.append("Experience: " + str(experience.years) + " years " + experience.description)
    lines.append("Technical strings: " + ", ".join(extraction.get_all_technical_strings()))
    unrecognized = extraction.get_unrecognized_skills()
    if len(unrecognized) > 0:
        lines.append("Not recognized:    " + ", ".join(unrecognized))

    lines.append(title("Stage 2 - Normalization (finite-state transducers)"))
    if details:
        for step in result.normalization.steps:
            token = step.token
            if token is None:
                token = "rejected"
            lines.append("  " + step.raw.ljust(22) + " -> " + str(step.preprocessed).ljust(22) + " -> " + token)
    lines.append("Canonical tokens: " + ", ".join(result.normalization.tokens))

    lines.append(title("Stage 3 - Classification (finite automata)"))
    for profile_name in result.classification:
        profile = PROFILES[profile_name]
        accepted = result.classification[profile_name]
        sequence = result.sorted_by_profile[profile_name]
        lines.append(profile.display_name + " [" + profile.automaton_type + "]: " + status_text(accepted))
        lines.append("    sequence: " + (", ".join(sequence) or "(empty)"))
        if not accepted:
            missing = AUTOMATA[profile_name].missing_groups(sequence)
            if len(missing) > 0:
                lines.append("    missing:  " + ", ".join(missing))

    lines.append(title("Stage 4 - Candidate profile DSL (textX)"))
    if details:
        lines.append(result.dsl_text)
    if result.error is None:
        lines.append("The candidate profile is VALID for the grammar.")
    else:
        lines.append("The candidate profile was REJECTED: " + str(result.error))
    return "\n".join(lines)


def save_text(path, text):
    folder = os.path.dirname(path)
    if folder != "":
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
    return path


def save_outputs(result, base_name, folder=OUTPUT_DIR):
    # Saves the JSON of stage 1, the DSL and the HTML (only if the DSL is valid)
    saved = []
    saved.append(save_text(os.path.join(folder, base_name + ".json"), result.extraction.to_json()))
    saved.append(save_text(os.path.join(folder, base_name + ".resume"), result.dsl_text))
    if result.html != "":
        saved.append(save_text(os.path.join(folder, base_name + ".html"), result.html))
    return saved


def list_samples():
    names = []
    for name in sorted(os.listdir(SAMPLES_DIR)):
        if name.endswith(".txt"):
            names.append(name)
    return names


def show_profiles():
    lines = []
    for name in PROFILES:
        profile = PROFILES[name]
        lines.append(title(profile.display_name + " (" + profile.automaton_type + ")"))
        lines.append(profile.description)
        for group in profile.groups:
            kind = "required"
            if not group.required:
                kind = "optional"
            lines.append("  " + group.name.ljust(20) + kind.ljust(10) + ", ".join(group.tokens))
    return "\n".join(lines)


def analyze_and_offer_save(result, base_name, ask):
    print(format_report(result, details=True))
    answer = ask("\nSave JSON, DSL and HTML in data/output? (y/n): ")
    if answer.strip().lower() == "y":
        for path in save_outputs(result, base_name):
            print("saved", path)


def read_pasted_text(ask):
    print("Paste the resume. Write END in a new line to finish.")
    lines = []
    while True:
        line = ask("")
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def interactive_menu(ask=input):
    while True:
        print(title("ResumeLens - formal language based resume screening"))
        print("1. Analyze a sample resume")
        print("2. Analyze a resume file")
        print("3. Paste a resume")
        print("4. Show the four profiles")
        print("5. Exit")
        option = ask("Choose an option: ").strip()

        if option == "1":
            samples = list_samples()
            for number in range(len(samples)):
                print(str(number + 1) + ". " + samples[number])
            choice = ask("Sample number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(samples):
                name = samples[int(choice) - 1]
                result = run_resume_file(os.path.join(SAMPLES_DIR, name))
                analyze_and_offer_save(result, name.replace(".txt", ""), ask)
            else:
                print("Invalid sample number.")
        elif option == "2":
            path = ask("Path of the file: ").strip()
            if os.path.isfile(path):
                base_name = os.path.splitext(os.path.basename(path))[0]
                analyze_and_offer_save(run_resume_file(path), base_name, ask)
            else:
                print("File not found: " + path)
        elif option == "3":
            result = run_resume_pipeline(read_pasted_text(ask))
            analyze_and_offer_save(result, "pasted_resume", ask)
        elif option == "4":
            print(show_profiles())
        elif option == "5":
            print("Bye!")
            return
        else:
            print("Invalid option.")


def short_status(accepted):
    if accepted:
        return "ACCEPTED"
    return "-"


def run_batch(folder=SAMPLES_DIR, output_folder=OUTPUT_DIR):
    # Runs every .txt resume of a folder, saves its outputs and returns a summary table
    profile_names = list(PROFILES.keys())
    header = "Resume".ljust(36)
    for name in profile_names:
        header = header + PROFILES[name].display_name.split(" ")[0].ljust(12)
    header = header + "DSL"
    lines = [header, "-" * len(header)]

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue
        result = run_resume_file(os.path.join(folder, filename))
        save_outputs(result, filename.replace(".txt", ""), output_folder)

        row = filename.ljust(36)
        for name in profile_names:
            row = row + short_status(result.classification[name]).ljust(12)
        if result.error is None:
            row = row + "valid"
        else:
            row = row + "rejected (" + result.error.kind.lower() + ")"
        lines.append(row)
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(description="ResumeLens: formal language based resume screening")
    parser.add_argument("resume_path", nargs="?", default=None, help="resume text file (without it, the interactive menu opens)")
    parser.add_argument("--all", action="store_true", help="analyze every sample resume and save the outputs in data/output")
    parser.add_argument("--details", action="store_true", help="show every transducer step and the generated DSL")
    parser.add_argument("--save", action="store_true", help="save the JSON, DSL and HTML in data/output")
    parser.add_argument("--output-html", default=None, help="save the HTML report in this path")
    return parser


def main(arguments=None):
    args = build_parser().parse_args(arguments)
    if args.all:
        print(run_batch())
        print("\nOutputs saved in " + OUTPUT_DIR)
        return 0

    if args.resume_path is None:
        interactive_menu()
        return 0

    if not os.path.isfile(args.resume_path):
        print("File not found: " + args.resume_path)
        return 1

    result = run_resume_file(args.resume_path)
    print(format_report(result, details=args.details))

    base_name = os.path.splitext(os.path.basename(args.resume_path))[0]
    if args.save:
        for path in save_outputs(result, base_name):
            print("saved", path)
    if args.output_html:
        if result.html == "":
            print("No HTML: the candidate profile is not valid.")
        else:
            print("saved", save_text(args.output_html, result.html))
    return 0


if __name__ == "__main__":
    main()
