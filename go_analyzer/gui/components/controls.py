"""
Control buttons and event handlers for Go Analyzer GUI.

Provides action buttons for running analysis, clearing results,
loading files, and saving results with proper styling and event wiring.
"""

import tkinter as tk
from tkinter import ttk


class ControlPanel(tk.Frame):
    """Control panel with action buttons for the analyzer."""

    def __init__(self, parent, callbacks=None):
        """
        Initialize the control panel.

        Args:
            parent: Parent widget
            callbacks (dict, optional): Dictionary of callback functions
                Expected keys: 'run_analysis', 'clear_results', 'load_file', 'save_results'
        """
        super().__init__(parent)

        # Store callbacks
        self.callbacks = callbacks or {}

        # Set up the control panel UI
        self._setup_ui()

    def _setup_ui(self):
        """Set up the control panel user interface."""
        # Create button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=5)

        # Run Analysis button (primary action)
        self.run_button = ttk.Button(
            button_frame,
            text="▶ Run Analysis",
            command=self._on_run_analysis,
            width=15
        )
        self.run_button.pack(side=tk.LEFT, padx=5)

        # Clear button
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Results",
            command=self._on_clear_results,
            width=15
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Load File button
        self.load_button = ttk.Button(
            button_frame,
            text="📁 Load File",
            command=self._on_load_file,
            width=15
        )
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Save Results button
        self.save_button = ttk.Button(
            button_frame,
            text="💾 Save Results",
            command=self._on_save_results,
            width=15
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Status label on the right
        self.status_label = ttk.Label(
            button_frame,
            text="Ready",
            font=('Arial', 9),
            foreground="#4ec9b0"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

    def _on_run_analysis(self):
        """Handle run analysis button click."""
        callback = self.callbacks.get('run_analysis')
        if callback:
            callback()

    def _on_clear_results(self):
        """Handle clear results button click."""
        callback = self.callbacks.get('clear_results')
        if callback:
            callback()

    def _on_load_file(self):
        """Handle load file button click."""
        callback = self.callbacks.get('load_file')
        if callback:
            callback()

    def _on_save_results(self):
        """Handle save results button click."""
        callback = self.callbacks.get('save_results')
        if callback:
            callback()

    def set_status(self, message, status_type="normal"):
        """
        Update the status label.

        Args:
            message (str): Status message to display
            status_type (str): Type of status - "normal", "running", "success", "error"
        """
        color_map = {
            "normal": "#4ec9b0",      # Cyan
            "running": "#dcdcaa",     # Yellow
            "success": "#4ec9b0",     # Green
            "error": "#f48771"        # Red
        }

        color = color_map.get(status_type, "#d4d4d4")
        self.status_label.config(text=message, foreground=color)

    def enable_buttons(self, enabled=True):
        """
        Enable or disable all buttons.

        Args:
            enabled (bool): True to enable, False to disable
        """
        state = tk.NORMAL if enabled else tk.DISABLED
        self.run_button.config(state=state)
        self.clear_button.config(state=state)
        self.load_button.config(state=state)
        self.save_button.config(state=state)

    def set_callback(self, action, callback):
        """
        Set or update a callback function.

        Args:
            action (str): Action name ('run_analysis', 'clear_results', etc.)
            callback (callable): Callback function
        """
        self.callbacks[action] = callback

    def pack(self, **kwargs):
        """Override pack to apply to the frame."""
        super().pack(**kwargs)

    def grid(self, **kwargs):
        """Override grid to apply to the frame."""
        super().grid(**kwargs)
