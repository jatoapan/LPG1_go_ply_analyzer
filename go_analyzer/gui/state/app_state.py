"""
Application state management for Go Analyzer GUI.

Tracks current file, analysis history, and user preferences with
optional state persistence between sessions.
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any


class AppState:
    """Manages application state and preferences."""

    def __init__(self, config_dir=None):
        """
        Initialize the application state manager.

        Args:
            config_dir (str, optional): Directory for storing config files.
                                       Defaults to ~/.go_analyzer
        """
        # Set config directory
        if config_dir is None:
            home_dir = os.path.expanduser("~")
            self.config_dir = os.path.join(home_dir, ".go_analyzer")
        else:
            self.config_dir = config_dir

        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)

        # State file path
        self.state_file = os.path.join(self.config_dir, "state.json")

        # Current state
        self._current_file = None
        self._analysis_history = []
        self._preferences = {
            "theme": "dark",
            "font_size": 11,
            "auto_save": False,
            "show_line_numbers": False
        }

        # Load saved state
        self._load_state()

    def set_current_file(self, file_path: Optional[str]):
        """
        Set the current file path.

        Args:
            file_path (str or None): Path to the current file
        """
        self._current_file = file_path

    def get_current_file(self) -> Optional[str]:
        """
        Get the current file path.

        Returns:
            str or None: Current file path, or None if no file is set
        """
        return self._current_file

    def add_to_history(self, file_path: str, result: Dict[str, Any]):
        """
        Add an analysis result to the history.

        Args:
            file_path (str): Path to the analyzed file
            result (dict): Analysis result dictionary
        """
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "success": result.get("success", False),
            "error_count": len(result.get("errors", []))
        }

        self._analysis_history.append(history_entry)

        # Keep only the last 100 entries
        if len(self._analysis_history) > 100:
            self._analysis_history = self._analysis_history[-100:]

    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent analysis history.

        Args:
            limit (int): Maximum number of entries to return (default: 10)

        Returns:
            list: List of history entries
        """
        return self._analysis_history[-limit:]

    def clear_history(self):
        """Clear all analysis history."""
        self._analysis_history = []

    def set_preference(self, key: str, value: Any):
        """
        Set a user preference.

        Args:
            key (str): Preference key
            value: Preference value
        """
        self._preferences[key] = value

    def get_preference(self, key: str, default=None) -> Any:
        """
        Get a user preference.

        Args:
            key (str): Preference key
            default: Default value if preference not found

        Returns:
            The preference value or default
        """
        return self._preferences.get(key, default)

    def get_all_preferences(self) -> Dict[str, Any]:
        """
        Get all user preferences.

        Returns:
            dict: Dictionary of all preferences
        """
        return self._preferences.copy()

    def save_state(self) -> bool:
        """
        Save the current state to disk.

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            state_data = {
                "current_file": self._current_file,
                "analysis_history": self._analysis_history,
                "preferences": self._preferences,
                "last_saved": datetime.now().isoformat()
            }

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving state: {e}")
            return False

    def _load_state(self) -> bool:
        """
        Load saved state from disk.

        Returns:
            bool: True if load was successful, False otherwise
        """
        try:
            if not os.path.exists(self.state_file):
                return False

            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)

            # Restore state
            self._current_file = state_data.get("current_file")
            self._analysis_history = state_data.get("analysis_history", [])

            # Merge preferences (keep new defaults, override with saved values)
            saved_prefs = state_data.get("preferences", {})
            self._preferences.update(saved_prefs)

            return True

        except Exception as e:
            print(f"Error loading state: {e}")
            return False

    def reset(self):
        """Reset state to defaults (does not delete saved state file)."""
        self._current_file = None
        self._analysis_history = []
        self._preferences = {
            "theme": "dark",
            "font_size": 11,
            "auto_save": False,
            "show_line_numbers": False
        }

    def get_recent_files(self, limit: int = 5) -> List[str]:
        """
        Get list of recently analyzed files.

        Args:
            limit (int): Maximum number of files to return (default: 5)

        Returns:
            list: List of file paths, most recent first
        """
        # Extract unique file paths from history, maintaining order
        seen = set()
        recent_files = []

        for entry in reversed(self._analysis_history):
            file_path = entry.get("file_path")
            if file_path and file_path not in seen:
                recent_files.append(file_path)
                seen.add(file_path)

            if len(recent_files) >= limit:
                break

        return recent_files

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about analysis history.

        Returns:
            dict: Dictionary containing various statistics
        """
        if not self._analysis_history:
            return {
                "total_analyses": 0,
                "successful_analyses": 0,
                "failed_analyses": 0,
                "total_errors": 0
            }

        total = len(self._analysis_history)
        successful = sum(1 for entry in self._analysis_history if entry.get("success", False))
        failed = total - successful
        total_errors = sum(entry.get("error_count", 0) for entry in self._analysis_history)

        return {
            "total_analyses": total,
            "successful_analyses": successful,
            "failed_analyses": failed,
            "total_errors": total_errors,
            "average_errors": total_errors / total if total > 0 else 0
        }
