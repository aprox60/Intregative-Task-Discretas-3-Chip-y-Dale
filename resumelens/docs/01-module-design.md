# Module Design

ResumeLens is a pipeline of four stages. Each one uses a different formal model and lives in its own package. Every stage reads only the output of the previous one, so each one can be tested on its own.

```text
resume text ─► extraction ─► normalization ─► classification ─► dsl ─► HTML
                 (regex)       (FST + sort)       (automata)      (CFG)
```

## Data model (`src/resumelens/models.py`)

| Class | Fields | Produced by |
|---|---|---|
| `Education` | `degree`, `field`, `institution` | extraction |
| `Experience` | `years`, `description` | extraction |
| `ExtractionResult` | `name`, `emails`, `phones`, `links`, six technical lists (`programming_languages`, `frameworks`, `libraries`, `databases`, `tools`, `other_qualifications`), `education`, `experience`, `skills_section` | extraction |
| `PipelineResult` | `extraction`, `normalization`, `sorted_by_profile`, `classification`, `dsl_text`, `model`, `html`, `error` | pipeline |

`ExtractionResult` methods: `get_technical_items()`, `get_all_technical_strings()`, `get_unrecognized_skills()`, `to_dict()`, `to_json()`.
`PipelineResult` methods: `get_accepted_profiles()`.

## 1. Extraction: regular expressions (`extraction/`)

| Function | Input | Output |
|---|---|---|
| `patterns.py` (module) | — | compiled regexes: `NAME_REGEX`, `EMAIL_REGEX`, `PHONE_REGEX`, `URL_REGEX`, `TECHNICAL_REGEXES` (category → list of regexes), `EDUCATION_REGEX`, `EXPERIENCE_REGEX`, `SKILLS_SECTION_REGEX`, and `DESCRIPTIONS` |
| `find_all(regex, text)` | regex, text | list of matched strings without repetitions |
| `find_all_in_order(regexes, text)` | several regexes, text | matches in text order; a match inside a longer one is dropped |
| `extract_name(text)` | text | first line if it looks like a name, else `""` |
| `extract_education(text)` | text | `list[Education]` |
| `extract_experience(text)` | text | `list[Experience]` |
| `extract_skills_section(text)` | text | items written after `Skills:` |
| `extract_resume(text)` | text | `ExtractionResult` |
| `ResumeExtractor(text)` | text | `.extract()`, `.to_json()`, `.save_json(path)`, `ResumeExtractor.from_file(path)` |

## 2. Normalization: finite-state transducers (`normalization/`)

| Function | Input | Output |
|---|---|---|
| `variants.py` (module) | — | `VARIANTS_BY_CATEGORY`: category → {preprocessed variant → canonical token} |
| `Transducer` | — | wrapper around `pyformlang.fst.FST` that also stores Q, Σ, Γ, δ/ω, q0 and F |
| `build_preprocessing_transducer()` | — | the one-state transducer that lower-cases and deletes separators |
| `build_category_transducer(category, variants)` | name, variants | trie transducer that writes the canonical token on `$` |
| `preprocess(text)` | raw string | preprocessed string, or `None` if rejected |
| `canonicalize(word, category)` | preprocessed string, category | canonical token, or `None` |
| `normalize_string(raw, category)` | raw string, category | canonical token, or `None` |
| `normalize_extraction(extraction)` | `ExtractionResult` | `NormalizationResult` (`tokens`, `steps`, `unknown`) |
| `sort_for_profile(tokens, profile)` | tokens, `Profile` | the profile's tokens in canonical order |
| `sort_for_all_profiles(tokens, profiles)` | tokens, profiles | profile name → sorted sequence |

## 3. Classification: finite automata (`classification/` and `profiles/`)

| Function | Input | Output |
|---|---|---|
| `profiles/*.json` | — | one file per profile: `name`, `display_name`, `area`, `automaton_type`, `description`, ordered `groups` (`name`, `tokens`, `required`) |
| `load_profile(path)` | JSON path | `Profile`; checks disjoint groups and that optional groups only appear in ENFAs |
| `load_profiles()` / `PROFILES` | — | the four profiles in project order |
| `ProfileAutomaton(profile)` | `Profile` | pyformlang DFA, NFA or ε-NFA plus its 5-tuple; `.accepts(tokens)`, `.missing_groups(tokens)` |
| `build_automata(profiles)` / `AUTOMATA` | profiles | profile name → `ProfileAutomaton` |
| `classify(tokens, profile_name)` | sorted tokens, name | `True` / `False` |
| `classify_all_profiles(sorted_by_profile)` | name → sequence | name → `True` / `False` |
| `status_text(accepted)` | bool | `"ACCEPTED"` / `"REJECTED"` |

## 4. Candidate profile DSL: context-free grammar (`dsl/`)

| Function | Input | Output |
|---|---|---|
| `resume.tx` | — | textX grammar of the candidate profile language |
| `generate_dsl(extraction, tokens, classification)` | results of stages 1–3 | DSL text |
| `parse_dsl(text)` | DSL text | textX model, or raises `ResumeValidationError(kind, message, line, column)` |
| `is_valid(text)` | DSL text | `True` / `False` |
| `render_html(model)` | validated textX model | HTML page |

## Pipeline (`pipeline.py`)

| Function | Input | Output |
|---|---|---|
| `run_resume_pipeline(text)` | résumé text | `PipelineResult` |
| `run_resume_file(path)` | path to a `.txt` résumé | `PipelineResult` |

## User interface (`ui/cli.py`, `__main__.py`)

| Function | Input | Output |
|---|---|---|
| `main(arguments)` | command-line arguments | runs one résumé, or opens the menu when no file is given |
| `interactive_menu(ask)` | input function | menu: analyze a sample, analyze a file, paste a résumé, show profiles |
| `format_report(result, details)` | `PipelineResult` | stage-by-stage text report |
| `save_outputs(result, base_name, folder)` | result, name | writes `.json`, `.resume` (DSL) and `.html` |
| `show_profiles()` | — | text with the groups of each profile |

## Documentation export (`docs_export.py`)

| Function | Output |
|---|---|
| `export_transducers()` | `docs/diagrams/transducers/*.md`: 7-tuple and Mermaid diagram of each transducer |
| `export_automata()` | `docs/diagrams/automata/*.md`: 5-tuple and Mermaid diagram of each automaton |
