# memory_manager.py

# =========================
# GLOBAL + CONSTANT MEMORY
# =========================

class GlobalMemory:
    def __init__(self):
        self.segments = {
            "global": { "int": {}, "float": {} },
            "const":  { "int": {}, "float": {}, "string": {} }
        }

        self.offset = {
            "global": { "int": 1000, "float": 2000 },
            "const":  { "int": 8000, "float": 9000, "string": 10000 }
        }

    def write(self, scope, tipo, valor=None):
        direccion = self.offset[scope][tipo]
        self.segments[scope][tipo][direccion] = valor
        self.offset[scope][tipo] += 1
        return direccion

    def read(self, direccion):
        for scope in self.segments:
            for tipo in self.segments[scope]:
                if direccion in self.segments[scope][tipo]:
                    return self.segments[scope][tipo][direccion]
        return None



# LOCAL + TEMP MEMORY (STACK FRAME)

class LocalMemory:
    def __init__(self):
        self.segments = {
            "local": { "int": {}, "float": {} },
            "temp":  { "int": {}, "float": {}, "bool": {} }
        }

        self.offset = {
            "local": { "int": 3000, "float": 4000 },
            "temp":  { "int": 5000, "float": 6000, "bool": 7000 }
        }

    def write(self, scope, tipo, valor=None):
        direccion = self.offset[scope][tipo]
        self.segments[scope][tipo][direccion] = valor
        self.offset[scope][tipo] += 1
        return direccion

    def read(self, direccion):
        for scope in self.segments:
            for tipo in self.segments[scope]:
                if direccion in self.segments[scope][tipo]:
                    return self.segments[scope][tipo][direccion]
        return None


# MASTER MEMORY MANAGER

class MemoryManager:
    def __init__(self):
        self.global_memory = GlobalMemory()
        self.call_stack = []   # Stack de LocalMemory (1 por función)

    #CONTEXTOS 

    def push_context(self):
        """Crear memoria local para una nueva función"""
        self.call_stack.append(LocalMemory())

    def pop_context(self):
        """Eliminar memoria local al salir de función"""
        if not self.call_stack:
            raise RuntimeError("No hay contexto local para eliminar")
        self.call_stack.pop()

    # WRITE 

    def write(self, scope, tipo, valor=None):
        if scope in ["local", "temp"]:
            if not self.call_stack:
                raise RuntimeError("No hay contexto local activo")
            return self.call_stack[-1].write(scope, tipo, valor)

        if scope in ["global", "const"]:
            return self.global_memory.write(scope, tipo, valor)

        raise ValueError(f"Scope inválido: {scope}")

    #READ 

    def read(self, direccion):
        #intentar leer desde contexto local
        if self.call_stack:
            valor = self.call_stack[-1].read(direccion)
            if valor is not None:
                return valor

        # intentar leer desde memoria global/const
        valor = self.global_memory.read(direccion)
        if valor is not None:
            return valor

        raise ValueError(f"Dirección {direccion} no encontrada")

    # DEBUG 

    def dump(self):
        print("\n========== GLOBAL MEMORY ==========")
        for scope, tipos in self.global_memory.segments.items():
            print(f"\n[{scope.upper()}]")
            for tipo, tabla in tipos.items():
                print(f"  {tipo}: {tabla}")

        print("\n========== LOCAL STACK ==========")
        for i, frame in enumerate(self.call_stack):
            print(f"\n--- FRAME {i} ---")
            for scope, tipos in frame.segments.items():
                print(f"[{scope.upper()}]")
                for tipo, tabla in tipos.items():
                    print(f"  {tipo}: {tabla}")

        print("=================================\n")
