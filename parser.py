import ply.yacc as yacc
from lexer import tokens
from semantics import DirectorioFunciones, Avail, QuadManager, TablaConstantes
from cubo_semantico import cubo_semantico

# ----------------------------
# REGLAS GRAMATICALES
# ----------------------------

def p_programa(p):
    'programa : PROGRAM create_dir ID fill_dir SEMI var_or_not funcs_or_not main_block END clean_memory'
    pass

def p_main_block(p):
    'main_block : MAIN set_global_scope body'
    pass

def p_set_global_scope(p):
    'set_global_scope :'
    # Recuperar el nombre del programa (la primera función creada)
    global_name = list(p.parser.dir_func.funciones.keys())[0]
    p.parser.nombre_funcion = global_name
    p.parser.current_var_table = p.parser.dir_func.funciones[global_name]["tabla_variables"]

    # El GoTo del quad 0 salta al inicio del main
    p.parser.Quad.quads[0] = ["GoTo", None, None, p.parser.Quad.counter]

    # Crear contexto local para temporales y (si quisieras) locales de main
    p.parser.memoria.push_context()


def p_create_dir(p):
    "create_dir : "
    p.parser.dir_func = DirectorioFunciones(p.parser.memoria)
    p.parser.Quad.generate("GoTo", None, None, None)

def p_fill_dir(p):
    "fill_dir : "
    p.parser.nombre_funcion = p[-1]
    p.parser.dir_func.agregar_funcion(p.parser.nombre_funcion,"PROGRAM","global")

def p_clean_memory(p):
    "clean_memory :"
    p.parser.Quad.show()
    p.parser.memoria.dump()
    p.parser.dir_func.dump()

    # Cerrar contexto de main si quedó alguno
    if p.parser.memoria.call_stack:
        p.parser.memoria.pop_context()

    # exportar objeto
    export_obj(p.parser,"program.obj")

    #exportar objeto
    export_obj(p.parser,"program.obj")




def p_var_or_not(p):
    '''var_or_not : vars
                  | empty'''
    pass

def p_vars(p):
    'vars : VAR dec_var'
    pass

def p_dec_var(p):
    'dec_var : list_id COLON type create_vars SEMI dec_var_opt'
    pass

def p_create_vars(p):
    'create_vars : '
    tipo = p.parser.current_type
    func = p.parser.nombre_funcion

    tabla = p.parser.dir_func.funciones[func]["tabla_variables"]
    for nombre in p.parser.id_list:
        tabla.agregar_variable(nombre, tipo)

    # Limpiar la lista para la próxima declaración
    p.parser.id_list.clear()

def p_dec_var_opt(p):
    '''dec_var_opt : dec_var
                   | empty'''
    pass


def p_list_id(p):
    '''list_id : ID capture_id list_id_opt'''
    pass

def p_capture_id(p):
    "capture_id :"
    nombre_id = p[-1]
    p.parser.id_list.append(nombre_id)

def p_list_id_opt(p):
    '''list_id_opt : COMMA list_id
                   | empty'''
    pass

def p_type(p):
    '''type : INT capture_type
            | FLOAT capture_type'''
    pass

def p_capture_type(p):
    "capture_type :"
    p.parser.current_type = p[-1]

def p_funcs(p):
    'funcs : void_or_type ID create_func LPAREN ids RPAREN LBRACE vars_or_not body RBRACE end_func SEMI'
    pass

def p_end_func(p):
    'end_func :'
    p.parser.current_var_table = None
    p.parser.Quad.generate("EndFunc", None, None, None)

    # Sacar el contexto local de la función
    p.parser.memoria.pop_context()


def p_create_func(p):
    'create_func :'
    # Nuevo contexto de memoria local para esta función
    p.parser.memoria.push_context()

    p.parser.nombre_funcion = p[-1]
    # La tabla de variables de esta función usará scope "local"
    p.parser.dir_func.agregar_funcion(p.parser.nombre_funcion, p.parser.current_type, "local")
    p.parser.dir_func.funciones[p.parser.nombre_funcion]["cuadruplo_inicio"] = p.parser.Quad.counter


def p_void_or_type(p):
    '''void_or_type : VOID func_type
                    | type
    '''
    pass

def p_func_type(p):
    'func_type : '
    p.parser.current_type = p[-1] 

def p_funcs_or_not(p):
    '''funcs_or_not : funcs funcs_or_not
                    | empty'''
    pass


def p_ids(p):
    '''ids : ID capture_id COLON type create_params ids_loop
           | empty'''
    pass

def p_create_param(p):
    'create_params : '
    tipo = p.parser.current_type
    func = p.parser.nombre_funcion

    for nombre in p.parser.id_list:
        p.parser.dir_func.agregar_parametro(func, nombre, tipo)

    # Limpiar la lista para la próxima declaración
    p.parser.id_list.clear()

def p_ids_loop(p):
    '''ids_loop : COMMA ids
                | empty'''
    pass

def p_vars_or_not(p):
    '''vars_or_not : vars
                   | empty'''
    pass

def p_body(p):
    'body : LBRACE statement_loop RBRACE'
    pass

def p_statement_loop(p):
    '''statement_loop : statement statement_loop
                      | empty'''
    pass

def p_statement(p):
    '''statement : assign
                 | condition
                 | cycle
                 | llamada SEMI
                 | print
                 | LBRACKET statement_loop RBRACKET
                 | RETURN expresion SEMI end_return 
                 '''
    pass

def p_end_return(p):
    'end_return :'
    func = p.parser.nombre_funcion
    tipo_funcion = p.parser.dir_func.funciones[func]["tipo_retorno"]
    dir_retorno = p.parser.dir_func.funciones[func]["dir_retorno"]

    result = p.parser.PilaO.pop()
    result_type = p.parser.PTypes.pop()

    if tipo_funcion == "void":
        raise TypeError("Una función void no puede retornar un valor.")

    if result_type != tipo_funcion:
        raise TypeError(f"Tipo de retorno incorrecto: se esperaba {tipo_funcion}, se obtuvo {result_type}")

    # Generar el cuádruplo
    p.parser.Quad.generate("RETURN", result, None, dir_retorno)

def p_assign(p):
    'assign : ID ASSIGN expresion SEMI'
    var_name = p[1]
    # obtener el resultado de la expresión
    result = p.parser.PilaO.pop()
    result_type = p.parser.PTypes.pop()

    # obtener tipo de la variable
    var_type = p.parser.dir_func.obtener_funcion(p.parser.nombre_funcion)["tabla_variables"].get_type(var_name)
    # get address
    var_dir = p.parser.dir_func.obtener_funcion(p.parser.nombre_funcion)["tabla_variables"].get_address(var_name)

    if result_type == var_type or (result_type == "int" and var_type == "float"):
        # generar el cuádruplo de asignación
        p.parser.Quad.generate("=", result, None, var_dir)
    else:
        raise TypeError(f"Tipo incompatible en asignación: {var_type} = {result_type}")

def p_expresion(p):
    '''expresion : exp relations_or_not'''
    pass

def p_relations_or_not(p):
    '''relations_or_not : GT capture_relation exp check_relation
                        | LT capture_relation exp check_relation
                        | NEQ capture_relation exp check_relation
                        | EQ capture_relation exp check_relation
                        | empty'''
    pass

def p_capture_relation(p):
    'capture_relation :'
    p.parser.Poper.append(p[-1])

def p_check_relation(p):
    'check_relation :'
    if p.parser.Poper and p.parser.Poper[-1] in ['>', '<', '==', '!=']:
            right_operand = p.parser.PilaO.pop()
            right_type = p.parser.PTypes.pop()
            left_operand = p.parser.PilaO.pop()
            left_type = p.parser.PTypes.pop()
            operator = p.parser.Poper.pop()
            result_type = cubo_semantico[operator][left_type][right_type]
            if result_type != 'error':
                result = p.parser.temp_list.next(result_type)
                p.parser.Quad.generate(operator,left_operand,right_operand,result)
                p.parser.PilaO.append(result)
                p.parser.PTypes.append(result_type)
            else:
                raise TypeError("Tipo no válido")


def p_exp(p):
    'exp : term more_terms'
    pass

def p_do_plus_minus(p):
    'do_plus_minus :'
    if p.parser.Poper and p.parser.Poper[-1] in ['+', '-']:
        right_operand = p.parser.PilaO.pop()
        right_type = p.parser.PTypes.pop()
        left_operand = p.parser.PilaO.pop()
        left_type = p.parser.PTypes.pop()
        operator = p.parser.Poper.pop()
        result_type = cubo_semantico[operator][left_type][right_type]
        if result_type != 'error':
            result = p.parser.temp_list.next(result_type)
            p.parser.Quad.generate(operator, left_operand, right_operand, result)
            p.parser.PilaO.append(result)
            p.parser.PTypes.append(result_type)
        else:
            raise TypeError("Tipo no válido en suma/resta")


def p_more_terms(p):
    '''more_terms : PLUS capture_Oper term do_plus_minus more_terms
                  | MINUS capture_Oper term do_plus_minus more_terms
                  | empty'''
    pass

def p_capture_Oper(p):
    'capture_Oper :'
    p.parser.Poper.append(p[-1])

def p_term(p):
    'term : factor more_factors'
    pass


def p_do_mult_div(p):
    'do_mult_div :'
    if p.parser.Poper and p.parser.Poper[-1] in ['*', '/']:
        right_operand = p.parser.PilaO.pop()
        right_type = p.parser.PTypes.pop()
        left_operand = p.parser.PilaO.pop()
        left_type = p.parser.PTypes.pop()
        operator = p.parser.Poper.pop()
        result_type = cubo_semantico[operator][left_type][right_type]
        if result_type != 'error':
            result = p.parser.temp_list.next(result_type)
            p.parser.Quad.generate(operator, left_operand, right_operand, result)
            p.parser.PilaO.append(result)
            p.parser.PTypes.append(result_type)
        else:
            raise TypeError("Tipo no válido en mult/div")


def p_more_factors(p):
    '''more_factors : TIMES capture_Oper factor do_mult_div more_factors
                    | DIVIDE capture_Oper factor do_mult_div more_factors
                    | empty'''
    pass

def p_factor_type(p):
    '''factor_type : LPAREN begin_paren expresion RPAREN end_paren
                   | PLUS unary_sign
                   | MINUS unary_sign
                   | id_or_cte
                   | llamada'''
    pass


def p_unary_sign(p):
    'unary_sign : id_or_cte'
    # El operando ya quedó en PilaO por id_or_cte
    # Checar si venía un signo negativo justo antes (p[-1] == '-')
    if p[-1] == '-':
        val = p.parser.PilaO.pop()
        tipo_val = p.parser.PTypes.pop()

        # TEMPORAL del MISMO TIPO
        temp = p.parser.temp_list.next(tipo_val)

        # Generar cuadruplo de negación unaria
        p.parser.Quad.generate("NEG", val, None, temp)

        # Push temporal ya negado a la pila
        p.parser.PilaO.append(temp)
        p.parser.PTypes.append(tipo_val)

def p_begin_paren(p):
    'begin_paren :'
    p.parser.Poper.append("(")

def p_end_paren(p):
    'end_paren :'
    p.parser.Poper.pop()

def p_factor(p):
    '''factor : factor_type
    '''
    pass

def p_id_or_cte(p):
    '''id_or_cte : ID capture_id_oper
                 | cte'''
    pass

def p_capture_id_oper(p):
    'capture_id_oper :'
    nombre = p[-1]

    # 1. Intentar obtener variable local
    try:
        tabla_local = p.parser.dir_func.obtener_funcion(p.parser.nombre_funcion)["tabla_variables"]
        direccion = tabla_local.get_address(nombre)
        tipo = tabla_local.get_type(nombre)
    
    except:
        # 2. Buscar la función global por su tipo_retorno "PROGRAM"
        nombre_global = next(
            n for n, info in p.parser.dir_func.funciones.items()
            if info["tipo_retorno"] == "PROGRAM"
        )

        tabla_global = p.parser.dir_func.obtener_funcion(nombre_global)["tabla_variables"]
        direccion = tabla_global.get_address(nombre)
        tipo = tabla_global.get_type(nombre)

    # Finalmente push a las pilas
    p.parser.PilaO.append(direccion)
    p.parser.PTypes.append(tipo)




def p_llamada(p):
    'llamada : ID create_era save_call_name LPAREN expresion_or_not RPAREN finish_call'
    pass

def p_save_call_name(p):
    'save_call_name :'
    p.parser.nombre_funcion_llamada = p[-2]
    p.parser.param_counter = 0

def p_finish_call(p):
    'finish_call :'
    func = p.parser.nombre_funcion_llamada
    func_info = p.parser.dir_func.obtener_funcion(func)

    # Validar número de argumentos
    if p.parser.param_counter != len(func_info["parametros"]):
        raise TypeError(f"Número incorrecto de argumentos en llamada a {func}")

    # Crear GOSUB
    start = func_info["cuadruplo_inicio"]
    p.parser.Quad.generate("GOSUB", func, None, start)

    # Manejar retorno si no es void
    if func_info["tipo_retorno"] != "void":
        ret_dir = func_info["dir_retorno"]
        tipo_ret = func_info["tipo_retorno"]

        temp = p.parser.temp_list.next(tipo_ret)
        p.parser.Quad.generate("=", ret_dir, None, temp)

        # Push resultado de la función como cualquier temporal normal
        p.parser.PilaO.append(temp)
        p.parser.PTypes.append(tipo_ret)

def p_create_era(p):
    'create_era :'
    p.parser.Quad.generate("Era", None, None, p[-1])

def p_expresion_or_not(p):
    '''expresion_or_not : expresion handle_param expresion_loop
                        | empty
    '''
    pass

def p_expresion_loop(p):
    '''expresion_loop : COMMA expresion handle_param expresion_loop
                        | empty
    '''
    pass

def p_handle_param(p):
    'handle_param :'
    
    func = p.parser.nombre_funcion_llamada
    func_info = p.parser.dir_func.obtener_funcion(func)

    # Verificar que no excede
    if p.parser.param_counter >= len(func_info["parametros"]):
        raise TypeError(f"Demasiados argumentos en llamada a {func}")

    # Sacar el argumento
    arg = p.parser.PilaO.pop()
    arg_type = p.parser.PTypes.pop()

    expected_type = func_info["parametros"][p.parser.param_counter]
    if arg_type != expected_type:
        raise TypeError(f"Argumento {p.parser.param_counter+1} incorrecto: se esperaba {expected_type}, se obtuvo {arg_type}")

    # Obtener el nombre correcto del parámetro
    param_name = func_info["parametros_nombres"][p.parser.param_counter]

    # Obtener su dirección real de la tabla de variables
    param_dir = func_info["tabla_variables"].get_address(param_name)

    # Crear el cuádruplo PARAM hacia esa dirección
    p.parser.Quad.generate("PARAM", arg, None, param_dir)

    p.parser.param_counter += 1


def p_cte(p):
    '''cte : CTE_INT capture_cte_int
           | CTE_FLOAT capture_cte_float'''
    pass

def p_capture_cte_int(p):
    'capture_cte_int :'
    valor = p[-1]
    tipo = "int"

    direccion = p.parser.constantes.agregar_constante(valor, tipo)

    p.parser.PilaO.append(direccion)
    p.parser.PTypes.append(tipo)


def p_capture_cte_float(p):
    'capture_cte_float :'
    valor = p[-1]
    tipo = "float"

    direccion = p.parser.constantes.agregar_constante(valor, tipo)

    p.parser.PilaO.append(direccion)
    p.parser.PTypes.append(tipo)


def p_condition(p):
    'condition : IF LPAREN expresion RPAREN mark_if body else_or_not SEMI mark_end_if'
    pass


def p_mark_if(p):
    'mark_if :'
    exp_type = p.parser.PTypes.pop()
    if exp_type != "bool":
        raise TypeError("Type mismatch: IF condition must be bool")

    # 2. Sacar el resultado de la expresión
    result = p.parser.PilaO.pop()

    # 3. Crear GotoF <expr>, _, ?
    p.parser.Quad.generate("GoToF", result, None, None)

    # 4. Guardar el índice del cuádruplo pendiente
    p.parser.PJumps.append(p.parser.Quad.counter - 1)


def p_mark_end_if(p):
    'mark_end_if :'
    # Sacar el salto pendiente
    pending_jump = p.parser.PJumps.pop()

    # Rellenar el destino con el índice del siguiente cuádruplo
    end = p.parser.Quad.counter

    op, left, right, _ = p.parser.Quad.quads[pending_jump]
    p.parser.Quad.quads[pending_jump] = (op, left, right, end)

def p_else_or_not(p):
    '''else_or_not : mark_else ELSE body
                   | empty'''
    pass


def p_mark_else(p):
    'mark_else : '
    p.parser.Quad.generate("GoTo", None, None, None)
    false = p.parser.PJumps.pop()
    p.parser.PJumps.append(p.parser.Quad.counter - 1)
    op, left, right, _ = p.parser.Quad.quads[false]
    p.parser.Quad.quads[false] = [op, left, right, p.parser.Quad.counter]


def p_cycle(p):
    'cycle : WHILE mark_while LPAREN expresion RPAREN skip_while DO body SEMI return_while'
    pass

def p_mark_while(p):
    'mark_while : '
    p.parser.PJumps.append(p.parser.Quad.counter)

def p_skip_while(p):
    'skip_while : '
    exp_type = p.parser.PTypes.pop()
    if exp_type != "bool":
        raise TypeError("Type mismatch: while condition must be bool")
    result = p.parser.PilaO.pop()
    p.parser.Quad.generate("GoToF", result, None, None)
    p.parser.PJumps.append(p.parser.Quad.counter-1)

def p_return_while(p):
    'return_while :'
    end = p.parser.PJumps.pop()
    return_while = p.parser.PJumps.pop()
    p.parser.Quad.generate("GoTo", None, None, return_while)
    op, left, right, _ = p.parser.Quad.quads[end]
    p.parser.Quad.quads[end] = (op, left, right, p.parser.Quad.counter)


def p_print(p):
    'print : PRINT LPAREN expresion_or_string RPAREN SEMI'
    pass

def p_expresion_or_string(p):
    '''expresion_or_string : expresion print_expr list_objs
                           | CTE_STRING print_str list_objs'''
    pass

def p_print_expr(p):
    'print_expr :'
    expr = p.parser.PilaO.pop()
    p.parser.PTypes.pop()
    p.parser.Quad.generate("PRINT", None, None, expr)

def p_print_str(p):
    'print_str :'
    valor = p[-1][1:-1]   # Quitar comillas
    direccion = p.parser.constantes.agregar_constante(valor, "string")
    p.parser.Quad.generate("PRINT", None, None, direccion)


def p_list_objs(p):
    '''list_objs : COMMA expresion_or_string
                 | empty'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis en '{p.value}' línea {p.lineno}")
    else:
        raise SyntaxError("Error de sintaxis al final del archivo")



def export_obj(parser, filename):
    data = {
        "funciones": {},
        "constantes": parser.constantes.constantes,
        "cuadruplos": parser.Quad.get_all()
    }

    for nombre, f in parser.dir_func.funciones.items():
        data["funciones"][nombre] = {
            "tipo_retorno": f["tipo_retorno"],
            "dir_retorno": f["dir_retorno"],
            "cuadruplo_inicio": f["cuadruplo_inicio"],
            "parametros": f["parametros"],
            "variables": f["tabla_variables"].variables  # ← SERIALLIZABLE
        }

    import json
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def create_parser(memoria):
    parser = yacc.yacc()

    # Inicialización de estructuras del parser
    parser.memoria = memoria
    parser.temp_list = Avail(memoria)
    parser.constantes = TablaConstantes(memoria)
    parser.Quad = QuadManager()

    parser.current_type = None
    parser.current_var_table = None
    parser.dir_func = None
    parser.param_counter = 0
    parser.nombre_funcion_llamada = None
    parser.nombre_funcion = None
    parser.id_list = []

    parser.PilaO = []
    parser.PTypes = []
    parser.Poper = []
    parser.PJumps = []

    return parser
