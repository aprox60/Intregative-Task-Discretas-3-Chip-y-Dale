# Literature Review

This review covers the problem (automatic résumé screening) and the four formal models we use to solve it. For each topic it says what we took from the sources and how it shaped our design.

## 1. Résumé information extraction

Résumés are semi-structured documents. They follow common conventions (contact block, skills list, education, experience), but the wording and order change from one candidate to another. Yu, Guan and Zhou [1] showed that résumé extraction works better in **cascaded stages**: first find the general blocks, then extract detailed fields inside them. Chen, Zhang and Niu [2] also split the process in two steps, first classifying text blocks and then extracting attributes.

**What we took:** ResumeLens is also a cascade, but each stage is a different formal model: regex → transducer → automaton → grammar. Unlike the statistical models of [1, 2], every decision of our system can be traced to an explicit rule. That matters in a screening context.

## 2. Responsible use of automated screening

Raghavan et al. [3] reviewed commercial pre-employment screening tools and found that vendors rarely explain how their models decide, which makes bias hard to audit. The case of a recruiting model trained on historical data that learned to penalize résumés mentioning women's organizations [4] is often cited as an example of what opaque learning-based screening can do.

**What we took:** ResumeLens does **not** rank candidates or make hiring decisions (as the assignment requires). It only checks whether *explicit* qualifications match *explicit* patterns, and every rejection can be explained (`missing_groups`). The formal approach is less flexible than machine learning, but it is fully transparent.

## 3. Regular expressions

Kleene's regular expressions and Thompson's construction [5] made it possible to search text by compiling a pattern into an automaton. Friedl [6] describes the practical engines (such as Python's `re`), which add extensions like look-around assertions and named groups. Those extensions go beyond the theoretical regular operators, but the patterns we use with them still describe regular languages.

**What we took:** we use regular expressions only for **finding** strings (stage 1), which is what they are good at. Look-arounds were needed because the standard word boundary `\b` fails with names like `Node.js` or `C#`.

## 4. Finite-state transducers

Mohri [7] presents finite-state transducers as the standard tool for string-to-string rewriting in language and speech processing, and studies their determinization and composition. Roche and Schabes [8] and Beesley and Karttunen [9] show how lexicons are compiled into transducers (letter tries) and how a lexical rewriting step is done by composing a simple normalizing transducer with a lexicon transducer.

**What we took:** our normalization is exactly that design: a one-state preprocessing transducer (case folding, separator deletion) applied before a **trie transducer per category** that maps each variant to its canonical form. Following [7], we keep the transducers deterministic by adding an end-of-word mark, so the output is written only once the whole word has been read.

## 5. Finite automata

Rabin and Scott [10] introduced nondeterministic finite automata and proved that every NFA has an equivalent DFA (subset construction). Hopcroft, Motwani and Ullman [11] and Sipser [12] extend this to ε-NFAs and show that the three models (DFA, NFA, ε-NFA) recognize exactly the regular languages.

**What we took:** each profile pattern is a regular language $G_0^+ G_1^+ \cdots$, so finite automata are enough. Following the equivalence results, we chose the type that expresses each pattern most naturally: a DFA for a plain sequence, an NFA for the $G^*G$ formulation, and an ε-NFA to skip optional groups. A test checks the NFA/DFA equivalence with pyformlang [13].

## 6. Context-free grammars and DSLs

Chomsky [14] placed context-free grammars above regular languages in the hierarchy. Nested structures, such as balanced braces, need a CFG. Fowler [15] describes domain-specific languages as small languages focused on one problem, and textX [16] lets you define a DSL in Python with a grammar from which the parser and the object model are built automatically. textX is built on Arpeggio, a parser for parsing expression grammars (PEGs) [17], which use ordered choice instead of ambiguous alternatives.

**What we took:** the candidate profile is a nested, repeated structure, so it is described by a CFG and implemented with textX. Since our grammar has no two alternatives starting with the same keyword, the PEG accepts the same language as the CFG. Like compilers [18], we separate lexical, syntactic and semantic errors.

## 7. Tools

- **pyformlang** [13] is an educational Python library for formal languages. It provides `FST`, `DeterministicFiniteAutomaton`, `NondeterministicFiniteAutomaton` and `EpsilonNFA`, plus operations such as `is_deterministic` and `is_equivalent_to`, which we use in the tests.
- **textX** [16] is a meta-language and parser generator for DSLs, with *object processors* for semantic checks.

## Summary: from the literature to our design

| Source idea | Where it is in ResumeLens |
|---|---|
| Cascaded extraction [1, 2] | four stages, each one consuming the previous output |
| Transparency in screening [3, 4] | explicit patterns, explained rejections, no ranking |
| Regex for search [5, 6] | stage 1 |
| Normalizer ∘ lexicon transducer, tries, end mark [7, 8, 9] | stage 2 |
| DFA / NFA / ε-NFA equivalence [10, 11, 12] | stage 3, three types, equivalence test |
| CFG + DSL with textX [14, 15, 16, 17] | stage 4 |
| Lexical / syntactic / semantic errors [18] | `ResumeValidationError.kind` |

## References

1. Yu, K., Guan, G., & Zhou, M. (2005). Resume information extraction with cascaded hybrid model. In *Proceedings of the 43rd Annual Meeting of the Association for Computational Linguistics (ACL'05)* (pp. 499–506).
2. Chen, J., Zhang, C., & Niu, Z. (2018). A two-step resume information extraction algorithm. *Mathematical Problems in Engineering*, 2018.
3. Raghavan, M., Barocas, S., Kleinberg, J., & Levy, K. (2020). Mitigating bias in algorithmic hiring: Evaluating claims and practices. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAT\* '20)* (pp. 469–481).
4. Dastin, J. (2018, October 10). Amazon scraps secret AI recruiting tool that showed bias against women. *Reuters*.
5. Thompson, K. (1968). Regular expression search algorithm. *Communications of the ACM*, 11(6), 419–422.
6. Friedl, J. E. F. (2006). *Mastering Regular Expressions* (3rd ed.). O'Reilly Media.
7. Mohri, M. (1997). Finite-state transducers in language and speech processing. *Computational Linguistics*, 23(2), 269–311.
8. Roche, E., & Schabes, Y. (Eds.). (1997). *Finite-State Language Processing*. MIT Press.
9. Beesley, K. R., & Karttunen, L. (2003). *Finite State Morphology*. CSLI Publications.
10. Rabin, M. O., & Scott, D. (1959). Finite automata and their decision problems. *IBM Journal of Research and Development*, 3(2), 114–125.
11. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2007). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson.
12. Sipser, M. (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
13. Romero, J. (2021). Pyformlang: An educational library for formal language manipulation. In *Proceedings of the 52nd ACM Technical Symposium on Computer Science Education (SIGCSE '21)*.
14. Chomsky, N. (1956). Three models for the description of language. *IRE Transactions on Information Theory*, 2(3), 113–124.
15. Fowler, M. (2010). *Domain-Specific Languages*. Addison-Wesley.
16. Dejanović, I., Vaderna, R., Milosavljević, G., & Vuković, Ž. (2017). TextX: A Python tool for domain-specific languages implementation. *Knowledge-Based Systems*, 115, 1–4.
17. Ford, B. (2004). Parsing expression grammars: A recognition-based syntactic foundation. In *Proceedings of the 31st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '04)* (pp. 111–122).
18. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.
