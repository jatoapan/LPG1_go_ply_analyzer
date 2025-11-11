import sys
from go_analyzer.core.parser import run_parser

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_parser.py tests/<file.go> <username>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        username = sys.argv[2]
        run_parser(file_path, username)
