"""
Output panel for displaying analysis results.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont, QPalette


class OutputPanel(QWidget):
    """
    Panel for displaying analysis results including:
    - Tokens
    - AST
    - Symbol Table
    - Errors and Warnings
    """

    error_clicked = Signal(int)  # Emit line number when error is clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.set_dark_theme()

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tab widget for different views
        self.tab_widget = QTabWidget()

        # Tokens tab
        self.tokens_table = self.create_table(
            ["Type", "Value", "Line", "Column"],
            [200, 200, 80, 80]
        )
        self.tab_widget.addTab(self.tokens_table, "Tokens")

        # AST tab
        self.ast_text = self.create_text_view()
        self.tab_widget.addTab(self.ast_text, "AST")

        # Symbol Table tab
        self.symbol_table = self.create_table(
            ["Name", "Kind", "Type", "Line", "Scope", "Used"],
            [150, 100, 120, 60, 80, 60]
        )
        self.tab_widget.addTab(self.symbol_table, "Symbol Table")

        # Errors tab
        self.errors_table = self.create_table(
            ["Severity", "Message", "Line", "Column"],
            [80, 400, 60, 60]
        )
        self.errors_table.cellClicked.connect(self.on_error_clicked)
        self.tab_widget.addTab(self.errors_table, "Errors")

        # Console/Log tab
        self.console_text = self.create_text_view()
        self.tab_widget.addTab(self.console_text, "Console")

        layout.addWidget(self.tab_widget)

    def create_table(self, headers, column_widths):
        """Create a table widget with specified headers and column widths."""
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Set column widths
        for i, width in enumerate(column_widths):
            table.setColumnWidth(i, width)

        # Configure table
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.horizontalHeader().setStretchLastSection(True)

        return table

    def create_text_view(self):
        """Create a read-only text view."""
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        font = QFont("Consolas", 9)
        font.setStyleHint(QFont.Monospace)
        text_edit.setFont(font)
        return text_edit

    def set_dark_theme(self):
        """Apply dark theme to the output panel."""
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor("#1E1E1E"))
        palette.setColor(QPalette.Text, QColor("#D4D4D4"))
        palette.setColor(QPalette.AlternateBase, QColor("#2D2D30"))

        self.tokens_table.setPalette(palette)
        self.symbol_table.setPalette(palette)
        self.errors_table.setPalette(palette)
        self.ast_text.setPalette(palette)
        self.console_text.setPalette(palette)

    def display_tokens(self, tokens):
        """Display lexical tokens."""
        self.tokens_table.setRowCount(0)
        self.tokens_table.setRowCount(len(tokens))

        for i, token in enumerate(tokens):
            self.tokens_table.setItem(i, 0, QTableWidgetItem(str(token.type)))
            self.tokens_table.setItem(i, 1, QTableWidgetItem(str(token.value)))
            self.tokens_table.setItem(i, 2, QTableWidgetItem(str(token.lineno)))
            self.tokens_table.setItem(i, 3, QTableWidgetItem(str(token.column)))

        self.log(f"Displayed {len(tokens)} tokens")

    def display_ast(self, ast_node):
        """Display Abstract Syntax Tree."""
        if ast_node:
            ast_str = self.format_ast(ast_node)
            self.ast_text.setPlainText(ast_str)
            self.log("AST generated successfully")
        else:
            self.ast_text.setPlainText("No AST available (parsing failed)")
            self.log("AST generation failed")

    def format_ast(self, node, indent=0):
        """Format AST node for display."""
        result = "  " * indent + repr(node) + "\n"

        # Recursively format child nodes
        if hasattr(node, '__dict__'):
            for key, value in node.__dict__.items():
                if key.startswith('_'):
                    continue

                if isinstance(value, list):
                    for item in value:
                        if hasattr(item, '__dict__') and hasattr(item, '__class__'):
                            result += self.format_ast(item, indent + 1)
                elif hasattr(value, '__dict__') and hasattr(value, '__class__'):
                    if value.__class__.__module__.startswith('go_analyzer.core'):
                        result += self.format_ast(value, indent + 1)

        return result

    def display_symbol_table(self, symbols):
        """Display symbol table."""
        self.symbol_table.setRowCount(0)
        self.symbol_table.setRowCount(len(symbols))

        for i, symbol in enumerate(symbols):
            self.symbol_table.setItem(i, 0, QTableWidgetItem(symbol.name))
            self.symbol_table.setItem(i, 1, QTableWidgetItem(symbol.kind.name))
            self.symbol_table.setItem(i, 2, QTableWidgetItem(str(symbol.type or '')))
            self.symbol_table.setItem(i, 3, QTableWidgetItem(str(symbol.line)))
            self.symbol_table.setItem(i, 4, QTableWidgetItem(str(symbol.scope_level)))
            self.symbol_table.setItem(i, 5, QTableWidgetItem('Yes' if symbol.is_used else 'No'))

            # Color code unused variables
            if not symbol.is_used:
                for col in range(6):
                    item = self.symbol_table.item(i, col)
                    if item:
                        item.setForeground(QColor("#CE9178"))  # Orange

        self.log(f"Displayed {len(symbols)} symbols")

    def display_errors(self, lexical_errors, syntax_errors, semantic_errors, warnings):
        """Display all errors and warnings."""
        self.errors_table.setRowCount(0)

        all_errors = []

        # Collect all errors
        for error in lexical_errors:
            all_errors.append(("Error", error.message, error.line, error.column))

        for error in syntax_errors:
            all_errors.append(("Error", error.message, error.line, error.column))

        for error in semantic_errors:
            all_errors.append((error.severity.capitalize(), error.message, error.line, error.column))

        for warning in warnings:
            all_errors.append(("Warning", warning.message, warning.line, warning.column))

        # Sort by line number
        all_errors.sort(key=lambda x: x[2])

        # Display errors
        self.errors_table.setRowCount(len(all_errors))

        for i, (severity, message, line, column) in enumerate(all_errors):
            severity_item = QTableWidgetItem(severity)
            message_item = QTableWidgetItem(message)
            line_item = QTableWidgetItem(str(line))
            column_item = QTableWidgetItem(str(column))

            # Color code by severity
            if severity == "Error":
                color = QColor("#F48771")  # Red
            elif severity == "Warning":
                color = QColor("#CCA700")  # Yellow
            else:
                color = QColor("#75BEFF")  # Blue

            severity_item.setForeground(color)

            self.errors_table.setItem(i, 0, severity_item)
            self.errors_table.setItem(i, 1, message_item)
            self.errors_table.setItem(i, 2, line_item)
            self.errors_table.setItem(i, 3, column_item)

        # Switch to errors tab if there are errors
        if all_errors:
            self.tab_widget.setCurrentWidget(self.errors_table)
            self.log(f"Found {len(all_errors)} issues")

    def on_error_clicked(self, row, column):
        """Handle error row click."""
        line_item = self.errors_table.item(row, 2)
        if line_item:
            try:
                line_number = int(line_item.text())
                self.error_clicked.emit(line_number)
            except ValueError:
                pass

    def log(self, message):
        """Add a message to the console."""
        self.console_text.append(f"[INFO] {message}")

    def log_error(self, message):
        """Add an error message to the console."""
        self.console_text.append(f"[ERROR] {message}")

    def clear_all(self):
        """Clear all output."""
        self.tokens_table.setRowCount(0)
        self.ast_text.clear()
        self.symbol_table.setRowCount(0)
        self.errors_table.setRowCount(0)
        self.console_text.clear()
        self.log("Output cleared")

    def show_tab(self, tab_name):
        """Switch to a specific tab."""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == tab_name:
                self.tab_widget.setCurrentIndex(i)
                break
