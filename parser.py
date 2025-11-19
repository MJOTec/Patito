import ply.yacc as yacc
from lexer import tokens
from semantics import DirectorioFunciones, Avail, QuadManager
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
    print(f"[DEBUG] Entrando a main, usando contexto global: {global_name}")


def p_create_dir(p):
    "create_dir : "
    p.parser.dir_func = DirectorioFunciones()
    print("Entre al programa")

def p_fill_dir(p):
    "fill_dir : "
    p.parser.nombre_funcion = p[-1]
    p.parser.dir_func.agregar_funcion(p.parser.nombre_funcion,"VOID")

def p_clean_memory(p):
    "clean_memory :"
    p.parser.Quad.show()
    # Borrar referencias globales
    p.parser.dir_func = None
    p.parser.current_var_table = None
    p.parser.current_type = None
    p.parser.nombre_funcion = None
    p.parser.id_list.clear()


def p_var_or_not(p):
    '''var_or_not : vars
                  | empty'''
    pass

def p_vars(p):
    'vars : VAR dec_var'
    pass

def p_dec_var(p):
    'dec_var : list_id COLON type SEMI dec_var_opt'
    pass

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

    # Agregar todas las variables que estaban en espera
    for nombre_var in p.parser.id_list:
        p.parser.dir_func.funciones[p.parser.nombre_funcion]["tabla_variables"].agregar_variable(nombre_var, p.parser.current_type)

    # Limpiar la lista para la próxima declaración
    p.parser.id_list.clear()

def p_funcs(p):
    'funcs : void_or_type ID create_func LPAREN ids RPAREN LBRACE vars_or_not body RBRACE end_func SEMI'
    pass

def p_end_func(p):
    'end_func :'
    p.parser.dir_func.funciones[p.parser.nombre_funcion]["tabla_variables"] = None
    p.parser.current_var_table = None

def p_create_func(p):
    'create_func :'
    p.parser.nombre_funcion = p[-1]
    p.parser.dir_func.agregar_funcion(p.parser.nombre_funcion,p.parser.current_type)

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
    '''ids : ID capture_id COLON type capture_type ids_loop
           | empty'''
    pass


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
                 '''
    pass

def p_assign(p):
    'assign : ID ASSIGN expresion SEMI'
    var_name = p[1]
    # obtener el resultado de la expresión
    result = p.parser.PilaO.pop()
    result_type = p.parser.PTypes.pop()

    # obtener tipo de la variable
    var_type = p.parser.dir_func.obtener_funcion(p.parser.nombre_funcion)["tabla_variables"].get_type(var_name)

    if result_type == var_type or (result_type == "int" and var_type == "float"):
        # generar el cuádruplo de asignación
        p.parser.Quad.generate("=", result, None, var_name)
        print(f"[QUAD] =, {result}, None, {var_name}")
    else:
        print(f"Error: Tipo incompatible en asignación {var_type} = {result_type}")

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
    print("Se agrego " + p[-1] + " a los operadores")

def p_check_relation(p):
    'check_relation :'
    if p.parser.Poper and p.parser.Poper[-1] in ['>', '<', '==', '!=']:
            print("Entre al check types")
            right_operand = p.parser.PilaO.pop()
            right_type = p.parser.PTypes.pop()
            left_operand = p.parser.PilaO.pop()
            left_type = p.parser.PTypes.pop()
            operator = p.parser.Poper.pop()
            result_type = cubo_semantico[operator][left_type][right_type]
            print("El tipo final es: " + result_type)
            if result_type != 'error':
                result = p.parser.temp_list.next()
                p.parser.Quad.generate(operator,left_operand,right_operand,result)
                p.parser.PilaO.append(result)
                p.parser.PTypes.append(result_type)
            else:
                print("Error: Tipo no valido")

def p_exp(p):
    'exp : term check_plus_minus more_terms'
    pass

def p_check_plus_minus(p):
    'check_plus_minus :'

    if p.parser.Poper and p.parser.Poper[-1] in ['+', '-']:
        print("Entre al check types")
        right_operand = p.parser.PilaO.pop()
        right_type = p.parser.PTypes.pop()
        left_operand = p.parser.PilaO.pop()
        left_type = p.parser.PTypes.pop()
        operator = p.parser.Poper.pop()
        result_type = cubo_semantico[operator][left_type][right_type]
        print("El tipo final es: " + result_type)
        if result_type != 'error':
            result = p.parser.temp_list.next()
            p.parser.Quad.generate(operator,left_operand,right_operand,result)
            p.parser.PilaO.append(result)
            p.parser.PTypes.append(result_type)
        else:
            print("Error: Tipo no valido")


def p_more_terms(p):
    '''more_terms : PLUS capture_Oper exp
                  | MINUS capture_Oper exp
                  | empty'''
    pass

def p_capture_Oper(p):
    'capture_Oper :'
    p.parser.Poper.append(p[-1])
    print("Se agrego " + p[-1] + " a los operadores")

def p_term(p):
    'term : factor check_mult_div more_factors'
    pass

def p_check_mult_div(p):
    'check_mult_div :'
    if p.parser.Poper and p.parser.Poper[-1] in ['*', '/']:
        print("Entre al check types")
        right_operand = p.parser.PilaO.pop()
        right_type = p.parser.PTypes.pop()
        left_operand = p.parser.PilaO.pop()
        left_type = p.parser.PTypes.pop()
        operator = p.parser.Poper.pop()
        result_type = cubo_semantico[operator][left_type][right_type]
        print("El tipo final es: " + result_type)
        if result_type != 'error':
            result = p.parser.temp_list.next()
            p.parser.Quad.generate(operator,left_operand,right_operand,result)
            p.parser.PilaO.append(result)
            p.parser.PTypes.append(result_type)
        else:
            print("Error: Tipo no valido")

def p_more_factors(p):
    '''more_factors : TIMES capture_Oper term
                    | DIVIDE capture_Oper term
                    | empty'''
    pass

def p_factor_type(p):
    '''factor_type : LPAREN begin_paren expresion RPAREN end_paren
              | PLUS id_or_cte
              | MINUS id_or_cte
              | id_or_cte
              | llamada'''
    pass

def p_begin_paren(p):
    'begin_paren :'
    p.parser.Poper.append("(")
    print("Entro en ()")

def p_end_paren(p):
    'end_paren :'
    p.parser.Poper.pop()
    print("Saliendo del ()")

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
    p.parser.nombre_id = p[-1]
    p.parser.PilaO.append(p.parser.nombre_id)
    print("Se agrego a la pilaO: " + p.parser.nombre_id)
    tipo_var = p.parser.dir_func.obtener_funcion(p.parser.nombre_funcion)["tabla_variables"].get_type(p.parser.nombre_id)
    print("El tipo de la variable es: " + tipo_var)
    p.parser.PTypes.append(tipo_var)

def p_llamada(p):
    'llamada : ID LPAREN expresion_or_not RPAREN'
    pass

def p_expresion_or_not(p):
    '''expresion_or_not : expresion expresion_loop
                        | empty
    '''
    pass

def p_expresion_loop(p):
    '''expresion_loop : COMMA expresion expresion_loop
                        | empty
    '''
    pass

def p_cte(p):
    '''cte : CTE_INT capture_cte_int
           | CTE_FLOAT capture_cte_float'''
    pass

def p_capture_cte_int(p):
    'capture_cte_int :'
    valor = p[-1]
    tipo = "int"
    p.parser.PilaO.append(valor)
    print("Se agrego a la pilaO: " + str(valor))
    print("El tipo de la variable es: " + tipo)
    p.parser.PTypes.append(tipo)

def p_capture_cte_float(p):
    'capture_cte_float :'
    valor = p[-1]
    tipo = "float"
    p.parser.PilaO.append(valor)
    print("Se agrego a la pilaO: " + str(valor))
    print("El tipo de la variable es: " + tipo)
    p.parser.PTypes.append(tipo)

def p_condition(p):
    'condition : IF LPAREN expresion RPAREN mark_if body else_or_not SEMI mark_end_if'
    pass


def p_mark_if(p):
    'mark_if :'
    exp_type = p.parser.PTypes.pop()
    print("El tipo es: " + exp_type)
    if exp_type != "bool":
        raise TypeError("Type mismatch: IF condition must be bool")

    # 2. Sacar el resultado de la expresión
    result = p.parser.PilaO.pop()

    # 3. Crear GotoF <expr>, _, ?
    p.parser.Quad.generate("GotoF", result, None, None)

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
    print(p.parser.Quad.quads[pending_jump])

def p_else_or_not(p):
    '''else_or_not : mark_else ELSE body
                   | empty'''
    pass


def p_mark_else(p):
    'mark_else : '
    p.parser.Quad.generate("Goto", None, None, None)
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
    p.parser.Quad.generate("GotoF", result, None, None)
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
    print(f"[QUAD] PRINT, None, None, {expr}")

def p_print_str(p):
    'print_str :'
    p.parser.Quad.generate("PRINT", None, None, p[-1])
    print(f"[QUAD] PRINT, None, None, {p[-1]}")

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


parser = yacc.yacc()


# Inicializar los atributos del parser
parser.current_type = None
parser.current_var_table = None
parser.dir_func = None
parser.nombre_funcion = None
parser.id_list = []

parser.PilaO = []
parser.PTypes = []
parser.Poper = []
parser.PJumps = []

parser.temp_list = Avail()
parser.Quad = QuadManager()