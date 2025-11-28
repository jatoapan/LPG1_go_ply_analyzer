"""
Event handlers for Go Analyzer GUI.

Contains handler modules for analysis orchestration, error handling,
and file operations.
"""

from .analysis_handler import AnalysisHandler
from .error_handler import ErrorHandler

__all__ = ['AnalysisHandler', 'ErrorHandler']
