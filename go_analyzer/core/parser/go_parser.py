from go_analyzer.core.lexer import tokens
import ply.yacc as yacc

# START Contribution: José Toapanta
# Parser rules for package declaration, imports, and global program structure
# Function declarations with multiple return types: func name() (type1, type2) { }
# Slice data structure []type{values} for dynamic arrays with type safety
# For loop control structure with three variations: condition-only, infinite, and classic (init; cond; incr)
# Arithmetic expressions with multiple operators (+, -, *, /, %) respecting precedence and associativity
# Logical conditions with connectors (&&, ||, !) combined with relational operators (==, !=, <, >, <=, >=)
# Variable assignment with all primitive types (int, float64, string, bool) supporting explicit and type inference
# Complete expression evaluation with literals, identifiers, post-increment/decrement, and parenthesized grouping
# END Contribution: José Toapanta

# START Contribution: José Toapanta
precedence = (
    ('right', 'LNOT'),
    ('right', 'UMINUS', 'UPLUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'AND'),
    ('left', 'XOR'),
    ('left', 'OR'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LAND'),
    ('left', 'LOR')
)

def p_program(p):
    "program : package_declaration multiple_import global_sequence"

def p_package_declaration(p):
    "package_declaration : PACKAGE IDENTIFIER optional_semicolon"

def p_multiple_import(p):
    """multiple_import : multiple_import simple_import
                       | empty"""

def p_simple_import(p):
    "simple_import : IMPORT STRING optional_semicolon"

def p_empty(p):
    "empty :"

def p_optional_semicolon(p):
    """optional_semicolon : SEMICOLON
                          | empty"""

def p_global_sequence(p):
    """global_sequence : global_sequence global_statement
                       | global_statement
                       | empty"""

def p_global_statement(p):
    """global_statement : statement optional_semicolon
                        | function_declaration"""

def p_block(p):
    "block : LBRACE statement_sequence RBRACE"

def p_statement(p):
    """statement : assignment
                 | assignment_compound
                 | variable_declaration
                 | expression
                 | return_statement
                 | for_statement"""

def p_for_statement(p):
    """for_statement : FOR expression block
                     | FOR block
                     | FOR for_clause block"""

def p_for_clause(p):
    """for_clause : assignment optional_semicolon expression optional_semicolon expression
                  | optional_semicolon expression optional_semicolon expression"""

def p_return_statement(p):
    """return_statement : RETURN
                        | RETURN return_list"""

def p_return_list(p):
    """return_list : return_list COMMA expression
                   | expression"""

def p_statement_sequence(p):
    """statement_sequence : statement_sequence statement optional_semicolon
                          | statement optional_semicolon
                          | empty"""

def p_function_declaration(p):
    "function_declaration : FUNC IDENTIFIER LPAREN parameter_list RPAREN return_type block"

def p_parameter_list(p):
    """parameter_list : parameter_list COMMA parameter
                      | parameter
                      | empty"""

def p_parameter(p):
    """parameter : IDENTIFIER type
                 | IDENTIFIER ELLIPSIS primitive_type"""

def p_return_type(p):
    """return_type : type
                   | LPAREN type_list RPAREN
                   | empty"""

def p_type_list(p):
    """type_list : type_list COMMA type
                 | type"""

def p_assignment(p):
    """assignment : IDENTIFIER ASSIGN expression
                  | IDENTIFIER SHORT_ASSIGN expression"""

def p_assignment_compound(p):
    """assignment_compound : IDENTIFIER PLUS_ASSIGN expression
                           | IDENTIFIER MINUS_ASSIGN expression
                           | IDENTIFIER MULT_ASSIGN expression
                           | IDENTIFIER DIV_ASSIGN expression
                           | IDENTIFIER MOD_ASSIGN expression
                           | IDENTIFIER AND_ASSIGN expression
                           | IDENTIFIER OR_ASSIGN expression
                           | IDENTIFIER XOR_ASSIGN expression
                           | IDENTIFIER LSHIFT_ASSIGN expression
                           | IDENTIFIER RSHIFT_ASSIGN expression"""

def p_variable_declaration(p):
    """variable_declaration : VAR IDENTIFIER type ASSIGN expression
                            | CONST IDENTIFIER type ASSIGN expression
                            | VAR IDENTIFIER ASSIGN expression
                            | CONST IDENTIFIER ASSIGN expression"""

def p_type(p):
    """type : primitive_type
            | slice_type"""

def p_primitive_type(p):
    """primitive_type : INT_TYPE
                      | FLOAT64_TYPE
                      | STRING_TYPE
                      | BOOL_TYPE"""

def p_slice_type(p):
    "slice_type : LBRACKET RBRACKET primitive_type"

def p_expression_binary(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression LAND expression
                  | expression LOR expression
                  | expression AND expression
                  | expression OR expression
                  | expression XOR expression
                  | expression AND_NOT expression
                  | expression LSHIFT expression
                  | expression RSHIFT expression"""

def p_expression_unary(p):
    """expression : PLUS expression %prec UPLUS
                  | MINUS expression %prec UMINUS
                  | LNOT expression %prec LNOT"""

def p_expression_slice(p):
    """expression : LBRACKET RBRACKET primitive_type LBRACE expression_list RBRACE
                  | LBRACKET RBRACKET primitive_type LBRACE RBRACE"""

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"

def p_expression_int(p):
    "expression : INT"

def p_expression_float(p):
    "expression : FLOAT64"

def p_expression_boolean(p):
    """expression : TRUE
                  | FALSE"""

def p_expression_identifier(p):
    "expression : IDENTIFIER"

def p_expression_string(p):
    "expression : STRING"

def p_expression_postfix(p):
    """expression : IDENTIFIER PLUSPLUS
                  | IDENTIFIER MINUSMINUS"""

def p_expression_list(p):
    """expression_list : expression_list COMMA expression
                       | expression"""
# END Contribution: José Toapanta

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def main():
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)

if __name__ == '__main__':
    main()