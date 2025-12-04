import ply.lex as lex

tokens = [
    'ID', 'CTE_INT', 'CTE_FLOAT', 'CTE_STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
    'ASSIGN', 'GT', 'LT', 'LE', 'GE','NEQ', 'EQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',   
    'SEMI', 'COMMA', 'COLON'
]

reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'void': 'VOID',
    'main': 'MAIN',
    'end': 'END',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'print': 'PRINT',
    'return': 'RETURN',
}

tokens += list(reserved.values())

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'

t_NEQ       = r'!='
t_EQ        = r'=='
t_GE        = r'>='
t_LE        = r'<='
t_GT        = r'>'
t_LT        = r'<'

t_ASSIGN    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACKET  = r'\['   
t_RBRACKET  = r'\]'   

t_SEMI      = r';'
t_COMMA     = r','
t_COLON     = r':'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_CTE_FLOAT(t):
    r'\d+\.\d+([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'"([^\\\n]|(\\.))*?"'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
