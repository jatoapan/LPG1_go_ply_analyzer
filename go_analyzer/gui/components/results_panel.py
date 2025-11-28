"""
Results display panel for Go Analyzer GUI.

Provides a formatted display area for analysis results with color-coded
sections and error highlighting.
"""

import tkinter as tk
from tkinter import scrolledtext
from ..config import (
    RESULTS_BG, RESULTS_FG, RESULTS_FONT, RESULTS_PADDING_X, RESULTS_PADDING_Y,
    DEFAULT_WELCOME_MESSAGE, get_tag_config
)


class ResultsPanel(tk.Frame):
    """Results display panel with formatted output and color coding."""

    def __init__(self, parent):
        """
        Initialize the results panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Create the text widget (read-only) with config settings
        self.text_widget = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=RESULTS_FONT,
            bg=RESULTS_BG,
            fg=RESULTS_FG,
            state=tk.DISABLED,
            padx=RESULTS_PADDING_X,
            pady=RESULTS_PADDING_Y,
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
        tag_configs = get_tag_config()
        for tag_name, tag_config in tag_configs.items():
            self.text_widget.tag_config(tag_name, **tag_config)

    def _display_welcome_message(self):
        """Display the welcome message."""
        self._append_text(DEFAULT_WELCOME_MESSAGE, "info")

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
