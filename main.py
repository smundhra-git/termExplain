#!/usr/bin/env python3
"""
termExplain - AI-powered CLI error explainer using Gemini

A command-line tool that explains terminal errors using Google's Gemini AI.
"""

import sys
import click
import subprocess
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.prompt import Prompt

from gemini_client import GeminiClient
from prompt_builder import PromptBuilder
from utils.formatter import OutputFormatter
from utils.cache import ErrorCache

console = Console()

def run_file_and_catch_errors(file_path):
    """
    Run a Python or JavaScript file and return any error output.
    
    Args:
        file_path: Path to the file to run
        
    Returns:
        tuple: (success: bool, output: str, error: str)
    """
    if not os.path.exists(file_path):
        return False, "", f"File not found: {file_path}"
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.py':
            # Run Python file
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
        elif file_ext in ['.js', '.mjs']:
            # Run JavaScript file
            result = subprocess.run(
                ['node', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            return False, "", f"Unsupported file type: {file_ext}. Only .py, .js, and .mjs files are supported."
        
        success = result.returncode == 0
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "", "Execution timed out after 30 seconds"
    except FileNotFoundError as e:
        if file_ext == '.py':
            return False, "", "Python interpreter not found"
        elif file_ext in ['.js', '.mjs']:
            return False, "", "Node.js not found. Please install Node.js to run JavaScript files"
        else:
            return False, "", str(e)
    except Exception as e:
        return False, "", f"Error running file: {e}"

@click.command()
@click.argument('error_text', required=False)
@click.option('--save', is_flag=True, help='Cache the explanation for future use')
@click.option('--pretty', is_flag=True, default=True, help='Format output with colors and styling')
@click.option('--no-cache', is_flag=True, help='Skip cache and always fetch fresh explanation')
@click.option('--api-key', envvar='GEMINI_API_KEY', help='Gemini API key (or set GEMINI_API_KEY env var)')
@click.option('--file', 'file_path', help='Run a Python or JavaScript file and explain any errors')
@click.version_option(version='1.0.0', prog_name='termExplain')
def main(error_text, save, pretty, no_cache, api_key, file_path):
    """
    Explain terminal errors using AI.
    
    You can provide the error text as an argument, pipe it via stdin, or run a file with --file.
    
    Examples:
        termExplain "ModuleNotFoundError: No module named 'requests'"
        cat error.log | termExplain
        termExplain --save "Permission denied"
        termExplain --file my_script.py
        termExplain --file app.js
    """
    
    # Initialize components
    try:
        gemini_client = GeminiClient(api_key)
        prompt_builder = PromptBuilder()
        formatter = OutputFormatter(pretty)
        cache = ErrorCache()
    except Exception as e:
        console.print(f"[red]Error initializing components: {e}[/red]")
        sys.exit(1)
    
    # Handle --file option
    if file_path:
        console.print(f"[blue]🚀 Running file: {file_path}[/blue]")
        success, stdout, stderr = run_file_and_catch_errors(file_path)
        
        if success:
            console.print("[green]✅ File executed successfully![/green]")
            if stdout.strip():
                console.print("[blue]Output:[/blue]")
                console.print(stdout)
            return
        else:
            # File failed - explain the error
            error_input = stderr.strip() if stderr.strip() else stdout.strip()
            if not error_input:
                error_input = "Unknown error occurred while running the file"
            
            console.print(f"[red]❌ File execution failed[/red]")
            console.print(f"[yellow]Error: {error_input}[/yellow]")
    
    # Get error text from argument or stdin (if not using --file)
    elif error_text:
        error_input = error_text
    elif not sys.stdin.isatty():
        # Read from stdin if piped
        error_input = sys.stdin.read().strip()
    else:
        # Interactive mode
        console.print("[yellow]No error text provided. Enter your error below:[/yellow]")
        error_input = Prompt.ask("Error text")
    
    if not error_input:
        console.print("[red]No error text provided. Use --help for usage information.[/red]")
        sys.exit(1)
    
    # Check cache first (unless --no-cache is specified)
    if not no_cache:
        cached_explanation = cache.get(error_input)
        if cached_explanation:
            console.print("[green]Found cached explanation:[/green]")
            formatter.display_explanation(cached_explanation)
            return
    
    # Get explanation from Gemini
    try:
        console.print("[blue]🤖 Analyzing error[/blue]")
        
        prompt = prompt_builder.build_prompt(error_input)
        explanation = gemini_client.get_explanation(prompt)
        
        # Display the explanation
        formatter.display_explanation(explanation)
        
        # Cache if requested
        if save:
            cache.save(error_input, explanation)
            console.print("[green]✅ Explanation saved to cache[/green]")
            
    except Exception as e:
        console.print(f"[red]❌ Error getting explanation: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main()