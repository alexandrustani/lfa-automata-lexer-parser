from .NFA import NFA
from dataclasses import dataclass

EPSILON = ''

class Regex:
    id_of_state = 0

    def thompson(self) -> NFA[int]:
        pass

    def get_next_state(self) -> int:
        my_id = Regex.id_of_state
        Regex.id_of_state += 1

        return my_id

@dataclass
class Character(Regex):
    char: str
    
    def thompson(self) -> NFA[int]: 
        new_q0 = self.get_next_state()
        new_qf = self.get_next_state()

        new_S = set(self.char)

        new_K = {new_q0, new_qf}

        d = dict()
        d[(new_q0, self.char)] = {new_qf}

        f = set()
        f.add(new_qf)

        return NFA (
            new_S,
            new_K,
            new_q0,
            d,
            f
        )

@dataclass
class Star(Regex):
    regex: Regex
    
    def thompson(self) -> NFA[int]:
        nfa = self.regex.thompson()
        new_q0 = self.get_next_state()
        new_qf = self.get_next_state()

        new_K = nfa.K.copy()
        new_K.update([new_q0, new_qf])

        d = nfa.d.copy()
        
        d[(new_q0, EPSILON)] = {nfa.q0, new_qf}

        old_qf = next(iter(nfa.F))

        if old_qf not in d:
            d[(old_qf, EPSILON)] = {nfa.q0, new_qf}
        else:
            d[(old_qf, EPSILON)].add({nfa.q0, new_qf})
        
        new_F = set()
        new_F.add(new_qf)

        return NFA (
            nfa.S,
            new_K,
            new_q0,
            d,
            new_F
        )

@dataclass
class Union(Regex):
    left: Regex
    right: Regex

    def thompson(self) -> NFA[int]:
        left_NFA = self.left.thompson()
        right_NFA = self.right.thompson()

        new_q0 = self.get_next_state()
        new_qf = self.get_next_state()

        new_S = left_NFA.S.copy()
        new_S |= right_NFA.S.copy()

        new_K = left_NFA.K.copy()
        new_K |= right_NFA.K.copy()

        new_K.update([new_q0, new_qf])

        old_left_qf = next(iter(left_NFA.F))
        old_right_qf = next(iter(right_NFA.F))

        d = left_NFA.d.copy()
        d.update(right_NFA.d)

        d[(new_q0, EPSILON)] = {left_NFA.q0, right_NFA.q0}

        if (old_left_qf, EPSILON) not in d:
            d[(old_left_qf, EPSILON)] = {new_qf}
        else:
            d[(old_left_qf, EPSILON)].add(new_qf)
        
        if (old_right_qf, EPSILON) not in d:
            d[(old_right_qf, EPSILON)] = {new_qf}
        else:
            d[(old_right_qf, EPSILON)].add(new_qf)
        
        F = {new_qf}

        return NFA(
            new_S,
            new_K,
            new_q0,
            d,
            F
        )

@dataclass
class Concat(Regex):
    left: Regex
    right: Regex

    def thompson(self) -> NFA[int]:
        left_NFA = self.left.thompson()
        right_NFA = self.right.thompson()

        new_S = left_NFA.S.copy()
        new_S |= right_NFA.S.copy()

        new_K = left_NFA.K.copy()
        new_K |= right_NFA.K.copy()

        old_left_qf = next(iter(left_NFA.F))
        new_qf = next(iter(right_NFA.F))

        d = left_NFA.d.copy()
        d.update(right_NFA.d)

        if (old_left_qf, EPSILON) not in d:
            d[(old_left_qf, EPSILON)] = {right_NFA.q0}
        else:
            d[(old_left_qf, EPSILON)].add(right_NFA.q0)
        
        F = {new_qf}

        return NFA(
            new_S,
            new_K,
            left_NFA.q0,
            d,
            F
        )

@dataclass
class Plus(Regex):
    regex: Regex
    
    def thompson(self) -> NFA[int]:
        nfa = self.regex.thompson()

        new_q0 = self.get_next_state()
        new_qf = self.get_next_state()

        new_K  = nfa.K.copy()
        new_K.update([new_q0, new_qf])
        q0 = new_q0
        old_qf = next(iter(nfa.F))

        d = nfa.d.copy()

        d[(new_q0, EPSILON)] = {nfa.q0}

        if old_qf not in d:
            d[(old_qf, EPSILON)] = {nfa.q0, new_qf}
        else:
            d[(old_qf, EPSILON)].add({nfa.q0, new_qf})

        new_F = set()
        new_F.update([new_qf])

        return NFA (
            nfa.S,
            new_K,
            q0,
            d,
            new_F
        )

@dataclass
class Question_Mark(Regex):
    regex: Regex
    
    def thompson(self) -> NFA[int]:
        nfa = self.regex.thompson()

        new_q0 = self.get_next_state()
        new_qf = self.get_next_state()

        new_K  = nfa.K.copy()
        new_K.update([new_q0, new_qf])
        q0 = new_q0
        old_qf = next(iter(nfa.F))

        d = nfa.d.copy()

        d[(new_q0, EPSILON)] = {nfa.q0, new_qf}
        
        if old_qf not in d:
            d[(old_qf, EPSILON)] = {new_qf}
        else:
            d[(old_qf, EPSILON)].add(new_qf)

        new_F = set()
        new_F.update([new_qf])

        return NFA (
            nfa.S,
            new_K,
            q0,
            d,
            new_F
        )

class ExtractRegex:
    def __init__(self, str_regex):
        self.proccesed_regex = preprocess_regex(str_regex)
        self.pos = 0

    def parse(self) -> Regex:
        return self.parse_union()

    def parse_union(self) -> Regex:
        left_expr = self.parse_concat()

        while self.pos < len(self.proccesed_regex) and self.proccesed_regex[self.pos] == '|':
            self.pos += 1

            right_expr = self.parse_concat()

            left_expr = Union(left_expr, right_expr)

        return left_expr
    
    def parse_concat(self) -> Regex:
        expr = []

        while self.pos < len(self.proccesed_regex) and self.proccesed_regex[self.pos] not in [')', '|']:
            expr.append(self.parse_unary())

        regex = expr[0]

        index = 1

        while index < len(expr):
            regex = Concat(regex, expr[index])
            index += 1

        return regex
    
    def parse_unary(self) -> Regex:
        expr = self.parse_base()

        while self.pos < len(self.proccesed_regex):
            if self.proccesed_regex[self.pos] == '*':
                self.pos += 1
                expr = Star(expr)
            elif self.proccesed_regex[self.pos] == '+':
                self.pos += 1
                expr = Plus(expr)
            elif self.proccesed_regex[self.pos] == '?':
                self.pos += 1
                expr = Question_Mark(expr)
            else:
                break
        
        return expr
    
    def parse_base(self) -> Regex:
        if self.proccesed_regex[self.pos] == '\\':
            self.pos += 1

            if self.pos < len(self.proccesed_regex):
                escaped_char = self.proccesed_regex[self.pos]
                self.pos += 1

            return Character(escaped_char)
        elif self.proccesed_regex[self.pos] == '(':
            self.pos += 1
            expr = self.parse_union()
            self.pos += 1

            return expr
        else:
            char_to_return = self.proccesed_regex[self.pos]
            self.pos += 1

            return Character(char_to_return)

def preprocess_regex(str_regex: str) -> str:
    result = ""
    index = 0

    while index < len(str_regex):
        if str_regex.startswith("[0-9]", index):
            result += '(' + '|'.join(str(number) for number in range(0, 10)) + ')'
            index += 5
        elif str_regex.startswith("[a-z]", index):
            result += '(' + '|'.join(chr(char) for char in range(ord('a'), ord('z') + 1)) + ')'
            index += 5
        elif str_regex.startswith("[A-Z]", index):
            result += '(' + '|'.join(chr(char) for char in range(ord('A'), ord('Z') + 1)) + ')'
            index += 5
        elif str_regex[index] == '\\':
            result += str_regex[index]
            index += 1

            if index < len(str_regex):
                result += str_regex[index]
                index += 1
        elif str_regex[index] == ' ':
            index += 1
        else:
            result += str_regex[index]
            index += 1
    
    return result

def parse_regex(str_regex: str) -> Regex:
    parser = ExtractRegex(str_regex)
    return parser.parse()
