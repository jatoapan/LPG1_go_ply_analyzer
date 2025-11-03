import ply.lex as lex

tokens = (
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",  # We use TIMES instead of MUL to avoid conflicts
    "DIVIDE",
    "LPAREN",
    "RPAREN",
)

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"


def t_NUMBER(t):
    r"\d+"  # The docstring is the regex for one or more digits
    t.value = int(t.value)  # Convert the matched string to an integer
    return t


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