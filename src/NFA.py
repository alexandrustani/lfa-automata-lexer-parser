from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs

@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        epsStates = set()
        stack = [state]

        epsStates.add(state)

        while stack:
            currentState = stack.pop()

            for nxt in self.d.get((currentState, EPSILON), set()):
                if nxt not in epsStates:
                    epsStates.add(nxt)
                    stack.append(nxt)
        
        return epsStates

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        new_K = set()
        new_d = dict()
        new_F = set()

        new_q0 = frozenset(self.epsilon_closure(self.q0))
        stack = [new_q0]
        new_K.add(new_q0)

        while stack:
            currentState = stack.pop()

            for c in self.S:
                statesForChr = set()

                for state in currentState:
                    nextState = self.d.get((state, c), set())

                    for nxt in nextState:
                        statesForChr |= self.epsilon_closure(nxt)
                
                newState = frozenset(statesForChr)

                if newState not in new_K:
                    new_K.add(newState)
                    stack.append(newState)
                
                new_d[(currentState, c)] = newState
        
        for state in new_K:
            if state & self.F:
                new_F.add(state)
        
        return DFA(self.S, new_K, new_q0, new_d, new_F)

    def remap_states[OTHER_STATE](self, _: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        return self
