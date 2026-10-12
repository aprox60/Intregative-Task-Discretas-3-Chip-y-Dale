# Presentation Outline (10 minutes, in English)

Ten slides, about one minute each. The presentation is technical: it explains the modeling choices and their justification, not the product. The two speakers alternate by stage.

| # | Slide | Time | Speaker |
|---|---|---|---|
| 1 | Problem and goal | 0:45 | Valeria |
| 2 | Pipeline and formal models | 0:45 | Valeria |
| 3 | Stage 1: regular expressions | 1:00 | Ivan |
| 4 | Stage 2: transducers | 1:30 | Ivan |
| 5 | Canonical order | 0:30 | Ivan |
| 6 | Stage 3: automata and profiles | 1:30 | Valeria |
| 7 | Stage 4: grammar and DSL | 1:15 | Ivan |
| 8 | Results | 1:00 | Valeria |
| 9 | Limitations and improvements | 0:45 | Ivan |
| 10 | Conclusions | 0:30 | Valeria |

---

## Slide 1: Problem and goal
- The same qualification is written in many ways: *JS / Javascript / JavaScript*, *sklearn / Scikit-learn*.
- Goal: decide whether a résumé **explicitly** satisfies the qualification pattern of a profile, using formal models.
- Not a ranking or hiring tool. That is a deliberate design choice: every decision must be explainable.

**Speaker note:** opaque screening tools are hard to audit (Raghavan et al., 2020). A formal pipeline gives a reason for every rejection.

## Slide 2: Pipeline and formal models
- Text → **regex** → raw strings → **FST** → canonical tokens → **sort** → **automata** → ACCEPTED/REJECTED → **CFG (textX)** → validated profile → HTML.
- Each stage only reads the output of the previous one.
- Show the diagram from `docs/04-architecture.md`.

**Speaker note:** each stage uses the smallest model that can solve its sub-problem: three regular models and one context-free one.

## Slide 3: Stage 1, regular expressions
- One regex per category: language, framework, library, database, tool, other. Plus contact, education and experience.
- Decisions: custom boundaries (`\b` fails on `Node.js`, `C#`), optional separator `[\s.\-]?`, case-sensitive short names (`Go`, `R`, `REST`).
- Example: `Technical Skills: JS, React.js, NodeJS, Postgres, Git.` → 5 raw strings.

**Speaker note:** regex only **finds** strings. Deciding that `JS` = `JavaScript` is not its job.

## Slide 4: Stage 2, finite-state transducers
- $M=(Q,\Sigma,\Gamma,\delta,\omega,q_0,F)$.
- $M_{pre}$: one state; lower case; separators → ε. `Scikit-learn` → `scikitlearn`.
- $M_{category}$: a trie of the variants; ε output while reading; the canonical token is written on the end mark `$`.
- Show the GIT/GITHUB/GITLAB part of the tools transducer (`docs/02-formalization.md` §2.2).
- Why: the end mark keeps it deterministic (`postgres` vs `postgresql`). One transducer per category keeps each one small (34–85 states instead of more than 300).

## Slide 5: Canonical order
- Example from the assignment: `Git, NodeJS, JS, Postgres, React.js` → `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT`.
- The profile's alphabet filters and orders the tokens.
- Why: "all groups in any order" needs $2^n$ states; "groups in order" needs $n+1$.

## Slide 6: Stage 3, automata and profiles
- A pattern is $G_0^+ G_1^+ \cdots G_{n-1}^+$ (optional group: $G_i^*$). States $q_0 \dots q_n$, $F=\{q_n\}$.
- Our profiles: **Backend Developer** (software) and **Data Scientist** (AI/data), and why they differ from Full Stack and ML.
- Type of each: ML = **DFA** (δ is a function), Backend = **NFA** (δ(q₀, JAVA) = {q₀, q₁}), Full Stack and Data Scientist = **ε-NFA** (ε skips the optional group).
- Show the Full Stack diagram and the run on Wednesday's sequence, including the ε step.

**Speaker note:** all three are equivalent (Rabin–Scott); a test checks NFA ≡ DFA with pyformlang. We picked the type that expresses each pattern most naturally.

## Slide 7: Stage 4, grammar and DSL
- Why a CFG: nested `{ }` blocks, repeated experience and education, ordered sections.
- Show a few EBNF rules and Nina Patel's generated document.
- Validation: **lexical** (`email: wednesday-nevermore`), **syntactic** (missing `email`), **semantic** (repeated skill, object processors).
- HTML is generated only from a validated model.

## Slide 8: Results
- Table: each sample accepted only by its profile; Kim accepted by two; Rosa rejected with `missing: VERSION_CONTROL`; the edge case rejected by the grammar.
- Live or recorded demo: `python -m resumelens data/sample_resumes/kim_possible_multi_profile.txt --details`.
- Around 90 automated tests, one suite per stage.

## Slide 9: Limitations and improvements
- Explicit mentions only; unknown spellings rejected (never guessed).
- Presence, not proficiency: weighted automata could add years per skill.
- Plain text only.

## Slide 10: Conclusions
- Each sub-problem fits one level of the Chomsky hierarchy.
- Formal models give traceable decisions: every rejection has a reason.
- Each stage simplifies the next: normalization and sorting are what keep the automata at 6–7 states.

---

## Likely questions (prepare an answer)

- *Why not a single transducer?* Size and readability; categories from stage 1 already narrow the search.
- *Is the NFA really needed?* No, every NFA has an equivalent DFA. It shows the $G^*G$ formulation, and the equivalence is tested.
- *Why can't a regex validate the DSL?* Nested braces are not regular; you need a CFG.
- *textX is PEG, is it still a CFG?* Our grammar has no two alternatives that start with the same token, so ordered choice and CFG alternation accept the same language.
- *What happens with `Postgre`?* The transducer rejects it (it's a prefix, not a variant). It shows up as *unknown*.
