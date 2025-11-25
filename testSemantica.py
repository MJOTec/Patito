import io
import sys
import importlib
import lexer as lexer_module
import parser as parser_module
from semantics import Avail, QuadManager, TablaConstantes
from dirVirtual import MemoryManager


def crear_parser_nuevo():
    importlib.reload(lexer_module)
    importlib.reload(parser_module)

    memoria = MemoryManager()

    lexer = lexer_module.lexer

    # Llamar a una función que construya un parser nuevo con memoria nueva
    parser = parser_module.create_parser(memoria)

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

codigoif = """
Program prueba;
var x,y: int;
main { 
    if (x > y){
        print("x es mayor que y");
    };
    print(x);
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

codelse= """
Program prueba;
var x : int;
main {
    if(x>1){
        print("X es mayor que 1");
    }
    else{
        print("X es menor que 1");
    };
    print("Se acabo el programa");
}
end
"""

codewhile= """
Program prueba;
var x : int;
main {
    while(x>1)
    do{
        x = x + 1;
    };
}
end
"""

codeLoopIf = """
Program prueba;
var a,b,c,d : int;
main {
    if(a+b>d){
        if(a<b){
            a = 0;
            b = b+d;
        }
        else{
            c = a+b;
        };
    }
    else{
        a = b+c;
    };
    d = b+a*c;
}
end
"""

codigo10 = '''
program test;
var a,b,c,d : int;
    f, e : float;

    void suma(a: float, y: int){
        var res : float;
        {
            res = a + y;
        }
    }; 

    void resta(uno: int, dos: int){
        var res : int;
        {
            res = uno - dos;
        }
    }; 
main
{
    if(a < b){
        a = b;
        a = 2;
        while (a > b) do {
        print(c);
        };
        print("hola", "papa", 1 + 2);
    } else {
        b = 1;
    };
    print(a);
    suma(a,b);
}
end
'''

codigo11 = '''
program test;
var a,b: int;

    int suma(a: int, y: int){
        var res : int;
        {
            res = a + y;
            return res;
        }
    }; 

main
{
    a = 1;
    b = 2;
    print(suma(a,b));
}
end
'''

# Ejecutar pruebas
for codigo in [codigo11]:
    probar_codigo(codigo)
