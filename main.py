#!/usr/bin/env python3
"""
termExplain - AI-powered CLI error explainer using Gemini

A command-line tool that explains terminal errors using Google's Gemini AI.
"""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.prompt import Prompt
import os

from gemini_client import GeminiClient
from prompt_builder import PromptBuilder
from utils.formatter import OutputFormatter
from utils.cache import ErrorCache

console = Console()

@click.command()
@click.argument('error_text', required=False)
@click.option('--save', is_flag=True, help='Cache the explanation for future use')
@click.option('--pretty', is_flag=True, default=True, help='Format output with colors and styling')
@click.option('--no-cache', is_flag=True, help='Skip cache and always fetch fresh explanation')
@click.option('--api-key', envvar='GEMINI_API_KEY', help='Gemini API key (or set GEMINI_API_KEY env var)')
@click.version_option(version='1.0.0', prog_name='termExplain')
def main(error_text, save, pretty, no_cache, api_key):
    """
    Explain terminal errors using AI.
    
    You can provide the error text as an argument or pipe it via stdin.
    
    Examples:
        termExplain "ModuleNotFoundError: No module named 'requests'"
        cat error.log | termExplain
        termExplain --save "Permission denied"
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
    
    # Get error text from argument or stdin
    if error_text:
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