# Test Cases

All tests are automated with **pytest** and run with `python -m pytest` from the `resumelens` folder. There is one test file per stage, plus end-to-end and interface tests.

| File | Tests | What it covers |
|---|---|---|
| `tests/test_extraction.py` | 22 | stage 1: every regular expression, false positives, sample résumés |
| `tests/test_normalization.py` | 6 | stage 2: assignment transformations, our transformations, sorting |
| `tests/test_transducers.py` | 12 | stage 2: structure of the transducers (7-tuple, determinism, trie, end mark) |
| `tests/test_classification.py` | 19 | stage 3: automaton types, accepted/rejected sequences, samples |
| `tests/test_dsl.py` | 17 | stage 4: valid documents, lexical, syntax and semantic errors |
| `tests/test_pipeline_e2e.py` | 7 | the four stages together, from text to HTML |
| `tests/test_cli.py` | 10 | the user interface (arguments, saving, interactive menu) |
| `tests/test_batch.py` | 4 | batch mode: every sample, expected summary, saved files |

## Sample résumés (`data/sample_resumes/`)

| File | Scenario | Expected result |
|---|---|---|
| `wednesday_addams.txt` | example from the assignment | Full Stack **ACCEPTED**, others rejected |
| `mary_jane_watson.txt` | example from the assignment | ML Engineer **ACCEPTED**, others rejected |
| `alex_rivera_backend.txt` | our software profile | Backend Developer **ACCEPTED**, others rejected |
| `nina_patel_data_scientist.txt` | our AI/data profile | Data Scientist **ACCEPTED**, others rejected |
| `kim_possible_multi_profile.txt` | one résumé, two patterns | Full Stack **and** Backend **ACCEPTED** |
| `invalid_missing_qualification.txt` | ML-like candidate without Git, Data Science-like without visualization | all **REJECTED** (`missing: VERSION_CONTROL`) |
| `invalid_edge_case.txt` | no name, an invalid email, `Skills: ???` | all **REJECTED**; the generated DSL is **rejected by the grammar** (no email) |

## Scenarios by stage

### Stage 1: extraction (regular expressions)

| # | Scenario | Input | Expected |
|---|---|---|---|
| E1 | Assignment fragment | `Technical Skills: JS, React.js, NodeJS, Postgres, Git.` | `JS, React.js, NodeJS, Postgres, Git` in that order |
| E2 | Spelling variants of each category | `Javascript`, `Java Script`, `C#`, `Spring Boot`, `Tensor Flow`, `k8s`, `REST APIs`... | each one found exactly once |
| E3 | Ambiguous short names are not ordinary words | `I want to go home`, `R&D department`, `the rest of the team` | nothing found |
| E4 | Overlapping names | `JavaScript`, `REST APIs`, `NoSQL`, `Node.JS` | only `JavaScript`, only `REST APIs`, nothing, no `JS` |
| E5 | Tool name inside a URL | `github.com/arivera` | not a tool, but a link |
| E6 | Contact data | `+57 300 123 4567`, `(602) 555-0187`, `not-an-email`, `2019-2023` | the two phones; no email; the date is not a phone |
| E7 | Education and experience | `BSc in Software Engineering at Universidad Icesi.` / `5+ years of professional experience in backend services.` | degree, field and institution; 5 years + description |
| E8 | Unknown skill | `Skills: Python, Haskell, SQL.` | `Haskell` reported as unrecognized |
| E9 | Output file | `save_json` | JSON containing the raw strings |

### Stage 2: normalization (transducers and sorting)

| # | Scenario | Input | Expected |
|---|---|---|---|
| N1 | Assignment transformations | `JS`, `Javascript`, `React.js`, `ReactJS`, `NodeJS`, `Node.js`, `Postgres`, `sklearn`, `scikit learn`, `Scikit-learn`, `Tensor Flow`, `PyTorch` | the canonical tokens of the assignment |
| N2 | Our transformations | `C#`, `Golang`, `.NET`, `GitHub`, `k8s`, `Power BI`, `RESTful APIs`, `statistical analysis` | `CSHARP`, `GO`, `DOTNET`, `GIT`, `KUBERNETES`, `POWER_BI`, `REST_API`, `STATISTICS` |
| N3 | Rejection | `Haskell` as a language, `React` as a database, `Café` | `None` (rejected) |
| N4 | Prefix and extension of a variant | `postgre`, `reac`, `reactnative` | rejected |
| N5 | Duplicates | `JavaScript, JS, React, ReactJS, Git, GitHub` | `JAVASCRIPT, REACT, GIT` |
| N6 | Structure | every category transducer | deterministic; output only on `$`; one transducer per category; shared prefixes |
| N7 | Sorting (assignment example) | `GIT, NODE_JS, JAVASCRIPT, POSTGRESQL, REACT` | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` |
| N8 | Projection | `GIT, PYTHON, DOCKER, PANDAS` for ML | `PYTHON, PANDAS, GIT` (DOCKER is not in the ML alphabet) |

### Stage 3: classification (automata)

| # | Scenario | Input sequence | Profile | Expected |
|---|---|---|---|---|
| C1 | Assignment example | `PYTHON PANDAS TENSORFLOW POSTGRESQL GIT` | ML | ACCEPTED |
| C2 | Assignment example | `JAVASCRIPT REACT NODE_JS POSTGRESQL GIT` | Full Stack | ACCEPTED |
| C3 | Several tokens per group | `PYTHON PANDAS NUMPY SCIKIT_LEARN TENSORFLOW PYTORCH SQL GIT` | ML | ACCEPTED |
| C4 | Missing required group | `PYTHON PANDAS TENSORFLOW POSTGRESQL` | ML | REJECTED, missing `VERSION_CONTROL` |
| C5 | Optional group present / absent (ε) | with and without `REST_API` | Full Stack | ACCEPTED both |
| C6 | Optional ML library absent (ε) | `R PANDAS STATISTICS TABLEAU SQL` | Data Scientist | ACCEPTED |
| C7 | Required group of our profile | without `DOCKER` / with `DOCKER` | Backend | REJECTED / ACCEPTED |
| C8 | Wrong order | `GIT NODE_JS JAVASCRIPT POSTGRESQL REACT` | Full Stack | REJECTED |
| C9 | Symbol outside Σ | `... DOCKER ...` | ML | REJECTED |
| C10 | Empty sequence | `ε` | all | REJECTED |
| C11 | Automaton types | — | all | ML is a deterministic DFA, Backend an NFA, Full Stack and Data Scientist ε-NFAs, and only those have ε-transitions |
| C12 | Equivalence | NFA and DFA built from the same groups | — | `is_equivalent_to` is true |

### Stage 4: DSL (textX)

| # | Scenario | Change to a valid document | Expected |
|---|---|---|---|
| D1 | Valid document | — | parsed; every field reachable in the model |
| D2 | Repetition | two `experience` blocks | accepted |
| D3 | Optional parts | no phone, no links | accepted |
| D4 | Comments | `// ...` line | ignored |
| D5 | Lexical error | `email: wednesday-nevermore` | Lexical error, line 3 |
| D6 | Lexical error | `skills { javascript }` / `years: three` | Lexical error |
| D7 | Syntax error | no `email` line | Syntax error "Expected 'email'" |
| D8 | Syntax error | `skills [ ... ]`, status `MAYBE`, unknown profile, empty evaluation, sections out of order | Syntax error |
| D9 | Semantic error | `candidate ""` | Semantic error |
| D10 | Semantic error | `REACT, REACT` | Semantic error (repeated skill) |
| D11 | Semantic error | `years: 99` | Semantic error (more than 60) |
| D12 | Semantic error | the same profile twice | Semantic error, line 19 |

### End to end and interface

| # | Scenario | Expected |
|---|---|---|
| P1 | Wednesday through the four stages | the exact intermediate results of the assignment, valid DSL, HTML with her name |
| P2 | Every sample with an email | generated DSL accepted by the grammar |
| P3 | Model keeps all the data | email, phone, link, years, institution, skills and each status read back from the textX model |
| P4 | Edge case | DSL rejected → no model, no HTML |
| P5 | HTML | one badge per profile; `<script>` in the résumé is escaped |
| P6 | Quotes in values | `"big data"` does not break the DSL |
| U1 | Report | shows the four stages, the automaton type and the missing groups |
| U2 | Saving | `.json`, `.resume` and `.html` written; `--output-html` works |
| U3 | Menu | analyze a sample, paste a résumé, list profiles, invalid option, exit |
| U4 | Batch mode (`--all`) | one row per sample with the expected results; `.json` and `.resume` for all of them, `.html` only when the DSL is valid |
