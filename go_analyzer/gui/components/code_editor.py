"""
Code editor component for Go Analyzer GUI.

Provides a text editor widget with syntax-aware features and dark theme styling
for editing Go source code.
"""

import tkinter as tk
from tkinter import scrolledtext


class CodeEditor(tk.Frame):
    """Code editor component with dark theme and enhanced features."""

    def __init__(self, parent):
        """
        Initialize the code editor.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Configure dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"
        self.insert_color = "#aeafad"
        self.select_bg = "#264f78"
        self.select_fg = "#ffffff"

        # Create the text widget
        self.text_widget = scrolledtext.ScrolledText(
            self,
            wrap=tk.NONE,
            font=("Courier New", 11),
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.insert_color,
            selectbackground=self.select_bg,
            selectforeground=self.select_fg,
            undo=True,
            maxundo=-1,
            padx=5,
            pady=5,
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
            self.text_widget.insert(tk.INSERT, "    ")  # Insert 4 spaces
            return "break"  # Prevent default tab behavior

        def handle_shift_tab(event):
            """Handle shift+tab key press for dedenting."""
            # Get current line
            line_num = self.text_widget.index(tk.INSERT).split('.')[0]
            line_start = f"{line_num}.0"
            line_end = f"{line_num}.end"
            line_text = self.text_widget.get(line_start, line_end)

            # Remove up to 4 leading spaces
            if line_text.startswith("    "):
                self.text_widget.delete(line_start, f"{line_num}.4")
            elif line_text.startswith("   "):
                self.text_widget.delete(line_start, f"{line_num}.3")
            elif line_text.startswith("  "):
                self.text_widget.delete(line_start, f"{line_num}.2")
            elif line_text.startswith(" "):
                self.text_widget.delete(line_start, f"{line_num}.1")

            return "break"

        # Bind tab and shift+tab
        self.text_widget.bind("<Tab>", handle_tab)
        self.text_widget.bind("<Shift-Tab>", handle_shift_tab)

    def _insert_welcome_message(self):
        """Insert a welcome message into the editor."""
        welcome_text = """// Welcome to Go Analyzer!
//
// Write or paste your Go code here, then click "Run Analysis"
// or press Ctrl+R to analyze it.
//
// Example Go code:

package main

import "fmt"

func main() {
    x := 10
    y := 20
    fmt.Println(x + y)
}
"""
        self.text_widget.insert("1.0", welcome_text)

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
