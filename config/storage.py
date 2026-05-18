import json
import os
from typing import Optional
from .settings import AppConfig

CONFIG_FILE = ".config/models.json"

def save_config(config: AppConfig):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        f.write(config.model_dump_json(indent=2))

def load_config() -> Optional[AppConfig]:
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return AppConfig(**data)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None
