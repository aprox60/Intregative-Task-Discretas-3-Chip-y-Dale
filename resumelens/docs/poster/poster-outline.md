# Poster Outline

## 1. Problem

Résumé screening often depends on ambiguous interpretation or manual review. In this project, the goal is to formalize the matching process using explicit language models and deterministic validation.

## 2. Formal models

- Regular expressions for evidence extraction.
- Finite-state transducers for canonical normalization.
- Finite automata for profile-language recognition.
- textX grammar for candidate validation and serialization.

## 3. Architecture

The system follows a four-stage pipeline: extraction, normalization, classification, and DSL validation/visualization.

## 4. Results

- Demonstrated extraction of skills and qualifications from raw résumé text.
- Canonicalization of common skill variants.
- Classification results for four profile templates.
- HTML rendering of the validated candidate output.

## 5. Limitations

- The system validates explicit qualification patterns only.
- It does not infer latent expertise or solve subjective hiring decisions.
- The profile templates for the last two roles are intentionally left as placeholders for future completion.

## TODO
- Add final design diagrams and screenshots.
- Add a brief result summary when the project is tested.
- Replace placeholder team information with actual names.
