"""
Model configuration package for VTube Studio integration.

This package contains model-specific parameter mappings and emotion presets
for different Live2D models.

Usage:
    from models import get_model, list_models
    
    # Load a specific model
    model = get_model("chino11")
    
    # Use model's emotions
    params = model.emotions["happy"]
    await vts_inject_parameters(ws, params)
    
    # Apply intensity
    params = model.apply_intensity("sad", 0.5)
"""

from typing import Dict, Optional
from .base_model import VTuberModel

# Import model configurations
from .chino11 import Chino11Model

# Registry of available models
_MODEL_REGISTRY: Dict[str, type] = {
    "chino11": Chino11Model,
}

# Singleton instances cache
_model_instances: Dict[str, VTuberModel] = {}


def get_model(model_name: str) -> VTuberModel:
    """
    Get a model instance by name.
    
    Args:
        model_name: Model identifier (e.g., "chino11")
        
    Returns:
        Model instance
        
    Raises:
        ValueError: If model name is not found
    """
    if model_name not in _MODEL_REGISTRY:
        available = ", ".join(_MODEL_REGISTRY.keys())
        raise ValueError(
            f"Unknown model: {model_name}. Available models: {available}"
        )
    
    # Return cached instance or create new one
    if model_name not in _model_instances:
        _model_instances[model_name] = _MODEL_REGISTRY[model_name]()
    
    return _model_instances[model_name]


def list_models() -> list:
    """Return list of available model names."""
    return list(_MODEL_REGISTRY.keys())


def register_model(name: str, model_class: type) -> None:
    """
    Register a new model configuration.
    
    Args:
        name: Model identifier
        model_class: Model class (must inherit from VTuberModel)
    """
    if not issubclass(model_class, VTuberModel):
        raise TypeError(f"{model_class} must inherit from VTuberModel")
    
    _MODEL_REGISTRY[name] = model_class
    # Clear cached instance if it exists
    _model_instances.pop(name, None)


__all__ = [
    "VTuberModel",
    "get_model",
    "list_models", 
    "register_model",
    "Chino11Model",
]
