"""
Results Panel Component for Go Analyzer

A simple, read-only text display for showing formatted analysis results.
Features color-coded sections for errors, success messages, and different
analysis outputs.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPalette, QTextCharFormat, QTextCursor


class ResultsPanel(QWidget):
    """
    A read-only text panel for displaying formatted analysis results.

    Features:
    - Read-only text display with scrolling
    - Color-coded sections (errors in red, success in green, info in blue)
    - Welcome message on initialization
    - Clear/reset functionality
    - Consistent dark theme styling
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_text_formats()
        self.set_dark_theme()
        self.show_welcome_message()

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Text display area (read-only, scrollable)
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)

        # Set monospace font for better code/data display
        font = QFont("Consolas", 9)
        font.setStyleHint(QFont.Monospace)
        self.text_display.setFont(font)

        # Enable line wrap for better readability
        self.text_display.setLineWrapMode(QTextEdit.WidgetWidth)

        layout.addWidget(self.text_display)

        # Button bar at bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        # Clear button
        self.clear_button = QPushButton("Clear Results")
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.setFixedHeight(30)

        # Copy button
        self.copy_button = QPushButton("Copy All")
        self.copy_button.clicked.connect(self.copy_all_text)
        self.copy_button.setFixedHeight(30)

        button_layout.addStretch()
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

    def setup_text_formats(self):
        """Set up text formatting styles for different message types."""
        # Error format (red)
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("#F48771"))  # Light red
        self.error_format.setFontWeight(QFont.Bold)

        # Success format (green)
        self.success_format = QTextCharFormat()
        self.success_format.setForeground(QColor("#4EC9B0"))  # Cyan/green
        self.success_format.setFontWeight(QFont.Bold)

        # Warning format (yellow/orange)
        self.warning_format = QTextCharFormat()
        self.warning_format.setForeground(QColor("#CCA700"))  # Yellow

        # Info format (blue)
        self.info_format = QTextCharFormat()
        self.info_format.setForeground(QColor("#75BEFF"))  # Light blue

        # Header format (white, bold)
        self.header_format = QTextCharFormat()
        self.header_format.setForeground(QColor("#FFFFFF"))
        self.header_format.setFontWeight(QFont.Bold)

        # Normal format (default text color)
        self.normal_format = QTextCharFormat()
        self.normal_format.setForeground(QColor("#D4D4D4"))  # Light gray

        # Separator format (dim)
        self.separator_format = QTextCharFormat()
        self.separator_format.setForeground(QColor("#6A6A6A"))  # Dim gray

    def set_dark_theme(self):
        """Apply dark theme consistent with the editor."""
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor("#1E1E1E"))  # Background
        palette.setColor(QPalette.Text, QColor("#D4D4D4"))  # Text
        self.text_display.setPalette(palette)

        # Style buttons to match theme
        button_style = """
        QPushButton {
            background-color: #0E639C;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #1177BB;
        }
        QPushButton:pressed {
            background-color: #094771;
        }
        """
        self.clear_button.setStyleSheet(button_style)
        self.copy_button.setStyleSheet(button_style)

    def show_welcome_message(self):
        """Display welcome message on initialization."""
        self.clear()
        self.append_header("=" * 70)
        self.append_header("         Welcome to Go Analyzer - Results Display")
        self.append_header("=" * 70)
        self.append_text("\n")
        self.append_info("This panel displays formatted analysis results including:")
        self.append_text("  • Lexical analysis (tokenization)")
        self.append_text("  • Syntax analysis (parsing)")
        self.append_text("  • Semantic analysis (type checking, symbol resolution)")
        self.append_text("\n")
        self.append_info("Click 'Analyze' (F5) to analyze your Go code.")
        self.append_text("\n")
        self.append_separator("-" * 70)

    def append_text(self, text, format=None):
        """
        Append text with optional formatting.

        Args:
            text: Text to append
            format: QTextCharFormat to apply (None for default)
        """
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.End)

        if format:
            cursor.insertText(text + "\n", format)
        else:
            cursor.insertText(text + "\n", self.normal_format)

        # Auto-scroll to bottom
        self.text_display.setTextCursor(cursor)
        self.text_display.ensureCursorVisible()

    def append_header(self, text):
        """Append text as a header (white, bold)."""
        self.append_text(text, self.header_format)

    def append_error(self, text):
        """Append text as an error (red, bold)."""
        self.append_text("✗ " + text, self.error_format)

    def append_success(self, text):
        """Append text as a success message (green, bold)."""
        self.append_text("✓ " + text, self.success_format)

    def append_warning(self, text):
        """Append text as a warning (yellow)."""
        self.append_text("⚠ " + text, self.warning_format)

    def append_info(self, text):
        """Append text as info (blue)."""
        self.append_text("ℹ " + text, self.info_format)

    def append_separator(self, text=None):
        """Append a separator line (dim gray)."""
        if text is None:
            text = "-" * 70
        self.append_text(text, self.separator_format)

    def display_results(self, results_text):
        """
        Display formatted results text with automatic color coding.

        This method parses the results text and applies appropriate
        formatting based on content markers (✗, ✓, etc.).

        Args:
            results_text: Formatted analysis results as string
        """
        self.clear()

        # Split into lines and process each
        for line in results_text.split("\n"):
            # Detect line type and apply appropriate formatting
            if line.startswith("="):
                self.append_header(line)
            elif "✗" in line or "Error" in line:
                self.append_error(line.replace("✗ ", ""))
            elif "✓" in line or "No " in line and "error" in line.lower():
                self.append_success(line.replace("✓ ", ""))
            elif "⚠" in line or "Warning" in line:
                self.append_warning(line.replace("⚠ ", ""))
            elif line.startswith("-") and all(c == "-" for c in line.strip()):
                self.append_separator(line)
            elif any(
                keyword in line
                for keyword in ["ANALYSIS", "SOURCE CODE", "SYMBOL TABLE"]
            ):
                self.append_header(line)
            else:
                self.append_text(line)

    def set_text(self, text):
        """
        Set the entire text content (simple version without formatting).

        Args:
            text: Plain text to display
        """
        self.text_display.setPlainText(text)

    def clear(self):
        """Clear all text from the display."""
        self.text_display.clear()

    def reset(self):
        """Reset to welcome message."""
        self.show_welcome_message()

    def copy_all_text(self):
        """Copy all text to clipboard."""
        self.text_display.selectAll()
        self.text_display.copy()
        cursor = self.text_display.textCursor()
        cursor.clearSelection()
        self.text_display.setTextCursor(cursor)

    def get_text(self):
        """
        Get all text content.

        Returns:
            str: All text in the display
        """
        return self.text_display.toPlainText()

    def append_analysis_output(self, output_type, content):
        """
        Append a section of analysis output with header.

        Args:
            output_type: Type of output (e.g., "Lexical Analysis", "Parser Analysis")
            content: The content to display
        """
        self.append_text("\n")
        self.append_header(f"{'=' * 70}")
        self.append_header(f"{output_type.upper()}")
        self.append_header(f"{'=' * 70}")
        self.append_text("\n")
        self.display_results(content)

    def show_error_message(self, error_msg):
        """
        Show an error message.

        Args:
            error_msg: Error message to display
        """
        self.clear()
        self.append_header("=" * 70)
        self.append_header("ERROR")
        self.append_header("=" * 70)
        self.append_text("\n")
        self.append_error(error_msg)

    def show_success_message(self, success_msg):
        """
        Show a success message.

        Args:
            success_msg: Success message to display
        """
        self.clear()
        self.append_header("=" * 70)
        self.append_header("SUCCESS")
        self.append_header("=" * 70)
        self.append_text("\n")
        self.append_success(success_msg)
