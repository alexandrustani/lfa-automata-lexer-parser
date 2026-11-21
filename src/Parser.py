from .Lexer import Lexer
from .Grammar import Grammar

class Parser():
    def __init__(self, lexer: Lexer, grammar: Grammar) -> None:
        self.lexer = lexer
        self.grammar = grammar
    
    def parse(self, input: str) -> str:
        lexical_analization = self.lexer.lex(input)

        tokens = [token for token in lexical_analization if token[0] != "SPACE"]

        parseTree = self.grammar.cykParse(tokens)

        if parseTree is None:
            return None
        
        return parseTree.to_string()
