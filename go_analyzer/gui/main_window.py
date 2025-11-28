"""
Main window for Go Analyzer GUI.

Provides the primary application window with a two-panel layout
for code editing and results display.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .components.code_editor import CodeEditor
from .components.results_panel import ResultsPanel
from .components.controls import ControlPanel
from .handlers.analysis_handler import AnalysisHandler
from .handlers.file_handler import FileHandler
from .state.app_state import AppState
from .config import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    LABEL_FONT_BOLD, STATUS_CLEARED,
    SHORTCUT_RUN_ANALYSIS, SHORTCUT_CLEAR_RESULTS,
    SHORTCUT_LOAD_FILE, SHORTCUT_SAVE_RESULTS
)


class MainWindow:
    """Main application window for Go Analyzer."""

    def __init__(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        # Set minimum window size
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Configure window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize state manager
        self.state = AppState()

        # Initialize components
        self._setup_ui()
        self._setup_shortcuts()

    def _setup_ui(self):
        """Set up the user interface components."""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create PanedWindow for resizable panels
        paned_window = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Left panel - Code Editor
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)

        # Editor label
        editor_label = ttk.Label(left_frame, text="Go Code Editor", font=LABEL_FONT_BOLD)
        editor_label.pack(pady=(0, 5))

        # Code editor component
        self.code_editor = CodeEditor(left_frame)
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Right panel - Results Display
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)

        # Results label
        results_label = ttk.Label(right_frame, text="Analysis Results", font=LABEL_FONT_BOLD)
        results_label.pack(pady=(0, 5))

        # Results panel component
        self.results_panel = ResultsPanel(right_frame)
        self.results_panel.pack(fill=tk.BOTH, expand=True)

        # Bottom control panel
        self._setup_control_panel(main_container)

    def _setup_control_panel(self, parent):
        """Set up the control panel with action buttons."""
        # Create control panel with callbacks
        callbacks = {
            'run_analysis': self.run_analysis,
            'clear_results': self.clear_results,
            'load_file': self.load_file,
            'save_results': self.save_results
        }

        self.control_panel = ControlPanel(parent, callbacks=callbacks)
        self.control_panel.pack(fill=tk.X, pady=(5, 0))

        # Initialize handlers
        self.analysis_handler = AnalysisHandler(
            self.code_editor,
            self.results_panel,
            self.control_panel
        )

        self.file_handler = FileHandler(
            self.code_editor,
            self.results_panel,
            self.control_panel,
            self.state
        )

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts using config constants."""
        # Ctrl+R - Run analysis
        for shortcut in SHORTCUT_RUN_ANALYSIS:
            self.root.bind(shortcut, lambda e: self.run_analysis())

        # Ctrl+L - Clear results
        for shortcut in SHORTCUT_CLEAR_RESULTS:
            self.root.bind(shortcut, lambda e: self.clear_results())

        # Ctrl+O - Load file
        for shortcut in SHORTCUT_LOAD_FILE:
            self.root.bind(shortcut, lambda e: self.load_file())

        # Ctrl+S - Save results
        for shortcut in SHORTCUT_SAVE_RESULTS:
            self.root.bind(shortcut, lambda e: self.save_results())

    def run_analysis(self):
        """Run analysis on the current code."""
        # Delegate to analysis handler
        self.analysis_handler.handle_analysis()

    def clear_results(self):
        """Clear the results panel."""
        self.results_panel.clear()
        self.control_panel.set_status(STATUS_CLEARED, "success")

    def load_file(self):
        """Load a file into the editor."""
        self.file_handler.load_file()

    def save_results(self):
        """Save results to a file."""
        self.file_handler.save_results()

    def on_closing(self):
        """Handle window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Save state before closing
            self.state.save_state()
            self.root.destroy()

    def run(self):
        """Start the GUI application main loop."""
        self.root.mainloop()
