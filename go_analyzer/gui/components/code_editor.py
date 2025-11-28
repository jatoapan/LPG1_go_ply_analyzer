"""
Code editor component for Go Analyzer GUI.

Provides a text editor widget with syntax-aware features and dark theme styling
for editing Go source code.
"""

import tkinter as tk
from tkinter import scrolledtext
from ..config import (
    EDITOR_BG, EDITOR_FG, EDITOR_INSERT, EDITOR_SELECT_BG, EDITOR_SELECT_FG,
    EDITOR_FONT, TAB_SIZE, EDITOR_UNDO_ENABLED, EDITOR_MAX_UNDO,
    DEFAULT_EDITOR_CONTENT, TEXT_PADDING_X, TEXT_PADDING_Y
)


class CodeEditor(tk.Frame):
    """Code editor component with dark theme and enhanced features."""

    def __init__(self, parent):
        """
        Initialize the code editor.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Create the text widget with config settings
        self.text_widget = scrolledtext.ScrolledText(
            self,
            wrap=tk.NONE,
            font=EDITOR_FONT,
            bg=EDITOR_BG,
            fg=EDITOR_FG,
            insertbackground=EDITOR_INSERT,
            selectbackground=EDITOR_SELECT_BG,
            selectforeground=EDITOR_SELECT_FG,
            undo=EDITOR_UNDO_ENABLED,
            maxundo=EDITOR_MAX_UNDO,
            padx=TEXT_PADDING_X,
            pady=TEXT_PADDING_Y,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Configure tab handling
        self._setup_tab_handling()

        # Insert welcome message
        self._insert_welcome_message()

    def _setup_tab_handling(self):
        """Configure tab key to insert spaces instead of tab character."""
        def handle_tab(event):
            """Handle tab key press."""
            self.text_widget.insert(tk.INSERT, " " * TAB_SIZE)
            return "break"  # Prevent default tab behavior

        def handle_shift_tab(event):
            """Handle shift+tab key press for dedenting."""
            # Get current line
            line_num = self.text_widget.index(tk.INSERT).split('.')[0]
            line_start = f"{line_num}.0"
            line_end = f"{line_num}.end"
            line_text = self.text_widget.get(line_start, line_end)

            # Remove up to TAB_SIZE leading spaces
            spaces_to_remove = 0
            for i in range(min(TAB_SIZE, len(line_text))):
                if line_text[i] == " ":
                    spaces_to_remove += 1
                else:
                    break

            if spaces_to_remove > 0:
                self.text_widget.delete(line_start, f"{line_num}.{spaces_to_remove}")

            return "break"

        # Bind tab and shift+tab
        self.text_widget.bind("<Tab>", handle_tab)
        self.text_widget.bind("<Shift-Tab>", handle_shift_tab)

    def _insert_welcome_message(self):
        """Insert a welcome message into the editor."""
        self.text_widget.insert("1.0", DEFAULT_EDITOR_CONTENT)

    def get_code(self):
        """
        Get the current code from the editor.

        Returns:
            str: The code content
        """
        return self.text_widget.get("1.0", tk.END)

    def set_code(self, code):
        """
        Set the code in the editor.

        Args:
            code (str): The code to insert
        """
        self.clear()
        self.text_widget.insert("1.0", code)

    def clear(self):
        """Clear all text from the editor."""
        self.text_widget.delete("1.0", tk.END)

    def pack(self, **kwargs):
        """Override pack to apply to the frame."""
        super().pack(**kwargs)

    def grid(self, **kwargs):
        """Override grid to apply to the frame."""
        super().grid(**kwargs)
