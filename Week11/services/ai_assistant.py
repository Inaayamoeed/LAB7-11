from typing import List, Dict, Optional

class AIAssistant:
    """Wrapper around an AI/chat model for multi-domain queries.
    
    In your real project, connect this to OpenAI, HuggingFace, or another provider.
    """
    
    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        """Initialize the AI assistant.
        
        Args:
            system_prompt: System prompt for the AI model
        """
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt.
        
        Args:
            prompt: New system prompt
        """
        self._system_prompt = prompt
    
    def send_message(self, user_message: str, domain: Optional[str] = None) -> str:
        """Send a message and get a response.
        
        Replace this body with your real API call to OpenAI/HuggingFace/etc.
        
        Args:
            user_message: Message from the user
            domain: Optional domain context (cybersecurity, data_science, etc.)
        
        Returns:
            AI response string
        """
        # Add user message to history
        self._history.append({
            "role": "user",
            "content": user_message
        })
        
        # TODO: Replace with real API call
        # Example for OpenAI:
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "system", "content": self._system_prompt}] + self._history,
        # )
        # response_text = response.choices[0].message["content"]
        
        # Fake response for now:
        if domain:
            response = f"[AI ({domain}) reply to]: {user_message[:50]}..."
        else:
            response = f"[AI reply to]: {user_message[:50]}..."
        
        # Add assistant response to history
        self._history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
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