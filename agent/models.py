from abc import ABC, abstractmethod
from typing import List, Any, Optional
from google import genai
from google.genai import types
from config.settings import ModelConfig, ModelProvider

class LLMResponse:
    def __init__(self, text: Optional[str], function_calls: List[Any], usage: Any):
        self.text = text
        self.function_calls = function_calls
        self.usage = usage

class LLMProvider(ABC):
    @abstractmethod
    def generate_content(self, prompt: str, tools: Any, history: List[Any], system_prompt: str = None) -> LLMResponse:
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, config: ModelConfig):
        self.config = config
        self.client = genai.Client(api_key=config.api_key)
        self.model_id = config.model_id

    def generate_content(self, prompt: str, tools: Any, history: List[Any], system_prompt: str = None) -> LLMResponse:
        try:
            # Convert history to Gemini types if necessary
            # For the first call, history is just the user prompt
            contents = history if history else [types.Content(role="user", parts=[types.Part(text=prompt)])]
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[tools]  # tools expects a list of Tool objects
                ),
            )
            
            text = response.text if response.text else None
            function_calls = response.function_calls if response.function_calls else []
            usage = response.usage_metadata
            
            return LLMResponse(text, function_calls, usage)
        except Exception as e:
            # Return a safe error response instead of crashing
            return LLMResponse(
                text=f"API Error: {str(e)}",
                function_calls=[],
                usage=None
            )

    def get_model_info(self) -> dict:
        return {
            "name": self.config.name,
            "id": self.model_id,
            "provider": "Google Gemini"
        }
