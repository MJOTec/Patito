import lexer
import parser

# Inicializar lexer y parser
lexer = lexer.lexer
parser = parser.parser

# ==========================================================
# Función para probar código fuente
# ==========================================================
def probar_codigo(codigo):
    print("\n==============================")
    print("Probando código:\n")
    print(codigo.strip())
    print("==============================")
    result = parser.parse(codigo, lexer=lexer)
    print(" Resultado:", result)
    print("==============================\n")

# ==========================================================
# Códigos de prueba
# ==========================================================

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

codigo4 = """
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

codigo5 = """
Program expresiones;
var float x, y;
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

# ==========================================================
# Ejecutar todas las pruebas
# ==========================================================
for codigo in [ codigo1, codigo2, codigo3, codigo4, codigo5]:
    probar_codigo(codigo)