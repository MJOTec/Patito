import lexer
import parser as little_duck_parser
import io
import sys


# Inicializar lexer y parser
lexer = lexer.lexer
parser = little_duck_parser.parser


def probar_codigo(codigo):
    print("\n==============================")
    print("Probando código: \n")
    print(codigo.strip())
    print("==============================")

    # Redirigir la salida estándar (para capturar prints del parser o lexer)
    buffer = io.StringIO()
    sys_stdout_original = sys.stdout
    sys.stdout = buffer

    try:
        little_duck_parser.reset_parser_state()
        result = parser.parse(codigo, lexer=lexer)
    except Exception as e:
        # Si ocurre una excepción inesperada se registra
        buffer.write(f"\nExcepción durante el análisis: {e}\n")
    finally:
        # Restaurar salida estándar
        sys.stdout = sys_stdout_original

    # Obtener todo lo que se imprimió durante el análisis
    salida_parser = buffer.getvalue()

    # Mostrar lo que el parser imprimió
    if salida_parser.strip():
        print(salida_parser.strip())

    # Si existe la palabra error, detectarlo
    if "Error" in salida_parser or "error" in salida_parser:
        print("Resultado: Error detectado durante el análisis.")
    else:
        print("Resultado: Análisis completado correctamente.")

    print("==============================\n")


# Casos de prueba válidos

codigo1 = """
Program prueba;
main { }
end
"""

codigo2 = """
program calc;
main {
    a = -10;
    [n = 3;]
    while (a) do {
        print("a:", b);
        a = a + 1;
    } ;
} end
"""

codigo3 = """
Program bloques;
main {
    [ 
        print("bloque 1");
        [ 
            print("bloque 2");
        ]
    ]
}
end
"""

codigo4 = """
Program expresiones;
var x,y : float ;
main {
    x = 3.5 + 2 * (4 - 1) / 2;
    y = -x + +5.5 * 2;
    if (x == y) {
        print("iguales");
    } else {
        print("diferentes");
    };
}
end
"""


codigo5 = """
program flow;
var n: int; acc: int;
main {
    n = 3;
    acc = 0;
    while (n) do {
        acc = acc + 1;
        print("iter", acc, "n=", n);
        n = n - 1;
    } ;
    if (acc) {
        print("done", acc, "iters");
    } else {
        print("never");
    } ;
    [
        n = 3;
        acc = 0; 
        while (n) do {
            acc = acc + 1;
            print("iter", acc, "n=", n);
            n = n - 1;
        } ;
        if (acc) {
            print("done", acc, "iters");
        } else {
            print("never");
        } ;
    ]
} end
"""


# Casos de prueba inválidos

# Error léxico: carácter '@' no reconocido
codigo_err_lex = """
program test;
main {
    x = 10 @ 5;
}
end
"""

# Error sintáctico: falta de llaves en if
codigo_err_sint = """
program test;
main {
    if (x == 3)
        print("error");
end
"""

# Ejecutar todas las pruebas
for codigo in [ codigo1, codigo2, codigo3, codigo4, codigo5, codigo_err_lex, codigo_err_sint]:
    probar_codigo(codigo)