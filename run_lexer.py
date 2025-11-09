import sys
from go_analyzer.core.lexer import run_lexer

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_lexer.py tests/<file.go> <username>")
    else:
        file_path = sys.argv[1]
        username = sys.argv[2]
        run_lexer(file_path, username)