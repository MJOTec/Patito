from lexer import lexer

# Lista de casos de prueba “rompibles”
casos = [
    '1variable',            # Identificador inválido
    'var$var',              # Caracter ilegal
    '123.45.67',            # Número mal formado
    '12a34',                # Mezcla número-letra
    '"hola',                # String sin cierre
    '"hola\\"mundo"',       # String con escape válido
    '"hola\\q"',            # String con escape inválido
    '@ # &',                # Símbolos desconocidos
    'program1var;',         # Palabra reservada + número
    'ifelse',               # Palabra reservada pegada
    'program miPrograma;',  # Caso válido
    'var int x, y;',        # Caso válido
    'float z;',             # Caso válido
    '+1.',
    '1a'
]

for i, codigo in enumerate(casos, 1):
    print(f"\n=== CASO {i}: {codigo} ===")
    lexer.input(codigo)
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Imprimir en el formato original LexToken
        print(tok)
