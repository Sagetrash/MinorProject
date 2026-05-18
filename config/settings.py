from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class ModelProvider(str, Enum):
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"

class ModelConfig(BaseModel):
    name: str
    model_id: str
    provider: ModelProvider
    api_key: Optional[str] = None
    is_active: bool = False

class AppConfig(BaseModel):
    active_model_id: Optional[str] = None
    available_models: List[ModelConfig] = []
    working_directory: str = "./calculator"
    max_iterations: int = 20
    system_prompt: str = "You are a helpful AI coding agent.\n\nWhen a user asks a question or makes a request, make a function call plan. You can perform the following operations:\n\n- List files and directories\n- Read a file\n- Write a file\n- run python Files\n\nThe Plan may or may not have multiple function calls\nAll paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons."
