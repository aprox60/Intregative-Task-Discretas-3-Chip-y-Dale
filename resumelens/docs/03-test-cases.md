# Test Cases

## Objective

The repository will include a focused suite of tests to validate extraction, normalization, classification, DSL validation, and end-to-end pipeline behavior.

## Required scenarios

1. Two reference resumes are accepted.
   - `wednesday_addams.txt`
   - `mary_jane_watson.txt`
2. A résumé missing a required qualification is rejected.
3. Different skill orderings yield the same result under canonical sorting.
4. Spelling variants normalize to the same canonical token.
5. Invalid DSL input with a lexical error is rejected.
6. Invalid DSL input with a syntax error is rejected.
7. End-to-end pipeline generation produces HTML output.

## Test categories

### Extraction tests
- Verify that `JS`, `React.js`, `NodeJS`, `Postgres`, and `Git` are extracted from the reference example.
- Verify that phone, email, and URL patterns are recognized.

### Normalization tests
- Ensure `Javascript` and `JS` both map to `JAVASCRIPT`.
- Ensure `Node.js` and `NodeJS` both map to `NODE_JS`.
- Ensure canonical sort order is stable.

### Classification tests
- Verify accepted profile pattern for the ML engineer reference examples.
- Verify Full Stack automaton accepts a well-ordered token sequence.
- Verify missing required skills results in `REJECTED`.

### DSL tests
- Confirm invalid tokens trigger lexical diagnostics.
- Confirm broken grammar triggers syntax diagnostics.
- Check that a valid object serializes to DSL text and renders HTML.

## Sample test matrix

| Test ID | Scenario | Expected result |
| --- | --- | --- |
| EX-01 | Extract JavaScript skills | Raw skill list returned |
| NORM-01 | JS + Javascript mapping | `JAVASCRIPT` |
| CLASS-01 | ML token sequence matches | `ACCEPTED` |
| CLASS-02 | Missing `GIT` in ML output | `REJECTED` |
| DSL-01 | Invalid keyword | validation error |
| DSL-02 | Missing comma or braces | syntax error |
| E2E-01 | End-to-end pipeline | HTML generated |

## TODO
- Add each scenario to `tests/*.py` with exact assertions.
- Fill in additional edge cases for profile 3 and profile 4 once those profiles are chosen.
