def inicializar_memoria(program_obj):
    memoria = {}

    # 1. Cargar constantes
    for valor, info in program_obj["constantes"].items():
        # Manejar ints y strings automáticamente
        if info["tipo"] == "int":
            memoria[info["direccion"]] = int(valor)
        elif info["tipo"] == "string":
            memoria[info["direccion"]] = valor
        else:
            memoria[info["direccion"]] = valor

    # 2. Inicializar variables globales
    for func, data in program_obj["funciones"].items():
        if data["tipo_retorno"] == "PROGRAM":  
            for varinfo in data["variables"].values():
                memoria[varinfo["direccion"]] = None

    return memoria



class VM:
    def __init__(self, quadruples, memory):
        self.quadruples = quadruples
        self.memory = memory
        self.ip = 0  # instruction pointer
    
    def get(self, addr):
        return self.memory.get(addr, None)

    def set(self, addr, value):
        self.memory[addr] = value

    def run(self):
        while self.ip < len(self.quadruples):
            op, left, right, result = self.quadruples[self.ip]

            # ================== ASIGNACIÓN ==================
            if op == '=':
                self.set(result, self.get(left))

            # ================== ARITMÉTICA ==================
            elif op == '+':
                self.set(result, self.get(left) + self.get(right))

            elif op == '-':
                self.set(result, self.get(left) - self.get(right))

            elif op == '*':
                self.set(result, self.get(left) * self.get(right))

            elif op == '/':
                self.set(result, self.get(left) / self.get(right))

            # ================== RELACIONALES ==================
            elif op in ['<', '>', '==', '!=', '<=', '>=']:
                a = self.get(left)
                b = self.get(right)
                if op == '<':   self.set(result, a < b)
                if op == '>':   self.set(result, a > b)
                if op == '==':  self.set(result, a == b)
                if op == '!=':  self.set(result, a != b)
                if op == '<=':  self.set(result, a <= b)
                if op == '>=':  self.set(result, a >= b)

            # ================== SALTOS ==================
            elif op == 'GoTo':
                self.ip = result
                continue

            elif op == 'GoToF':
                if not self.get(left):
                    self.ip = result
                    continue

            # ================== PRINT ==================
            elif op == 'PRINT':
                print(self.get(result))

            else:
                raise Exception(f"Operación no implementada: {op}")

            self.ip += 1


import json
with open("program.obj", "r") as f:
    program_obj = json.load(f)

memory = inicializar_memoria(program_obj)
quadruples = program_obj["cuadruplos"]

vm = VM(quadruples, memory)
vm.run()


