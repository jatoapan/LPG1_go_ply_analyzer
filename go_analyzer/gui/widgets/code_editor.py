"""
Code editor widget with Go syntax highlighting.
"""

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import (
    QColor, QTextCharFormat, QFont, QSyntaxHighlighter,
    QPainter, QTextFormat, QPalette
)
import re


class GoSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Go language."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Define formats
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))  # Blue
        keyword_format.setFontWeight(QFont.Bold)

        # Go keywords
        keywords = [
            'break', 'case', 'chan', 'const', 'continue', 'default',
            'defer', 'else', 'fallthrough', 'for', 'func', 'go', 'goto',
            'if', 'import', 'interface', 'map', 'package', 'range',
            'return', 'select', 'struct', 'switch', 'type', 'var'
        ]

        for keyword in keywords:
            pattern = f'\\b{keyword}\\b'
            self.highlighting_rules.append((re.compile(pattern), keyword_format))

        # Built-in types
        type_format = QTextCharFormat()
        type_format.setForeground(QColor("#4EC9B0"))  # Cyan

        types = [
            'bool', 'byte', 'complex64', 'complex128', 'error', 'float32',
            'float64', 'int', 'int8', 'int16', 'int32', 'int64', 'rune',
            'string', 'uint', 'uint8', 'uint16', 'uint32', 'uint64',
            'uintptr'
        ]

        for type_name in types:
            pattern = f'\\b{type_name}\\b'
            self.highlighting_rules.append((re.compile(pattern), type_format))

        # Built-in functions
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor("#DCDCAA"))  # Yellow

        builtins = [
            'append', 'cap', 'close', 'complex', 'copy', 'delete',
            'imag', 'len', 'make', 'new', 'panic', 'print', 'println',
            'real', 'recover'
        ]

        for builtin in builtins:
            pattern = f'\\b{builtin}\\b'
            self.highlighting_rules.append((re.compile(pattern), builtin_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))  # Light green
        self.highlighting_rules.append((
            re.compile(r'\b[0-9]+\.?[0-9]*([eE][+-]?[0-9]+)?\b'),
            number_format
        ))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Orange

        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((re.compile(r'`[^`]*`'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # Single-line comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Green
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r'//[^\n]*'), comment_format))

        # Multi-line comments
        self.comment_start_expression = re.compile(r'/\*')
        self.comment_end_expression = re.compile(r'\*/')
        self.multi_line_comment_format = comment_format

    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text."""
        # Apply single-line rules
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format)

        # Handle multi-line comments
        self.setCurrentBlockState(0)

        start_index = 0
        if self.previousBlockState() != 1:
            match = self.comment_start_expression.search(text)
            start_index = match.start() if match else -1

        while start_index >= 0:
            match = self.comment_end_expression.search(text, start_index)
            if match:
                end_index = match.end()
                length = end_index - start_index
                self.setFormat(start_index, length, self.multi_line_comment_format)
                match = self.comment_start_expression.search(text, end_index)
                start_index = match.start() if match else -1
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start_index
                self.setFormat(start_index, length, self.multi_line_comment_format)
                break


class LineNumberArea(QWidget):
    """Widget for displaying line numbers."""

    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """
    Enhanced code editor with line numbers and syntax highlighting.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up font
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        # Line number area
        self.line_number_area = LineNumberArea(self)

        # Connect signals
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Initialize
        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Syntax highlighter
        self.highlighter = GoSyntaxHighlighter(self.document())

        # Set colors
        self.set_dark_theme()

        # Tab settings
        self.setTabStopDistance(40)  # 4 spaces

    def set_dark_theme(self):
        """Apply dark theme to the editor."""
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor("#1E1E1E"))
        palette.setColor(QPalette.Text, QColor("#D4D4D4"))
        self.setPalette(palette)

    def line_number_area_width(self):
        """Calculate the width needed for line numbers."""
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        """Update the width of the line number area."""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """Update the line number area when scrolling."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(),
                                         self.line_number_area.width(),
                                         rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(),
                  self.line_number_area_width(), cr.height())
        )

    def highlight_current_line(self):
        """Highlight the current line."""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor("#2D2D30")

            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        """Paint the line numbers."""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#252526"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#858585"))
                painter.drawText(0, top,
                               self.line_number_area.width() - 2,
                               self.fontMetrics().height(),
                               Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def get_current_line(self):
        """Get the current line number (1-indexed)."""
        return self.textCursor().blockNumber() + 1

    def get_current_column(self):
        """Get the current column number (1-indexed)."""
        return self.textCursor().columnNumber() + 1

    def goto_line(self, line_number):
        """Go to a specific line number."""
        cursor = self.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.movePosition(cursor.Down, cursor.MoveAnchor, line_number - 1)
        self.setTextCursor(cursor)
        self.centerCursor()

    def highlight_error_line(self, line_number):
        """Highlight a line with an error."""
        # This would be used to visually mark error lines
        pass
