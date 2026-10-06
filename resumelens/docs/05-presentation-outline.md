# Presentation Outline (10 minutes)

## Slide 1 — Problem
- Goal: formal-language-based résumé screening.
- The task is not to rank candidates; it is to check explicit qualification patterns.
- The system accepts or rejects based on the presence of formal qualification sequences.

## Slide 2 — Methodology and formal models
- Regex extraction for local lexical detection.
- FST normalization for canonical skill mapping.
- Finite automata for profile matching.
- textX grammar for candidate validation and structured representation.

## Slide 3 — Regex stage
- Why regular expressions are adequate for retrieving emails, URLs, skills, and experience values.
- Why this stage does not make equivalence decisions.

## Slide 4 — FST stage
- Canonicalization examples: `JS -> JAVASCRIPT`, `NodeJS -> NODE_JS`, `Postgres -> POSTGRESQL`.
- Explanation of the 7-tuple and lexicon-driven design.

## Slide 5 — Automata stage
- Formal sequence pattern for ML and Full Stack profiles.
- Why NFA representations are convenient for sets of possible tokens.
- Accepted/rejected classification examples.

## Slide 6 — DSL stage
- Grammar for candidate metadata, skills, experiences, education, and classification result.
- Validation approach with lexical and syntactic checks.
- Short explanation of the structural characteristics of the textX language.

## Slide 7 — Results with examples
- Example detection from raw skills: `JS, React.js, NodeJS, Postgres, Git`.
- Example normalization and sorting sequence.
- Example acceptance/rejection of a profile.

## Slide 8 — Design decisions
- Alphabet abstraction and tokenization.
- Why ordering is canonical before automata recognition.
- Why profile matching is pattern-based and traceable.

## Slide 9 — Limitations and future work
- The system is transparent but limited to explicit qualifications.
- It does not infer soft skills or subjective quality.
- More advanced profiles and richer grammars can be added later.

## Slide 10 — Closing
- Summary of the formal-language pipeline.
- Emphasize the assignment’s requirement: explicit pattern checking, not hiring decisions.

> Note: The PDF's presentation section mentions a "security problem in code repositories" as a copy-paste leftover from another assignment. This project is about résumé screening. The design and examples below therefore focus on formal résumé screening instead.

## TODO
- Insert final team names and actual examples once the project is implemented.
