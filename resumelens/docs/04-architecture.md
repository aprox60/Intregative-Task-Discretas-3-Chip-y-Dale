# Architecture

## Overview

This project uses a staged pipeline with explicit operations on strings, canonical tokens, automata, and a domain-specific language.

## Component diagram

```mermaid
flowchart TD
    A[Raw résumé text] --> B[Stage 1: Regex extraction]
    B --> C[Stage 2: FST normalization]
    C --> D[Stage 3: Automata classification]
    D --> E[Stage 4: textX DSL validation]
    E --> F[HTML / Markdown visualization]

    B --> G[Extracted evidence JSON]
    C --> H[Canonical skill tokens]
    D --> I[Accepted / rejected profile decisions]
    E --> J[Validated candidate model]
```

## Responsibilities

- Stage 1 extracts concrete evidence using regular expressions.
- Stage 2 resolves lexical variants and enforces canonical ordering.
- Stage 3 matches explicit qualification patterns against profile automata.
- Stage 4 validates the structured output and renders it visually.

## Design constraints

- No ranking logic is included.
- No hiring decisions are made.
- The system is intentionally pattern-based and transparent.

## TODO
- Add more detailed data-flow diagrams once the final profile requirements are chosen.
- Export a graph of the transducer and automata to `docs/diagrams/` as image files.
