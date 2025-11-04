import ply.lex as lex
from datetime import datetime

# START Contribution: José Toapanta
# Tokens and regex rules for identifiers, arithmetic and relational operators, assignment, and primitive types
# Reserved keywords for declarations, booleans, and basic types (int, float64, string, bool)
# Functions for recognizing IDENTIFIER and INT literals
# END Contribution: José Toapanta

# START Contribution: Juan Fernández
# Logical operators (AND, OR, NOT), compound assignment operators
# Reserved keywords for control flow (switch, case, fallthrough, default) and type declarations
# Functions for recognizing FLOAT64 and STRING literals
# END Contribution: Juan Fernández

# START Contribution: Nicolás Fiallo
# Bitwise operators, shift operators, delimiters, and punctuation tokens
# Reserved keywords for conditional and loop constructs (if, else, for, break, continue, range, map)
# Functions for handling single-line and multi-line comments
# END Contribution: Nicolás Fiallo

tokens = (
    # START Contribution: José Toapanta
    "IDENTIFIER", "PLUS", "MINUS", "TIMES", "DIVIDE", 
    "MODULE", "PLUSPLUS", "MINUSMINUS", "EQ", "NEQ",
    "LT", "LE", "GT", "GE", "INT",
    # END Contribution: José Toapanta
    #
    # START Contribution: Juan Fernández
    "LAND", "LOR", "LNOT", "ASSIGN", "SHORT_ASSIGN",
    "PLUS_ASSIGN", "MINUS_ASSIGN", "MULT_ASSIGN", "DIV_ASSIGN",
    "MOD_ASSIGN", "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN",
    "LSHIFT_ASSIGN", "RSHIFT_ASSIGN", "FLOAT64", "STRING",
    # END Contribution: Juan Fernández

    #START Contribution: Nicolás Fiallo
    "AND", "OR", "XOR", "AND_NOT", "LSHIFT", "RSHIFT",
    "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACKET", "RBRACKET",
    "COMMA", "DOT", "SEMICOLON", "COLON"
    #END Contribution: Nicolás Fiallo

)

reserved = {
    # START Contribution: José Toapanta
    "package": "PACKAGE",
    "import": "IMPORT",
    "var": "VAR",
    "const": "CONST",
    "func": "FUNC",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
    "int": "INT_TYPE",
    "float64": "FLOAT64_TYPE",
    "string": "STRING_TYPE",
    "bool": "BOOL_TYPE",
    # END Contribution: José Toapanta
    #
    # START Contribution: Juan Fernández
    "switch": "SWITCH",
    "case": "CASE",
    "fallthrough": "FALLTHROUGH",
    "default": "DEFAULT",
    "type": "TYPE",
    "struct": "STRUCT",
    "interface": "INTERFACE",
    # END Contribution: Juan Fernández
}

tokens += tuple(reserved.values())

# START Contribution: José Toapanta
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MODULE = r"%"
t_PLUSPLUS = r"\+\+"
t_MINUSMINUS = r"--"
t_EQ = r"=="
t_NEQ = r"!="
t_LT = r"<"
t_LE = r"<="
t_GT = r">"
t_GE = r">="
# END Contribution: José Toapanta

# START Contribution: Juan Fernández
t_LAND = r"&&"
t_LOR = r"\|\|"
t_LNOT = r"!"
t_ASSIGN = r"="
t_SHORT_ASSIGN = r":="
t_PLUS_ASSIGN = r"\+="
t_MINUS_ASSIGN = r"-="
t_MULT_ASSIGN = r"\*="
t_DIV_ASSIGN = r"/="
t_MOD_ASSIGN = r"%="
t_AND_ASSIGN = r"&="
t_OR_ASSIGN = r"\|="
t_XOR_ASSIGN = r"\^="
t_LSHIFT_ASSIGN = r"<<="
t_RSHIFT_ASSIGN = r">>="
# END Contribution: Juan Fernández

#START Contribution: Nicolás Fiallo
t_AND = r"&"
t_OR = r"\|"
t_XOR = r"\^"
t_AND_NOT = r"&\^"
t_LSHIFT = r"<<"
t_RSHIFT = r">>"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COMMA = r","
t_DOT = r"\."
t_SEMICOLON = r";"
t_COLON = r":"
#END Contribution: Nicolás Fiallo


t_ignore = " \t"


# START Contribution: José Toapanta
def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t


def t_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t


# END Contribution: José Toapanta


# START Contribution: Juan Fernández
def t_FLOAT64(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t


# END Contribution: Juan Fernández

#START Contribution: Nicolás Fiallo
def t_SINGLE_LINE_COMMENT(t):
    r"\/\/[^\n]*"
    pass

def t_MULTI_LINE_COMMENT(t):
    r"\/\*(.|\n)*\*\/"
    t.lexer.lineno += t.value.count("\n")
    pass
#END Contribution: Nicolás Fiallo

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

lexical_errors = []


# Error handling rule
def t_error(t):
    message = f"Illegal character '{t.value[0]}' on line {t.lineno}"
    print(message)
    lexical_errors.append(message)
    t.lexer.skip(1)  # Skip the illegal character and continue

lexer = lex.lex()

def run_lexer(file_path, github_user):
    with open(file_path, "r", encoding="utf-8") as input_file:
        source_code = input_file.read()
        lexer.input(source_code)

        user_id = github_user.lower().replace(" ", "")
        now = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        log_file_path = f"logs/lexer-{user_id}-{now}.txt"

        with open(log_file_path, "w", encoding="utf-8") as log_file:
            while True:
                token = lexer.token()
                if not token:
                    break
                line = f"{token.type}({token.value}) at line {token.lineno}\n"
                log_file.write(line)
                print(line.strip())

            if lexical_errors:
                log_file.write("\nLexical errors detected:\n")
                for error_msg in lexical_errors:
                    log_file.write(f"- {error_msg}\n")

