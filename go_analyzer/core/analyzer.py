"""
Unified Analyzer Module for Go Source Code Analysis

This module provides a single entry point for performing complete lexical,
syntactic, and semantic analysis on Go source code. It orchestrates calls
to both the lexer and parser GUI functions.
"""

from .lexer.go_lexer import run_lexer_gui
from .parser.go_parser import run_parser_gui


def analyze_code(source_code: str) -> dict:
    """
    Perform complete analysis on Go source code.

    This function orchestrates both lexical and syntactic/semantic analysis,
    providing a unified interface for GUI applications.

    Args:
        source_code: Go source code as a string

    Returns:
        Dictionary containing analysis results with the following structure:
        {
            "status": str,              # "success" or "error"
            "lexical_analysis": str,    # Formatted lexical analysis output
            "parser_analysis": str,     # Formatted parser analysis output
            "error_message": str|None   # Error message if analysis failed
        }

    Example:
        >>> result = analyze_code('package main\\nvar x int')
        >>> print(result["status"])
        success
        >>> print(result["lexical_analysis"])
        PACKAGE(package) at line 1
        IDENTIFIER(main) at line 1
        ...
    """
    result = {
        "status": "success",
        "lexical_analysis": "",
        "parser_analysis": "",
        "error_message": None,
    }

    try:
        # Perform lexical analysis
        try:
            lexical_output = run_lexer_gui(source_code)
            result["lexical_analysis"] = lexical_output
        except Exception as lexer_error:
            result["lexical_analysis"] = (
                f"Lexical Analysis Failed\n"
                f"{'=' * 70}\n"
                f"Error: {str(lexer_error)}\n"
                f"{'=' * 70}"
            )
            # Continue to parser even if lexer fails (for robustness)

        # Perform syntax and semantic analysis
        try:
            parser_output = run_parser_gui(source_code)
            result["parser_analysis"] = parser_output
        except Exception as parser_error:
            result["parser_analysis"] = (
                f"Parser Analysis Failed\n"
                f"{'=' * 70}\n"
                f"Error: {str(parser_error)}\n"
                f"{'=' * 70}"
            )

        # Check if there were any errors
        if (
            "Error" in result["lexical_analysis"]
            or "Error" in result["parser_analysis"]
        ):
            # Don't mark as error status unless analysis completely failed
            # This allows partial results to be displayed
            pass

        return result

    except Exception as e:
        # Catastrophic failure
        result["status"] = "error"
        result["error_message"] = f"Critical error during analysis: {str(e)}"
        return result


def analyze_code_detailed(source_code: str) -> dict:
    """
    Perform complete analysis with structured error extraction.

    This function provides more structured output than analyze_code(),
    extracting specific error counts and types for easier processing.

    Args:
        source_code: Go source code as a string

    Returns:
        Dictionary containing detailed analysis results:
        {
            "status": str,              # "success" or "error"
            "lexical_analysis": {
                "output": str,          # Full formatted output
                "has_errors": bool,     # True if lexical errors found
            },
            "syntax_analysis": {
                "output": str,          # Full formatted output
                "has_syntax_errors": bool,
                "has_semantic_errors": bool,
            },
            "summary": {
                "total_errors": int,    # Total error count
                "error_types": list,    # Types of errors found
            },
            "error_message": str|None
        }

    Example:
        >>> result = analyze_code_detailed('package main\\nconst X = 1\\nX = 2')
        >>> print(result["summary"]["total_errors"])
        1
        >>> print(result["summary"]["error_types"])
        ['semantic']
    """
    result = {
        "status": "success",
        "lexical_analysis": {
            "output": "",
            "has_errors": False,
        },
        "syntax_analysis": {
            "output": "",
            "has_syntax_errors": False,
            "has_semantic_errors": False,
        },
        "summary": {
            "total_errors": 0,
            "error_types": [],
        },
        "error_message": None,
    }

    try:
        # Lexical analysis
        try:
            lexical_output = run_lexer_gui(source_code)
            result["lexical_analysis"]["output"] = lexical_output

            # Check for lexical errors
            if "Lexical errors detected:" in lexical_output:
                result["lexical_analysis"]["has_errors"] = True
                result["summary"]["error_types"].append("lexical")

        except Exception as lexer_error:
            result["lexical_analysis"]["output"] = (
                f"Lexical Analysis Failed: {str(lexer_error)}"
            )
            result["lexical_analysis"]["has_errors"] = True
            result["summary"]["error_types"].append("lexical")

        # Parser analysis
        try:
            parser_output = run_parser_gui(source_code)
            result["syntax_analysis"]["output"] = parser_output

            # Extract error information from parser output
            if "✗ Syntax Errors Found:" in parser_output:
                result["syntax_analysis"]["has_syntax_errors"] = True
                result["summary"]["error_types"].append("syntax")

                # Try to extract error count
                for line in parser_output.split("\n"):
                    if "Total Syntax Errors:" in line:
                        try:
                            count = int(line.split(":")[-1].strip())
                            result["summary"]["total_errors"] += count
                        except:
                            pass

            if "✗ Semantic Errors Found:" in parser_output:
                result["syntax_analysis"]["has_semantic_errors"] = True
                if "semantic" not in result["summary"]["error_types"]:
                    result["summary"]["error_types"].append("semantic")

                # Try to extract error count
                for line in parser_output.split("\n"):
                    if "Total Semantic Errors:" in line:
                        try:
                            count = int(line.split(":")[-1].strip())
                            result["summary"]["total_errors"] += count
                        except:
                            pass

        except Exception as parser_error:
            result["syntax_analysis"]["output"] = (
                f"Parser Analysis Failed: {str(parser_error)}"
            )
            result["syntax_analysis"]["has_syntax_errors"] = True
            result["summary"]["error_types"].append("syntax")

        return result

    except Exception as e:
        result["status"] = "error"
        result["error_message"] = f"Critical error during analysis: {str(e)}"
        return result
