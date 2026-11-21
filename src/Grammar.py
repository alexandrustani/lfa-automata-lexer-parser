from .ParseTree import ParseTree
EPSILON = ""

class Grammar:
    @classmethod
    def fromFile(cls, file_name: str):
        with open(file_name, 'r') as f:
            V = set()
            R = set()
            S = None
            line = f.readline().strip()
            while line:
                v, rest = line.split(": ")
                V.add(v)
                if not S:
                    S = v

                alternatives = rest.split("|")
                for alt in alternatives:
                    if " " in alt:
                        n1, n2 = alt.split(" ")
                        V.add(n1)
                        V.add(n2)
                        R.add((v, n1, n2))
                    else: 
                        V.add(alt)
                        R.add((v, alt, None))
            
                line = f.readline().strip()

        return cls(V, R, S)
    
    def __init__(self, V: set[str], R: set[tuple[str, str, str|None]], S: str):
        self.V = V # multimea de neterminali si terminali
        self.R = R # regulile (in FNC)
        self.S = S # simbolul de start
        
    def cykParse(self, w: list[tuple[str, str]]):
        n = len(w)

        if n == 0:
            return None

        T = [[{} for _ in range(n)] for _ in range(n)]

        for j in range(n):
            token, lexeme = w[j]

            for lhs, rhs1, rhs2 in self.R:
                if rhs2 is None and token == rhs1:
                    T[j][j][lhs] = ParseTree(lhs, (token, lexeme))
        
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1

                for k in range(i, j):
                    left_cell = T[i][k]
                    right_cell = T[k + 1][j]

                    for lhs, rhs1, rhs2 in self.R:
                        if rhs2 == None:
                            continue

                        if rhs2 not in right_cell or rhs1 not in left_cell:
                            continue

                        newNode = ParseTree(lhs)

                        newNode.add_children(left_cell[rhs1])
                        newNode.add_children(right_cell[rhs2])

                        T[i][j][lhs] = newNode
        
        if self.S in T[0][n - 1]:
            return T[0][n - 1][self.S]
        
        return None
