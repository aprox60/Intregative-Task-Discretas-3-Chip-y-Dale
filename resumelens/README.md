# ResumeLens: Formal Language-Based Resume Screening

ResumeLens reads plain-text résumés and checks whether the qualifications written in them satisfy the qualification pattern of four professional profiles. Each step uses a formal model from *Computación y Estructuras Discretas III*:

| Stage | Formal model | Library |
|---|---|---|
| 1. Extraction | regular expressions | `re` |
| 2. Normalization | finite-state transducers | `pyformlang` |
| 3. Classification | DFA, NFA and ε-NFA | `pyformlang` |
| 4. Candidate profile language | context-free grammar (DSL) | `textX` |

ResumeLens **does not rank candidates or make hiring decisions**. It only reports whether explicit qualifications match formally defined patterns.

## Team and environment

- **Team:** Ivan Quintero Sanchez, Valeria Valencia
- **Course:** Computación y Estructuras Discretas III, Universidad Icesi, 2026-2
- **IDE:** Visual Studio Code
- **Language:** Python 3.11+ (developed with Python 3.12)

## Profiles

| Profile | Area | Automaton | Pattern (in order; *optional*) |
|---|---|---|---|
| Full Stack Developer | software | ε-NFA | frontend language → frontend framework → backend → database → *API* → Git |
| Machine Learning Engineer | AI/data | DFA | Python → Pandas/NumPy → ML framework → database → Git |
| **Backend Developer** (ours) | software | NFA | language → backend framework → database → REST/GraphQL → Docker/Kubernetes → Git |
| **Data Scientist** (ours) | AI/data | ε-NFA | Python/R → Pandas/NumPy → statistics → visualization → *scikit-learn* → database |

The profiles are JSON files in `src/resumelens/profiles/`.

## Setup

From the `resumelens` folder:

```bash
python -m venv .venv
```

Activate it (Windows PowerShell: `.\.venv\Scripts\Activate.ps1`, Git Bash: `source .venv/Scripts/activate`, Linux/macOS: `source .venv/bin/activate`), then:

```bash
pip install -r requirements.txt
```

```bash
pip install -e .
```

`pip install -e .` installs the package in editable mode, so `python -m resumelens` works from any folder. Without it, set `PYTHONPATH=src` before running.

## Usage

Interactive menu (analyze a sample, a file or pasted text, and see the profiles):

```bash
python -m resumelens
```

Analyze one résumé:

```bash
python -m resumelens data/sample_resumes/wednesday_addams.txt
```

Options:

| Option | Effect |
|---|---|
| `--details` | shows every transducer step (`React.js → reactjs → REACT`) and the generated DSL |
| `--save` | saves the extraction JSON, the DSL (`.resume`) and the HTML in `data/output/` |
| `--output-html PATH` | saves only the HTML report in `PATH` |

Example output (shortened):

```text
Stage 2 - Normalization (finite-state transducers)
Canonical tokens: JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT

Stage 3 - Classification (finite automata)
Full Stack Developer [ENFA]: ACCEPTED
    sequence: JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
Machine Learning Engineer [DFA]: REJECTED
    sequence: POSTGRESQL, GIT
    missing:  LANGUAGE, DATA_LIBRARY, ML_FRAMEWORK
...
Stage 4 - Candidate profile DSL (textX)
The candidate profile is VALID for the grammar.
```

## Tests

```bash
python -m pytest
```

There is one test file per stage, plus end-to-end and interface tests. See [docs/03-test-cases.md](docs/03-test-cases.md).

## Regenerating the formal definitions and diagrams

The 7-tuples of the transducers, the 5-tuples of the automata and their Mermaid diagrams in `docs/diagrams/` are generated from the pyformlang objects:

```bash
python -m resumelens.docs_export
```

## Documentation

| Document | Content |
|---|---|
| [00-literature-review.md](docs/00-literature-review.md) | literature review and how it shaped the design |
| [01-module-design.md](docs/01-module-design.md) | modules, functions, inputs and outputs |
| [02-formalization.md](docs/02-formalization.md) | regular expressions, transducers (7-tuples), automata (5-tuples), grammar (EBNF) |
| [03-test-cases.md](docs/03-test-cases.md) | test design and scenarios |
| [04-architecture.md](docs/04-architecture.md) | pipeline diagram, folder structure, design decisions |
| [05-presentation-outline.md](docs/05-presentation-outline.md) | outline of the 10-minute presentation |
| [poster/poster-outline.md](docs/poster/poster-outline.md) | content of the research poster |
| [diagrams/](docs/diagrams/README.md) | generated formal definitions and diagrams |

## Project structure

```text
resumelens/
├── src/resumelens/
│   ├── extraction/        stage 1 - regular expressions
│   ├── normalization/     stage 2 - transducers and canonical order
│   ├── classification/    stage 3 - automata
│   ├── profiles/          the four profiles (JSON)
│   ├── dsl/               stage 4 - textX grammar, generator, HTML
│   ├── ui/                command line interface
│   ├── models.py
│   ├── pipeline.py
│   └── docs_export.py
├── data/sample_resumes/   example résumés
├── data/output/           generated JSON, DSL and HTML
├── docs/                  design documents
└── tests/
```
