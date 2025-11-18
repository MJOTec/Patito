# --- Tabla de Variables ---
class TablaVariables:
    def __init__(self):
        self.variables = {}

    def agregar_variable(self, nombre, tipo):
        if nombre in self.variables:
            raise ValueError(f"Error: variable '{nombre}' ya declarada.")
        self.variables[nombre] = {
            "tipo": tipo,
        }

    def obtener_variable(self, nombre):
        if nombre not in self.variables:
            raise ValueError(f"Error: variable '{nombre}' no declarada.")
        return self.variables[nombre]
    
    def get_type(self, nombre):
        if nombre not in self.variables:
            raise ValueError(f"Error: variable '{nombre}' no declarada.")
        return self.variables[nombre]["tipo"]


# --- Directorio de Funciones ---
class DirectorioFunciones:
    def __init__(self):
        self.funciones = {}

    def agregar_funcion(self, nombre, tipo_retorno):
        if nombre in self.funciones:
            raise ValueError(f"Error: función '{nombre}' ya declarada.")
        self.funciones[nombre] = {
            "tipo_retorno": tipo_retorno,
            "parametros": [],
            "tabla_variables": TablaVariables()
        }

    def agregar_parametro(self, nombre_funcion, nombre_param, tipo_param):
        self.funciones[nombre_funcion]["parametros"].append({
            "nombre": nombre_param,
            "tipo": tipo_param
        })
        self.funciones[nombre_funcion]["tabla_variables"].agregar_variable(nombre_param, tipo_param)

    def obtener_funcion(self, nombre):
        if nombre not in self.funciones:
            raise ValueError(f"Error: función '{nombre}' no declarada.")
        return self.funciones[nombre]
    
class Avail:
    def __init__(self):
        self.temporaries = []
        self.counter = 0
    def next(self):
        "Devuelve un temporal libre o genera uno nuevo"
        if self.temporaries:
            return self.temporaries.pop()
        else:
            self.counter += 1
            return f"t{self.counter}"
    def release(self, temp):
        "Libera un temoral (lo devuelve al pool)"
        self.temporaries.append(temp)

class QuadManager:
    def __init__(self):
        self.quads = []
        self.counter = 0  # Para numerar los cuádruplos

    def generate(self, operator, left_operand, right_operand, result):
        """Crea un nuevo cuádruplo y lo agrega a la lista"""
        quad = (operator, left_operand, right_operand, result)
        self.quads.append(quad)
        self.counter += 1
        print(f"[Quad {self.counter}] {operator}, {left_operand}, {right_operand}, {result}")
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
