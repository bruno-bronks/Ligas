"""
Football Intelligence Dashboard - LLM Client
Abstraction layer for OpenAI and Google Gemini LLM providers.
Uses Strategy Pattern for provider switching.
"""

from abc import ABC, abstractmethod
from typing import Optional

from loguru import logger

from app.core.config import get_settings

settings = get_settings()


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response from the LLM."""
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model name being used."""
        ...


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4096,
                temperature=0.7,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return f"Error generating analysis: {e}"

    def get_model_name(self) -> str:
        return self.model


class GeminiProvider(LLMProvider):
    """Google Gemini provider."""

    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-pro"
        self.model = genai.GenerativeModel(self.model_name)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            response = await self.model.generate_content_async(
                full_prompt,
                generation_config={
                    "max_output_tokens": 4096,
                    "temperature": 0.7,
                },
            )
            return response.text or ""
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return f"Error generating analysis: {e}"

    def get_model_name(self) -> str:
        return self.model_name


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for local development without API keys."""

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        logger.info("Generating mock AI analysis (no API keys configured)")
        return (
            "### 🏟️ Tactical Preview & Analysis\n\n"
            "This match features a classic confrontation of tactical styles. The home side is expected to deploy "
            "a high-pressing 4-3-3 formation, utilizing wing-backs to overload the wide areas and deliver early crosses. "
            "The away side will likely counter with a compact 4-2-3-1, relying on low defensive blocks and quick transitions "
            "through their central midfielders.\n\n"
            "### 🔑 Key Factors & Matchups\n\n"
            "- **Midfield Battle**: Control of the half-spaces will be critical. The matchup between the home team's defensive anchor "
            "and the away team's creative playmaker will decide the rhythm of the game.\n"
            "- **Set Pieces**: The home side has scored 35% of their goals from set pieces, which could exploit the away team's "
            "recent vulnerability in defending aerial duels.\n\n"
            "### 🎯 Predicted Outcome & Rationale\n\n"
            "Given the tactical shapes and recent home/away performances, the home team holds a clear structural advantage. "
            "We expect the home team to control possession (approx. 58%) and gradually break down the opposition's defensive lines.\n\n"
            "**Predicted Score**: 2 - 1\n"
            "**Confidence Level**: High"
        )

    def get_model_name(self) -> str:
        return "local-mock-model"


def get_llm_provider() -> LLMProvider:
    """Factory function to get the configured LLM provider."""
    provider = settings.LLM_PROVIDER.lower()
    if provider == "openai" and settings.OPENAI_API_KEY:
        logger.info("Using OpenAI provider")
        return OpenAIProvider()
    elif provider == "gemini" and settings.GEMINI_API_KEY:
        logger.info("Using Gemini provider")
        return GeminiProvider()
    else:
        logger.warning(f"No valid LLM API keys configured. Using MockLLMProvider for local development.")
        return MockLLMProvider()
