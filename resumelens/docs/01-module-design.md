# Module Design

## Overview

The project follows a four-stage pipeline:

Raw résumé text -> Regex extraction -> FST normalization -> Automata classification -> textX validation + visualization.

Each stage is separated into its own module with a clear contract.

## 1. Extraction module

### Files
- `src/resumelens/extraction/patterns.py`
- `src/resumelens/extraction/extractor.py`

### Responsibility
Extract candidate evidence from raw résumé text using regular expressions. The extractor records raw matches and their categories but does not decide whether they satisfy a niche profile.

### Main functions
- `build_pattern_catalog() -> dict[str, re.Pattern[str]]`
- `extract_skills(text: str) -> list[str]`
- `extract_contact_info(text: str) -> dict[str, list[str]]`
- `extract_academic_qualifications(text: str) -> list[str]`
- `extract_experience(text: str) -> list[str]`
- `extract_candidate_evidence(text: str) -> dict[str, list[str]]`

### Input
- Raw text from a résumé file.

### Output
- A structured dictionary with extracted values for contact data, skills, qualifications, and experience.

## 2. Normalization module

### Files
- `src/resumelens/normalization/lexicon.py`
- `src/resumelens/normalization/transducers.py`
- `src/resumelens/normalization/sorter.py`

### Responsibility
Map extracted strings to canonical tokens. This stage preserves semantics but removes variants such as `JavaScript`, `Javascript`, and `JS`.

### Main functions
- `build_lexicon() -> dict[str, str]`
- `normalize_token(token: str, lexicon: dict[str, str]) -> str`
- `normalize_tokens(tokens: list[str]) -> list[str]`
- `sort_tokens(tokens: list[str], profile_name: str) -> list[str]`

### Input
- Extracted strings from stage 1.

### Output
- Canonical skill tokens in a stable, profile-aware order.

## 3. Classification module

### Files
- `src/resumelens/classification/profiles.py`
- `src/resumelens/classification/automata.py`
- `src/resumelens/classification/classifier.py`

### Responsibility
Check whether a normalized token sequence satisfies the explicit pattern of each profile.

### Main functions
- `build_profile_automaton(profile_config: dict) -> NFA | DFA`
- `classify(tokens: list[str], profile_name: str) -> bool`
- `classify_all_profiles(tokens: list[str]) -> dict[str, bool]`

### Input
- Sorted canonical tokens.

### Output
- Acceptance/rejection result per profile, without ranking or hiring decisions.

## 4. DSL module

### Files
- `src/resumelens/dsl/resume.tx`
- `src/resumelens/dsl/parser.py`
- `src/resumelens/dsl/validator.py`
- `src/resumelens/dsl/generator.py`
- `src/resumelens/dsl/visualizer.py`

### Responsibility
Validate a candidate model using a textual DSL and render a small HTML page from the accepted output.

### Main functions
- `parse_resume_text(text: str) -> Model`
- `validate_resume_model(model: object) -> None`
- `candidate_to_dsl(candidate: Candidate) -> str`
- `render_html(candidate: Candidate) -> str`

### Input
- Pipeline result object containing normalized skills, profile decisions, and candidate metadata.

### Output
- A structured validated DSL model and a generated HTML visualization.

## Data model

### Files
- `src/resumelens/models.py`

The project defines dataclasses for candidate information, extracted items, and classification results.

### Core dataclasses
- `ExtractedItem`
- `Candidate`
- `ProfileResult`
- `PipelineResult`

## Pipeline orchestrator

### File
- `src/resumelens/pipeline.py`

### Responsibility
Coordinate the entire process from raw text to validated output. It exposes a single high-level entry point used by both tests and CLI.

### Main function
- `run_resume_pipeline(text: str, profile_name: str | None = None) -> PipelineResult`

## TODO
- Expand the profile schema for PROFILE_3_TODO and PROFILE_4_TODO.
- Add more explicit type contracts for DSL validation errors and HTML rendering output.
