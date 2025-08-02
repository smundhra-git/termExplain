"""
Prompt Builder for termExplain

Builds structured prompts for Gemini AI to explain terminal errors.
"""

import re
from typing import Dict, List, Optional

class PromptBuilder:
    """Builds structured prompts for error explanation."""
    
    def __init__(self):
        """Initialize the prompt builder."""
        # Common error patterns for better context
        self.error_patterns = {
            'python': [
                r'ModuleNotFoundError',
                r'ImportError',
                r'SyntaxError',
                r'NameError',
                r'TypeError',
                r'AttributeError',
                r'FileNotFoundError',
                r'PermissionError',
                r'IndentationError',
                r'ValueError'
            ],
            'bash': [
                r'command not found',
                r'permission denied',
                r'no such file or directory',
                r'syntax error',
                r'cannot execute binary file'
            ],
            'docker': [
                r'image not found',
                r'container not found',
                r'port already in use',
                r'permission denied',
                r'no space left on device'
            ],
            'node': [
                r'Cannot find module',
                r'Unexpected token',
                r'ReferenceError',
                r'TypeError',
                r'ENOENT',
                r'EACCES'
            ]
        }
    
    def build_prompt(self, error_text: str) -> str:
        """
        Build a structured prompt for error explanation.
        
        Args:
            error_text: The error text to explain
            
        Returns:
            Formatted prompt string
        """
        # Detect error type for better context
        error_type = self._detect_error_type(error_text)
        
        # Build the base prompt
        prompt = self._get_base_prompt()
        
        # Add context based on error type
        if error_type:
            prompt += f"\n\nContext: This appears to be a {error_type} error."
        
        # Add the error text
        prompt += f"\n\nError: {error_text}"
        
        return prompt
    
    def _get_base_prompt(self) -> str:
        """Get the base prompt template."""
        return """You are an expert CLI assistant with deep knowledge of programming languages, operating systems, and development tools.

Explain the following terminal error in plain English. Structure your response in 3 parts:

1. **What this error means** - Explain the error in simple terms  (not more than 10 words)
2. **Why it likely occurred** - Common causes and scenarios  (not more than 20 words)
3. **How to fix it** - Step-by-step solutions  

Guidelines:  
- Keep each section short and to the point. Use bullet points for clarity.
- Focus on actionable solutions  
- If relevant, mention specific commands or code changes  
- Use clear, developer-friendly language  
- If the error is ambiguous, suggest common interpretations  

Format your response using markdown-style headers and bullet points where helpful.  
Use clean, readable language for a developer seeing this for the first time.
"""
    
    def _detect_error_type(self, error_text: str) -> Optional[str]:
        """
        Detect the type of error based on patterns.
        
        Args:
            error_text: The error text to analyze
            
        Returns:
            Detected error type or None
        """
        error_text_lower = error_text.lower()
        
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_text_lower, re.IGNORECASE):
                    return error_type
        
        return None
    
    def build_debug_prompt(self, error_text: str, context: Dict = None) -> str:
        """
        Build a more detailed prompt for complex debugging scenarios.
        
        Args:
            error_text: The error text
            context: Additional context (OS, language version, etc.)
            
        Returns:
            Enhanced prompt string
        """
        prompt = self._get_base_prompt()
        
        # Add context information
        if context:
            context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])
            prompt += f"\n\nAdditional Context:\n{context_str}"
        
        prompt += f"\n\nError: {error_text}"
        
        return prompt 