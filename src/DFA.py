from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
# import pandas as pd
from typing import TypeVar
from functools import reduce

STATE = TypeVar('STATE')

@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]

    def accept(self, word: str) -> bool:
        myState = self.q0

        for c in word:
            if c not in self.S:
                return False
            
            nextState = self.d.get((myState, c))
            if nextState is None:
                return False
            
            myState = nextState

        return myState in self.F

    def minimize(self) -> 'DFA[STATE]':
        W = [self.F, self.K - self.F]
        P = [self.F, self.K - self.F]

        while W:
            Q = W.pop()

            for c in self.S:
                X = set()

                for (src_state, chr), dst_state in self.d.items():
                   if dst_state in Q and chr == c:
                      X.add(src_state)
                
                for R in list(P):
                    R1 = R & X
                    R2 = R - X

                    if len(R1) <= 0 or len(R2) <= 0:
                        continue

                    P.remove(R)
                    P.append(R1)
                    P.append(R2)

                    if R in W:
                        W.remove(R)
                        W.append(R1)
                        W.append(R2)
                    elif len(R1) <= len(R2):
                        W.append(R1)
                    else:
                        W.append(R2)
        
        state_map = dict()

        for group in P:
            if len(group) == 0:
                continue

            frozen_group = frozenset(group)

            for state in self.K:
                if state in frozen_group:
                    state_map[state] = frozen_group

        new_K = set(state_map.values())

        new_q0 = state_map[self.q0]

        new_F = set()

        for state in new_K:
            if state & self.F:
                new_F.add(state)
        
        new_d = dict()

        for group in P:
            if len(group) == 0:
                continue

            frozen_group = frozenset(group)
            currentState = next(iter(frozen_group))

            for c in self.S:
                nxt = self.d.get((currentState, c), None)

                if nxt is None:
                    continue

                new_d[(frozen_group, c)] = state_map[nxt]
        
        return DFA(self.S, new_K, new_q0, new_d, new_F)
        
    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        return self