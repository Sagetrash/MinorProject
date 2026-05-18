from typing import List, Optional
from .settings import AppConfig, ModelConfig, ModelProvider
from .storage import save_config, load_config
import os

class ModelRegistry:
    def __init__(self):
        self.config = load_config() or AppConfig()
        self._initialize_defaults()

    def _initialize_defaults(self):
        # Pre-populate with Gemini model if key exists in env
        if not self.config.available_models:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                default_model = ModelConfig(
                    name="Gemini 2.0 Flash Lite",
                    model_id="gemini-2.0-flash-lite",
                    provider=ModelProvider.GEMINI,
                    api_key=api_key,
                    is_active=True
                )
                self.config.available_models.append(default_model)
                self.config.active_model_id = default_model.model_id
                save_config(self.config)

    def get_available_models(self) -> List[ModelConfig]:
        return self.config.available_models

    def add_model(self, model: ModelConfig) -> bool:
        # Remove existing model with same id
        self.config.available_models = [m for m in self.config.available_models if m.model_id != model.model_id]
        self.config.available_models.append(model)
        save_config(self.config)
        return True

    def remove_model(self, model_id: str) -> bool:
        self.config.available_models = [m for m in self.config.available_models if m.model_id != model_id]
        if self.config.active_model_id == model_id:
            self.config.active_model_id = None
        save_config(self.config)
        return True

    def set_active_model(self, model_id: str) -> bool:
        if any(m.model_id == model_id for m in self.config.available_models):
            self.config.active_model_id = model_id
            save_config(self.config)
            return True
        return False

    def get_active_model(self) -> Optional[ModelConfig]:
        if not self.config.active_model_id:
            return None
        return next((m for m in self.config.available_models if m.model_id == self.config.active_model_id), None)

    def get_config(self) -> AppConfig:
        return self.config
