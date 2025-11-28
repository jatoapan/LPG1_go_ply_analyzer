"""
Configuration module for Go Analyzer GUI.

Centralizes all GUI constants including colors, fonts, dimensions,
and other configuration settings.
"""


# ============================================================================
# WINDOW CONFIGURATION
# ============================================================================

WINDOW_TITLE = "Go Analyzer - Lexical, Syntax & Semantic Analysis"
WINDOW_SIZE = "1100x600"
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 400


# ============================================================================
# COLOR SCHEME (Dark Theme)
# ============================================================================

# Background colors
BG_DARK = "#1e1e1e"
BG_LIGHT = "#252526"

# Foreground colors
FG_PRIMARY = "#d4d4d4"
FG_SECONDARY = "#cccccc"

# Editor colors
EDITOR_BG = "#1e1e1e"
EDITOR_FG = "#d4d4d4"
EDITOR_INSERT = "#aeafad"
EDITOR_SELECT_BG = "#264f78"
EDITOR_SELECT_FG = "#ffffff"

# Results panel colors
RESULTS_BG = "#1e1e1e"
RESULTS_FG = "#d4d4d4"

# Syntax highlighting / Tag colors
COLOR_HEADER = "#569cd6"      # Bright blue
COLOR_SUCCESS = "#4ec9b0"     # Cyan/green
COLOR_ERROR = "#f48771"       # Red
COLOR_WARNING = "#dcdcaa"     # Yellow
COLOR_INFO = "#4fc1ff"        # Cyan
COLOR_SECTION = "#c586c0"     # Purple
COLOR_EMPHASIS = "#d4d4d4"    # Default foreground


# ============================================================================
# FONTS
# ============================================================================

# Code editor font
EDITOR_FONT_FAMILY = "Courier New"
EDITOR_FONT_SIZE = 11
EDITOR_FONT = (EDITOR_FONT_FAMILY, EDITOR_FONT_SIZE)

# Results panel font
RESULTS_FONT_FAMILY = "Courier New"
RESULTS_FONT_SIZE = 10
RESULTS_FONT = (RESULTS_FONT_FAMILY, RESULTS_FONT_SIZE)
RESULTS_FONT_BOLD = (RESULTS_FONT_FAMILY, RESULTS_FONT_SIZE, "bold")

# UI labels font
LABEL_FONT_FAMILY = "Arial"
LABEL_FONT_SIZE = 10
LABEL_FONT_BOLD = (LABEL_FONT_FAMILY, LABEL_FONT_SIZE, "bold")

# Status label font
STATUS_FONT_FAMILY = "Arial"
STATUS_FONT_SIZE = 9
STATUS_FONT = (STATUS_FONT_FAMILY, STATUS_FONT_SIZE)


# ============================================================================
# WIDGET DIMENSIONS
# ============================================================================

# Button dimensions
BUTTON_WIDTH = 15
BUTTON_PADDING_X = 5
BUTTON_PADDING_Y = 5

# Widget padding
WIDGET_PADDING_X = 10
WIDGET_PADDING_Y = 10

# Text widget padding
TEXT_PADDING_X = 5
TEXT_PADDING_Y = 5

# Results text padding
RESULTS_PADDING_X = 10
RESULTS_PADDING_Y = 10


# ============================================================================
# EDITOR CONFIGURATION
# ============================================================================

# Tab settings
TAB_SIZE = 4  # Number of spaces per tab

# Editor features
EDITOR_UNDO_ENABLED = True
EDITOR_MAX_UNDO = -1  # Unlimited undo


# ============================================================================
# STATUS MESSAGES
# ============================================================================

STATUS_READY = "Ready"
STATUS_ANALYZING = "Analyzing..."
STATUS_SUCCESS = "Analysis completed successfully"
STATUS_ERROR = "Analysis completed with errors"
STATUS_CLEARED = "Results cleared"
STATUS_FILE_LOADED = "File loaded"
STATUS_FILE_SAVED = "Results saved"


# ============================================================================
# WELCOME MESSAGES
# ============================================================================

DEFAULT_WELCOME_MESSAGE = """╔════════════════════════════════════════════════════╗
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


DEFAULT_EDITOR_CONTENT = """// Welcome to Go Analyzer!
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


# ============================================================================
# FILE DIALOG SETTINGS
# ============================================================================

# File type filters
GO_FILE_TYPES = [
    ("Go files", "*.go"),
    ("All files", "*.*")
]

TEXT_FILE_TYPES = [
    ("Text files", "*.txt"),
    ("All files", "*.*")
]

# Default file extensions
DEFAULT_GO_EXTENSION = ".go"
DEFAULT_TEXT_EXTENSION = ".txt"


# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================

SHORTCUT_RUN_ANALYSIS = ["<Control-r>", "<Control-R>"]
SHORTCUT_CLEAR_RESULTS = ["<Control-l>", "<Control-L>"]
SHORTCUT_LOAD_FILE = ["<Control-o>", "<Control-O>"]
SHORTCUT_SAVE_RESULTS = ["<Control-s>", "<Control-S>"]


# ============================================================================
# ANALYSIS CONFIGURATION
# ============================================================================

# Maximum analysis time (milliseconds) before showing warning
MAX_ANALYSIS_TIME = 10000  # 10 seconds

# Whether to show analysis timing in results
SHOW_ANALYSIS_TIMING = True


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_tag_config():
    """
    Get text tag configuration for results panel.

    Returns:
        dict: Dictionary mapping tag names to their configuration
    """
    return {
        "header": {
            "foreground": COLOR_HEADER,
            "font": (RESULTS_FONT_FAMILY, RESULTS_FONT_SIZE + 1, "bold")
        },
        "success": {
            "foreground": COLOR_SUCCESS
        },
        "error": {
            "foreground": COLOR_ERROR
        },
        "warning": {
            "foreground": COLOR_WARNING
        },
        "info": {
            "foreground": COLOR_INFO
        },
        "section": {
            "foreground": COLOR_SECTION,
            "font": RESULTS_FONT_BOLD
        },
        "emphasis": {
            "font": RESULTS_FONT_BOLD
        }
    }


def get_status_color(status_type):
    """
    Get color for status label based on type.

    Args:
        status_type (str): Type of status - "normal", "running", "success", "error"

    Returns:
        str: Hex color code
    """
    color_map = {
        "normal": COLOR_SUCCESS,
        "running": COLOR_WARNING,
        "success": COLOR_SUCCESS,
        "error": COLOR_ERROR
    }
    return color_map.get(status_type, FG_PRIMARY)
