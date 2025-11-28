"""
Main window for Go Analyzer application.
"""

import re
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QPushButton, QFileDialog, QMessageBox,
    QStatusBar, QMenuBar, QMenu, QToolBar, QLabel
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QAction, QIcon, QKeySequence

from .widgets.code_editor import CodeEditor
from .widgets.output_panel import OutputPanel

from ..core.analyzer import analyze_code

class AnalysisThread(QThread):
    """Thread for running analysis without blocking UI."""

    finished = Signal(dict)

    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self):
        """Run the analysis."""
        result = {
            'tokens': [],
            'ast': None,
            'symbols': [],
            'lexical_errors': [],
            'syntax_errors': [],
            'semantic_errors': [],
            'warnings': [],
            'raw_report': ""
        }

        try:
            # Lexical analysis
            analysis_result = analyze_code(self.code)
            lex_output = analysis_result['lexical_analysis']
            tokens_list = []
            
            token_pattern = re.compile(r'(\w+)\((.*?)\) at line (\d+), column (\d+)')

            for line in lex_output.split('\n'):
                match = token_pattern.match(line)
                if match:
                    tokens_list.append({
                        'type': match.group(1),
                        'value': match.group(2),
                        'line': int(match.group(3)),
                        'column': int(match.group(4))
                    })
                elif "Lexical errors detected:" in line:
                    pass  # Skip
                elif line.strip().startswith("- "):
                    error_msg = line.strip()
                    result['lexical_errors'].append(error_msg)

            result['tokens'] = tokens_list
            # Syntax analysis
            parser_output = analysis_result['parser_analysis']
            
            for line in parser_output.split('\n'):
                if "✗" in line or "Error" in line:
                    if "Sintactico" in line:
                        result['syntax_errors'].append(line.strip())
                    elif "Semantico" in line or "semántico" in line:
                        result['semantic_errors'].append(line.strip())

            result["raw_report"] = parser_output

        except Exception as e:
            result['error'] = str(e)

        self.finished.emit(result)


class MainWindow(QMainWindow):
    """
    Main window for Go Analyzer application.

    Features:
    - Code editor with syntax highlighting
    - File operations (open, save, new)
    - Analysis execution (lexer, parser, semantic)
    - Results display (tokens, AST, symbol table, errors)
    """

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_modified = False
        self.analysis_thread = None

        self.setup_ui()
        self.create_menus()
        self.create_toolbar()
        self.create_statusbar()

        self.setWindowTitle("Go Analyzer - Untitled")
        self.resize(1400, 900)

        # Apply dark theme
        self.set_dark_theme()

    def setup_ui(self):
        """Set up the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Splitter for editor and output
        splitter = QSplitter(Qt.Vertical)

        # Code editor
        self.code_editor = CodeEditor()
        self.code_editor.textChanged.connect(self.on_text_changed)

        # Output panel
        self.output_panel = OutputPanel()
        self.output_panel.error_clicked.connect(self.goto_error_line)

        # Add to splitter
        splitter.addWidget(self.code_editor)
        splitter.addWidget(self.output_panel)

        # Set initial sizes (60% editor, 40% output)
        splitter.setSizes([600, 400])

        layout.addWidget(splitter)

        # Sample code
        self.load_sample_code()

    def create_menus(self):
        """Create menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.code_editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.code_editor.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.code_editor.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.code_editor.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.code_editor.paste)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("Select &All", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self.code_editor.selectAll)
        edit_menu.addAction(select_all_action)

        # Analysis menu
        analysis_menu = menubar.addMenu("&Analysis")

        analyze_action = QAction("&Analyze Code", self)
        analyze_action.setShortcut(QKeySequence("F5"))
        analyze_action.triggered.connect(self.analyze_code)
        analysis_menu.addAction(analyze_action)

        analysis_menu.addSeparator()

        clear_action = QAction("&Clear Output", self)
        clear_action.setShortcut(QKeySequence("Ctrl+L"))
        clear_action.triggered.connect(self.output_panel.clear_all)
        analysis_menu.addAction(clear_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        view_tokens_action = QAction("View &Tokens", self)
        view_tokens_action.triggered.connect(lambda: self.output_panel.show_tab("Tokens"))
        view_menu.addAction(view_tokens_action)

        view_ast_action = QAction("View &AST", self)
        view_ast_action.triggered.connect(lambda: self.output_panel.show_tab("AST"))
        view_menu.addAction(view_ast_action)

        view_symbols_action = QAction("View &Symbol Table", self)
        view_symbols_action.triggered.connect(lambda: self.output_panel.show_tab("Symbol Table"))
        view_menu.addAction(view_symbols_action)

        view_errors_action = QAction("View &Errors", self)
        view_errors_action.triggered.connect(lambda: self.output_panel.show_tab("Errors"))
        view_menu.addAction(view_errors_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Create toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # New
        new_btn = QPushButton("New")
        new_btn.clicked.connect(self.new_file)
        toolbar.addWidget(new_btn)

        # Open
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.open_file)
        toolbar.addWidget(open_btn)

        # Save
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_file)
        toolbar.addWidget(save_btn)

        toolbar.addSeparator()

        # Analyze
        analyze_btn = QPushButton("Analyze (F5)")
        analyze_btn.setStyleSheet("background-color: #0E639C; font-weight: bold;")
        analyze_btn.clicked.connect(self.analyze_code)
        toolbar.addWidget(analyze_btn)

        # Clear
        clear_btn = QPushButton("Clear Output")
        clear_btn.clicked.connect(self.output_panel.clear_all)
        toolbar.addWidget(clear_btn)

    def create_statusbar(self):
        """Create status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Position label
        self.position_label = QLabel("Line: 1, Column: 1")
        self.statusbar.addPermanentWidget(self.position_label)

        # Update position on cursor change
        self.code_editor.cursorPositionChanged.connect(self.update_cursor_position)

        self.statusbar.showMessage("Ready")

    def set_dark_theme(self):
        """Apply dark theme to the application."""
        dark_stylesheet = """
        QMainWindow {
            background-color: #1E1E1E;
            color: #D4D4D4;
        }
        QMenuBar {
            background-color: #2D2D30;
            color: #D4D4D4;
        }
        QMenuBar::item:selected {
            background-color: #3E3E42;
        }
        QMenu {
            background-color: #252526;
            color: #D4D4D4;
        }
        QMenu::item:selected {
            background-color: #094771;
        }
        QToolBar {
            background-color: #2D2D30;
            border: none;
            spacing: 5px;
            padding: 5px;
        }
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
        QStatusBar {
            background-color: #007ACC;
            color: white;
        }
        QTabWidget::pane {
            border: 1px solid #3E3E42;
            background-color: #1E1E1E;
        }
        QTabBar::tab {
            background-color: #2D2D30;
            color: #D4D4D4;
            padding: 8px 16px;
            border: none;
        }
        QTabBar::tab:selected {
            background-color: #1E1E1E;
        }
        QTabBar::tab:hover {
            background-color: #3E3E42;
        }
        """
        self.setStyleSheet(dark_stylesheet)

    def load_sample_code(self):
        """Load sample Go code."""
        sample = '''package main

import "fmt"

// This is a sample Go program
func main() {
      var x int = 42
      y := 3.14
      message := "Hello, Go Analyzer!"

      if x > 10 {
          fmt.Println(message)
      }

      for i := 0; i < 10; i++ {
          fmt.Printf("%d ", i)
      }
}

func add(a int, b int) int {
    return a + b
}

type Person struct {
    Name string
    Age  int
}
'''
        self.code_editor.setPlainText(sample)
        self.is_modified = False

    def new_file(self):
        """Create a new file."""
        if self.check_save_changes():
            self.code_editor.clear()
            self.current_file = None
            self.is_modified = False
            self.setWindowTitle("Go Analyzer - Untitled")
            self.output_panel.clear_all()
            self.statusbar.showMessage("New file created")

    def open_file(self):
        """Open a file."""
        if not self.check_save_changes():
            return

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Go File",
            "",
            "Go Files (*.go);;All Files (*)"
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()

                self.code_editor.setPlainText(content)
                self.current_file = filename
                self.is_modified = False
                self.setWindowTitle(f"Go Analyzer - {filename}")
                self.output_panel.clear_all()
                self.statusbar.showMessage(f"Opened {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{str(e)}")

    def save_file(self):
        """Save the current file."""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save file with a new name."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Go File",
            "",
            "Go Files (*.go);;All Files (*)"
        )

        if filename:
            self.save_to_file(filename)

    def save_to_file(self, filename):
        """Save content to file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.code_editor.toPlainText())

            self.current_file = filename
            self.is_modified = False
            self.setWindowTitle(f"Go Analyzer - {filename}")
            self.statusbar.showMessage(f"Saved {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")

    def analyze_code(self):
        """Analyze the current code."""
        code = self.code_editor.toPlainText()

        if not code.strip():
            QMessageBox.warning(self, "Warning", "Please enter some code to analyze")
            return

        self.statusbar.showMessage("Analyzing code...")
        self.output_panel.clear_all()
        self.output_panel.log("Starting analysis...")

        # Run analysis in thread
        self.analysis_thread = AnalysisThread(code)
        self.analysis_thread.finished.connect(self.on_analysis_complete)
        self.analysis_thread.start()

    def on_analysis_complete(self, result):
        """Handle analysis completion."""
        if 'error' in result:
            self.output_panel.log_error(f"Analysis failed: {result['error']}")
            self.statusbar.showMessage("Analysis failed")
            return

        # Display results
        self.output_panel.display_tokens(result['tokens'])
        if result['raw_report']:
            self.output_panel.ast_text.setPlainText(result['raw_report'])
            self.output_panel.log("AST report generated.")
        
        self.output_panel.display_symbol_table(result['symbols'])
        self.output_panel.display_errors(
            result['lexical_errors'],
            result['syntax_errors'],
            result['semantic_errors'],
            result['warnings']
        )

        # Update status
        total_errors = len(result['lexical_errors']) + len(result['syntax_errors']) + len(result['semantic_errors'])
        total_warnings = len(result['warnings'])

        if total_errors == 0 and total_warnings == 0:
            self.statusbar.showMessage("Analysis complete - No issues found")
            self.output_panel.log("Analysis complete - No issues found!")
        else:
            self.statusbar.showMessage(f"Analysis complete - {total_errors} errors, {total_warnings} warnings")

    def goto_error_line(self, line_number):
        """Navigate to a specific line."""
        self.code_editor.goto_line(line_number)
        self.code_editor.setFocus()

    def update_cursor_position(self):
        """Update cursor position in status bar."""
        line = self.code_editor.get_current_line()
        column = self.code_editor.get_current_column()
        self.position_label.setText(f"Line: {line}, Column: {column}")

    def on_text_changed(self):
        """Handle text changes."""
        if not self.is_modified:
            self.is_modified = True
            title = self.windowTitle()
            if not title.endswith('*'):
                self.setWindowTitle(title + ' *')

    def check_save_changes(self):
        """Check if there are unsaved changes."""
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )

            if reply == QMessageBox.Save:
                self.save_file()
                return True
            elif reply == QMessageBox.Discard:
                return True
            else:
                return False

        return True

    def closeEvent(self, event):
        """Handle window close event."""
        if self.check_save_changes():
            event.accept()
        else:
            event.ignore()

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Go Analyzer",
            "<h2>Go Analyzer</h2>"
            "<p>A comprehensive lexical, syntax, and semantic analyzer for the Go programming language.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Lexical analysis (tokenization)</li>"
            "<li>Syntax analysis (AST generation)</li>"
            "<li>Semantic analysis (type checking, symbol resolution)</li>"
            "<li>Syntax highlighting</li>"
            "<li>Error detection and reporting</li>"
            "</ul>"
            "<p><b>Built with:</b> Python, PySide6, PLY</p>"
            "<p>Version 1.0</p>"
        )
