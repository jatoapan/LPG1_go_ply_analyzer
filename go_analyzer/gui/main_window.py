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


class MainWindow:
    """Main application window for Go Analyzer."""

    def __init__(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        self.root.title("Go Analyzer - Lexical, Syntax & Semantic Analysis")
        self.root.geometry("1100x600")

        # Set minimum window size
        self.root.minsize(800, 400)

        # Configure window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        editor_label = ttk.Label(left_frame, text="Go Code Editor", font=('Arial', 10, 'bold'))
        editor_label.pack(pady=(0, 5))

        # Code editor component
        self.code_editor = CodeEditor(left_frame)
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Right panel - Results Display
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)

        # Results label
        results_label = ttk.Label(right_frame, text="Analysis Results", font=('Arial', 10, 'bold'))
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

        # Initialize analysis handler
        self.analysis_handler = AnalysisHandler(
            self.code_editor,
            self.results_panel,
            self.control_panel
        )

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Ctrl+R - Run analysis
        self.root.bind('<Control-r>', lambda e: self.run_analysis())
        self.root.bind('<Control-R>', lambda e: self.run_analysis())

        # Ctrl+L - Clear results
        self.root.bind('<Control-l>', lambda e: self.clear_results())
        self.root.bind('<Control-L>', lambda e: self.clear_results())

        # Ctrl+O - Load file (placeholder)
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-O>', lambda e: self.load_file())

        # Ctrl+S - Save results (placeholder)
        self.root.bind('<Control-s>', lambda e: self.save_results())
        self.root.bind('<Control-S>', lambda e: self.save_results())

    def run_analysis(self):
        """Run analysis on the current code."""
        # Delegate to analysis handler
        self.analysis_handler.handle_analysis()

    def clear_results(self):
        """Clear the results panel."""
        self.results_panel.clear()
        self.control_panel.set_status("Results cleared", "success")

    def load_file(self):
        """Load a file into the editor (placeholder)."""
        # Will be implemented in Phase 4
        messagebox.showinfo("Load File", "File loading will be implemented in Phase 4.")

    def save_results(self):
        """Save results to a file (placeholder)."""
        # Will be implemented in Phase 4
        messagebox.showinfo("Save Results", "Results saving will be implemented in Phase 4.")

    def on_closing(self):
        """Handle window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def run(self):
        """Start the GUI application main loop."""
        self.root.mainloop()
