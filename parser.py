import ply.yacc as yacc
from lexer import tokens
from semantics import DirectorioFunciones

precedence = (
    ('right','UMINUS','UPLUS'),
    ('left','MINUS','PLUS'),
    ('left','TIMES','DIVIDE'),
    ('nonassoc','GT','LT', 'NEQ', 'EQ')
)

current_type = None
current_var_table = None
dir_func = None
nombre_funcion = None
id_list = []  # lista temporal para almacenar IDs antes de conocer su tipo

#Reset parser
def reset_parser_state():
    global current_type, current_var_table, dir_func, nombre_funcion, id_list
    current_type = None
    current_var_table = None
    dir_func = None
    nombre_funcion = None
    id_list = []


# ----------------------------
# REGLAS GRAMATICALES
# ----------------------------

def p_programa(p):
    'programa : PROGRAM create_dir ID fill_dir SEMI var_or_not funcs_or_not MAIN body END clean_memory'
    pass

def p_create_dir(p):
    "create_dir : "
    global dir_func
    dir_func = DirectorioFunciones()

def p_fill_dir(p):
    "fill_dir : "
    global dir_func, nombre_funcion
    nombre_funcion = p[-1]
    dir_func.agregar_funcion(nombre_funcion,"VOID")

def p_clean_memory(p):
    "clean_memory :"
    global dir_func, current_var_table, current_type, id_list, nombre_funcion
    # Borrar referencias globales
    dir_func = None
    current_var_table = None
    current_type = None
    nombre_funcion = None
    id_list.clear()


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
    global id_list
    nombre_id = p[-1]
    id_list.append(nombre_id)

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
    global current_type, id_list, dir_func, nombre_funcion

    current_type = p[-1]

    # Agregar todas las variables que estaban en espera
    for nombre_var in id_list:
        dir_func.funciones[nombre_funcion]["tabla_variables"].agregar_variable(nombre_var, current_type)

    # Limpiar la lista para la próxima declaración
    id_list.clear()

def p_funcs(p):
    'funcs : void_or_type ID create_func LPAREN ids RPAREN LBRACE vars_or_not body RBRACE end_func SEMI'
    pass

def p_end_func(p):
    'end_func :'
    global current_var_table, nombre_funcion, dir_func
    dir_func.funciones[nombre_funcion]["tabla_variables"] = None
    current_var_table = None

def p_create_func(p):
    'create_func :'
    global nombre_funcion, dir_func
    nombre_funcion = p[-1]
    dir_func.agregar_funcion(nombre_funcion,current_type)

def p_void_or_type(p):
    '''void_or_type : VOID func_type
                    | type
    '''
    pass

def p_func_type(p):
    'func_type : '
    global current_type
    current_type = p[-1] 

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
                 | llamada COMMA
                 | print
                 | LBRACKET statement_loop RBRACKET
                 '''
    pass

def p_assign(p):
    'assign : ID ASSIGN expresion SEMI'
    pass

def p_expresion(p):
    '''expresion : exp relations_or_not'''
    pass

def p_relations_or_not(p):
    '''relations_or_not : GT exp
                        | LT exp
                        | NEQ exp
                        | EQ exp
                        | empty'''
    pass

def p_exp(p):
    'exp : term more_terms'
    pass

def p_more_terms(p):
    '''more_terms : PLUS exp
                  | MINUS exp
                  | empty'''
    pass

def p_term(p):
    'term : factor more_factors'
    pass

def p_more_factors(p):
    '''more_factors : TIMES term
                    | DIVIDE term
                    | empty'''
    pass

def p_factor_type(p):
    '''factor_type : LPAREN expresion RPAREN
              | PLUS id_or_cte %prec UPLUS
              | MINUS id_or_cte %prec UMINUS
              | id_or_cte
              | llamada'''
    pass

def p_factor(p):
    '''factor : factor_type
    '''
    pass

def p_id_or_cte(p):
    '''id_or_cte : ID
                 | cte'''
    pass

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
    '''cte : CTE_INT
           | CTE_FLOAT'''
    pass

def p_condition(p):
    'condition : IF LPAREN expresion RPAREN body else_or_not SEMI'
    pass

def p_else_or_not(p):
    '''else_or_not : ELSE body
                   | empty'''
    pass

def p_cycle(p):
    'cycle : WHILE LPAREN expresion RPAREN DO body SEMI'
    pass

def p_print(p):
    'print : PRINT LPAREN expresion_or_string RPAREN SEMI'
    pass

def p_expresion_or_string(p):
    '''expresion_or_string : expresion list_objs
                           | CTE_STRING list_objs'''
    pass

def p_list_objs(p):
    '''list_objs : COMMA expresion_or_string
                 | empty'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' línea {p.lineno}")
    else:
        print("Error de sintaxis al final del archivo")

parser = yacc.yacc()
