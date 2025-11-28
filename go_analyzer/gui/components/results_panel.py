"""
Results display panel for Go Analyzer GUI.

Provides a formatted display area for analysis results with color-coded
sections and error highlighting.
"""

import tkinter as tk
from tkinter import scrolledtext


class ResultsPanel(tk.Frame):
    """Results display panel with formatted output and color coding."""

    def __init__(self, parent):
        """
        Initialize the results panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Configure dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"

        # Create the text widget (read-only)
        self.text_widget = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Courier New", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            state=tk.DISABLED,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for formatting
        self._setup_text_tags()

        # Display welcome message
        self._display_welcome_message()

    def _setup_text_tags(self):
        """Configure text tags for color-coded output."""
        # Header tag (bright blue)
        self.text_widget.tag_config(
            "header",
            foreground="#569cd6",
            font=("Courier New", 11, "bold")
        )

        # Success tag (green)
        self.text_widget.tag_config(
            "success",
            foreground="#4ec9b0"
        )

        # Error tag (red)
        self.text_widget.tag_config(
            "error",
            foreground="#f48771"
        )

        # Warning tag (yellow)
        self.text_widget.tag_config(
            "warning",
            foreground="#dcdcaa"
        )

        # Info tag (cyan)
        self.text_widget.tag_config(
            "info",
            foreground="#4fc1ff"
        )

        # Section tag (purple)
        self.text_widget.tag_config(
            "section",
            foreground="#c586c0",
            font=("Courier New", 10, "bold")
        )

        # Emphasis tag (bold)
        self.text_widget.tag_config(
            "emphasis",
            font=("Courier New", 10, "bold")
        )

    def _display_welcome_message(self):
        """Display the welcome message."""
        welcome = """╔════════════════════════════════════════════════════╗
║         Welcome to Go Analyzer!                    ║
╚════════════════════════════════════════════════════╝

This tool performs comprehensive analysis of Go code:

  Lexical Analysis - Tokenization and lexical error detection
  Syntax Analysis - Grammar validation and parse tree generation
  Semantic Analysis - Type checking and semantic rules

How to use:
  1. Write or load Go code in the left panel
  2. Click "Run Analysis" or press Ctrl+R
  3. View results here with color-coded output

Keyboard Shortcuts:
  Ctrl+R - Run analysis
  Ctrl+L - Clear results
  Ctrl+O - Load file
  Ctrl+S - Save results

Ready to analyze your Go code!
"""
        self._append_text(welcome, "info")

    def _append_text(self, text, tag=None):
        """
        Append text to the results panel.

        Args:
            text (str): Text to append
            tag (str, optional): Text tag for formatting
        """
        self.text_widget.config(state=tk.NORMAL)
        if tag:
            self.text_widget.insert(tk.END, text, tag)
        else:
            self.text_widget.insert(tk.END, text)
        self.text_widget.config(state=tk.DISABLED)
        self._auto_scroll()

    def _auto_scroll(self):
        """Scroll to the bottom of the text widget."""
        self.text_widget.see(tk.END)

    def clear(self):
        """Clear all text from the results panel."""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.config(state=tk.DISABLED)
        self._display_welcome_message()

    def display_message(self, message, tag="info"):
        """
        Display a message in the results panel.

        Args:
            message (str): Message to display
            tag (str): Text tag for formatting (default: "info")
        """
        self.clear()
        self._append_text(message, tag)

    def display_results(self, results_dict):
        """
        Display formatted analysis results.

        Args:
            results_dict (dict): Dictionary containing analysis results
                Expected keys: lexer_output, parser_output, errors, success
        """
        self.clear()

        # Header
        self._append_text("=" * 60 + "\n", "header")
        self._append_text("  GO CODE ANALYSIS RESULTS\n", "header")
        self._append_text("=" * 60 + "\n\n", "header")

        # Lexer output
        if "lexer_output" in results_dict:
            self._append_text("LEXICAL ANALYSIS\n", "section")
            self._append_text("-" * 60 + "\n", "section")
            self._append_text(results_dict["lexer_output"] + "\n\n")

        # Parser output
        if "parser_output" in results_dict:
            self._append_text("SYNTAX & SEMANTIC ANALYSIS\n", "section")
            self._append_text("-" * 60 + "\n", "section")
            self._append_text(results_dict["parser_output"] + "\n\n")

        # Errors summary
        if "errors" in results_dict and results_dict["errors"]:
            self._append_text("ERRORS DETECTED\n", "error")
            self._append_text("-" * 60 + "\n", "error")
            for error in results_dict["errors"]:
                self._append_text(f"  {error}\n", "error")
            self._append_text("\n")

        # Success indicator
        if "success" in results_dict:
            if results_dict["success"]:
                self._append_text("\nAnalysis completed successfully!\n", "success")
            else:
                self._append_text("\nAnalysis completed with errors.\n", "error")

        self._append_text("\n" + "=" * 60 + "\n", "header")

    def display_error(self, error_message):
        """
        Display an error message.

        Args:
            error_message (str): Error message to display
        """
        self.clear()
        self._append_text("ERROR\n", "error")
        self._append_text("-" * 60 + "\n", "error")
        self._append_text(error_message + "\n", "error")

    def get_text(self):
        """
        Get all text from the results panel.

        Returns:
            str: The results text content
        """
        return self.text_widget.get("1.0", tk.END)

    def pack(self, **kwargs):
        """Override pack to apply to the frame."""
        super().pack(**kwargs)

    def grid(self, **kwargs):
        """Override grid to apply to the frame."""
        super().grid(**kwargs)
