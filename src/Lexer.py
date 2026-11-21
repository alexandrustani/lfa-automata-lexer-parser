from .Regex import Regex, parse_regex
from .NFA import NFA, EPSILON
from functools import reduce

class Lexer:
    def build_nfas_list(self):
        idx = 0

        for elem in self.spec:
            tok_name, regex_str = elem

            regex = parse_regex(regex_str)
            nfa = regex.thompson()

            self.nfas_list.append((tok_name, idx, nfa))

            idx += 1
    
    def build_unique_nfa(self):
        new_q0 = Regex.get_next_state(Regex)

        new_D = dict()
        new_F = set()
        new_K = set()
        new_S = set()

        new_D[(new_q0, EPSILON)] = set()
        self.final_state_token = dict()
    
        for elem in self.nfas_list:
            token, idx, nfa = elem

            new_D |= nfa.d
            new_D[(new_q0, EPSILON)].add(nfa.q0)

            new_K |= nfa.K
            new_S |= nfa.S
            new_F |= nfa.F

            for final_state in nfa.F:
                self.final_state_token[final_state] = (token, idx)
            
        return NFA(new_S, new_K, new_q0, new_D, new_F)
        

    def __init__(self, spec: list[tuple[str, str]]) -> None:
        self.spec = spec
        self.nfas_list = []
        self.build_nfas_list()

        unique_nfa = self.build_unique_nfa()
        self.dfa = unique_nfa.subset_construction()
    
    def lex(self, word: str) -> list[tuple[str, str]]:
        i =  0
        col = 0
        line = 0
        tokens = []
        n = len(word)

        while i < n:
            currentState = self.dfa.q0
            j = i
            best = None

            while j < n:
                c = word[j]
                nextState = self.dfa.d.get((currentState, c))

                if nextState is None or not nextState:
                    break

                currentState = nextState
                j += 1

                if currentState in self.dfa.F:
                    candidates = []

                    for state in currentState:
                        if state in self.final_state_token:
                            candidates.append(self.final_state_token[state])

                    best_token, best_idx = candidates[0]

                    for token, idx in candidates:
                        if idx < best_idx:
                            best_token = token
                            best_idx = idx
                    
                    best = (j, best_token)
                
            if best is not None:
                best_end, best_token = best

                lexeme = word[i:best_end]

                tokens.append((best_token, lexeme))

                for chr in lexeme:
                    if chr == '\n':
                        line += 1
                        col = 0
                    else:
                        col += 1
                
                i = best_end
            else:
                error_col = col + (j - i)

                if j == n:
                    return [("", f"No viable alternative at character EOF, line {line}")]
                else:
                    return [("", f"No viable alternative at character {error_col}, line {line}")]

        return tokens
