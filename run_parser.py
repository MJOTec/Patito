from lexer import lexer
from parser_module import parser

# Leer archivo de código
archivo = "prueba.txt"  # Cambia por el nombre de tu archivo
with open(archivo, 'r') as f:
    codigo = f.read()

# Mostrar tokens
print("=== TOKENS ===")
lexer.input(codigo)
for tok in lexer:
    print(tok)

# Parsear
print("\n=== PARSE ===")
parser.parse(codigo)
print("=== PARSE COMPLETADO ===")
