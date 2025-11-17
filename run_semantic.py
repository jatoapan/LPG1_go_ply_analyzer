import sys
from go_analyzer.core.parser import run_semantic

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_semantic.py tests/<file.go> <username>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        username = sys.argv[2]
        run_semantic(file_path, username)
