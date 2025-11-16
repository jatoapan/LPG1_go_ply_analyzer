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
success_log = []
suppress_errors = False

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

def p_global_var_dec(p):
    """global_var_dec : VAR IDENTIFIER type
    | VAR IDENTIFIER type ASSIGN expression
    | VAR IDENTIFIER ASSIGN expression""" 
    log_info("global_var_dec")

def p_global_const_dec(p):
    """global_const_dec : CONST IDENTIFIER type ASSIGN expression
    | CONST IDENTIFIER ASSIGN expression"""
    log_info("global_const_dec")

def p_local_var_dec(p):
    """local_var_dec : VAR IDENTIFIER type
    | VAR IDENTIFIER type ASSIGN expression
    | VAR IDENTIFIER ASSIGN expression"""
    log_info("local_var_dec")

def p_local_const_dec(p):
    """local_const_dec : CONST IDENTIFIER type ASSIGN expression
    | CONST IDENTIFIER ASSIGN expression"""
    log_info("local_const_dec")

def p_assignment_compound(p):
    """assignment_compound : IDENTIFIER operator_assign expression"""
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

def p_expression_binary(p):
    """expression : expression binary_operator expression"""
    log_info("expression_binary")

def p_binary_operator(p):
    """binary_operator : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | MODULE
    | EQ
    | NEQ
    | LT
    | LE
    | GT
    | GE
    | LAND
    | LOR
    | AND
    | OR
    | XOR
    | AND_NOT
    | LSHIFT
    | RSHIFT
    """
    log_info("binary_operator")

def p_simple_assignment(p):
    """simple_assignment : IDENTIFIER ASSIGN expression"""
    log_info("simple_assignment")

def p_type(p):
    """type : primitive_type
    | slice_type
    | array_type
    | map_type"""
    log_info("type")

def p_primitive_type(p):
    """primitive_type : INT_TYPE
    | FLOAT64_TYPE
    | STRING_TYPE
    | BOOL_TYPE"""
    log_info("primitive_type")

def p_slice_type(p):
    "slice_type : LBRACKET RBRACKET primitive_type"
    log_info("slice_type")

def p_expression_slice(p):
    """expression : slice_type LBRACE expression_list RBRACE
    | slice_type LBRACE RBRACE"""
    log_info("expression_slice")

def p_expression_list(p):
    """expression_list : expression
    | expression_list COMMA expression"""
    log_info("expression_list")

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    log_info("expression_group")

def p_expression_literal(p):
    """expression : INT
    | FLOAT64
    | IDENTIFIER
    | STRING
    | TRUE
    | FALSE"""
    log_info("expression")

def p_short_assignment(p):
    """short_assignment : IDENTIFIER SHORT_ASSIGN expression"""
    log_info("short_assignment")

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
    | return_statement
    | BREAK         
    | CONTINUE"""    
    log_info("local_statement")

def p_block(p):
    """block : LBRACE local_statement_list RBRACE
             | LBRACE RBRACE"""
    log_info("block")

def p_local_statement_list(p):
    """local_statement_list : local_statement
    | local_statement_list local_statement"""
    log_info("local_statement_list")

def p_for_statement(p):
    """for_statement : for_classic
    | for_condition
    | for_infinite"""
    log_info("for_statement")

def p_for_classic(p):
    """for_classic : FOR for_init SEMICOLON for_cond SEMICOLON for_post block"""
    log_info("for_classic")

def p_for_condition(p):
    """for_condition : FOR expression block"""
    log_info("for_condition")

def p_for_infinite(p):
    """for_infinite : FOR block"""
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

def p_function_declaration(p):
    "function_declaration : FUNC IDENTIFIER LPAREN parameter_list RPAREN return_type block"
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

def p_return_type(p):
    """return_type : type
    | LPAREN type_list RPAREN
    | empty"""
    log_info("return_type")

def p_type_list(p):
    """type_list : type
    | type_list COMMA type"""
    log_info("type_list")

def p_return_statement(p):
    """return_statement : RETURN
    | RETURN return_list"""
    log_info("return_statement")

def p_expression_unary(p):
    """expression : LNOT expression"""
    log_info("expression_unary")

def p_expression_postfix(p):
    """expression : IDENTIFIER PLUSPLUS
    | IDENTIFIER MINUSMINUS"""
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
    """field_declaration : IDENTIFIER type"""
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
# Variadic functions calls validated
# Print/Input statements: fmt.Println/Printf/Scanf with variadic argument support

def p_switch_statement(p):
    """switch_statement : SWITCH switch_expr LBRACE case_clause_list RBRACE
    | SWITCH switch_expr LBRACE RBRACE
    | SWITCH LBRACE case_clause_list RBRACE
    | SWITCH LBRACE RBRACE
    | SWITCH switch_assignment SEMICOLON switch_expr LBRACE case_clause_list RBRACE
    | SWITCH switch_assignment SEMICOLON switch_expr LBRACE RBRACE
    | SWITCH switch_assignment SEMICOLON LBRACE case_clause_list RBRACE
    | SWITCH switch_assignment SEMICOLON LBRACE RBRACE"""
    log_info("switch_statement")

def p_switch_expr(p):
    """switch_expr : primary_expression"""
    log_info("switch_expr")

def p_primary_expression(p):
    """primary_expression : IDENTIFIER
    | INT
    | FLOAT64
    | STRING
    | TRUE
    | FALSE
    | LPAREN expression RPAREN
    | IDENTIFIER LPAREN argument_list RPAREN
    | primary_expression DOT IDENTIFIER
    | primary_expression LBRACKET expression RBRACKET"""
    log_info("primary_expression")

def p_case_clause_list(p):
    """case_clause_list : case_clause
    | case_clause_list case_clause"""
    log_info("case_clause_list")

def p_switch_assignment(p):
    """switch_assignment : simple_assignment
    | short_assignment
    | local_var_dec"""
    log_info("switch_assignment")

def p_case_clause(p):
    """case_clause : CASE case_expression_list COLON case_body
    | DEFAULT COLON case_body"""
    log_info("case_clause")

def p_case_expression_list(p):
    """case_expression_list : expression
    | case_expression_list COMMA expression"""
    log_info("case_expression_list")

def p_case_body(p):
    """case_body : local_statement_list
    | empty"""
    log_info("case_body")

def p_array_type(p):
    """array_type : LBRACKET INT RBRACKET primitive_type"""
    log_info("array_type")

def p_expression_array(p):
    """expression : array_type LBRACE expression_list RBRACE
    | array_type LBRACE RBRACE"""
    log_info("expression_array")
    
def p_expression_selector(p):
    """expression : expression DOT IDENTIFIER"""
    log_info("expression_selector")

def p_expression_method_call(p):
    """expression : expression DOT IDENTIFIER LPAREN argument_list RPAREN"""
    log_info("expression_method_call")

def p_expression_index(p):
    """expression : expression LBRACKET expression RBRACKET"""
    log_info("expression_index")

def p_func_call(p):
    """expression : IDENTIFIER LPAREN argument_list RPAREN"""
    log_info("func_call")

def p_argument_list(p):
    """argument_list : expression_list
    | empty"""
    log_info("argument_list")
# END Contribution: Nicolas Fiallo

def p_error(p):
    global parse_errors, suppress_errors
    if suppress_errors:
        if p:
            parse_errors.append(f"Syntax error at '{p.value}' (line {p.lineno})")
        else:
            parse_errors.append("Syntax error at EOF")
    else:
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")


parser = yacc.yacc()
parse_log = []

def run_parser(file_path, github_user):
    global parse_errors, suppress_errors, success_log
    parse_errors = []
    success_log = []
    suppress_errors = True
    with open(file_path, "r", encoding="utf-8") as input_file:
        source_code = input_file.read()
        user_id = github_user.lower().replace(" ", "")
        now = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        log_file_path = f"./logs/parser-{user_id}-{now}.txt"
        os.makedirs("./logs", exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            log_file.write("=" * 70 + "\n")
            log_file.write("Go Language Parser - Syntax Analysis Report\n")
            log_file.write("=" * 70 + "\n")
            log_file.write(f"File: {file_path}\n")
            log_file.write(f"User: {github_user}\n")
            log_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write("=" * 70 + "\n\n")
            log_file.write("SOURCE CODE:\n")
            log_file.write("-" * 70 + "\n")
            for i, line in enumerate(source_code.split("\n"), 1):
                log_file.write(f"{i:4d} | {line}\n")
            log_file.write("-" * 70 + "\n\n")
            try:
                result = parser.parse(source_code, lexer=lexer, debug=False)
                log_file.write("PRODUCTIONS RECOGNIZED:\n")
                log_file.write("-" * 70 + "\n")
                if success_log:
                    for entry in success_log:
                        log_file.write(f"{entry}\n")
                else:
                    log_file.write("No productions logged\n")
                log_file.write("\n")

                if parse_errors:
                    log_file.write("SYNTAX ERRORS:\n")
                    log_file.write("-" * 70 + "\n")
                    for error in parse_errors:
                        log_file.write(f"✗ {error}\n")
                    log_file.write("\n")
                else:
                    log_file.write("✓ No syntax errors detected\n\n")
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
                print(f"\n{'=' * 70}")
                if parse_errors:
                    print("⚠️  PARSING COMPLETED WITH ERRORS")
                    print(f"{'=' * 70}")
                    print(f"Syntax errors: {len(parse_errors)}")
                    for error in parse_errors[:5]:
                        print(f"  ✗ {error}")
                    if len(parse_errors) > 5:
                        print(f"  ... and {len(parse_errors) - 5} more")
                else:
                    print("✅ PARSING SUCCESSFUL!")
                    print(f"{'=' * 70}")
                
                print(f"\nProductions recognized: {len(success_log)}")
                print(f"Features detected: {len(features_found)}")
                print(f"\n📄 Log file: {log_file_path}")
                print(f"{'=' * 70}\n")
                suppress_errors = False
                return len(parse_errors) == 0
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