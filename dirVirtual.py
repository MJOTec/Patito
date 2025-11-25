class MemoryManager:
    def __init__(self):
        # Segmentos por tipo semántico
        self.segments = {
            "global":   { "int":{}, "float":{}},
            "local":    { "int":{}, "float":{}},
            "temp":     { "int":{}, "float":{}, "bool":{}},
            "const":    { "int":{}, "float":{}, "string":{} },
        } 

        # Offset inicial para cada segmento
        self.offset = {
            "global":  { "int":1000, "float":2000},
            "local":   { "int":3000, "float":4000},
            "temp":    { "int":5000, "float":6000, "bool":7000},
            "const":   { "int":8000, "float":9000, "string":10000 },
        }

    # WRITE: asigna dirección automática y guarda valor
    def write(self, scope, tipo, valor):
        direccion = self.offset[scope][tipo]

        # Guarda valor en su segmento
        self.segments[scope][tipo][direccion] = valor

        # Incrementa offset para la siguiente dirección del mismo tipo
        self.offset[scope][tipo] += 1

        return direccion

    # READ: obtiene valor con solo la dirección
    def read(self, direccion):
        # Buscar en todos los segmentos y tipos
        for scope in self.segments:
            for tipo in self.segments[scope]:
                if direccion in self.segments[scope][tipo]:
                    return self.segments[scope][tipo][direccion]
        raise ValueError(f"Dirección {direccion} no encontrada")
    
    def dump(self):
        print("\n" + "="*50)
        print("MEMORY DUMP (DEBUG) ")
        print("="*50)

        for scope, tipos in self.segments.items():
            print(f"\n--- SEGMENTO: {scope.upper()} ---")

            for tipo, tabla in tipos.items():
                print(f"  Tipo: {tipo}")

                if len(tabla) == 0:
                    print("     (vacío)")
                else:
                    for direccion, valor in sorted(tabla.items()):
                        print(f"     {direccion}: {valor}")

        print("="*50 + "\n")

