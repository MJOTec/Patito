#Tabla de Variables 
class TablaVariables:
    def __init__(self, memory_manager, scope):
        self.variables = {}
        self.memory = memory_manager
        self.scope = scope  # "global" o "local"

    def agregar_variable(self, nombre, tipo):
        if nombre in self.variables:
            raise ValueError(f"Error: variable '{nombre}' ya declarada.")

        
        direccion = self.memory.write(self.scope, tipo, None)

        self.variables[nombre] = {
            "tipo": tipo,
            "direccion": direccion
        }


    def obtener_variable(self, nombre):
        if nombre not in self.variables:
            raise ValueError(f"Error: variable '{nombre}' no declarada.")
        return self.variables[nombre]
    
    def get_type(self, nombre):
        return self.obtener_variable(nombre)["tipo"]

    def get_address(self, nombre):
        return self.obtener_variable(nombre)["direccion"]



class DirectorioFunciones:
    def __init__(self, memory_manager):
        self.funciones = {}
        self.memory = memory_manager

    def agregar_funcion(self, nombre, tipo_retorno, scope):
        if nombre in self.funciones:
            raise ValueError(f"Error: función '{nombre}' ya declarada.")

        if tipo_retorno not in ["void", "PROGRAM"]:
            dir_retorno = self.memory.write("global", tipo_retorno, None)
        else:
            dir_retorno = None

        cuadruplo_inicio = None

        self.funciones[nombre] = {
            "tipo_retorno": tipo_retorno,
            "parametros": [],
            "parametros_nombres": [], 
            "tabla_variables": TablaVariables(self.memory, scope),
            "dir_retorno": dir_retorno,
            "cuadruplo_inicio": cuadruplo_inicio
        }

    def agregar_parametro(self, nombre_funcion, nombre_param, tipo_param):
        func = self.funciones[nombre_funcion]

        # guardar tipo
        func["parametros"].append(tipo_param)

        # guardar nombre del parámetro
        if "parametros_nombres" not in func:
            func["parametros_nombres"] = []
        func["parametros_nombres"].append(nombre_param)

        # solo agregar a tabla de variables si NO existe
        tabla = func["tabla_variables"]
        if nombre_param not in tabla.variables:
            tabla.agregar_variable(nombre_param, tipo_param)

    
    def obtener_funcion(self, nombre):
        if nombre not in self.funciones:
            raise ValueError(f"Error: función '{nombre}' no declarada.")
        return self.funciones[nombre]
    
    def get_type(self, nombre_funcion):
        if nombre_funcion not in self.funciones:
            raise ValueError(f"Error: función '{nombre_funcion}' no declarada.")
        return self.funciones[nombre_funcion]["tipo_retorno"]

    def dump(self):
        print("\n=== DUMP: Directorio de Funciones ===")

        for nombre, funcion in self.funciones.items():
            print(f"\nFunción: {nombre}")
            print(f"  Tipo de retorno: {funcion['tipo_retorno']}")
            print(f"  Dirección retorno: {funcion['dir_retorno']}")
            print(f"  Cuádruplo inicio: {funcion['cuadruplo_inicio']}")

            #  Parámetros 
            print("  Parámetros:")
            if not funcion["parametros"]:
                print("    (ninguno)")
            else:
                for i, p in enumerate(funcion["parametros"]):
                    print(f"    {i}: {funcion["parametros"][i]}")

            #  Variables 
            print("  Variables:")
            tabla_vars = funcion.get("tabla_variables")

            if tabla_vars is None or not hasattr(tabla_vars, "variables"):
                print("    (sin tabla de variables)")
            elif not tabla_vars.variables:
                print("    (ninguna)")
            else:
                for var, info in tabla_vars.variables.items():
                    print(f"    {var}: tipo={info['tipo']}, dir={info['direccion']}")

        print("==============================\n")


    
class Avail:
    def __init__(self, memory_manager):
        self.memory = memory_manager

    def next(self, tipo):
        """Devuelve la dirección virtual para un temporal de tipo dado."""
        # Esto va a fallar si NO hay contexto local activo,
        # por eso se hace push_context() en funciones y en main.
        return self.memory.write("temp", tipo, None)
    
    def dump(self):
        print("\n--- DUMP: Temporales en Memoria ---")
        if not self.memory.call_stack:
            print("   (sin contextos locales)")
        else:
            frame = self.memory.call_stack[-1]  # frame actual
            for tipo, tabla in frame.segments["temp"].items():
                print(f"Tipo {tipo}:")
                if not tabla:
                    print("   (vacío)")
                else:
                    for direccion, valor in tabla.items():
                        print(f"   Dir {direccion} -> {valor}")
        print("-----------------------------------\n")

class TablaConstantes:
    def __init__(self, memory_manager):
        self.constantes = {}
        self.memory = memory_manager

    def agregar_constante(self, valor, tipo):
        if valor in self.constantes:
            return self.constantes[valor]["direccion"]

        direccion = self.memory.write("const", tipo, valor)

        self.constantes[valor] = {
            "tipo": tipo,
            "direccion": direccion
        }

        return direccion

    def obtener_direccion(self, valor):
        return self.constantes[valor]["direccion"]
    
    def dump(self):
        print("\n--- DUMP: Tabla de Constantes ---")
        if not self.constantes:
            print("(vacía)")
        else:
            for valor, entry in self.constantes.items():
                print(f"Valor '{valor}' (tipo {entry['tipo']}) -> Dir {entry['direccion']}")
        print("---------------------------------\n")

class QuadManager:
    def __init__(self):
        self.quads = []
        self.counter = 0  # Para numerar los cuádruplos

    def generate(self, operator, left_operand, right_operand, result):
        """Crea un nuevo cuádruplo y lo agrega a la lista"""
        quad = (operator, left_operand, right_operand, result)
        self.quads.append(quad)
        self.counter += 1
        return quad

    def get_all(self):
        """Devuelve todos los cuádruplos"""
        return self.quads

    def show(self):
        """Imprime todos los cuádruplos en formato legible"""
        print("\n=== Cuádruplos generados ===")
        for i, (op, left, right, res) in enumerate(self.quads):
            print(f"{i}: ({op}, {left}, {right}, {res})")
        print("============================\n")

    def reset(self):
        """Limpia la lista de cuádruplos"""
        self.quads.clear()
        self.counter = 0
