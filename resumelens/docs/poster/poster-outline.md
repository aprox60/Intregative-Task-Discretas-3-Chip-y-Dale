# Research Poster: Content

Text and figures for the poster, section by section. Figures marked 🖼 are already in the repository and can be exported from GitHub (the Mermaid diagrams render there) or from the generated HTML.

---

## Title

**ResumeLens: Screening Résumés with Regular Expressions, Transducers, Automata and Grammars**

Ivan Quintero Sanchez · Valeria Valencia
Computación y Estructuras Discretas III, Universidad Icesi, 2026-2

---

## 1. Problem

Recruiters read many résumés that describe the same skills in different ways: *JS*, *Javascript* and *JavaScript*; *sklearn* and *Scikit-learn*; *Postgres* and *PostgreSQL*. Deciding whether a résumé contains the qualifications of a profile means **finding** the information, **unifying** its spelling, **checking** it against a pattern and **reporting** it in a fixed structure.

**Research question:** can each of these steps be modeled with a formal language model, so that every decision is explicit and explainable?

> ResumeLens does not rank candidates or make hiring decisions. It only checks whether explicit qualifications satisfy formally defined patterns.

## 2. Objectives

- Extract candidate information with **regular expressions**.
- Normalize equivalent spellings with **finite-state transducers**.
- Recognize the qualification pattern of 4 profiles with **finite automata** (DFA, NFA, ε-NFA).
- Represent and validate the result with a **context-free grammar** (textX DSL).

## 3. Methodology

🖼 *Pipeline diagram:* `docs/04-architecture.md`

| Stage | Model | Input → Output | Example |
|---|---|---|---|
| 1 | Regular expressions | text → raw strings | `Technical Skills: JS, React.js, NodeJS` → `JS`, `React.js`, `NodeJS` |
| 2 | FST $M=(Q,\Sigma,\Gamma,\delta,\omega,q_0,F)$ | raw string → canonical token | `Scikit-learn` →(M_pre)→ `scikitlearn` →(M_libraries)→ `SCIKIT_LEARN` |
| 2b | Canonical order | tokens → sorted sequence per profile | `GIT NODE_JS JAVASCRIPT POSTGRESQL REACT` → `JAVASCRIPT REACT NODE_JS POSTGRESQL GIT` |
| 3 | Automata $M=(Q,\Sigma,\delta,q_0,F)$ | sequence → ACCEPTED / REJECTED | Full Stack ε-NFA accepts the sequence above |
| 4 | CFG (textX) | results → validated DSL → HTML | `candidate "Wednesday Addams" { contact {...} skills {...} evaluation {...} }` |

**Profiles (2 given, 2 ours)**

| Profile | Automaton | Why that type |
|---|---|---|
| Full Stack Developer | ε-NFA | optional API group, skipped with ε |
| Machine Learning Engineer | DFA | plain sequence of required groups |
| Backend Developer *(ours)* | NFA | "one or more" written as $G^*G$: δ(q, t) = {q, q'} |
| Data Scientist *(ours)* | ε-NFA | optional scikit-learn group |

🖼 *Automaton diagram:* `docs/diagrams/automata/full_stack_developer.md`
🖼 *Transducer diagram (GIT part):* section 2.2 of `docs/02-formalization.md`

## 4. Key design decisions

- **Two transducers in sequence.** A one-state normalizer (case, separators) followed by a trie per category. The end mark `$` keeps them deterministic.
- **Sort first, then recognize.** Sorting turns "all groups in any order" ($2^n$ states) into a chain of $n+1$ states.
- **Profiles are data.** Four JSON files, one shared automaton builder: the same software for every profile.
- **Grammar for structure, object processors for meaning.** Lexical, syntactic and semantic errors are reported separately.

## 5. Results

| Résumé | Full Stack | ML Eng. | Backend | Data Sci. | DSL |
|---|---|---|---|---|---|
| Wednesday Addams | ✅ | ❌ | ❌ | ❌ | valid |
| Mary Jane Watson | ❌ | ✅ | ❌ | ❌ | valid |
| Alex Rivera | ❌ | ❌ | ✅ | ❌ | valid |
| Nina Patel | ❌ | ❌ | ❌ | ✅ | valid |
| Kim Possible | ✅ | ❌ | ✅ | ❌ | valid |
| Rosa Diaz | ❌ (no Git) | ❌ | ❌ | ❌ (no visualization) | valid |
| Edge case | ❌ | ❌ | ❌ | ❌ | **rejected**: `Expected 'email'` |

- 7 transducers (1 normalizer + 6 categories, 34–85 states each), 70 variants → 41 canonical tokens.
- 4 automata of 6–7 states. A test confirms that the NFA and DFA constructions are equivalent.
- About 90 automated tests, all passing.

🖼 *Screenshot:* HTML report of Kim Possible (`python -m resumelens data/sample_resumes/kim_possible_multi_profile.txt --save`)

## 6. Conclusions

- Each sub-problem fits one level of the Chomsky hierarchy: **searching** and **rewriting** are regular (regex, FST), **pattern recognition** over canonical tokens is regular (automata), and the **nested structured output** needs a CFG.
- Formal models make every decision **traceable**: a rejection always names the missing group, and an invalid profile names the line and the kind of error.
- Normalization and sorting are what make the automata small. The work of each stage simplifies the next one.

## 7. Limitations and future work

- Only explicit mentions are recognized (no synonyms such as "frontend expert"), and unknown spellings are rejected.
- Patterns check presence, not level or years per skill. Weighted automata or transducers could add that.
- Input is plain text. PDF or DOCX would need a conversion step.
- Future work: learn new variants semi-automatically, add years per skill to the DSL.

## References (selection)

- Mohri, M. (1997). Finite-state transducers in language and speech processing. *Computational Linguistics*, 23(2).
- Hopcroft, J., Motwani, R., & Ullman, J. (2007). *Introduction to Automata Theory, Languages, and Computation*.
- Dejanović, I. et al. (2017). TextX: A Python tool for DSL implementation. *Knowledge-Based Systems*, 115.
- Romero, J. (2021). Pyformlang: An educational library for formal language manipulation. *SIGCSE '21*.
- Raghavan, M. et al. (2020). Mitigating bias in algorithmic hiring. *FAT\* '20*.

Full list: `docs/00-literature-review.md`.
