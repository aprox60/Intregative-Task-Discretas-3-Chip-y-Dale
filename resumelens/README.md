# ResumeLens: Formal Language-Based Resume Screening

This project is a university skeleton for the ICESI 2026-2 Integrative Task 1 in Computación y Estructuras Discretas III. The objective is to build a formal-language pipeline that checks whether an explicit qualification pattern is present in a résumé, without ranking candidates or making hiring decisions.

## Team and environment
- IDE: Visual Studio Code
- Team members: Ivan Quintero Sanchez, Valeria Valencia
- Course: Computación y Estructuras Discretas III
- Institution: ICESI
- Academic period: 2026-2

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   On Windows:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the CLI:
   ```bash
   python -m resumelens.ui.cli --help
   ```
4. Run the tests:
   ```bash
   pytest
   ```

## How to run the sample pipeline

From the project root:

```bash
PYTHONPATH=src python -m resumelens.ui.cli data/sample_resumes/wednesday_addams.txt --profile all
```

The CLI reads the raw résumé text, extracts strings, normalizes them to canonical tokens, classifies them according to profile automata, and optionally emits a DSL-formatted candidate model plus HTML output.

## Delivery constraints (do not execute)

- At least 10 meaningful commits, spaced at least 2 hours apart.
- Contributions must be traceable per team member via commit history.
- Team size: 2 members.
- Deadline: 11 October 2026.

See `docs/commit-plan.md` for a suggested commit sequence.

## Project structure

```text
resumelens/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── docs/
├── src/resumelens/
├── data/
├── tests/
└── .pytest_cache/  # ignored by git
```

## Notes

This repository intentionally contains a skeleton and a minimal smoke-tested reference pipeline, not a finished production system. The design is formal-language-oriented and pattern-based, consistent with the assignment requirements.
