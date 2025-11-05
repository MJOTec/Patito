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
