#!/usr/bin/env python3
"""
Go Analyzer GUI Entry Point

Launches the graphical user interface for the Go code analyzer.
Provides an interactive environment for lexical, syntax, and semantic analysis.

Usage:
    python run_gui.py
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from go_analyzer.gui import MainWindow


def main():
    """Main entry point for the GUI application."""
    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
