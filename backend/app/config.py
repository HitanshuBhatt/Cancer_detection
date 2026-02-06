from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "AI Lung Cancer Detection System"
    environment: str = "development"
    model_path: Optional[str] = None  # Optional path to trained model weights
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "protected_namespaces": ("settings_",)  # Fix protected namespace warning
    }