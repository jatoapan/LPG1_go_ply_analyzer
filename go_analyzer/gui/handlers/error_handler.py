"""
Error handler for Go Analyzer GUI.

Parses, formats, and displays error messages from analyzer output
with user-friendly formatting and visual indicators.
"""

import re
from typing import List, Dict, Tuple


class ErrorHandler:
    """Handles error parsing, formatting, and display."""

    def __init__(self):
        """Initialize the error handler."""
        self.lexical_errors = []
        self.syntax_errors = []
        self.semantic_errors = []

    def parse_errors(self, lexical_output: str, parser_output: str) -> Dict[str, List[str]]:
        """
        Parse errors from analyzer output.

        Args:
            lexical_output: Output from lexical analysis
            parser_output: Output from parser/semantic analysis

        Returns:
            Dictionary with categorized errors:
            {
                'lexical': [...],
                'syntax': [...],
                'semantic': [...]
            }
        """
        errors = {
            'lexical': [],
            'syntax': [],
            'semantic': []
        }

        # Parse lexical errors
        errors['lexical'] = self._parse_lexical_errors(lexical_output)

        # Parse syntax and semantic errors
        syntax_errs, semantic_errs = self._parse_parser_errors(parser_output)
        errors['syntax'] = syntax_errs
        errors['semantic'] = semantic_errs

        # Store for later use
        self.lexical_errors = errors['lexical']
        self.syntax_errors = errors['syntax']
        self.semantic_errors = errors['semantic']

        return errors

    def _parse_lexical_errors(self, output: str) -> List[str]:
        """
        Parse lexical errors from lexer output.

        Args:
            output: Lexical analysis output

        Returns:
            List of lexical error messages
        """
        errors = []

        # Look for error indicators in lexical output
        if "Lexical errors detected:" in output:
            # Extract error section
            lines = output.split('\n')
            in_error_section = False

            for line in lines:
                if "Lexical errors detected:" in line:
                    in_error_section = True
                    continue
                elif in_error_section:
                    # Stop at next section or empty line series
                    if line.startswith("=") or line.startswith("-"):
                        break
                    if line.strip() and not line.startswith(" " * 10):
                        errors.append(line.strip())

        # Alternative: Look for "Error" or "Invalid" in output
        lines = output.split('\n')
        for line in lines:
            if 'error' in line.lower() or 'invalid' in line.lower():
                if line.strip() and line not in errors:
                    errors.append(line.strip())

        return errors

    def _parse_parser_errors(self, output: str) -> Tuple[List[str], List[str]]:
        """
        Parse syntax and semantic errors from parser output.

        Args:
            output: Parser/semantic analysis output

        Returns:
            Tuple of (syntax_errors, semantic_errors)
        """
        syntax_errors = []
        semantic_errors = []

        lines = output.split('\n')
        in_syntax_section = False
        in_semantic_section = False

        for line in lines:
            # Detect sections
            if "Syntax Errors Found:" in line or "✗ Syntax Errors Found:" in line:
                in_syntax_section = True
                in_semantic_section = False
                continue
            elif "Semantic Errors Found:" in line or "✗ Semantic Errors Found:" in line:
                in_semantic_section = True
                in_syntax_section = False
                continue
            elif line.startswith("=") or line.startswith("-" * 10):
                # Section separator - reset flags
                if not ("Error" in line):
                    in_syntax_section = False
                    in_semantic_section = False
                continue

            # Collect errors based on current section
            if in_syntax_section and line.strip():
                if not line.startswith("Total") and not line.startswith("✗"):
                    syntax_errors.append(line.strip())
            elif in_semantic_section and line.strip():
                if not line.startswith("Total") and not line.startswith("✗"):
                    semantic_errors.append(line.strip())

        return syntax_errors, semantic_errors

    def format_error_summary(self) -> str:
        """
        Create a formatted summary of all errors.

        Returns:
            Formatted error summary string
        """
        lines = []

        total_errors = (
            len(self.lexical_errors) +
            len(self.syntax_errors) +
            len(self.semantic_errors)
        )

        if total_errors == 0:
            return "✓ No errors detected - Analysis successful!"

        lines.append("=" * 70)
        lines.append("  ERROR SUMMARY")
        lines.append("=" * 70)
        lines.append(f"Total Errors Found: {total_errors}")
        lines.append("")

        # Lexical errors
        if self.lexical_errors:
            lines.append(f"✗ Lexical Errors ({len(self.lexical_errors)}):")
            lines.append("-" * 70)
            for i, error in enumerate(self.lexical_errors, 1):
                lines.append(f"  {i}. {error}")
            lines.append("")

        # Syntax errors
        if self.syntax_errors:
            lines.append(f"✗ Syntax Errors ({len(self.syntax_errors)}):")
            lines.append("-" * 70)
            for i, error in enumerate(self.syntax_errors, 1):
                lines.append(f"  {i}. {error}")
            lines.append("")

        # Semantic errors
        if self.semantic_errors:
            lines.append(f"✗ Semantic Errors ({len(self.semantic_errors)}):")
            lines.append("-" * 70)
            for i, error in enumerate(self.semantic_errors, 1):
                lines.append(f"  {i}. {error}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def get_error_count(self) -> Dict[str, int]:
        """
        Get error counts by category.

        Returns:
            Dictionary with error counts:
            {
                'lexical': int,
                'syntax': int,
                'semantic': int,
                'total': int
            }
        """
        return {
            'lexical': len(self.lexical_errors),
            'syntax': len(self.syntax_errors),
            'semantic': len(self.semantic_errors),
            'total': len(self.lexical_errors) + len(self.syntax_errors) + len(self.semantic_errors)
        }

    def has_errors(self) -> bool:
        """
        Check if any errors were detected.

        Returns:
            True if any errors exist, False otherwise
        """
        return self.get_error_count()['total'] > 0

    def get_error_types(self) -> List[str]:
        """
        Get list of error types that were found.

        Returns:
            List of error type names (e.g., ['lexical', 'semantic'])
        """
        types = []
        if self.lexical_errors:
            types.append('lexical')
        if self.syntax_errors:
            types.append('syntax')
        if self.semantic_errors:
            types.append('semantic')
        return types

    def format_error_for_display(self, error_type: str, error_message: str) -> str:
        """
        Format a single error message for display.

        Args:
            error_type: Type of error ('lexical', 'syntax', 'semantic')
            error_message: The error message

        Returns:
            Formatted error string with icon
        """
        icons = {
            'lexical': '🔤',
            'syntax': '📝',
            'semantic': '🔍'
        }

        icon = icons.get(error_type, '❌')
        return f"{icon} [{error_type.upper()}] {error_message}"

    def clear_errors(self):
        """Clear all stored errors."""
        self.lexical_errors = []
        self.syntax_errors = []
        self.semantic_errors = []

    @staticmethod
    def extract_line_number(error_message: str) -> int:
        """
        Extract line number from error message.

        Args:
            error_message: Error message that may contain line number

        Returns:
            Line number if found, -1 otherwise
        """
        # Try to match patterns like "line 5", "at line 5", "Line: 5"
        patterns = [
            r'line\s+(\d+)',
            r'at\s+line\s+(\d+)',
            r'Line:\s*(\d+)',
            r'\[Line\s+(\d+)\]',
        ]

        for pattern in patterns:
            match = re.search(pattern, error_message, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return -1

    @staticmethod
    def highlight_error_line(code: str, line_number: int) -> str:
        """
        Highlight a specific line in the code (for display).

        Args:
            code: Source code
            line_number: Line number to highlight (1-indexed)

        Returns:
            Code with the error line highlighted
        """
        lines = code.split('\n')

        if 1 <= line_number <= len(lines):
            # Mark the error line
            lines[line_number - 1] = f">>> {lines[line_number - 1]}  <<<< ERROR HERE"

        return '\n'.join(lines)
