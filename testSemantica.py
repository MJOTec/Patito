import lexer
import parser
import io
import sys


# Inicializar lexer y parser
lexer = lexer.lexer
parser = parser.parser


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
var n,j,t: int;
p: float;
main { 
    print(n,j);
}
end
"""

codigo2 = """
Program prueba;
var n,j,t: int;
p: float;
main { 
    print(n,j);
}
end
"""

# Ejecutar todas las pruebas
for codigo in [ codigo1,codigo2]:
    probar_codigo(codigo)