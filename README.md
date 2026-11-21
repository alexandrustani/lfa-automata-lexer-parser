# Finite Automata, Regex, Lexer, and Parser

Etapa 2 project for Formal Languages and Automata (LFA). This repository implements a small language-processing pipeline in Python: regular-expression syntax is converted to automata, token specifications are combined into a lexer, and token streams can be parsed with a grammar.

## Implementation

- `src/DFA.py` defines deterministic finite automata, word acceptance, state remapping, and partition-refinement minimization.
- `src/NFA.py` defines nondeterministic finite automata, epsilon-closure traversal, and subset construction into a DFA.
- `src/Regex.py` models character, concatenation, union, Kleene-star, plus, and optional expressions; the parser builds these expression trees from regex text and Thompson construction creates NFAs.
- `src/Lexer.py` compiles the token regex specifications into one automaton and scans input using longest-match selection, with specification order used to break token ties.
- `src/Grammar.py` loads the project grammar format and applies CYK parsing; `src/Parser.py` connects lexing and parsing, and `src/ParseTree.py` represents the result.

## Inputs and tests

`lexer_spec.json`, `grammar_lambda.txt`, and `parser_grammar.txt` are example project specifications. `test/` contains the supplied unit tests; `tests_1/`, `tests_2/`, and `tests_4/` contain representative automata, regex, and grammar inputs. Oversized generated inputs and submission archives are omitted.

The code uses Python 3.12+ syntax. Run the supplied tests with `python -m unittest discover -s test`.
