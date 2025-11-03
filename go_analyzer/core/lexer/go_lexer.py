import ply.lex as lex
from datetime import datetime

# START Contribution: José Toapanta
# Tokens and regex rules for identifiers, arithmetic and relational operators, assignment, and primitive types
# Reserved keywords for declarations, booleans, and basic types (int, float64, string, bool)
# Functions for recognizing IDENTIFIER and INT literals
# END Contribution: José Toapanta

tokens = (
    #START Contribution: José Toapanta
    "IDENTIFIER",
    "PLUS", "MINUS", "TIMES", "DIVIDE", "MODULE", "PLUSPLUS", "MINUSMINUS", 
    "EQ", "NEQ", "LT", "LE", "GT", "GE",
    "ASSIGN", "SHORT_ASSIGN",
    #END Contribution: José Toapanta
)

reserved = {
    #START Contribution: José Toapanta
    "package":"PACKAGE",
    "import":"IMPORT",
    "var":"VAR",
    "const":"CONST",
    "func":"FUNC",
    "return":"RETURN",
    "true":"TRUE",
    "false":"FALSE",
    "int": "INT_TYPE",
    "float64": "FLOAT64_TYPE",
    "string": "STRING_TYPE",
    "bool": "BOOL_TYPE"
    #END Contribution: José Toapanta
}

tokens += tuple(reserved.values())

#START Contribution: José Toapanta
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
#END Contribution: José Toapanta

t_ignore = " \t"

#START Contribution: José Toapanta
def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t

def t_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t
#END Contribution: José Toapanta

t_ignore = " \t"

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
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