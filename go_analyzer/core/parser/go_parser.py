from go_analyzer.core.lexer import lexer, tokens
import ply.yacc as yacc
from datetime import datetime
import os

# START Contribution: José Toapanta
# Parser rules for package declaration, imports, and global program structure
# Function declarations with multiple return types: func name() (type1, type2) { }
# Slice data structure []type{values} for dynamic arrays with type safety
# For loop control structure with three variations: condition-only, infinite, and classic (init; cond; incr)
# Arithmetic expressions with multiple operators (+, -, *, /, %) respecting precedence and associativity
# Logical conditions with connectors (&&, ||, !) combined with relational operators (==, !=, <, >, <=, >=)
# Variable assignment with all primitive types (int, float64, string, bool) supporting explicit and type inference
# Complete expression evaluation with literals, identifiers, post-increment/decrement, and parenthesized grouping

parse_errors = []
syntax_errors = []
semantic_errors = []
success_log = []
suppress_errors = False

loop_context_stack = []

context_stack = [
    {
        "consts": {},
        "variables": {},
        "functions": {},
        "tipos": {
            "str-funciones": ["len"],
        },
    }
]


def log_info(msg):
    """Registra información de producciones reconocidas"""
    print(f"✔ {msg}")
    success_log.append(f"✔ {msg}")


def p_program(p):
    """program : package_declaration import global_statement_list"""
    log_info("program")


def p_package_declaration(p):
    "package_declaration : PACKAGE IDENTIFIER"
    log_info("package_declaration")


def p_import(p):
    """import : simple_import
    | import simple_import
    | empty"""
    log_info("import")


def p_simple_import(p):
    """simple_import : IMPORT STRING"""
    log_info("simple_import")
    context_stack[-1]["variables"][p[2]] = "imported_package"


def p_empty(p):
    "empty :"
    pass


def p_global_statement_list(p):
    """global_statement_list : global_statement
    | global_statement_list global_statement"""
    log_info("global_statement_list")


def p_global_statement(p):
    """global_statement : global_var_dec
    | global_const_dec
    | function_declaration
    | method_declaration
    | type_declaration"""
    log_info("global_statement")


def p_block(p):
    """block : LBRACE enter_block exit_block RBRACE
    | LBRACE enter_block statement_list  exit_block RBRACE"""


def p_statement_list(p):
    """statement_list : statement
    | statement_list statement"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_statement(p):
    """statement : assignment
    | assignment_compound
    | variable_declaration
    | expression
    | return_statement
    | for_statement
    | if_statement
    | switch_statement
    | break_statement
    | continue_statement
    | call_expression"""
    p[0] = p[1]


def p_global_var_dec(p):
    """global_var_dec : VAR IDENTIFIER type
    | VAR IDENTIFIER type ASSIGN expression
    | VAR IDENTIFIER ASSIGN expression"""
    var_name = p[2]
    # Check for redeclaration in global scope only
    if var_name in context_stack[-1]["variables"]:
        semantic_errors.append(
            f"Error semántico: La variable '{var_name}' ya fue declarada en este ámbito."
        )
    if len(p) == 4:  # VAR IDENTIFIER type
        tipo = p[3]
        context_stack[-1]["variables"][var_name] = tipo
    elif len(p) == 5:  # VAR IDENTIFIER ASSIGN expression
        tipo = p[4]
        context_stack[-1]["variables"][var_name] = tipo
    elif len(p) == 6:  # VAR IDENTIFIER type ASSIGN expression
        tipo_declarado = p[3]
        tipo_expresion = p[5]
        if tipo_declarado != tipo_expresion:
            semantic_errors.append(
                f"Error Semantico: Tipo declarado '{tipo_declarado}' no coincide con tipo de expresion '{tipo_expresion}'."
            )
        context_stack[-1]["variables"][var_name] = tipo_declarado
    log_info("global_var_dec")


def p_global_const_dec(p):
    """global_const_dec : CONST IDENTIFIER type ASSIGN expression
    | CONST IDENTIFIER ASSIGN expression"""
    var_name = p[2]
    if var_name in context_stack[0]["consts"]:
        semantic_errors.append(
            f"Error semántico: La constante '{var_name}' ya fue declarada previamente."
        )
    else:
        context_stack[0]["consts"][var_name] = True
    if len(p) == 6:
        tipo = p[3]
    else:
        tipo = p[4]
    context_stack[-1]["variables"][var_name] = tipo
    log_info("global_const_dec")


def p_local_var_dec(p):
    """local_var_dec : VAR IDENTIFIER type
    | VAR IDENTIFIER type ASSIGN expression
    | VAR IDENTIFIER ASSIGN expression"""
    var_name = p[2]
    # Semantic check: Variable redeclaration in same scope
    if var_name in context_stack[-1]["variables"]:
        semantic_errors.append(
            f"Error semántico: La variable '{var_name}' ya fue declarada en este ámbito."
        )
    else:
        if len(p) == 4:
            context_stack[-1]["variables"][var_name] = p[3]
        elif len(p) == 6:
            context_stack[-1]["variables"][var_name] = p[3]
        else:
            context_stack[-1]["variables"][var_name] = p[4]
    log_info("local_var_dec")


def p_local_const_dec(p):
    """local_const_dec : CONST IDENTIFIER type ASSIGN expression
    | CONST IDENTIFIER ASSIGN expression"""
    var_name = p[2]
    if var_name in context_stack[0]["consts"]:
        semantic_errors.append(
            f"Error semántico: La constante '{var_name}' ya fue declarada previamente."
        )
    else:
        context_stack[0]["consts"][var_name] = True
    if len(p) == 6:
        tipo = p[3]
    else:
        tipo = p[4]
    context_stack[-1]["variables"][var_name] = tipo
    log_info("local_const_dec")


def p_assignment_compound(p):
    """assignment_compound : IDENTIFIER operator_assign expression"""
    var_name = p[1]
    # Check if trying to modify a constant
    if var_name in context_stack[0]["consts"]:
        semantic_errors.append(
            f"Error semántico: La constante '{var_name}' no puede ser modificada"
        )
    log_info("assignment_compound")


def p_operator_assign(p):
    """operator_assign : PLUS_ASSIGN
    | MINUS_ASSIGN
    | MULT_ASSIGN
    | DIV_ASSIGN
    | MOD_ASSIGN
    | AND_ASSIGN
    | OR_ASSIGN
    | XOR_ASSIGN
    | LSHIFT_ASSIGN
    | RSHIFT_ASSIGN"""
    log_info("operator_assign")


def p_simple_assignment(p):
    """simple_assignment : IDENTIFIER ASSIGN expression"""
    log_info("simple_assignment")
    context_stack[-1]["variables"][p[1]] = p[3]
    p[0] = p[3]


def p_type(p):
    """type : primitive_type
    | slice_type
    | array_type
    | map_type"""
    log_info("type")
    p[0] = p[1]


def p_slice_type(p):
    "slice_type : LBRACKET RBRACKET primitive_type"
    log_info("slice_type")
    p[0] = ("slice", p[3])


def p_expression_slice(p):
    """expression : slice_type LBRACE expression_list RBRACE
    | slice_type LBRACE RBRACE"""
    log_info("expression_slice")


def p_expression_list(p):
    """expression_list : expression
    | expression_list COMMA expression"""
    log_info("expression_list")
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    log_info("expression_group")
    p[0] = p[2]


def p_short_assignment(p):
    """short_assignment : IDENTIFIER SHORT_ASSIGN expression"""
    log_info("short_assignment")
    nombre = p[1]
    tipo = p[3]
    actual = context_stack[-1]["variables"]
    actual[nombre] = tipo
    p[0] = (nombre, tipo)


def p_local_statement(p):
    """local_statement : local_var_dec
    | local_const_dec
    | short_assignment
    | simple_assignment
    | assignment_compound
    | expression
    | for_statement
    | if_statement
    | switch_statement
    | break_statement
    | continue_statement"""
    p[0] = p[1]


def p_break_statement(p):
    """break_statement : BREAK"""
    if not any(ctx == "loop" or ctx == "switch" for ctx in loop_context_stack):
        semantic_errors.append(
            "Error semántico: 'break' solo puede usarse dentro de un loop"
        )
    log_info("break_statement")


def p_continue_statement(p):
    """continue_statement : CONTINUE"""
    if not any(ctx == "loop" for ctx in loop_context_stack):
        semantic_errors.append(
            "Error semántico: 'continue' solo puede usarse dentro de un loop"
        )
    log_info("continue_statement")


def p_local_statement_list(p):
    """local_statement_list : local_statement
    | local_statement_list local_statement"""
    log_info("local_statement_list")


def p_for_statement(p):
    """for_statement : for_classic
    | for_condition
    | for_infinite"""
    log_info("for_statement")


def p_push_loop(p):
    """push_loop :"""
    loop_context_stack.append("loop")


def p_pop_loop(p):
    """pop_loop :"""
    if loop_context_stack:
        loop_context_stack.pop()


def p_for_classic(p):
    """for_classic : FOR for_init SEMICOLON for_cond SEMICOLON for_post push_loop block pop_loop"""
    log_info("for_classic")


def p_for_condition(p):
    """for_condition : FOR expression push_loop block pop_loop"""
    log_info("for_condition")


def p_for_infinite(p):
    """for_infinite : FOR push_loop block pop_loop"""
    log_info("for_infinite")


def p_for_init(p):
    """for_init : simple_assignment
    | short_assignment
    | local_var_dec
    | empty"""
    log_info("for_init")


def p_for_cond(p):
    """for_cond : expression
    | empty"""
    log_info("for_cond")


def p_for_post(p):
    """for_post : simple_assignment
    | assignment_compound
    | expression
    | empty"""
    log_info("for_post")


def p_return_list(p):
    """return_list : expression
    | return_list COMMA expression"""
    log_info("return_list")
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_function_declaration(p):
    "function_declaration : FUNC IDENTIFIER LPAREN parameter_list RPAREN return_type block"
    func_name = p[2]
    # Semantic check: Function redeclaration
    if func_name in context_stack[0].get("functions", {}):
        semantic_errors.append(
            f"Error semántico: La función '{func_name}' ya fue declarada previamente."
        )
    else:
        context_stack[0]["functions"] = context_stack[0].get("functions", {})
        context_stack[0]["functions"][func_name] = True
    log_info("function_declaration")


def p_parameter_list(p):
    """parameter_list : parameter_list COMMA parameter
    | parameter
    | empty"""
    log_info("parameter_list")


def p_parameter(p):
    """parameter : IDENTIFIER type
    | IDENTIFIER ELLIPSIS primitive_type"""
    log_info("parameter")
    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 4:
        p[0] = (p[1], p[3])


def p_return_type(p):
    """return_type : type
    | LPAREN type_list RPAREN
    | empty"""
    log_info("return_type")


def p_return_statement(p):
    """return_statement : RETURN
    | RETURN return_list"""
    log_info("return_statement")
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_type_list(p):
    """type_list : type_list COMMA type
    | type"""
    log_info("type_list")


def p_assignment(p):
    """assignment : IDENTIFIER ASSIGN expression
    | IDENTIFIER SHORT_ASSIGN expression"""
    nombre = p[1]
    if nombre in context_stack[0]["consts"]:
        semantic_errors.append(
            f"Error semántico: La constante '{nombre}' no puede ser modificada"
        )
    tipo = p[3]
    actual = context_stack[-1]["variables"]
    actual[nombre] = tipo
    p[0] = (nombre, tipo)


def p_variable_declaration(p):
    """variable_declaration : VAR IDENTIFIER type ASSIGN expression
    | CONST IDENTIFIER type ASSIGN expression
    | VAR IDENTIFIER ASSIGN expression
    | CONST IDENTIFIER ASSIGN expression"""
    nombre = p[2]
    tipo = p[-1]
    # Semantic check: Variable redeclaration in same scope
    if p[1] == "var" and nombre in context_stack[-1]["variables"]:
        semantic_errors.append(
            f"Error semántico: La variable '{nombre}' ya fue declarada en este ámbito."
        )
    elif p[1] == "const" and nombre in context_stack[-1].get("consts", {}):
        semantic_errors.append(
            f"Error semántico: La constante '{nombre}' ya fue declarada en este ámbito."
        )
    context_stack[-1]["variables"][nombre] = tipo


def p_primitive_type(p):
    """primitive_type : INT_TYPE
    | FLOAT64_TYPE
    | STRING_TYPE
    | BOOL_TYPE"""
    log_info("primitive_type")
    type = p.slice[1].type
    if type == "INT_TYPE":
        p[0] = "int"
    elif type == "FLOAT64_TYPE":
        p[0] = "float64"
    elif type == "STRING_TYPE":
        p[0] = "str"
    elif type == "BOOL_TYPE":
        p[0] = "bool"


def p_array_type(p):
    """array_type : LBRACKET INT RBRACKET primitive_type"""
    log_info("array_type")
    current = context_stack[-1]["array"] = {}
    current["element_type"] = p[4]
    current["size"] = p[2]
    p[0] = "array"  # element_type, size


def p_array_literal(p):
    """expression : array_type LBRACE RBRACE
    | array_type LBRACE expression_list RBRACE
    | LBRACKET ELLIPSIS RBRACKET primitive_type LBRACE RBRACE
    | LBRACKET ELLIPSIS RBRACKET primitive_type LBRACE expression_list RBRACE"""
    log_info("array_literal")
    current = context_stack[-1]

    if isinstance(p[1], str) and p[1] == "array":
        array_info = current.get("array", {})
        declared_size = array_info.get("size", 0)
        element_type = array_info.get("element_type", None)

        if len(p) == 5:  # array_type LBRACE expression_list RBRACE
            # Array with elements
            expression_types = p[3]
            # Check type consistency
            for t in expression_types:
                if t != element_type:
                    semantic_errors.append(
                        f"Error Semantico: Tipo de elemento en array '{t}' no coincide con tipo esperado '{element_type}'."
                    )
            # Check size consistency
            if len(expression_types) != declared_size:
                semantic_errors.append(
                    f"Error Semantico: Tamaño de array declarado '{declared_size}' no coincide con número de elementos proporcionados '{len(expression_types)}'."
                )
    else:
        # Ellipsis array [...]{} with size inferred from elements
        array_info = current.setdefault("array", {})
        element_type = p[4]
        array_info["element_type"] = element_type
        if len(p) == 7:  # LBRACKET ELLIPSIS RBRACKET primitive_type LBRACE RBRACE
            array_info["size"] = 0
            types = p[6]
            for t in types:
                if t != element_type:
                    semantic_errors.append(
                        f"Error Semantico: Tipo de elemento en array '{t}' no coincide con tipo esperado '{element_type}'."
                    )
        else:  # LBRACKET ELLIPSIS RBRACKET primitive_type LBRACE expression_list RBRACE
            array_info["size"] = len(p[6])
    p[0] = "array"


def p_expression_binary(p):
    """expression : binary_expression
    | relational_expression
    | logical_expression
    | bitwise_expression"""
    log_info("expression")


def p_expression_unary(p):
    """expression : LNOT expression"""
    log_info("expression_unary")


def p_expression_int(p):
    "expression : INT"
    log_info("expression")
    p[0] = "int"


def p_expression_float(p):
    "expression : FLOAT64"
    log_info("expression")
    p[0] = "float64"


def p_expression_boolean(p):
    """expression : TRUE
    | FALSE"""
    log_info("expression")
    p[0] = "bool"


def p_expression_identifier(p):
    "expression : IDENTIFIER"
    log_info("expression")
    nombre = p[1]
    found = False
    for context in context_stack[::-1]:
        if nombre in context["variables"]:
            p[0] = context["variables"][nombre]
            found = True
            break
    if not found:
        semantic_errors.append(
            f"Error Semantico: Variable {nombre} no se encuentra definida."
        )


def p_expression_string(p):
    "expression : STRING"
    log_info("expression")
    p[0] = "str"


def p_expression_postfix(p):
    """expression : IDENTIFIER PLUSPLUS
    | IDENTIFIER MINUSMINUS"""
    var_name = p[1]
    if var_name in context_stack[0]["consts"]:
        semantic_errors.append(
            f"Error semántico: La constante '{var_name}' ya fue declarada previamente."
        )
    log_info("expression_postfix")


# END Contribution: José Toapanta

# START Contribution: Juan Francisco Fernandez
# If/else conditional statements with optional else clause for branching logic
# Struct type declarations (type Name struct { fields }) for composite data types
# Struct field definitions with type annotations for data modeling
# Struct literals with field:value initialization syntax
# Method declarations with receiver syntax: func (receiver Type) method() { }
# Map type declarations map[KeyType]ValueType for key-value data structures
# Map literals with key:value pair initialization


def p_if_statement(p):
    """if_statement : IF expression block
    | IF expression block ELSE block
    | IF expression block ELSE if_statement
    | IF if_assignment SEMICOLON expression block
    | IF if_assignment SEMICOLON expression block ELSE block
    | IF if_assignment SEMICOLON expression block ELSE if_statement"""
    log_info("if_statement")


def p_if_assignment(p):
    """if_assignment : simple_assignment
    | short_assignment
    | local_var_dec"""
    log_info("if_assignment")


def p_map_type(p):
    """map_type : MAP LBRACKET primitive_type RBRACKET primitive_type"""
    log_info("map_type")


def p_expression_map(p):
    """expression : map_type LBRACE expression_map_list RBRACE
    | map_type LBRACE RBRACE"""
    log_info("expression_map")


def p_expression_map_list(p):
    """expression_map_list : key_value
    | expression_map_list COMMA key_value"""
    log_info("expression_map_list")


def p_key_value(p):
    """key_value : expression COLON expression"""
    log_info("key_value")


def p_field_list(p):
    """field_list : field_declaration
    | field_list field_declaration"""
    log_info("field_list")


def p_field_declaration(p):
    """field_declaration : IDENTIFIER type
    | IDENTIFIER"""
    log_info("field_declaration")


def p_method_declaration(p):
    "method_declaration : FUNC LPAREN receiver RPAREN IDENTIFIER LPAREN parameter_list RPAREN return_type block"
    log_info("method_declaration")


def p_receiver(p):
    """receiver : IDENTIFIER IDENTIFIER
    | IDENTIFIER TIMES IDENTIFIER
    | IDENTIFIER TIMES type"""
    log_info("receiver")


def p_type_declaration(p):
    """type_declaration : TYPE IDENTIFIER type_alias"""
    log_info("type_declaration")


def p_type_alias(p):
    """type_alias : struct_type
    | type
    | IDENTIFIER"""
    log_info("type_alias")


def p_struct_type(p):
    """struct_type : STRUCT LBRACE RBRACE
    | STRUCT LBRACE field_list RBRACE"""
    log_info("struct_type")


def p_keyed_element_list(p):
    """keyed_element_list : keyed_element
    | keyed_element_list COMMA keyed_element"""
    log_info("keyed_element_list")


def p_keyed_element(p):
    """keyed_element : IDENTIFIER COLON expression
    | INT COLON expression
    | expression"""
    log_info("keyed_element")


def p_expression_composite_literal(p):
    """expression : type_name LBRACE keyed_element_list RBRACE
    | type_name LBRACE RBRACE"""
    log_info("expression_composite_literal")


def p_type_name(p):
    """type_name : IDENTIFIER
    | slice_type
    | array_type
    | map_type"""
    log_info("type_name")


# END Contribution: Juan Francisco Fernandez

# START Contribution: Nicolas Fiallo
# Switch statement declaration
# Recursive case clauses, with terminal clause
# Case clause structure: CASE reserved word, expression
# Default reserved statement
# Array structure defined, added to expression_type
# Print/Input statements: fmt.Println/Printf/Scanf with variadic argument support


def find_variable(name):
    for context in context_stack[::-1]:
        if name in context["variables"]:
            return context["variables"][name], context
    semantic_errors.append(
        f"Error Semantico: Variable {name} no se encuentra definida."
    )
    return None, None


def p_binary_expression(p):
    """binary_expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression MODULE expression"""


def p_grouped_expression(p):
    """grouped_expression : LPAREN expression RPAREN"""


def p_relational_expression(p):
    """relational_expression : expression EQ expression
    | expression NEQ expression
    | expression LT expression
    | expression LE expression
    | expression GT expression
    | expression GE expression"""


def p_logical_expression(p):
    """logical_expression : expression LAND expression
    | expression LOR expression"""


def p_bitwise_expression(p):
    """bitwise_expression : expression AND expression
    | expression OR expression
    | expression XOR expression
    | expression AND_NOT expression
    | expression LSHIFT expression
    | expression RSHIFT expression"""


def p_postfix_expression(p):
    """postfix_expression : IDENTIFIER PLUSPLUS
    | IDENTIFIER MINUSMINUS"""


# def p_selector_expression(p):
#     """selector_expression : expression DOT IDENTIFIER"""


def p_func_call_expression(p):
    """func_call_expression : IDENTIFIER LPAREN argument_list RPAREN"""


def p_call_expression(p):
    """call_expression : print_expression
    | input_expression
    | func_call_expression"""


# def p_slice_expression(p):
#     """slice_expression : LBRACKET RBRACKET primitive_type LBRACE expression_list RBRACE
#     | LBRACKET RBRACKET primitive_type LBRACE RBRACE"""


def p_enter_block(p):
    """enter_block :"""
    context_stack.append(
        {
            "variables": {},
        }
    )


def p_exit_block(p):
    """exit_block :"""
    context_stack.pop()


def p_case_expression_list(p):
    """case_expression_list : expression
    | case_expression_list COMMA expression"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_case_clauses(p):
    """case_clauses : case_clause
    | case_clauses case_clause"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_case_clause(p):
    """case_clause : CASE case_expression_list COLON enter_block case_body exit_block
    | DEFAULT COLON enter_block case_body exit_block"""
    if p.slice[1].type == "CASE":
        parent_expected_type = context_stack[-1].get("switch_expression", None)
        expression_types = p[2]

        for expression in expression_types:
            if expression != parent_expected_type:
                semantic_errors.append(
                    f"Error Semantico: Tipo de expresion en case '{expression}' no coincide con tipo esperado '{parent_expected_type}'."
                )

        p[0] = ("case", p[2], p[5])  # case, case expressions, case body
    else:
        p[0] = ("default", p[4])  # default, case body
    context_stack[-1]["case_clause"] = p[0]


def p_case_body(p):
    """case_body : statement_list
    | empty"""
    p[0] = p[1]
    current = context_stack[-1]
    current["case_body"] = p[0]


def p_switch_primary(p):
    """switch_primary : IDENTIFIER
    | INT
    | FLOAT64
    | STRING
    | TRUE
    | FALSE"""
    if p.slice[1].type == "IDENTIFIER":
        p[0] = find_variable(p[1])[0]
    elif p.slice[1].type == "INT":
        p[0] = "int"
    elif p.slice[1].type == "FLOAT64":
        p[0] = "float64"
    elif p.slice[1].type == "STRING":
        p[0] = "str"
    elif p.slice[1].type in ["TRUE", "FALSE"]:
        p[0] = "bool"


def p_switch_init(p):
    """switch_init : assignment SEMICOLON switch_expression"""
    p[0] = (p[1], p[3])


def p_switch_expression(p):
    """switch_expression : switch_primary
    | empty"""
    p[0] = p[1]


def p_switch_header(p):
    """switch_header : switch_expression
    | switch_init"""
    if isinstance(p[1], tuple) and len(p[1]) == 2:
        assignment, expression = p[1]
        context_stack[-1]["switch_expression"] = expression
        context_stack[-1]["switch_assignment"] = assignment
        p[0] = (assignment, expression)
    else:
        context_stack[-1]["switch_expression"] = p[1]
        p[0] = p[1]


def p_switch_statement(p):
    """switch_statement : SWITCH enter_block switch_header LBRACE case_clauses RBRACE exit_block"""
    header = p[3]
    assignment, expression = None, None
    if isinstance(header, tuple):
        assignment, expression = header
    else:
        expression = header

    if expression is None:
        switch_type = "bool"
    else:
        switch_type = expression

    current = context_stack[-1]
    current["switch_expression"] = switch_type
    if assignment and not expression:
        semantic_errors.append(
            "Error Semantico: Switch con inicializacion debe tener expresion."
        )
    clauses = p[5]
    default = False
    for clause in clauses:
        clause_type = clause[0]
        if clause_type == "default":
            if default:
                semantic_errors.append(
                    "Error Semantico: Multiple default clauses en el switch statement."
                )
            default = True
    p[0] = clauses


def p_print_statement(p):
    """print_expression : IDENTIFIER DOT IDENTIFIER LPAREN argument_list RPAREN"""
    if p[1] != "fmt" or p[3] not in ["Println", "Printf", "Print"]:
        semantic_errors.append(
            f"Error Semantico: Llamada a funcion de impresion invalida '{p[1]}.{p[3]}'."
        )


def p_input_statement(p):
    """input_expression : IDENTIFIER DOT IDENTIFIER LPAREN AND IDENTIFIER COMMA argument_list RPAREN"""


def p_argument_list(p):
    """argument_list : expression_list
    | empty"""


# END Contribution: Nicolas Fiallo

# START Contribution: Juan Fernandez
#
# --- Semantic Rule 1: Function Redeclaration Detection ---
# Detects when a function with the same name is declared multiple times in the global scope.
# Implementation: Modified p_function_declaration (line ~360) to track function names in
# context_stack[0]["functions"] and report error if function name already exists.
# Error message: "Error semántico: La función '{name}' ya fue declarada previamente."
#
# --- Semantic Rule 2: Variable Redeclaration in Same Scope Detection ---
# Detects when a variable is declared multiple times within the same scope (not shadowing).
# Implementation locations:
#   - p_global_var_dec (line ~114): Global variable redeclaration check
#   - p_local_var_dec (line ~152): Local variable redeclaration check
#   - p_variable_declaration (line ~420): Statement-level variable redeclaration check
# Error message: "Error semántico: La variable '{name}' ya fue declarada en este ámbito."
#
# Both rules follow the SDT (Syntax-Directed Translation) pattern used throughout this parser,
# where semantic checks are embedded directly in grammar rule actions.
# Errors are collected in semantic_errors[] and written to logs/semantic-{user}-{date}-{time}.txt
#
# --- context_stack["functions"] ---
# Added "functions": {} to context_stack (line ~24) to track declared function names
# and prevent redeclaration at the global scope level.
#
# --- get_semantic_summary() ---
# Returns a dictionary summarizing all 8 semantic rules implemented in the parser.
# Useful for documentation and reporting purposes.
#
# --- run_semantic() (line ~1106) ---
# Dedicated semantic analysis function that focuses only on semantic errors.
# Features:
#   - Clean console output with numbered error list
#   - Semantic rules summary display
#   - Generates reports to logs/semantic-{user}-{date}-{time}.txt
#   - Called via: python run_semantic.py tests/<file.go> <username>
#
# =============================================================================


def get_semantic_summary():
    """Returns a summary of all semantic rules implemented in this parser."""
    return {
        "total_rules": 8,
        "rules": [
            "Constant immutability check",
            "Constant duplicate declaration",
            "Variable scope checking (undefined variables)",
            "Break/continue loop context validation",
            "Switch case type consistency",
            "Multiple default clause detection",
            "Function redeclaration detection",
            "Variable redeclaration in same scope",
        ],
    }


# END Contribution: Juan Fernandez (Semantic Rules)


def p_error(p):
    if p:
        msg = f"Syntax error at '{p.value}' (line {p.lineno}, column {p.lexpos})"
    else:
        msg = "Syntax error at EOF"
    print(msg)
    syntax_errors.append(msg)  # ← CAMBIO AQUÍ


parser = yacc.yacc()
parse_log = []


def run_parser(file_path, github_user):
    global syntax_errors, semantic_errors, suppress_errors, success_log, context_stack
    syntax_errors = []
    semantic_errors = []
    success_log = []
    suppress_errors = True
    context_stack = [{"consts": {}, "variables": {}, "functions": {}}]

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    user_id = github_user.lower().replace(" ", "")
    now = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_file_path = f"./logs/semantic-{user_id}-{now}.txt"
    os.makedirs("./logs", exist_ok=True)

    with open(log_file_path, "w", encoding="utf-8") as log_file:
        # ============ HEADER ============
        log_file.write("=" * 70 + "\n")
        log_file.write("Go Language Parser - Syntax & Semantic Analysis Report\n")
        log_file.write("=" * 70 + "\n")
        log_file.write(f"File: {file_path}\n")
        log_file.write(f"User: {github_user}\n")
        log_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 70 + "\n\n")

        # ============ SOURCE CODE ============
        log_file.write("SOURCE CODE:\n")
        log_file.write("-" * 70 + "\n")
        for i, line in enumerate(source_code.split("\n"), 1):
            log_file.write(f"{i:4d} | {line}\n")
        log_file.write("-" * 70 + "\n\n")

        try:
            # ============ PARSING ============
            result = parser.parse(source_code, lexer=lexer, debug=False)

            # ============ PRODUCCIONES RECONOCIDAS ============
            log_file.write("PRODUCTIONS RECOGNIZED:\n")
            log_file.write("-" * 70 + "\n")
            if success_log:
                for entry in success_log:
                    log_file.write(f"{entry}\n")
            else:
                log_file.write("No productions logged\n")
            log_file.write("\n")

            # ============ ERRORES SINTÁCTICOS ============
            if syntax_errors:
                log_file.write("SYNTAX ERRORS:\n")
                log_file.write("-" * 70 + "\n")
                for err in syntax_errors:
                    log_file.write(f"✗ {err}\n")
                log_file.write("\n")
            else:
                log_file.write("✓ No syntax errors detected\n\n")

            # ============ ERRORES SEMÁNTICOS ============
            if semantic_errors:
                log_file.write("SEMANTIC ERRORS:\n")
                log_file.write("-" * 70 + "\n")
                for err in semantic_errors:
                    log_file.write(f"✗ {err}\n")
                log_file.write("\n")
            else:
                log_file.write("✓ No semantic errors detected\n\n")

            # ============ VALIDATED GRAMMAR RULES ============
            log_file.write("VALIDATED GRAMMAR RULES:\n")
            log_file.write("-" * 70 + "\n")
            features_found = []
            if "package " in source_code:
                features_found.append("✓ Package declaration")
            if "import " in source_code:
                features_found.append("✓ Import statements")
            if "func " in source_code:
                features_found.append("✓ Function declarations")
            if "var " in source_code:
                features_found.append("✓ Variable declarations")
            if "const " in source_code:
                features_found.append("✓ Constant declarations")
            if ":=" in source_code:
                features_found.append("✓ Short variable declarations")
            if "if " in source_code:
                features_found.append("✓ If statements")
            if "else" in source_code:
                features_found.append("✓ Else clauses")
            if "for " in source_code:
                features_found.append("✓ For loops")
            if "break" in source_code:
                features_found.append("✓ Break statements")
            if "continue" in source_code:
                features_found.append("✓ Continue statements")
            if "switch " in source_code:
                features_found.append("✓ Switch statements")
            if "type " in source_code and "struct" in source_code:
                features_found.append("✓ Struct type declarations")
            if "[]" in source_code:
                features_found.append("✓ Slice types")
            if "[" in source_code and "]" in source_code:
                features_found.append("✓ Array types")
            if "++" in source_code or "--" in source_code:
                features_found.append("✓ Post-increment/decrement")
            if any(op in source_code for op in ["+", "-", "*", "/", "%"]):
                features_found.append("✓ Arithmetic expressions")
            if any(op in source_code for op in ["==", "!=", "<", ">", "<=", ">="]):
                features_found.append("✓ Relational operators")
            if any(op in source_code for op in ["&&", "||", "!"]):
                features_found.append("✓ Logical operators")

            for feature in features_found:
                log_file.write(f"{feature}\n")
            log_file.write("\n")
            log_file.write("=" * 70 + "\n")

            # ============ CONSOLE OUTPUT ============
            print(f"\n{'=' * 70}")

            total_errors = len(syntax_errors) + len(semantic_errors)

            if total_errors > 0:
                print("⚠️  PARSING COMPLETED WITH ERRORS")
                print(f"{'=' * 70}")

                # Errores sintácticos
                if syntax_errors:
                    print(f"\n🔴 SYNTAX ERRORS: {len(syntax_errors)}")
                    for err in syntax_errors[:3]:
                        print(f"  ✗ {err}")
                    if len(syntax_errors) > 3:
                        print(f"  ... and {len(syntax_errors) - 3} more")
                else:
                    print("\n✅ No syntax errors")

                # Errores semánticos
                if semantic_errors:
                    print(f"\n🟠 SEMANTIC ERRORS: {len(semantic_errors)}")
                    for err in semantic_errors[:3]:
                        print(f"  ✗ {err}")
                    if len(semantic_errors) > 3:
                        print(f"  ... and {len(semantic_errors) - 3} more")
                else:
                    print("\n✅ No semantic errors")
            else:
                print("✅ PARSING SUCCESSFUL!")
                print(f"{'=' * 70}")
                print("✓ No syntax errors")
                print("✓ No semantic errors")

            print(f"\nProductions recognized: {len(success_log)}")
            print(f"Features detected: {len(features_found)}")
            print(f"\n📄 Log file: {log_file_path}")
            print(f"{'=' * 70}\n")

            suppress_errors = False
            return len(syntax_errors) == 0 and len(semantic_errors) == 0

        except Exception as e:
            log_file.write("✗ PARSING FAILED\n")
            log_file.write(f"✗ Error: {str(e)}\n\n")
            log_file.write("=" * 70 + "\n")

            print(f"\n{'=' * 70}")
            print("❌ PARSING FAILED!")
            print(f"{'=' * 70}")
            print(f"Error: {str(e)}")
            print(f"\n📄 Log file: {log_file_path}")
            print(f"{'=' * 70}\n")

            suppress_errors = False
            return False


# START Contribution: Juan Fernandez
#
# This function provides a focused semantic analysis mode that:
#   - Runs the parser silently (suppresses production logs on console)
#   - Displays only semantic errors in a clean, numbered format
#   - Shows a summary of all 8 semantic rules being checked
#   - Generates a detailed report to logs/semantic-{user}-{date}-{time}.txt
#
# Usage: python run_semantic.py tests/<file.go> <username>
#
# Output includes:
#   - Source code with line numbers
#   - Enumerated list of all semantic errors
#   - List of semantic rules applied
#   - Total error count and rules summary
# =============================================================================


def run_semantic(file_path, github_user):
    """
    Run semantic analysis focused only on semantic errors.
    Outputs to logs/semantic-{user}-{date}-{time}.txt
    """
    global syntax_errors, semantic_errors, suppress_errors, success_log, context_stack
    syntax_errors = []
    semantic_errors = []
    success_log = []
    suppress_errors = True
    context_stack = [{"consts": {}, "variables": {}, "functions": {}}]

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    user_id = github_user.lower().replace(" ", "")
    now = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_file_path = f"./logs/semantic-{user_id}-{now}.txt"
    os.makedirs("./logs", exist_ok=True)

    with open(log_file_path, "w", encoding="utf-8") as log_file:
        # ============ HEADER ============
        log_file.write("=" * 70 + "\n")
        log_file.write("Go Language Semantic Analyzer - Error Report\n")
        log_file.write("=" * 70 + "\n")
        log_file.write(f"File: {file_path}\n")
        log_file.write(f"User: {github_user}\n")
        log_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 70 + "\n\n")

        # ============ SOURCE CODE ============
        log_file.write("SOURCE CODE:\n")
        log_file.write("-" * 70 + "\n")
        for i, line in enumerate(source_code.split("\n"), 1):
            log_file.write(f"{i:4d} | {line}\n")
        log_file.write("-" * 70 + "\n\n")

        try:
            # ============ PARSING (silent for syntax) ============
            result = parser.parse(source_code, lexer=lexer, debug=False)

            # ============ SEMANTIC ERRORS ============
            log_file.write("SEMANTIC ANALYSIS RESULTS:\n")
            log_file.write("-" * 70 + "\n\n")

            if semantic_errors:
                log_file.write(f"Total Semantic Errors: {len(semantic_errors)}\n\n")
                for i, err in enumerate(semantic_errors, 1):
                    log_file.write(f"{i:3d}. {err}\n")
                log_file.write("\n")
            else:
                log_file.write("✓ No semantic errors detected\n\n")

            # ============ SEMANTIC RULES SUMMARY ============
            log_file.write("SEMANTIC RULES CHECKED:\n")
            log_file.write("-" * 70 + "\n")
            summary = get_semantic_summary()
            for rule in summary["rules"]:
                log_file.write(f"  • {rule}\n")
            log_file.write(f"\nTotal rules applied: {summary['total_rules']}\n")
            log_file.write("=" * 70 + "\n")

            # ============ CONSOLE OUTPUT ============
            print(f"\n{'=' * 70}")
            print("GO SEMANTIC ANALYZER")
            print(f"{'=' * 70}")
            print(f"File: {file_path}")
            print(f"User: {github_user}")
            print(f"{'=' * 70}")

            if semantic_errors:
                print(f"\n🔴 SEMANTIC ERRORS FOUND: {len(semantic_errors)}\n")
                for i, err in enumerate(semantic_errors, 1):
                    print(f"  {i}. {err}")
                print()
            else:
                print("\n✅ NO SEMANTIC ERRORS\n")
                print("All semantic checks passed successfully.")
                print()

            print(f"Semantic rules checked: {summary['total_rules']}")
            print(f"\n📄 Report: {log_file_path}")
            print(f"{'=' * 70}\n")

            suppress_errors = False
            return len(semantic_errors) == 0

        except Exception as e:
            log_file.write("✗ SEMANTIC ANALYSIS FAILED\n")
            log_file.write(f"✗ Error: {str(e)}\n\n")
            log_file.write("=" * 70 + "\n")

            print(f"\n{'=' * 70}")
            print("❌ SEMANTIC ANALYSIS FAILED!")
            print(f"{'=' * 70}")
            print(f"Error: {str(e)}")
            print(f"\n📄 Report: {log_file_path}")
            print(f"{'=' * 70}\n")

            suppress_errors = False
            return False


# END Contribution: Juan Fernandez

# START Contribution: Juan Fernandez
#
# Add run_parser_gui(source_code: str) -> str to go_analyzer/core/parser/go_parser.py
# Function performs parsing and semantic analysis on string input
# Returns comprehensive formatted output (syntax + semantic results)
# Properly resets global state before each analysis
# Formats symbol table and error lists for display
# =============================================================================


def run_parser_gui(source_code: str) -> str:
    """
    GUI-compatible parser wrapper that accepts source code as string.

    Performs both syntax and semantic analysis on Go source code.

    Args:
        source_code: Go source code as string

    Returns:
        Formatted string containing:
        - Source code with line numbers
        - Syntax errors (if any)
        - Semantic errors (if any)
        - Symbol table (variables, constants, functions)
        - Production count
    """
    global syntax_errors, semantic_errors, success_log, parse_errors
    global suppress_errors, context_stack, loop_context_stack

    # Reset all global state for clean analysis
    syntax_errors = []
    semantic_errors = []
    success_log = []
    parse_errors = []
    suppress_errors = True
    context_stack = [
        {
            "consts": {},
            "variables": {},
            "functions": {},
            "tipos": {
                "str-funciones": ["len"],
            },
        }
    ]
    loop_context_stack = []

    # Build output string
    output_lines = []

    try:
        # Header
        output_lines.append("=" * 70)
        output_lines.append("PARSING & SEMANTIC ANALYSIS RESULTS")
        output_lines.append("=" * 70)
        output_lines.append("")

        # Source code section
        output_lines.append("SOURCE CODE:")
        output_lines.append("-" * 70)
        for i, line in enumerate(source_code.split("\n"), 1):
            output_lines.append(f"{i:4d} | {line}")
        output_lines.append("-" * 70)
        output_lines.append("")

        # Perform parsing (this will populate syntax_errors and semantic_errors)
        result = parser.parse(source_code, lexer=lexer, debug=False)

        # Syntax Analysis section
        output_lines.append("SYNTAX ANALYSIS:")
        output_lines.append("-" * 70)
        if syntax_errors:
            output_lines.append(f"✗ Syntax Errors Found: {len(syntax_errors)}")
            for i, err in enumerate(syntax_errors, 1):
                output_lines.append(f"✗ Error Sintactico {i}: {err}")
        else:
            output_lines.append("✓ No syntax errors")
        output_lines.append("")

        # Semantic Analysis section
        output_lines.append("SEMANTIC ANALYSIS:")
        output_lines.append("-" * 70)
        if semantic_errors:
            output_lines.append(f"✗ Semantic Errors Found: {len(semantic_errors)}")
            for i, err in enumerate(semantic_errors, 1):
                output_lines.append(f"  {i}. {err}")
        else:
            output_lines.append("✓ No semantic errors")
        output_lines.append("")

        # Symbol Table section
        output_lines.append("SYMBOL TABLE:")
        output_lines.append("-" * 70)

        # Extract global context
        global_context = context_stack[0] if context_stack else {}

        # Display Variables
        variables = global_context.get("variables", {})
        if variables:
            output_lines.append("Global Variables:")
            for var_name, var_type in variables.items():
                output_lines.append(f"  • {var_name}: {var_type}")
        else:
            output_lines.append("Global Variables: (none)")
        output_lines.append("")

        # Display Constants
        constants = global_context.get("consts", {})
        if constants:
            output_lines.append("Global Constants:")
            for const_name in constants.keys():
                # Get type from variables table if available
                const_type = variables.get(const_name, "unknown")
                output_lines.append(f"  • {const_name}: {const_type}")
        else:
            output_lines.append("Global Constants: (none)")
        output_lines.append("")

        # Display Functions
        functions = global_context.get("functions", {})
        if functions:
            output_lines.append("Global Functions:")
            for func_name in functions.keys():
                output_lines.append(f"  • {func_name}")
        else:
            output_lines.append("Global Functions: (none)")
        output_lines.append("")

        # Summary
        output_lines.append("-" * 70)
        output_lines.append(f"Productions Recognized: {len(success_log)}")
        output_lines.append(f"Total Syntax Errors: {len(syntax_errors)}")
        output_lines.append(f"Total Semantic Errors: {len(semantic_errors)}")
        output_lines.append("=" * 70)

        # Reset suppress flag
        suppress_errors = False

        return "\n".join(output_lines)

    except Exception as e:
        # Handle unexpected errors gracefully
        error_output = "\n".join(output_lines) if output_lines else ""
        if error_output:
            error_output += "\n\n"
        error_output += "=" * 70 + "\n"
        error_output += "✗ PARSING FAILED\n"
        error_output += "=" * 70 + "\n"
        error_output += f"Error during parsing: {str(e)}\n"
        error_output += "=" * 70

        # Reset suppress flag
        suppress_errors = False

        return error_output


# END Contribution: Juan Fernandez


def main():
    while True:
        try:
            s = input("Go > ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s, lexer=lexer)


if __name__ == "__main__":
    main()
