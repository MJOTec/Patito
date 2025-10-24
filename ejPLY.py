import ply.lex as lex
import ply.yacc as yacc

# ----- LÉXICO -----
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN')

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ignore  = ' \t'  # Ignorar espacios y tabulaciones

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# ----- PARSER -----
def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+': p[0] = p[1] + p[3]
    else: p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    if p[2] == '*': p[0] = p[1] * p[3]
    else: p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Error de sintaxis")

parser = yacc.yacc()

# ----- PRUEBA -----
expr = "(3 + 4) * 2 - 7 / 2"
result = parser.parse(expr)
print(f"Resultado: {result}")
