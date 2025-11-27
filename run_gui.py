import sys 
import os
from PySide6.QtWidgets import QApplication

try:
    from go_analyzer.gui.main_window import MainWindow
except ImportError as e:
    print("Error: Could not import MainWindow from go_analyzer.gui.main_window. \n"
    "Please ensure that the go_analyzer package is correctly installed and accessible.")
    print(f"Error Details: {e}")
    sys.exit(1)

def main():
    """
    Punto de entrada principal para la GUI del Analizador Go.
    """
    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Go Analyzer")
    app.setOrganizationName("LPG1 Team")
    app.setApplicationVersion("1.0")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    print("Starting Go Analyzer GUI...")
    main()