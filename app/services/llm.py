from __future__ import annotations

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import logging

from app.utils.config import settings

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Base exception for LLM-related errors"""
    pass


class LLMConnectionError(LLMError):
    """Raised when LLM server connection fails"""
    pass


class LLMTimeoutError(LLMError):
    """Raised when LLM request times out"""
    pass


class LLMResponseError(LLMError):
    """Raised when LLM returns invalid response"""
    pass


class LLMClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        timeout: int | None = None,
        temperature: float | None = None,
    ) -> None:
        self.base_url = (base_url or settings.llm_base_url).rstrip("/")
        self.api_key = api_key if api_key is not None else settings.llm_api_key
        self.model = model or settings.llm_model
        self.timeout = timeout or settings.llm_timeout
        self.temperature = temperature if temperature is not None else settings.llm_temperature

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 512,
        temperature: float | None = None,
    ) -> str:
        """
        Generate text using LLM with comprehensive error handling.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system instructions
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text content
            
        Raises:
            LLMConnectionError: If connection to LLM server fails
            LLMTimeoutError: If request times out
            LLMResponseError: If response is invalid
        """
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt provided to LLM")
            return ""

        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": max_tokens,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            logger.info(f"Sending request to LLM: {self.base_url}/chat/completions")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            
        except Timeout as e:
            error_msg = f"LLM request timed out after {self.timeout}s"
            logger.error(error_msg)
            raise LLMTimeoutError(error_msg) from e
            
        except ConnectionError as e:
            error_msg = f"Failed to connect to LLM server at {self.base_url}"
            logger.error(error_msg)
            raise LLMConnectionError(error_msg) from e
            
        except RequestException as e:
            error_msg = f"LLM request failed: {str(e)}"
            logger.error(error_msg)
            raise LLMConnectionError(error_msg) from e

        try:
            data = response.json()
            if "choices" not in data or not data["choices"]:
                raise LLMResponseError("Invalid response structure: missing 'choices'")
                
            content = data["choices"][0]["message"]["content"]
            logger.info(f"Successfully received LLM response ({len(content)} chars)")
            return content.strip()
            
        except (KeyError, IndexError, ValueError) as e:
            error_msg = f"Failed to parse LLM response: {str(e)}"
            logger.error(error_msg)
            raise LLMResponseError(error_msg) from e
