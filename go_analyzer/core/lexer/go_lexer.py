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


tokens = (
    # START Contribution: José Toapanta
    "IDENTIFIER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULE",
    "PLUSPLUS",
    "MINUSMINUS",
    "EQ",
    "NEQ",
    "LT",
    "LE",
    "GT",
    "GE",
    "INT",
    # END Contribution: José Toapanta
    #
    # START Contribution: Juan Fernández
    "LAND",
    "LOR",
    "LNOT",
    "ASSIGN",
    "SHORT_ASSIGN",
    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "MULT_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "OR_ASSIGN",
    "XOR_ASSIGN",
    "LSHIFT_ASSIGN",
    "RSHIFT_ASSIGN",
    "FLOAT64",
    "STRING",
    # END Contribution: Juan Fernández
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

# --- Now, let's test it ---
if __name__ == "__main__":
    data = """
    5 * (2 + 3)
    10 / 2 - 1
    """

    # Give the lexer some input
    lexer.input(data)

    # Tokenize the input
    print("--- Generated Tokens ---")
    while True:
        tok = lexer.token()  # Get the next token
        if not tok:
            break  # No more input
        print(tok)
