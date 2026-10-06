# Literature Review

## 1. Résumé parsing and information extraction

Résumé parsing is a specialized information extraction problem in which unstructured natural-language documents are converted into structured fields. In practice, résumé processing often combines lightweight rule-based techniques with named-entity recognition (NER) and domain-specific heuristics. For academic tasks such as this one, the emphasis is on explicit pattern compliance rather than semantic ranking.

### Key questions
- What information should be extracted from the document?
- How should the system handle abbreviations, symbols, and punctuation?
- How can we separate raw evidence from profile-specific suitability decisions?

### TODO
- Add relevant course and assignment references.
- Add academic sources on résumé parsing and CV information extraction.

## 2. NER vs. regular-expression extraction

Named-entity recognition is useful when broad categories such as email, skills, and organizations must be detected from general text. However, the assignment intentionally constrains the extraction stage to regular expressions. This provides a deterministic, explainable mechanism and makes formal-language reasoning explicit.

### Design choice in this project
- Regex extraction is used for local pattern recognition.
- It does not decide equivalence classes or profile fit.
- Normalization and classification are separated into later formal stages.

### TODO
- Add relevant references on regex-based extraction and NER comparisons.

## 3. FSTs in text normalization

Finite-state transducers are well suited to normalization because they map strings from one alphabet to another while preserving lexical structure. In this project, the transducer is used to rewrite skill variants into canonical tokens such as `JS -> JAVASCRIPT` and `NodeJS -> NODE_JS`.

### Why FSTs here?
- Case-insensitive input treatment.
- Deterministic canonicalization.
- Explicit formal model with a well-defined input/output alphabet.

### TODO
- Add references to finite-state transducer literature and practical uses in text normalization.

## 4. Automata for pattern recognition

Automata are a natural fit for profile matching because a profile specification can be expressed as a language of acceptable qualification sequences. The project treats the problem as one of checking whether the normalized token stream belongs to a target language.

### Key observations
- A profile can be modeled as a DFA or ε-NFA depending on the pattern structure.
- The automaton is used to validate explicit qualification ordering and required expertise combinations.
- Classification should not entail ranking or hiring decisions.

### TODO
- Add references on formal-language approaches to pattern checking and automata classification.

## 5. DSLs and textX

Domain-specific languages allow structured representation of a résumé candidate model. textX is well suited to formalizing the grammar because it supports clear syntax, lexical rules, validation, and model generation. The DSL here is used after classification, to validate the candidate structure and generate a human-readable HTML or Markdown output.

### TODO
- Add references on domain-specific languages, model-driven engineering, and textX.

## References

- TODO: add literature references to résumé parsing, regular-expression extraction, FSTs, automata, and textX.
- TODO: add academic articles or books.
- TODO: add course materials or assignment readings.
