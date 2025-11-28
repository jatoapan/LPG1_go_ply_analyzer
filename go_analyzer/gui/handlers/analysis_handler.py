"""
Analysis handler for Go Analyzer GUI.

Coordinates between the GUI and the analyzer backend, managing the analysis
workflow and formatting results for display.
"""

from ...core.analyzer import analyze_code, analyze_code_detailed


class AnalysisHandler:
    """Handles analysis orchestration between GUI and backend."""

    def __init__(self, code_editor, results_panel, control_panel):
        """
        Initialize the analysis handler.

        Args:
            code_editor: CodeEditor instance for retrieving source code
            results_panel: ResultsPanel instance for displaying results
            control_panel: ControlPanel instance for status updates
        """
        self.code_editor = code_editor
        self.results_panel = results_panel
        self.control_panel = control_panel

    def handle_analysis(self):
        """
        Perform complete analysis on the current code.

        This method orchestrates the entire analysis workflow:
        1. Get code from editor
        2. Validate input
        3. Call analyzer backend
        4. Format results
        5. Display in results panel
        6. Update status
        """
        # Update status to running
        self.control_panel.set_status("Running analysis...", "running")
        self.control_panel.enable_buttons(False)

        try:
            # Get code from editor
            code = self.code_editor.get_code()

            # Validate input
            if not code or not code.strip():
                self.results_panel.display_error(
                    "No code to analyze.\n\n"
                    "Please enter some Go code in the editor before running analysis."
                )
                self.control_panel.set_status("No code provided", "error")
                return

            # Clear previous results
            self.results_panel.clear()

            # Perform analysis using the unified analyzer
            result = analyze_code(code)

            # Format and display results
            self._display_analysis_results(result)

            # Update status based on result
            if result["status"] == "success":
                # Check if there were actual errors in the output (more precise detection)
                lexical_output = result.get("lexical_analysis", "")
                parser_output = result.get("parser_analysis", "")

                has_errors = (
                    "Lexical errors detected:" in lexical_output or
                    "✗ Syntax Errors Found:" in parser_output or
                    "✗ Semantic Errors Found:" in parser_output or
                    "Analysis Failed" in lexical_output or
                    "Analysis Failed" in parser_output
                )

                if has_errors:
                    self.control_panel.set_status("Analysis completed with errors", "error")
                else:
                    self.control_panel.set_status("Analysis completed successfully", "success")
            else:
                self.control_panel.set_status("Analysis failed", "error")

        except Exception as e:
            # Handle unexpected errors
            error_message = (
                f"Unexpected error during analysis:\n\n"
                f"{str(e)}\n\n"
                f"Please check your code and try again."
            )
            self.results_panel.display_error(error_message)
            self.control_panel.set_status("Analysis failed", "error")

        finally:
            # Re-enable buttons
            self.control_panel.enable_buttons(True)

    def _display_analysis_results(self, result):
        """
        Format and display analysis results.

        Args:
            result (dict): Analysis result dictionary from analyzer.analyze_code()
        """
        # Build formatted output
        output_lines = []

        # Header
        output_lines.append("=" * 70)
        output_lines.append("  GO CODE ANALYSIS RESULTS")
        output_lines.append("=" * 70)
        output_lines.append("")

        # Check for critical error
        if result.get("error_message"):
            output_lines.append("CRITICAL ERROR")
            output_lines.append("-" * 70)
            output_lines.append(result["error_message"])
            output_lines.append("")
        else:
            # Lexical Analysis section
            if "lexical_analysis" in result and result["lexical_analysis"]:
                output_lines.append("LEXICAL ANALYSIS")
                output_lines.append("-" * 70)
                output_lines.append(result["lexical_analysis"])
                output_lines.append("")

            # Parser Analysis section
            if "parser_analysis" in result and result["parser_analysis"]:
                output_lines.append("SYNTAX & SEMANTIC ANALYSIS")
                output_lines.append("-" * 70)
                output_lines.append(result["parser_analysis"])
                output_lines.append("")

        # Footer
        output_lines.append("=" * 70)

        # Join and display
        formatted_output = "\n".join(output_lines)
        self.results_panel.clear()

        # Display with appropriate formatting
        self.results_panel.text_widget.config(state="normal")
        self.results_panel.text_widget.delete("1.0", "end")

        # Parse and apply formatting
        self._apply_formatted_text(formatted_output, result)

        self.results_panel.text_widget.config(state="disabled")
        self.results_panel._auto_scroll()

    def _apply_formatted_text(self, text, result):
        """
        Apply color-coded formatting to the results text.

        Args:
            text (str): The formatted text to display
            result (dict): Analysis result for context
        """
        lines = text.split("\n")

        for line in lines:
            # Determine the appropriate tag based on content
            if line.startswith("="):
                # Header separator
                self.results_panel.text_widget.insert("end", line + "\n", "header")
            elif "GO CODE ANALYSIS RESULTS" in line:
                # Main title
                self.results_panel.text_widget.insert("end", line + "\n", "header")
            elif line.startswith("-"):
                # Section separator
                self.results_panel.text_widget.insert("end", line + "\n", "section")
            elif any(keyword in line for keyword in ["LEXICAL ANALYSIS", "SYNTAX & SEMANTIC ANALYSIS", "CRITICAL ERROR"]):
                # Section headers
                self.results_panel.text_widget.insert("end", line + "\n", "section")
            elif "Error" in line or "error" in line.lower():
                # Error lines
                self.results_panel.text_widget.insert("end", line + "\n", "error")
            elif "✓" in line or "Success" in line:
                # Success indicators
                self.results_panel.text_widget.insert("end", line + "\n", "success")
            elif "✗" in line or "Warning" in line:
                # Warning indicators
                self.results_panel.text_widget.insert("end", line + "\n", "warning")
            else:
                # Normal text
                self.results_panel.text_widget.insert("end", line + "\n")

    def handle_detailed_analysis(self):
        """
        Perform detailed analysis with structured error extraction.

        This is an alternative analysis method that provides more
        structured output. Can be used for advanced error reporting.
        """
        self.control_panel.set_status("Running detailed analysis...", "running")
        self.control_panel.enable_buttons(False)

        try:
            code = self.code_editor.get_code()

            if not code or not code.strip():
                self.results_panel.display_error("No code to analyze.")
                self.control_panel.set_status("No code provided", "error")
                return

            # Use detailed analyzer
            result = analyze_code_detailed(code)

            # Format detailed results
            self._display_detailed_results(result)

            # Update status
            total_errors = result.get("summary", {}).get("total_errors", 0)
            if total_errors > 0:
                self.control_panel.set_status(
                    f"Analysis completed with {total_errors} error(s)",
                    "error"
                )
            else:
                self.control_panel.set_status("Analysis completed successfully", "success")

        except Exception as e:
            self.results_panel.display_error(f"Unexpected error: {str(e)}")
            self.control_panel.set_status("Analysis failed", "error")

        finally:
            self.control_panel.enable_buttons(True)

    def _display_detailed_results(self, result):
        """
        Display detailed analysis results with structured formatting.

        Args:
            result (dict): Detailed analysis result from analyze_code_detailed()
        """
        output_lines = []

        # Header
        output_lines.append("=" * 70)
        output_lines.append("  DETAILED GO CODE ANALYSIS")
        output_lines.append("=" * 70)
        output_lines.append("")

        # Lexical Analysis
        lex_result = result.get("lexical_analysis", {})
        output_lines.append("LEXICAL ANALYSIS")
        output_lines.append("-" * 70)
        output_lines.append(lex_result.get("output", "No output"))

        if lex_result.get("has_errors"):
            output_lines.append("\n✗ Lexical errors detected")
        else:
            output_lines.append("\n✓ No lexical errors")
        output_lines.append("")

        # Syntax Analysis
        syntax_result = result.get("syntax_analysis", {})
        output_lines.append("SYNTAX & SEMANTIC ANALYSIS")
        output_lines.append("-" * 70)
        output_lines.append(syntax_result.get("output", "No output"))
        output_lines.append("")

        # Summary
        summary = result.get("summary", {})
        output_lines.append("ANALYSIS SUMMARY")
        output_lines.append("-" * 70)
        output_lines.append(f"Total Errors: {summary.get('total_errors', 0)}")
        output_lines.append(f"Error Types: {', '.join(summary.get('error_types', [])) or 'None'}")
        output_lines.append("")

        output_lines.append("=" * 70)

        # Display
        formatted_output = "\n".join(output_lines)
        self.results_panel.clear()
        self.results_panel.text_widget.config(state="normal")
        self.results_panel.text_widget.delete("1.0", "end")
        self._apply_formatted_text(formatted_output, result)
        self.results_panel.text_widget.config(state="disabled")
        self.results_panel._auto_scroll()
