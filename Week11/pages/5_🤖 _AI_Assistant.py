import streamlit as st
from typing import List, Dict, Optional
import os
from openai import OpenAI

class AIAssistant:
    """Wrapper around OpenAI Chat API for multi-domain queries."""

    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []

        self._api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

        if not self._api_key:
            st.error("OpenAI API key not found. Add OPENAI_API_KEY in .streamlit/secrets.toml")
            self._client = None
        else:
            self._client = OpenAI(api_key=self._api_key)

    def set_system_prompt(self, prompt: str) -> None:
        self._system_prompt = prompt

    def send_message(self, user_message: str, domain: Optional[str] = None) -> str:
        if self._client is None:
            return "Error: API key not configured"

        try:
            # Simple domain hint (optional)
            if domain:
                user_message = f"[{domain}] {user_message}"

            self._history.append({"role": "user", "content": user_message})

            messages = [{"role": "system", "content": self._system_prompt}] + self._history

            response = self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            response_text = response.choices[0].message.content

            self._history.append({"role": "assistant", "content": response_text})
            return response_text

        except Exception as e:
            # ✅ Remove last user message so history doesn’t break
            if self._history and self._history[-1]["role"] == "user":
                self._history.pop()
            return f"Error calling OpenAI API: {str(e)}"

    def get_history(self) -> List[Dict[str, str]]:
        return self._history.copy()

    def clear_history(self) -> None:
        self._history.clear()

    def get_context_window(self, max_messages: int = 10) -> List[Dict[str, str]]:
        return self._history[-max_messages:]
