"""
Gemini API Client for termExplain

Handles communication with Google's Gemini AI service to get error explanations.
"""

import os
import google.generativeai as genai
from typing import Optional
import logging

class GeminiClient:
    """Client for interacting with Google's Gemini AI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                "or provide it via --api-key option."
            )
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model (using Gemini Pro 1.5)
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini model: {e}")
        
        # Set up logging - suppress INFO messages
        logging.basicConfig(level=logging.WARNING)
        self.logger = logging.getLogger(__name__)
    
    def get_explanation(self, prompt: str) -> str:
        """
        Get an explanation from Gemini AI.
        
        Args:
            prompt: The formatted prompt to send to Gemini
            
        Returns:
            The AI-generated explanation
            
        Raises:
            Exception: If the API call fails
        """
        try:
            self.logger.info("Sending request to Gemini API")
            
            # Generate content with safety settings
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Lower temperature for more focused responses
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=500,  # Limit response length for shorter answers
                ),
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            )
            
            if response.text:
                self.logger.info("Successfully received response from Gemini")
                return response.text.strip()
            else:
                raise Exception("Empty response from Gemini")
                
        except Exception as e:
            self.logger.error(f"Error calling Gemini API: {e}")
            raise Exception(f"Failed to get explanation from Gemini: {e}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            test_prompt = "Hello, this is a test message. Please respond with 'OK' if you can see this."
            response = self.model.generate_content(test_prompt)
            return response.text is not None
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False 
        
