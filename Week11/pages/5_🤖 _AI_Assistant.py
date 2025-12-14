import streamlit as st
from typing import List, Dict, Optional

class AIAssistant:
    """Wrapper around OpenAI ChatGPT API for multi-domain queries."""
    
    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        """Initialize the AI assistant with OpenAI API.
        
        Args:
            system_prompt: System prompt for the AI model
        """
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
        
        # Get API key from Streamlit secrets
        try:
            self._api_key = st.secrets["openai_api_key"]
        except KeyError:
            st.error("OpenAI API key not found in secrets.toml")
            self._api_key = None
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt.
        
        Args:
            prompt: New system prompt
        """
        self._system_prompt = prompt
    
    def send_message(self, user_message: str, domain: Optional[str] = None) -> str:
        """Send a message to OpenAI API and get a response.
        
        Args:
            user_message: Message from the user
            domain: Optional domain context (cybersecurity, data_science, etc.)
        
        Returns:
            AI response string
        """
        if self._api_key is None:
            return "Error: API key not configured"
        
        try:
            import openai
            
            # Set API key
            openai.api_key = self._api_key
            
            # Add user message to history
            self._history.append({
                "role": "user",
                "content": user_message
            })
            
            # Create messages with system prompt
            messages = [
                {"role": "system", "content": self._system_prompt}
            ] + self._history
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response text
            response_text = response.choices[0].message["content"]
            
            # Add assistant response to history
            self._history.append({
                "role": "assistant",
                "content": response_text
            })
            
            return response_text
            
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._history.clear()
    
    def get_context_window(self, max_messages: int = 10) -> List[Dict[str, str]]:
        """Get the most recent messages (context window).
        
        Args:
            max_messages: Maximum number of recent messages to return
        
        Returns:
            List of recent message dictionaries
        """
        return self._history[-max_messages:]