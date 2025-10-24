from lark import Lark, Transformer

# ----- GRAMÁTICA -----
grammar = """
?start: expr

?expr: expr "+" term   -> add
     | expr "-" term   -> sub
     | term

?term: term "*" factor -> mul
     | term "/" factor -> div
     | factor

?factor: NUMBER        -> number
       | "(" expr ")"

%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""

# ----- TRANSFORMADOR (EVALUADOR) -----
class Eval(Transformer):
    def number(self, n): return float(n[0])
    def add(self, items): return items[0] + items[1]
    def sub(self, items): return items[0] - items[1]
    def mul(self, items): return items[0] * items[1]
    def div(self, items): return items[0] / items[1]

# ----- PARSER + EVALUADOR -----
parser = Lark(grammar, parser="lalr", transformer=Eval())

expr = "(3 + 4) * 2 - 7 / 2"
result = parser.parse(expr)
print(f"Resultado: {result}")
