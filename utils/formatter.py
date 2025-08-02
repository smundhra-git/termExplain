"""
Output Formatter for termExplain

Handles formatting and display of error explanations with rich terminal output.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.layout import Layout
from rich.columns import Columns
from rich.table import Table
import re
from typing import Optional

class OutputFormatter:
    """Formats and displays error explanations with rich styling."""
    
    def __init__(self, pretty: bool = True):
        """
        Initialize the formatter.
        
        Args:
            pretty: Whether to use rich formatting (default: True)
        """
        self.pretty = pretty
        self.console = Console()
    
    def display_explanation(self, explanation: str):
        """
        Display the explanation with formatting.
        
        Args:
            explanation: The AI-generated explanation
        """
        if self.pretty:
            self._display_pretty(explanation)
        else:
            self._display_plain(explanation)
    
    def _display_pretty(self, explanation: str):
        """Display explanation with rich formatting."""
        # Parse the explanation into sections
        sections = self._parse_explanation(explanation)
        
        # Create a layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=1)
        )
        
        # Header
        header_text = Text("🔍 Error Explanation", style="bold blue")
        layout["header"].update(Panel(header_text, style="blue"))
        
        # Body content
        body_content = []
        
        for section in sections:
            if section['type'] == 'what':
                icon = "❓"
                color = "yellow"
                title = "What this error means"
            elif section['type'] == 'why':
                icon = "🔍"
                color = "cyan"
                title = "Why it likely occurred"
            elif section['type'] == 'how':
                icon = "🛠️"
                color = "green"
                title = "How to fix it"
            else:
                icon = "📝"
                color = "white"
                title = section.get('title', 'Additional Information')
            
            # Format the content
            content = section['content'].strip()
            if content:
                # Highlight code snippets
                content = self._highlight_code_snippets(content)
                
                panel = Panel(
                    Markdown(content),
                    title=f"{icon} {title}",
                    border_style=color,
                    padding=(1, 2)
                )
                body_content.append(panel)
        
        # Display sections in columns for better layout
        if len(body_content) == 3:
            # Three sections - display in a nice layout
            columns = Columns(body_content, equal=True, expand=True)
            layout["body"].update(columns)
        else:
            # Stack vertically - display each panel separately
            for panel in body_content:
                self.console.print(panel)
            return  # Exit early since we're printing panels directly
        
        # Footer
        footer_text = Text("Powered by Gemini AI", style="dim")
        layout["footer"].update(Panel(footer_text, style="dim"))
        
        # Display the layout
        self.console.print(layout)
    
    def _display_plain(self, explanation: str):
        """Display explanation in plain text format."""
        self.console.print("\n" + "="*60)
        self.console.print("ERROR EXPLANATION")
        self.console.print("="*60)
        self.console.print(explanation)
        self.console.print("="*60 + "\n")
    
    def _parse_explanation(self, explanation: str) -> list:
        """
        Parse the explanation into structured sections.
        
        Args:
            explanation: Raw explanation text
            
        Returns:
            List of section dictionaries
        """
        sections = []
        
        # Split by common section markers
        lines = explanation.split('\n')
        current_section = {'type': 'general', 'content': '', 'title': 'Explanation'}
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if re.match(r'^[0-9]+\.\s*[❓🔍🛠️]?\s*\*\*.*\*\*', line):
                # Save previous section
                if current_content:
                    current_section['content'] = '\n'.join(current_content)
                    sections.append(current_section)
                
                # Start new section
                if 'what' in line.lower() or '❓' in line:
                    current_section = {'type': 'what', 'content': '', 'title': 'What this error means'}
                elif 'why' in line.lower() or '🔍' in line:
                    current_section = {'type': 'why', 'content': '', 'title': 'Why it likely occurred'}
                elif 'how' in line.lower() or '🛠️' in line:
                    current_section = {'type': 'how', 'content': '', 'title': 'How to fix it'}
                else:
                    current_section = {'type': 'general', 'content': '', 'title': 'Additional Information'}
                
                current_content = []
            else:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            current_section['content'] = '\n'.join(current_content)
            sections.append(current_section)
        
        # If no sections were detected, treat the whole thing as one section
        if not sections:
            sections = [{'type': 'general', 'content': explanation, 'title': 'Explanation'}]
        
        return sections
    
    def _highlight_code_snippets(self, text: str) -> str:
        """
        Highlight code snippets in the text.
        
        Args:
            text: Text containing potential code snippets
            
        Returns:
            Text with highlighted code snippets
        """
        # Find code snippets (backticks, commands, file paths)
        patterns = [
            (r'`([^`]+)`', r'`\1`'),  # Inline code
            (r'```(\w+)?\n(.*?)\n```', r'```\1\n\2\n```'),  # Code blocks
            (r'(\w+\.py|\w+\.js|\w+\.ts|\w+\.sh|\w+\.md)', r'`\1`'),  # File names
            (r'(pip install|npm install|docker run|git clone|python|node)', r'`\1`'),  # Commands
        ]
        
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE | re.DOTALL)
        
        return text
    
    def display_error(self, error_message: str, error_type: str = "Error"):
        """
        Display an error message with formatting.
        
        Args:
            error_message: The error message
            error_type: Type of error (Error, Warning, etc.)
        """
        if self.pretty:
            error_text = Text(f"❌ {error_type}: {error_message}", style="bold red")
            self.console.print(Panel(error_text, border_style="red"))
        else:
            self.console.print(f"ERROR: {error_message}")
    
    def display_success(self, message: str):
        """
        Display a success message with formatting.
        
        Args:
            message: The success message
        """
        if self.pretty:
            success_text = Text(f"✅ {message}", style="bold green")
            self.console.print(Panel(success_text, border_style="green"))
        else:
            self.console.print(f"SUCCESS: {message}")
    
    def display_info(self, message: str):
        """
        Display an info message with formatting.
        
        Args:
            message: The info message
        """
        if self.pretty:
            info_text = Text(f"ℹ️  {message}", style="bold blue")
            self.console.print(Panel(info_text, border_style="blue"))
        else:
            self.console.print(f"INFO: {message}") 