def inicializar_memoria(program_obj):
    memoria = {}

    # Cargar constantes
    for valor, info in program_obj["constantes"].items():
        if info["tipo"] == "int":
            memoria[info["direccion"]] = int(valor)
        else:
            memoria[info["direccion"]] = valor

    # Inicializar variables globales
    for func, data in program_obj["funciones"].items():
        if data["tipo_retorno"] == "PROGRAM":
            for varinfo in data["variables"].values():
                memoria[varinfo["direccion"]] = None

    return memoria


class ActivationRecord:
    def __init__(self):
        self.memory = {}   # locals + temps


class VM:
    def __init__(self, quadruples, program_obj):
        self.quadruples = quadruples
        self.ip = 0

        self.global_memory = inicializar_memoria(program_obj)
        self.funcs = program_obj["funciones"]

        self.call_stack = []
        self.return_ips = []
        self.pending_ar = None

    def get(self, addr):
        if self.call_stack:
            frame = self.call_stack[-1].memory
            if addr in frame:
                return frame[addr]
        return self.global_memory.get(addr, None)

    def set(self, addr, value):
        # locals or temps
        if 3000 <= addr < 8000:
            self.call_stack[-1].memory[addr] = value
        else:
            self.global_memory[addr] = value

    def run(self):
        # Frame for MAIN
        self.call_stack.append(ActivationRecord())

        while self.ip < len(self.quadruples):
            op, left, right, result = self.quadruples[self.ip]

            # === ERA ===
            if op == "Era":
                self.pending_ar = ActivationRecord()

            # === PARAM ===
            elif op == "PARAM":
                val = self.get(left)
                self.pending_ar.memory[result] = val

            # === GOSUB ===
            elif op == "GOSUB":
                self.return_ips.append(self.ip + 1)
                self.call_stack.append(self.pending_ar)
                self.pending_ar = None
                self.ip = result
                continue

            # === RETURN ===
            elif op == "RETURN":
                val = self.get(left)
                self.global_memory[result] = val
                self.ip += 1
                continue

            # === EndFunc ===
            elif op == "EndFunc":
                self.call_stack.pop()
                if not self.return_ips:
                    return
                self.ip = self.return_ips.pop()
                continue

            # === ASIGNACIÓN ===
            elif op == "=":
                self.set(result, self.get(left))

            # === NEGACIÓN ===
            elif op == "NEG":
                self.set(result, -self.get(left))

            # === ARITMÉTICAS ===
            elif op == "+":
                self.set(result, self.get(left) + self.get(right))
            elif op == "-":
                self.set(result, self.get(left) - self.get(right))
            elif op == "*":
                self.set(result, self.get(left) * self.get(right))
            elif op == "/":
                self.set(result, self.get(left) / self.get(right))

            # === RELACIONALES ===
            elif op == "<":
                self.set(result, self.get(left) < self.get(right))
            elif op == ">":
                self.set(result, self.get(left) > self.get(right))
            elif op == "==":
                self.set(result, self.get(left) == self.get(right))
            elif op == "!=":
                self.set(result, self.get(left) != self.get(right))

            # === SALTOS ===
            elif op == "GoTo":
                self.ip = result
                continue

            elif op == "GoToF":
                if not self.get(left):
                    self.ip = result
                    continue

            # === PRINT ===
            elif op == "PRINT":
                val = self.get(result)
                print(val)

            else:
                raise Exception(f"Operación no implementada: {op}")

            self.ip += 1

import json

# Cargar el archivo .obj generado por el compilador
with open("program.obj", "r") as f:
    program_obj = json.load(f)

# Extraer cuádruplos y construir la VM
quadruples = program_obj["cuadruplos"]
vm = VM(quadruples, program_obj)

# Ejecutar el programa
print("\n======= INICIANDO VIRTUAL MACHINE =======\n")
vm.run()
print("\n======= FIN DE LA EJECUCIÓN =======\n")