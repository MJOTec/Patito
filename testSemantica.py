import io
import sys
import importlib
import lexer as lexer_module
import parser as parser_module
from semantics import Avail, QuadManager


def crear_parser_nuevo():
    """Reimporta e inicializa un parser completamente nuevo."""
    importlib.reload(lexer_module)
    importlib.reload(parser_module)

    lexer = lexer_module.lexer
    parser = parser_module.parser

    # Reinciar atributos personalizados del parser
    parser.current_type = None
    parser.current_var_table = None
    parser.dir_func = None
    parser.nombre_funcion = None
    parser.id_list = []

    parser.PilaO = []
    parser.PTypes = []
    parser.Poper = []
    parser.temp_list = Avail()
    parser.Quad = QuadManager()

    return lexer, parser


def probar_codigo(codigo):
    print("\n==============================")
    print("Probando código: \n")
    print(codigo.strip())
    print("==============================")

    # Crear lexer y parser limpios para este código
    lexer, parser = crear_parser_nuevo()

    buffer = io.StringIO()
    sys_stdout_original = sys.stdout
    sys.stdout = buffer

    try:
        result = parser.parse(codigo, lexer=lexer)
    except Exception as e:
        buffer.write(f"\nExcepción durante el análisis: {e}\n")
    finally:
        sys.stdout = sys_stdout_original

    salida_parser = buffer.getvalue()

    if salida_parser.strip():
        print(salida_parser.strip())

    if "Error" in salida_parser or "error" in salida_parser:
        print("Resultado: Error detectado durante el análisis.")
    else:
        print("Resultado: Análisis completado correctamente.")

    print("==============================\n")


# Casos de prueba
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
var n: int;
void hola (){{}}; 
int papa (){{}}; 
main { 
    print(n);
}
end
"""

codigo3 = """
Program prueba;
var n: int;
void hola (x:int, j:int){{}}; 
main { 
    print(n);
}
end
"""

codigo4 = """
Program prueba;
var n: int;
void hola (x:int, x:int){{}}; 
main { 
    print(n);
}
end
"""

codigo5 = """
Program prueba;
var n,z: int ;
float Division (z:float, y:float){
    {
    resultado = z/y;
    }
};
main { 
    print(n);
}
end
"""

codigo6 = """
Program papa;
var n,z: int ;
float Division (z:int, y:float){
    {
    resultado = z+y;
    }
};
float Mate (){
    {
    resultado = 5;
    }
};
main { 
    print(2);
}
end
"""

codigo7 = """
Program prueba;
var n,j,t: int;
main { 
    print((t*j/(t+n))*j);
}
end
"""

codigo8 = """
Program prueba;
var x,y: int;
main { 
    x = 5*y;
    print(x);
    print("hello world",y);
}
end
"""

codigo9 = """
Program prueba;
var x,y: int;
main { 
    x = (5*y*6+y)>y;
}
end
"""

codigo_if_else = """
Program prueba;
var A,B,C,D: int;
main { 
    if (A+B>D){
        if(A<B){
            A=0;
            B=B+D;
        }
    }
}
end
"""

# Ejecutar pruebas
for codigo in [codigo_if_else]:
    probar_codigo(codigo)
