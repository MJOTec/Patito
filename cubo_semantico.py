cubo_semantico = {
    '+': {
        'int':   {'int': 'int', 'float': 'float', 'bool': 'error'},
        'float': {'int': 'float', 'float': 'float', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '-': {
        'int':   {'int': 'int', 'float': 'float', 'bool': 'error'},
        'float': {'int': 'float', 'float': 'float', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '*': {
        'int':   {'int': 'int', 'float': 'float', 'bool': 'error'},
        'float': {'int': 'float', 'float': 'float', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '/': {
        'int':   {'int': 'float', 'float': 'float', 'bool': 'error'},  # división siempre produce float
        'float': {'int': 'float', 'float': 'float', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '<': {
        'int':   {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'float': {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '>': {
        'int':   {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'float': {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '<=': {
        'int':   {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'float': {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '>=': {
        'int':   {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'float': {'int': 'bool', 'float': 'bool', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'error'}
    },
    '==': {
        'int':   {'int': 'bool', 'float': 'error', 'bool': 'error'},
        'float': {'int': 'error', 'float': 'bool', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'bool'}
    },
    '!=': {
        'int':   {'int': 'bool', 'float': 'error', 'bool': 'error'},
        'float': {'int': 'error', 'float': 'bool', 'bool': 'error'},
        'bool':  {'int': 'error', 'float': 'error', 'bool': 'bool'}
    }
}

# Ejemplo 1: int + float
print(cubo_semantico['+']['int']['float'])  # → float

# Ejemplo 2: float > int
print(cubo_semantico['>']['float']['int'])  # → bool

# Ejemplo 3: bool == bool
print(cubo_semantico['==']['bool']['bool'])  # → bool

# Ejemplo 4: int == float
print(cubo_semantico['==']['int']['float'])  # → error
