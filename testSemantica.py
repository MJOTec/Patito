import importlib
import lexer as lexer_module
import parser as parser_module
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
caso1 = """
Program prueba;
var a, b, c, d, suma : int;

main {
    a = 3;
    b = 7;
    c = 2;
    d = 8;

    suma = a + b + c + d;

    print(suma);
}
end
"""

caso2 = """
Program prueba;
var x, y : int;

main {
    x = 1;
    y = 0;

    while (x < 5) do {
        y = y + (x * 2);
        x = x + 1;
    };

    print(y);
}
end
"""

caso3 = """
Program prueba;
var r : int;

int evaluar(x:int){
    var t : int;
    {
        if (x > 10) {
            return x * 2;
        }
        else {
            t = x + 5;
            return t;
        };
    }
};

main {
    r = evaluar(8);
    print(r);
}
end
"""

caso4 = """
Program prueba;
var n, res : int;

int cuenta(x:int){
    {
        if (x == 0) {
            return 0;
        }
        else {
            return cuenta(x - 1);
        };
    }
};

main {
    n = 4;
    res = cuenta(n);
    print(res);
}
end
"""

caso5 = """
Program prueba;
var res : int;

int sumaRec(x:int){
    {
        if (x < 1) {
            return 0;
        }
        else {
            return x + sumaRec(x - 1);
        };
    }
};

main {
    res = sumaRec(5);
    print(res);
}
end
"""

factorialIterativo = """
Program prueba;
var n, res : int;

int factorial(x:int){
    var i, acc : int;
    {
        acc = 1;
        i = x;

        while (i > 1) do {
            acc = acc * i;
            i = i - 1;
        };

        return acc;
    }
};

main {
    n = 5;
    res = factorial(n);
    print(res);
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

fibonacciIterativo = """
Program prueba;
var n, res : int;

int fib(x:int){
    var a, b, i, temp : int;
    {
        if (x < 2) {
            return x;
        };

        a = 0;
        b = 1;
        i = 2;

        while (i <= x) do {
            temp = a + b;
            a = b;
            b = temp;
            i = i + 1;
        };

        return b;
    }
};

main {
    n = 6;
    res = fib(n);
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
            return fib(x-1) + fib(x-2);
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
    x = -5;
    y = +(4-x);
    print(resta(x));
}
end
"""

# Ejecutar pruebas
probar_codigo(caso1)
