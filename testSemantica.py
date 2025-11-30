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
    print("Probando código:\n")
    print(codigo.strip())
    print("==============================")

    # Crear lexer y parser limpios
    lexer, parser = crear_parser_nuevo()

    try:
        parser.parse(codigo, lexer=lexer)
        print("\nResultado: Análisis completado correctamente.")
    except Exception as e:
        print(f"\nError durante el análisis:\n   {e}")

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

    void suma(a: int, y: int){
        var res : int;
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

    void imprimir(a: int, b:int){
        {
            print(suma(a,b));
        }
    };

main
{
    a = 1;
    b = 2;
    imprimir(a,b);
}
end
'''
codigo12 = '''
program programa;
var a, b, c : int;

main
{
    a = 5;
    b = 3;

    print("Valores iniciales:");
    print(a, b);

    c = a + b;
    print(c);

    if (c < 10) {
        print("c es menor que 10");
    } else {
        print("c es mayor o igual a 10");
    };

    while (b < 10) do {
        b = b + 2;
        print(b);
    };

    print("Fin del programa");
}
end
'''

codigo13 = """
Program prueba;
var a, b: int;

int suma(x: int, y: int){
    {
        return x+y;
    }
};

main {
    a = 3;
    b = 4;
    print(suma(a,b) + suma(2,5));
}
end

"""

factorialRecursivo = """
Program prueba;
var n, res: int;

int fact(x: int){
    var temp: int;
    {
        if (x < 2) {
            return 1;
        }
        else {
            temp = x - 1;
            return x * fact(temp);
        };
    }
};

main {
    n = 5;
    res = fact(n);
    print(res);
}
end

"""

fibonacciRecursivo = """
Program prueba;
var n, res: int;

int fib(x: int){
    var a, b: int;
    {
        if (x < 2) {
            return x;
        }
        else {
            a = x - 1;
            b = x - 2;
            return fib(a) + fib(b);
        };
    }
};

main {
    n = 6;
    res = fib(n);
    print(res);
}
end

"""

negativo_simple = """
Program prueba;
var x, y : int;

int resta(x: int){
    {
        return (x - y);
    }
};


main {
    y = 3;
    x = 5;
    print(resta(x));
}
end
"""


# Ejecutar pruebas
for codigo in [negativo_simple]:
    probar_codigo(codigo)
