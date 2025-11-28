"""
File operations handler for Go Analyzer GUI.

Provides functionality for loading Go files into the editor and saving
analysis results to text files.
"""

import os
from pathlib import Path
from tkinter import filedialog, messagebox
from ..config import GO_FILE_TYPES, TEXT_FILE_TYPES, DEFAULT_GO_EXTENSION, DEFAULT_TEXT_EXTENSION


class FileHandler:
    """Handles file loading and saving operations for the GUI."""

    def __init__(self, code_editor, results_panel, control_panel, state_manager=None):
        """
        Initialize the file handler.

        Args:
            code_editor: Code editor component instance
            results_panel: Results panel component instance
            control_panel: Control panel component instance
            state_manager (optional): Application state manager instance
        """
        self.code_editor = code_editor
        self.results_panel = results_panel
        self.control_panel = control_panel
        self.state_manager = state_manager

        # Track current file path
        self._current_file_path = None

        # Get path to examples directory
        self._examples_dir = self._get_examples_directory()

    def _get_examples_directory(self):
        """
        Get the path to the examples directory.

        Returns:
            str: Path to examples directory, or current directory if not found
        """
        try:
            # Get the directory where this file is located
            current_file = Path(__file__).resolve()

            # Navigate to gui/resources/examples/
            gui_dir = current_file.parent.parent  # Go up to gui/
            examples_dir = gui_dir / "resources" / "examples"

            # Check if directory exists
            if examples_dir.exists() and examples_dir.is_dir():
                return str(examples_dir)
        except:
            pass

        # Fallback to current directory
        return os.getcwd()

    def load_file(self):
        """
        Open a file dialog and load a Go file into the editor.

        Returns:
            bool: True if file was loaded successfully, False otherwise
        """
        try:
            # Determine initial directory
            # If we have a current file, use its directory
            # Otherwise, use the examples directory
            if self._current_file_path:
                initial_dir = os.path.dirname(self._current_file_path)
            else:
                initial_dir = self._examples_dir

            # Open file dialog
            file_path = filedialog.askopenfilename(
                title="Load Go File",
                filetypes=GO_FILE_TYPES,
                defaultextension=DEFAULT_GO_EXTENSION,
                initialdir=initial_dir
            )

            # Check if user cancelled
            if not file_path:
                return False

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Load content into editor
            self.code_editor.set_code(content)

            # Update current file path
            self._current_file_path = file_path

            # Update state manager if available
            if self.state_manager:
                self.state_manager.set_current_file(file_path)

            # Update status
            filename = os.path.basename(file_path)
            self.control_panel.set_status(f"Loaded: {filename}", "success")

            return True

        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found",
                f"The file '{file_path}' was not found."
            )
            return False

        except PermissionError:
            messagebox.showerror(
                "Permission Denied",
                f"Permission denied to read '{file_path}'."
            )
            return False

        except UnicodeDecodeError:
            messagebox.showerror(
                "Encoding Error",
                "The file could not be read. It may not be a valid text file."
            )
            return False

        except Exception as e:
            messagebox.showerror(
                "Error Loading File",
                f"An error occurred while loading the file:\n{str(e)}"
            )
            return False

    def save_code(self):
        """
        Save the current code in the editor to a file.

        Returns:
            bool: True if file was saved successfully, False otherwise
        """
        try:
            # If we have a current file, save to it
            if self._current_file_path:
                file_path = self._current_file_path
            else:
                # Otherwise, show save dialog
                file_path = filedialog.asksaveasfilename(
                    title="Save Go File",
                    filetypes=GO_FILE_TYPES,
                    defaultextension=DEFAULT_GO_EXTENSION
                )

            # Check if user cancelled
            if not file_path:
                return False

            # Get code from editor
            code = self.code_editor.get_code()

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code)

            # Update current file path
            self._current_file_path = file_path

            # Update state manager if available
            if self.state_manager:
                self.state_manager.set_current_file(file_path)

            # Update status
            filename = os.path.basename(file_path)
            self.control_panel.set_status(f"Saved: {filename}", "success")

            return True

        except PermissionError:
            messagebox.showerror(
                "Permission Denied",
                f"Permission denied to write to '{file_path}'."
            )
            return False

        except Exception as e:
            messagebox.showerror(
                "Error Saving File",
                f"An error occurred while saving the file:\n{str(e)}"
            )
            return False

    def save_code_as(self):
        """
        Save the current code to a new file (always show save dialog).

        Returns:
            bool: True if file was saved successfully, False otherwise
        """
        try:
            # Show save dialog
            file_path = filedialog.asksaveasfilename(
                title="Save Go File As",
                filetypes=GO_FILE_TYPES,
                defaultextension=DEFAULT_GO_EXTENSION
            )

            # Check if user cancelled
            if not file_path:
                return False

            # Get code from editor
            code = self.code_editor.get_code()

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code)

            # Update current file path
            self._current_file_path = file_path

            # Update state manager if available
            if self.state_manager:
                self.state_manager.set_current_file(file_path)

            # Update status
            filename = os.path.basename(file_path)
            self.control_panel.set_status(f"Saved as: {filename}", "success")

            return True

        except PermissionError:
            messagebox.showerror(
                "Permission Denied",
                f"Permission denied to write to '{file_path}'."
            )
            return False

        except Exception as e:
            messagebox.showerror(
                "Error Saving File",
                f"An error occurred while saving the file:\n{str(e)}"
            )
            return False

    def save_results(self):
        """
        Save the analysis results to a text file.

        Returns:
            bool: True if results were saved successfully, False otherwise
        """
        try:
            # Show save dialog
            file_path = filedialog.asksaveasfilename(
                title="Save Analysis Results",
                filetypes=TEXT_FILE_TYPES,
                defaultextension=DEFAULT_TEXT_EXTENSION,
                initialfile="analysis_results.txt"
            )

            # Check if user cancelled
            if not file_path:
                return False

            # Get results text
            results_text = self.results_panel.get_text()

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(results_text)

            # Update status
            filename = os.path.basename(file_path)
            self.control_panel.set_status(f"Results saved: {filename}", "success")

            # Show success message
            messagebox.showinfo(
                "Results Saved",
                f"Analysis results saved to:\n{file_path}"
            )

            return True

        except PermissionError:
            messagebox.showerror(
                "Permission Denied",
                f"Permission denied to write to '{file_path}'."
            )
            return False

        except Exception as e:
            messagebox.showerror(
                "Error Saving Results",
                f"An error occurred while saving results:\n{str(e)}"
            )
            return False

    def get_current_file_path(self):
        """
        Get the current file path.

        Returns:
            str or None: Current file path, or None if no file is loaded
        """
        return self._current_file_path

    def has_unsaved_changes(self):
        """
        Check if there are unsaved changes (placeholder for future implementation).

        Returns:
            bool: Always returns False for now
        """
        # TODO: Implement change tracking if needed
        return False
