# Formalization

## 1. Regular expressions (stage 1: extraction)

Implementation: `src/resumelens/extraction/patterns.py` (the patterns) and `src/resumelens/extraction/extractor.py` (where they are applied).

Each regular expression $r$ denotes a regular language $L(r) \subseteq \Sigma^*$, where $\Sigma$ is the set of characters that can appear in a résumé. The extractor returns every non-overlapping substring of the résumé that belongs to $L(r)$ (`re.finditer`). This stage does **not** decide whether two strings are equivalent (stage 2) or whether a candidate fits a profile (stage 3).

### Design decisions

- **One category, one transducer.** Each technical category (`programming_languages`, `frameworks`, `libraries`, `databases`, `tools`, `other_qualifications`) has its own regex, and in stage 2 its own transducer. That keeps each formal model small enough to draw.
- **Our own word boundaries.** Python's `\b` does not work with names like `Node.js` or `C#`, because `.`, `+` and `#` are not word characters. We use `BEFORE = (?<![\w+#&.])` and `AFTER = (?![\w+#&]|\.\w)`. Because of `BEFORE`, the `JS` inside `Node.JS` is not taken as a language. Because of `AFTER`, `github` inside `github.com/...` is not taken as the tool Git.
- **Optional separators.** `SEP = [\s.\-]?` lets one pattern accept `Scikit-learn`, `scikit learn` and `scikitlearn`.
- **Short names are case-sensitive.** `JS`, `TS`, `Go`, `R`, `REST` and `Express` are also ordinary words (*go home*, *the rest*, *R&D*), so they have a separate regex without `re.IGNORECASE` and only match with that exact capitalization. Every other technical regex is case-insensitive.
- **Longest match wins.** When two regexes of the same category match at overlapping positions (`REST` and `REST APIs`), only the longest one is kept (`find_all_in_order`).
- **Named groups.** Education and experience use named groups (`degree`, `field`, `institution`, `years`, `description`), so the result goes straight into the DSL in stage 4.
- **Output.** An `ExtractionResult` object (`src/resumelens/models.py`). `ResumeExtractor.save_json(path)` saves it as JSON.

### Known limitations

- A date written as `2019.10.07` can match the phone pattern.
- The name is only detected when it is the first non-empty line.
- Spellings that are not listed (e.g. `ECMAScript`) are not extracted. If they appear under `Skills:`, they show up in `get_unrecognized_skills()`.

### Example (assignment fragment)

Input:

```text
Wednesday Addams
3 years of experience developing web applications.
Technical Skills:
JS, React.js, NodeJS, Postgres, Git.
```

Output of `get_all_technical_strings()`: `["JS", "React.js", "NodeJS", "Postgres", "Git"]`. This is the input of stage 2.

### Patterns

#### `name`

**Language recognized:** Two to five capitalized words separated by spaces. It is only checked against the first non-empty line.

```regex
[A-ZÀ-Ý][A-Za-zÀ-ÿ'\-]+(\s+[A-ZÀ-Ý][A-Za-zÀ-ÿ'\-]+){1,4}
```

#### `emails`

**Language recognized:** local part, '@', domain labels separated by dots and a top level domain of 2 or more letters.

```regex
(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])
```

#### `phones`

**Language recognized:** Optional '+', then a prefix (can be in parentheses) followed by 2 to 4 digit blocks, each one after exactly one space, dot or hyphen. Or 7 to 15 digits together.

```regex
(?<![\w+])(\+?\(?\d{1,4}\)?([\s.\-]\d{2,4}){2,4}|\+?\d{7,15})(?!\w)
```

#### `links`

**Language recognized:** Text that starts with http://, https:// or www. (or linkedin.com/, github.com/) until the next space or comma.

```regex
(https?://|www\.)[^\s,;]*[^\s,;.]|(?<![\w.])(linkedin|github)\.com/[^\s,;]*[^\s,;.]
```

#### `programming_languages`

**Language recognized:** JavaScript, TypeScript, Python, Java, Go, Kotlin, C# and R with their usual spellings. JS, TS, Go and R only with that exact capitalization.

```regex
(?<![\w+#&.])(java[\s\-]?script|type[\s\-]?script|python(\s?3)?|java|golang|kotlin|c\s?#|c[\s\-]sharp|csharp)(?![\w+#&]|\.\w)
```
_(case-insensitive)_

```regex
(?<![\w+#&.])(JS|TS|Go|R)(?![\w+#&]|\.\w)
```
_(case-sensitive)_

#### `frameworks`

**Language recognized:** React, Angular, Vue, Node and Express with or without '.js'/'JS', plus Django, Flask, FastAPI, Spring Boot and .NET.

```regex
(?<![\w+#&.])(react([\s.\-]?js)?|angular([\s.\-]?js)?|vue([\s.\-]?js)?|node([\s.\-]?js)?|express[\s.\-]?js|django|flask|fast[\s\-]?api|spring[\s\-]?boot|asp\.net(\s?core)?|\.net(\s?core)?|dotnet)(?![\w+#&]|\.\w)
```
_(case-insensitive)_

```regex
(?<![\w+#&.])(Express)(?![\w+#&]|\.\w)
```
_(case-sensitive)_

#### `libraries`

**Language recognized:** Python data, machine learning and plotting libraries, allowing a space or hyphen inside compound names (Tensor Flow, Scikit-learn, Py Torch).

```regex
(?<![\w+#&.])(pandas|num[\s\-]?py|scikit[\s\-]?learn|sk[\s\-]?learn|tensor[\s\-]?flow|py[\s\-]?torch|keras|matplotlib|seaborn|plotly)(?![\w+#&]|\.\w)
```
_(case-insensitive)_

#### `databases`

**Language recognized:** PostgreSQL/Postgres, MySQL, MongoDB/Mongo, SQLite, Redis and the SQL language.

```regex
(?<![\w+#&.])(postgres|postgre\s?sql|my\s?sql|mongo(\s?db)?|sqlite|redis|sql)(?![\w+#&]|\.\w)
```
_(case-insensitive)_

#### `tools`

**Language recognized:** Git, GitHub, GitLab, Docker, Kubernetes/k8s, Tableau and Power BI.

```regex
(?<![\w+#&.])(git|github|gitlab|docker|kubernetes|k8s|tableau|power[\s\-]?bi)(?![\w+#&]|\.\w)
```
_(case-insensitive)_

#### `other_qualifications`

**Language recognized:** REST, RESTful, REST APIs, GraphQL, statistics and statistical analysis. REST alone only in upper case.

```regex
(?<![\w+#&.])(rest(ful)?[\s\-]?apis?|restful|graph\s?ql|statistics|statistical(\s+(analysis|modeling|modelling))?)(?![\w+#&]|\.\w)
```
_(case-insensitive)_

```regex
(?<![\w+#&.])(REST)(?![\w+#&]|\.\w)
```
_(case-sensitive)_

#### `education`

**Language recognized:** A degree (BS, BSc, MSc, PhD, Bachelor's, Master's...) followed by 'in' or 'of', a field that starts with a capital letter and optionally ', Institution' or 'at Institution'.

```regex
(?<!\w)(?P<degree>Ph\.?\s?D\.?|M\.?\s?Sc\.?|B\.?\s?Sc\.?|M\.?S\.?|B\.?S\.?|B\.?A\.?|M\.?A\.?|Doctorate|(Bachelor|Master)('s)?(\s+of\s+(Science|Arts|Engineering))?)(\s+degree)?\s+(in|of)\s+(?P<field>[A-Z][A-Za-z&/ ]*?[A-Za-z])((\s*[,\-]\s*|\s+(at|from)\s+)(?P<institution>[A-Z][\w&.' ]*?\w))?\s*(?=[.;\n]|$)
```

#### `experience`

**Language recognized:** A number of years, 'years of experience' and an optional description until the end of the sentence.

```regex
(?<!\w)(?P<years>\d{1,2})\+?\s*(years?|yrs?)\s+of\s+(professional\s+)?experience(\s+(?P<description>[^.\n]+))?
```

#### `skills_section`

**Language recognized:** A line that starts with 'Skills:' or 'Technical Skills:'. Its items are split by commas, semicolons or bars.

```regex
^\s*(technical\s+)?skills\s*:\s*(?P<items>.+)$
```


## 2. Finite-state transducers (stage 2: normalization)

Implementation: `src/resumelens/normalization/variants.py` (the transformations), `transducers.py` (the pyformlang FSTs), `normalizer.py` (applying them) and `sorter.py` (canonical order).

The same qualification can be written in many ways (`JS`, `Javascript`, `JavaScript`). Normalization uses finite-state transducers to map every variant to one canonical token. Each transducer is a 7-tuple

$$M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$$

where $\delta : Q \times \Sigma \to Q$ is the transition function and $\omega : Q \times \Sigma \to \Gamma^*$ is the output function. A string $w$ is translated if, reading it from $q_0$, the transducer ends in a state of $F$. The translation is the concatenation of the outputs of the transitions it took. When a pair $(q, a)$ is not defined, the string is rejected.

Each string goes through **two transducers in sequence** (composition):

```text
"Scikit-learn" --M_pre--> "scikitlearn" --(append $)--> "scikitlearn$" --M_libraries--> SCIKIT_LEARN
```

### 2.1 Preprocessing transducer $M_{pre}$

| Part | Value |
|---|---|
| $Q$ | $\{q_0\}$ |
| $\Sigma$ | $\{A..Z,\ a..z,\ 0..9,\ +,\ \#,\ ␣,\ .,\ -,\ \_,\ /\}$ (71 symbols) |
| $\Gamma$ | $\{a..z,\ 0..9,\ +,\ \#\}$ |
| $\delta$ | $\delta(q_0, x) = q_0$ for every $x \in \Sigma$ |
| $\omega$ | $\omega(q_0, X) = $ lower case of $X$ for $X \in A..Z$; $\omega(q_0, x) = x$ for $x \in a..z,\ 0..9,\ +,\ \#$; $\omega(q_0, s) = \varepsilon$ for $s \in \{␣, ., -, \_, /\}$ |
| $q_0$ | $q_0$ |
| $F$ | $\{q_0\}$ |

It is a one-state transducer, so the language it accepts is $\Sigma^*$. Its job is to remove differences in case and separators, so `Tensor Flow`, `TensorFlow` and `tensor-flow` all become `tensorflow`. A character outside $\Sigma$ (like `é`) makes it reject the string. Full table and diagram: [diagrams/transducers/preprocessing.md](diagrams/transducers/preprocessing.md).

### 2.2 Category transducers $M_c$

There is one transducer for each technical category $c$ found in stage 1. They are all built the same way (`build_category_transducer`) from the table of variants $V_c$ in `variants.py`:

| Part | Value |
|---|---|
| $Q$ | $\{q_0, q_f\} \cup$ one state for each prefix of a variant in $V_c$ (a **trie**) |
| $\Sigma$ | the characters used in the variants of $V_c$, plus the end mark `$` |
| $\Gamma$ | the canonical tokens of category $c$ |
| $\delta$ | $\delta(p, a) = pa$ when $pa$ is a prefix of a variant; $\delta(w, \$) = q_f$ when $w \in V_c$ |
| $\omega$ | $\omega(p, a) = \varepsilon$ for every character; $\omega(w, \$) = V_c(w)$, the canonical token of the variant $w$ |
| $q_0$ | $q_0$ (the empty prefix) |
| $F$ | $\{q_f\}$ |

Size of each one:

| Transducer | Variants | States | Transitions | Canonical tokens (Γ) |
|---|---|---|---|---|
| `programming_languages` | 13 | 51 | 62 | JAVASCRIPT, TYPESCRIPT, PYTHON, JAVA, GO, KOTLIN, CSHARP, R |
| `frameworks` | 19 | 85 | 102 | REACT, ANGULAR, VUE, NODE_JS, EXPRESS, DJANGO, FLASK, FASTAPI, SPRING_BOOT, DOTNET |
| `libraries` | 10 | 72 | 80 | PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, PYTORCH, KERAS, MATPLOTLIB, SEABORN, PLOTLY |
| `databases` | 8 | 34 | 40 | POSTGRESQL, MYSQL, MONGODB, SQLITE, REDIS, SQL |
| `tools` | 8 | 43 | 49 | GIT, DOCKER, KUBERNETES, TABLEAU, POWER_BI |
| `other_qualifications` | 12 | 56 | 66 | REST_API, GRAPHQL, STATISTICS |

Complete 7-tuples (every transition with its output) and diagrams:
[programming_languages](diagrams/transducers/programming_languages.md) ·
[frameworks](diagrams/transducers/frameworks.md) ·
[libraries](diagrams/transducers/libraries.md) ·
[databases](diagrams/transducers/databases.md) ·
[tools](diagrams/transducers/tools.md) ·
[other_qualifications](diagrams/transducers/other_qualifications.md).
They are generated from the pyformlang objects with `python -m resumelens.docs_export`, so the documentation and the code can't disagree.

#### Example: part of $M_{tools}$ (the variants of GIT)

```mermaid
flowchart LR
    start(( )) --> q0
    qf(((qf)))
    q0 -- "g / ε" --> q1
    q1 -- "i / ε" --> q2
    q2 -- "t / ε" --> q3
    q3 -- "$ / GIT" --> qf
    q3 -- "h / ε" --> q4
    q4 -- "u / ε" --> q5
    q5 -- "b / ε" --> q6
    q6 -- "$ / GIT" --> qf
    q3 -- "l / ε" --> q7
    q7 -- "a / ε" --> q8
    q8 -- "b / ε" --> q9
    q9 -- "$ / GIT" --> qf
```

Run on `github$`: $q_0 \xrightarrow{g/\varepsilon} q_1 \xrightarrow{i/\varepsilon} q_2 \xrightarrow{t/\varepsilon} q_3 \xrightarrow{h/\varepsilon} q_4 \xrightarrow{u/\varepsilon} q_5 \xrightarrow{b/\varepsilon} q_6 \xrightarrow{\$/GIT} q_f$, output `GIT`.
Run on `gi$`: from $q_2$ there is no transition on `$`, so the string is rejected.

### 2.3 Design decisions

- **Two transducers in sequence instead of one.** Without preprocessing, the trie would need a branch for every combination of case and separator (`React.js`, `ReactJS`, `react js`...). With it, each canonical token needs only a few variants.
- **One transducer per category.** A single trie for all ~70 variants would have more than 300 states and could not be drawn or explained. Splitting by category keeps each model small, and it reuses the categories from stage 1, so a string is only compared with the variants of its own category. (`React` under `databases` is rejected.)
- **End mark `$`.** `postgres` is a prefix of `postgresql`. If the output were written while reading the last letter, the transducer could not know whether the word ends there. With the mark, the output is written only when the whole word has been read, and the transducer stays **deterministic** (at most one transition for each $(q, a)$, checked in `tests/test_transducers.py`).
- **Output only at the end.** Every character transition writes $\varepsilon$, so a rejected string produces no partial output.
- **Prefix sharing (trie).** Variants with a common beginning share states (`git`, `github`, `gitlab` share $q_0 \dots q_3$).
- **Unknown strings are kept apart.** A string that a transducer rejects is not invented into a token. It is reported in `NormalizationResult.unknown`.
- **Duplicates are removed.** `JS` and `JavaScript` produce the same token once.

### 2.4 Our transformations

Besides the examples in the assignment (`JS → JAVASCRIPT`, `React.js → REACT`, `NodeJS → NODE_JS`, `Postgres → POSTGRESQL`, `sklearn → SCIKIT_LEARN`, `Tensor Flow → TENSORFLOW`, `Py Torch → PYTORCH`...), we added the ones our two profiles need:

| Variants | Canonical token |
|---|---|
| `C#`, `c sharp`, `csharp` | CSHARP |
| `Go`, `Golang` | GO |
| `TS`, `TypeScript` | TYPESCRIPT |
| `.NET`, `.NET Core`, `ASP.NET`, `dotnet` | DOTNET |
| `Spring Boot`, `SpringBoot`, `spring-boot` | SPRING_BOOT |
| `Express`, `Express.js` | EXPRESS |
| `Mongo`, `MongoDB` | MONGODB |
| `Git`, `GitHub`, `GitLab` | GIT |
| `Kubernetes`, `k8s` | KUBERNETES |
| `Power BI`, `PowerBI` | POWER_BI |
| `REST`, `RESTful`, `REST API(s)`, `RESTful API(s)` | REST_API |
| `Statistics`, `statistical analysis`, `statistical modeling` | STATISTICS |

### 2.5 Canonical order (sorting)

Before classification, the normalized tokens are put in the order defined by each profile (`sorter.py`). The order is the order of the profile groups, and inside a group the order of the JSON file. Tokens that are not in the profile's alphabet are left out, so each automaton only reads symbols of its own $\Sigma$, and the result does not depend on the order in which the candidate wrote the skills.

Example from the assignment (Full Stack): `Git, NodeJS, JS, Postgres, React.js` → normalization → `GIT, NODE_JS, JAVASCRIPT, POSTGRESQL, REACT` → sorting → `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT`.

## 3. Finite automata (stage 3: qualification pattern recognition)

Implementation: `src/resumelens/profiles/*.json` (the patterns), `classification/profiles.py` (loading them), `classification/automata.py` (the pyformlang automata) and `classification/classifier.py`.

### 3.1 Profile patterns

A profile is an ordered list of **qualification groups**. A candidate satisfies the profile when the sorted sequence from stage 2 has **at least one token of every required group, in the order of the groups**. The tokens of a profile are its alphabet $\Sigma$. With groups $G_0, \dots, G_{n-1}$ the pattern is the regular language

$$L = G_0^{+}\, G_1^{+} \cdots G_{n-1}^{+}$$

where an optional group contributes $G_i^{*}$ instead of $G_i^{+}$.

| Profile | Type | Pattern (canonical order) |
|---|---|---|
| Full Stack Developer | ε-NFA | {JAVASCRIPT, TYPESCRIPT}⁺ {REACT, ANGULAR, VUE}⁺ {NODE_JS, EXPRESS, DJANGO, FLASK, SPRING_BOOT}⁺ {SQL, POSTGRESQL, MYSQL, MONGODB, SQLITE}⁺ **{REST_API, GRAPHQL}\*** {GIT}⁺ |
| Machine Learning Engineer | DFA | {PYTHON}⁺ {PANDAS, NUMPY}⁺ {SCIKIT_LEARN, TENSORFLOW, PYTORCH, KERAS}⁺ {SQL, POSTGRESQL, MYSQL}⁺ {GIT}⁺ |
| Backend Developer *(ours, software)* | NFA | {JAVA, PYTHON, GO, CSHARP, KOTLIN, JAVASCRIPT, TYPESCRIPT}⁺ {SPRING_BOOT, DJANGO, FLASK, FASTAPI, NODE_JS, EXPRESS, DOTNET}⁺ {SQL, POSTGRESQL, MYSQL, MONGODB, REDIS}⁺ {REST_API, GRAPHQL}⁺ {DOCKER, KUBERNETES}⁺ {GIT}⁺ |
| Data Scientist *(ours, AI/data)* | ε-NFA | {PYTHON, R}⁺ {PANDAS, NUMPY}⁺ {STATISTICS}⁺ {MATPLOTLIB, SEABORN, PLOTLY, TABLEAU, POWER_BI}⁺ **{SCIKIT_LEARN}\*** {SQL, POSTGRESQL, MYSQL}⁺ |

**Why these two profiles.** *Backend Developer* is the server half of Full Stack, without frontend evidence but with two things a backend role needs and a full-stack one does not: an API style and containers. *Data Scientist* is the analysis side of AI/data. It needs statistics and visualization, which separates it from the ML Engineer, who needs an ML framework and Git. The two pairs overlap on purpose (`PYTHON`, `SQL`, `NODE_JS`...), so one résumé can satisfy more than one profile (see `kim_possible_multi_profile.txt`, accepted as Full Stack and Backend).

### 3.2 General construction

All four automata come from the same function (`ProfileAutomaton.build`), so the four profiles go through the same software, as the assignment asks. With $n$ groups:

- $Q = \{q_0, q_1, \dots, q_n\}$. Being in $q_i$ means "groups $G_0 \dots G_{i-1}$ are already satisfied".
- $\Sigma = G_0 \cup \dots \cup G_{n-1}$. The groups are disjoint; `load_profile` checks this.
- Initial state $q_0$, final states $F = \{q_n\}$.
- $\delta$ depends on the type:

| Type | Transitions for each $t \in G_i$ | Optional group |
|---|---|---|
| **DFA** | $\delta(q_i, t) = q_{i+1}$ and $\delta(q_{i+1}, t) = q_{i+1}$ | not allowed |
| **NFA** | $\delta(q_i, t) = \{q_i, q_{i+1}\}$ | not allowed |
| **ε-NFA** | $\delta(q_i, t) = \{q_{i+1}\}$, $\delta(q_{i+1}, t) = \{q_{i+1}\}$ | $\delta(q_i, \varepsilon) = \{q_{i+1}\}$ |

### 3.3 Type of each automaton, and why

- **Machine Learning Engineer: DFA.** $\delta$ is a function $Q \times \Sigma \to Q$: for every state and symbol there is at most one next state, and there are no ε-transitions. The groups are disjoint, so in $q_{i+1}$ the loop symbols ($G_i$) and the forward symbols ($G_{i+1}$) never clash. pyformlang confirms it with `is_deterministic() == True`. Missing pairs go to an implicit dead state.
- **Backend Developer: NFA.** $\delta : Q \times \Sigma \to \mathcal{P}(Q)$ and, for example, $\delta(q_0, \mathrm{JAVA}) = \{q_0, q_1\}$. After reading a language the automaton does not know whether more languages will follow (stay in $q_0$) or whether the next token is a framework (go to $q_1$), so it follows both paths. It recognizes $G_i^{*} G_i = G_i^{+}$. There are no ε-transitions, so it is an NFA and not an ε-NFA. `tests/test_classification.py` checks with `is_equivalent_to` that this construction and the DFA construction accept the same language.
- **Full Stack Developer and Data Scientist: ε-NFA.** They have an optional group (API for Full Stack, ML library for Data Scientist). The cleanest way to say "this group may be absent" is an ε-transition $\delta(q_i, \varepsilon) = \{q_{i+1}\}$ that skips it without reading a token. Since $\delta$ is defined on $Q \times (\Sigma \cup \{\varepsilon\})$, they are ε-NFAs.

All four are equivalent to some DFA (subset construction). We kept the three types to show when each one is the natural model.

### 3.4 Formal definitions and diagrams

Complete 5-tuples, transition tables and Mermaid diagrams, generated from the pyformlang objects:
[full_stack_developer](diagrams/automata/full_stack_developer.md) ·
[machine_learning_engineer](diagrams/automata/machine_learning_engineer.md) ·
[backend_developer](diagrams/automata/backend_developer.md) ·
[data_scientist](diagrams/automata/data_scientist.md).

#### Example: Full Stack Developer (ε-NFA)

```mermaid
flowchart LR
    start(( )) --> q0
    q6(((q6)))
    q0 -- "JAVASCRIPT, TYPESCRIPT" --> q1
    q1 -- "JAVASCRIPT, TYPESCRIPT" --> q1
    q1 -- "REACT, ANGULAR, VUE" --> q2
    q2 -- "REACT, ANGULAR, VUE" --> q2
    q2 -- "NODE_JS, EXPRESS, DJANGO, FLASK, SPRING_BOOT" --> q3
    q3 -- "NODE_JS, EXPRESS, DJANGO, FLASK, SPRING_BOOT" --> q3
    q3 -- "SQL, POSTGRESQL, MYSQL, MONGODB, SQLITE" --> q4
    q4 -- "SQL, POSTGRESQL, MYSQL, MONGODB, SQLITE" --> q4
    q4 -- "REST_API, GRAPHQL" --> q5
    q5 -- "REST_API, GRAPHQL" --> q5
    q4 -- "ε" --> q5
    q5 -- "GIT" --> q6
    q6 -- "GIT" --> q6
```

Run on the sequence from the assignment, `JAVASCRIPT REACT NODE_JS POSTGRESQL GIT`:
$q_0 \xrightarrow{JAVASCRIPT} q_1 \xrightarrow{REACT} q_2 \xrightarrow{NODE\_JS} q_3 \xrightarrow{POSTGRESQL} q_4 \xrightarrow{\varepsilon} q_5 \xrightarrow{GIT} q_6 \in F$ → **ACCEPTED**.

Run on `PYTHON PANDAS TENSORFLOW POSTGRESQL` in the ML DFA: it ends in $q_4 \notin F$ (the GIT group is missing) → **REJECTED**. `missing_groups` reports `VERSION_CONTROL`.

### 3.5 Design decisions

- **Alphabet = canonical tokens, not characters.** Stage 2 already turned the text into symbols, so the automata work at the level of qualifications, which keeps them small (6 or 7 states).
- **Sorting makes the pattern regular and small.** Without the canonical order, "has a language, a framework, a database..." in any order would need a state for every subset of satisfied groups ($2^n$ states). Sorting first reduces it to a chain of $n+1$ states.
- **Several tokens per group.** The loops accept `PANDAS NUMPY` or `SCIKIT_LEARN TENSORFLOW PYTORCH`. The skeleton version accepted exactly one token per group and wrongly rejected Mary Jane Watson.
- **Patterns in JSON, construction in code.** Adding or changing a profile does not need new code, only a JSON file with its groups and type.
- **Explaining rejections.** `missing_groups` lists the required groups with no token. It is used by the UI; it does not affect the decision, which is made only by the automaton.

## 4. Candidate profile language (stage 4: context-free grammar with textX)

Implementation: `src/resumelens/dsl/resume.tx` (the grammar), `parser.py` (parsing and validation), `generator.py` (writing the DSL from stages 1–3) and `visualizer.py` (HTML).

The first three stages produce loose pieces of information. This stage defines a **domain-specific language** with one fixed structure for a candidate profile. The pipeline writes every candidate in this language, and textX validates it against the grammar. Only a document that passes validation is turned into HTML.

### 4.1 Grammar in EBNF

$G = (V, T, P, S)$ with start symbol $S$ = `CandidateProfile`.

```ebnf
CandidateProfile = "candidate", STRING, "{",
                       Contact,
                       { Experience },
                       { Education },
                       Skills,
                       Evaluation,
                   "}" ;

Contact          = "contact", "{",
                       "email", ":", EMAIL,
                       [ "phone", ":", PHONE ],
                       { Link },
                   "}" ;
Link             = "link", ":", URL ;

Experience       = "experience", "{",
                       "years", ":", INT,
                       [ "description", ":", STRING ],
                   "}" ;

Education        = "education", "{",
                       "degree", ":", STRING,
                       "field", ":", STRING,
                       [ "institution", ":", STRING ],
                   "}" ;

Skills           = "skills", "{", [ TOKEN, { ",", TOKEN } ], "}" ;

Evaluation       = "evaluation", "{", ProfileResult, { ProfileResult }, "}" ;
ProfileResult    = "profile", ProfileName, ":", Status ;
ProfileName      = "FULL_STACK_DEVELOPER" | "MACHINE_LEARNING_ENGINEER"
                 | "BACKEND_DEVELOPER" | "DATA_SCIENTIST" ;
Status           = "ACCEPTED" | "REJECTED" ;

(* terminals defined by regular expressions *)
TOKEN  = /[A-Z][A-Z0-9_]*/ ;
EMAIL  = /[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}/ ;
PHONE  = /\+?\(?[0-9][0-9 ()\-]{5,}[0-9]/ ;
URL    = /((https?:\/\/|www\.)|(linkedin|github)\.com\/)[^\s{}]+/ ;
INT    = /[0-9]+/ ;                      (* built into textX *)
STRING = /"([^"\\]|\\.)*"/ ;             (* built into textX *)
COMMENT = /\/\/.*$/ ;                    (* ignored *)
```

### 4.2 Terminals and non-terminals

| | Symbols |
|---|---|
| **Non-terminals** $V$ | `CandidateProfile`, `Contact`, `Link`, `Experience`, `Education`, `Skills`, `Evaluation`, `ProfileResult`, `ProfileName`, `Status` |
| **Terminals** $T$: keywords | `candidate`, `contact`, `email`, `phone`, `link`, `experience`, `years`, `description`, `education`, `degree`, `field`, `institution`, `skills`, `evaluation`, `profile`, `ACCEPTED`, `REJECTED`, the four profile names |
| **Terminals** $T$: punctuation | `{`, `}`, `:`, `,` |
| **Terminals** $T$: regular expressions | `TOKEN`, `EMAIL`, `PHONE`, `URL`, `INT`, `STRING` |

### 4.3 Structural characteristics

- **Context-free and nested.** Blocks are delimited by `{ … }` and nested two levels deep (`candidate { contact { … } }`). Balanced brackets are a classic context-free structure; no regular expression can check them for arbitrary nesting.
- **Fixed order of sections.** Contact → experience → education → skills → evaluation. A document with the sections in another order is rejected, which gives every profile the same shape.
- **Repetition.** `{ Experience }`, `{ Education }`, `{ Link }` (zero or more), `TOKEN { "," TOKEN }` (a comma-separated list) and `ProfileResult { ProfileResult }` (one or more).
- **Optional elements.** Phone, description and institution, written `[ … ]`.
- **Closed vocabulary for the result.** A profile name and a status can only be one of the listed keywords, so a document cannot claim an unknown profile or a status like `MAYBE`.
- **Skills are canonical tokens.** `TOKEN` only accepts the upper-case form produced by the transducers, so raw text like `React.js` cannot appear in a valid profile.
- **The grammar is unambiguous.** Every block starts with a different keyword, so one token of lookahead is enough to know which rule applies. textX parses with Arpeggio, a PEG (parsing expression grammar) parser whose alternatives are *ordered*. Because no two alternatives of our grammar can start with the same keyword, the ordered choice never has to pick between two matches, and the PEG accepts exactly the language of the CFG written in 4.1.

### 4.4 Validation: what is rejected and why

| Kind | Detected by | Examples (all in `tests/test_dsl.py`) |
|---|---|---|
| **Lexical** | a value does not match its regex terminal | `email: wednesday-nevermore` · `skills { javascript }` · `years: three` |
| **Syntactic** | the structure does not match the rules | missing `email` · `skills [ … ]` · status `MAYBE` · unknown profile · empty `evaluation` · sections out of order |
| **Semantic** | textX *object processors* registered in `parser.py` | empty candidate name · repeated skill · more than 60 years of experience · the same profile evaluated twice |

Every error is turned into `ResumeValidationError(kind, message, line, column)`. For example, the résumé `invalid_edge_case.txt` has no email, and its generated document is rejected with `Syntax error: Expected 'email' (line 4, column 5)`, so no HTML is produced for it.

### 4.5 Example of a valid document

Generated by the pipeline for `nina_patel_data_scientist.txt`:

```text
// Generated by ResumeLens
candidate "Nina Patel" {
    contact {
        email: nina.patel@example.com
        phone: +44 20 7946 0958
    }
    experience {
        years: 4
        description: "statistical analysis and data visualization for retail companies"
    }
    education {
        degree: "Master's"
        field: "Applied Statistics"
        institution: "University of Leeds"
    }
    skills { R, PYTHON, PANDAS, NUMPY, MATPLOTLIB, SEABORN, POSTGRESQL, POWER_BI, STATISTICS }
    evaluation {
        profile FULL_STACK_DEVELOPER: REJECTED
        profile MACHINE_LEARNING_ENGINEER: REJECTED
        profile BACKEND_DEVELOPER: REJECTED
        profile DATA_SCIENTIST: ACCEPTED
    }
}
```

### 4.6 Visualization

`render_html(model)` reads the **validated textX model**, not the raw résumé, so the page only shows information that passed the grammar. It shows the name and contact information, the result for each profile, the normalized skills, the experience and the education. Every value is escaped with `html.escape`, so text from a résumé cannot inject HTML.

### 4.7 Design decisions

- **Keywords at the start of each block** keep the language readable and make the grammar easy to parse without lookahead problems.
- **Terminals reuse the regex ideas from stage 1** (email, phone, URL), but they are stricter, because here they validate a value instead of searching inside free text.
- **Syntax in the grammar, consistency in object processors.** Rules such as "a skill can't be repeated" would make the CFG much bigger, so they are checked after parsing.
- **The DSL is written by the program but can be edited by hand.** That is why it validates its input instead of trusting the generator; the tests feed it hand-written invalid documents.
