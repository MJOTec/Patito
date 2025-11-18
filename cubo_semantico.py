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
