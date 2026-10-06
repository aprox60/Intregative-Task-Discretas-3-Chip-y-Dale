# Formalization

## 1. Regex languages and extraction

The extraction stage uses Python `re` to detect lexical features in natural-language resumes. The goal is to find explicit textual evidence without deciding equivalence or fit.

| Pattern name | Regex pattern | Language recognized | Notes |
| --- | --- | --- | --- |
| Email | `(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b` | Email addresses | Matches standard email addresses. |
| Phone | `(?i)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)\d{3}[-.\s]?\d{4}` | Phone numbers | Accepts common formatting variations. |
| URL | `(?i)https?://\S+|www\.\S+` | Hyperlinks | Matches web URLs and www links. |
| Programming language | `(?i)\b(python|javascript|js|java|c\+\+|c#|ruby|php|go|rust|swift|typescript|typescriptcript)\b` | Programming languages | Raw match only; no normalization at this stage. |
| Framework | `(?i)\b(react|react\.js|node\.js|django|spring\s*boot|flask|angular|vue|pandas|scikit\-learn|tensorflow)\b` | Frameworks and libraries | Captures common examples. |
| Database | `(?i)\b(postgres|postgresql|mysql|mongodb|sqlite|redis|sql)\b` | Database technologies | Base evidence for profile patterns. |
| Tool | `(?i)\b(git|docker|kubernetes|linux|aws|azure|jenkins|figma)\b` | Tools and technologies | Generic category for platform tooling. |
| Academic qualification | `(?i)\b(bsc|bs|ba|msc|m\.sc|phd|master\s*degree|bachelor\s*degree)\b` | Education credentials | Used to detect explicit education lines. |
| Experience | `(?i)(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:of\s+)?experience` | Experience durations | Stores duration evidence, not profile fit. |

### Regex note

The extracted data should be kept as raw strings. This ensures the later normalization stage can decide canonical forms without losing the original lexical evidence.

## 2. FST formalization

The normalization stage uses a finite-state transducer (FST) to map lexically different skill names to a canonical token. The transducer is built from a lexicon; each entry maps a set of variants to the canonical symbol used by the automata.

### Canonical variant map

- `JS`, `Javascript`, `JavaScript` -> `JAVASCRIPT`
- `React.js`, `ReactJS`, `React JS` -> `REACT`
- `NodeJS`, `Node.js`, `Node JS` -> `NODE_JS`
- `Postgres`, `PostgreSQL` -> `POSTGRESQL`
- `pandas` -> `PANDAS`
- `sklearn`, `scikit learn`, `Scikit-learn` -> `SCIKIT_LEARN`
- `Tensor Flow`, `TensorFlow` -> `TENSORFLOW`
- `Py Torch`, `PyTorch` -> `PYTORCH`

### FST template

The transducer is documented as a 7-tuple: M = (Q, Σ, Γ, δ, ω, q0, F)

| Symbol | Meaning | Example in this project |
| --- | --- | --- |
| Q | Finite set of states | `{q0, q1, q2, q3, ...}` |
| Σ | Input alphabet | Lowercase/uppercase letters, dot, whitespace, hyphen, slash |
| Γ | Output alphabet | Canonical upper-case symbols such as `JAVASCRIPT`, `REACT`, `NODE_JS` |
| δ | Transition function | Maps character sequences to new states and emits canonical output |
| ω | Output function | Emits canonical token on accepting paths |
| q0 | Initial state | `q0` |
| F | Accepted states | Final states corresponding to valid normalized tokens |

### Design decision

A single lexicon-driven transducer is preferred over one transducer per skill because:
- the canonicalization strategy is easier to maintain;
- skill variants are defined declaratively in a dictionary;
- the same normalization logic can be reused for different profiles;
- the input alphabet and output alphabet remain conceptually unified.

### Example graphical interpretation

The graphical representation is exported to `docs/diagrams/` and can illustrate a sequence of transition states such as `JS -> JAVASCRIPT` or `Node.js -> NODE_JS`.

## 3. Automata formalization

The profile classification stage uses finite automata over the sorted normalized token stream.

### Reference ML automaton

The canonical accepted pattern for the ML profile is:

`q0 -PYTHON-> q1 -{PANDAS,NUMPY}-> q2 -{SCIKIT_LEARN,TENSORFLOW,PYTORCH}-> q3 -{SQL,POSTGRESQL}-> q4 -GIT-> q5`

with `q5` accepting.

### 5-tuple for automata

For a profile automaton A = (Q, Σ, δ, q0, F):

| Symbol | Meaning | Example |
| --- | --- | --- |
| Q | Finite set of states | `{q0, q1, q2, q3, q4, q5}` |
| Σ | Input alphabet | `{PYTHON, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, PYTORCH, SQL, POSTGRESQL, GIT}` |
| δ | Transition function | State transitions on accepted tokens |
| q0 | Start state | `q0` |
| F | Accepting states | `{q5}` |

### Type justification

The ML-like pattern is naturally expressed as an NFA because it contains transitions on sets of possible tokens (`{PANDAS, NUMPY}` and `{SCIKIT_LEARN, TENSORFLOW, PYTORCH}`), which is easier to specify than a DFA with a fully enumerated transition table. The implementation may still be determinized internally by `pyformlang` if required.

### Full Stack automaton

The Full Stack profile can be modeled analogously, for example:

`q0 -{JS,TS}-> q1 -{REACT,ANGULAR,VUE}-> q2 -{NODE_JS,DJANGO,SPRING_BOOT}-> q3 -{SQL,POSTGRESQL,MONGODB}-> q4 -REST-> q5 -GIT-> q6`

with `q6` accepting.

## 4. Candidate profile language (CFG, textX)

The DSL organizes a résumé candidate into candidate metadata, repeated experience blocks, repeated education blocks, repeated normalized skills, and the profile classification outcome.

### EBNF skeleton

```ebnf
resume          = {personal_info, contact_info, experience_block, education_block, skill_block, profile_result};
personal_info   = 'candidate', ':', IDENT, ',', 'name', ':', STRING ;
contact_info    = 'email', ':', EMAIL, ',', 'phone', ':', PHONE ;
experience_block = 'experience', ':', '{', experience_entry, { ',', experience_entry }, '}' ;
experience_entry = 'role', ':', STRING, ',', 'years', ':', NUMBER ;
education_block = 'education', ':', '{', education_entry, { ',', education_entry }, '}' ;
education_entry = 'degree', ':', STRING, ',', 'institution', ':', STRING ;
skill_block     = 'skills', ':', '[', skill, { ',', skill }, ']' ;
skill           = IDENT ;
profile_result  = 'profile', ':', IDENT, ',', 'status', ':', ('ACCEPTED' | 'REJECTED') ;

IDENT           = /[A-Za-z_][A-Za-z0-9_\-]*/ ;
STRING          = /"[^"]*"/ | /'[^"]*'/ ;
EMAIL           = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/ ;
PHONE           = /\+?[0-9()\-\s]{7,}/ ;
NUMBER          = /[0-9]+/ ;
```

### Structural characteristics

- Personal and contact data are explicit.
- Experience and education are repeated blocks rather than single values.
- Skills are normalized and represented as canonical tokens.
- Classification results are stored as explicit accepted/rejected profile checks.
- The grammar is intentionally small and academically tractable for the assignment.

## 5. TODOs for the final formalization document

- Fill in the exact formal tuples for each implemented profile.
- Add diagrams for the transducer and automata states.
- Add precise lexical rules if the team expands the DSL.
- Confirm the final set of profile keywords for PROFILE_3_TODO and PROFILE_4_TODO.
