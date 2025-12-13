"""
Base interface for Live2D model configurations.

All model-specific modules should inherit from VTuberModel
to ensure consistent interface across different models.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class VTuberModel(ABC):
    """
    Abstract base class for Live2D VTuber model configurations.
    
    Each model should implement this interface to provide:
    - Parameter mappings
    - Emotion presets
    - Model-specific metadata
    """
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model's display name."""
        pass
    
    @property
    @abstractmethod
    def parameter_map(self) -> Dict[str, str]:
        """
        Map generic action names to model-specific parameter IDs.
        
        Example:
            {
                "head_x": "PARAM_ANGLE_X",
                "eye_left_open": "PARAM_EYE_L_OPEN",
            }
        """
        pass
    
    @property
    @abstractmethod
    def parameter_ranges(self) -> Dict[str, Dict[str, float]]:
        """
        Parameter ranges with min, default, max values.
        
        Example:
            {
                "PARAM_ANGLE_X": {"min": -30.0, "default": 0.0, "max": 30.0}
            }
        """
        pass
    
    @property
    @abstractmethod
    def emotions(self) -> Dict[str, Dict[str, float]]:
        """
        Emotion presets mapping emotion names to parameter values.
        
        Example:
            {
                "happy": {"PARAM_MOUTH_FORM": 0.8, "PARAM_EYE_L_OPEN": 0.8}
            }
        """
        pass
    
    @property
    def micro_expressions(self) -> Dict[str, Dict[str, float]]:
        """
        Micro-expression presets for quick subtle reactions.
        Override in subclass to add model-specific micro-expressions.
        
        Example:
            {
                "raise_eyebrows": {"PARAM_BROW_L_Y": 0.6, "PARAM_BROW_R_Y": 0.6}
            }
        """
        return {}
    
    @property
    def composite_expressions(self) -> Dict[str, Dict[str, float]]:
        """
        Composite expression presets for complex emotion combinations.
        Override in subclass to add model-specific composites.
        
        Example:
            {
                "sarcastic": {"PARAM_MOUTH_FORM": 0.5, "PARAM_BROW_R_Y": 0.3}
            }
        """
        return {}
    
    def clamp_parameter(self, param_id: str, value: float) -> float:
        """Clamp parameter value to valid range."""
        if param_id not in self.parameter_ranges:
            return value
        
        range_info = self.parameter_ranges[param_id]
        return max(range_info["min"], min(range_info["max"], value))
    
    def get_default_parameters(self) -> Dict[str, float]:
        """Get all parameters at default values."""
        return {
            param_id: range_info["default"]
            for param_id, range_info in self.parameter_ranges.items()
        }
    
    def apply_intensity(self, emotion: str, intensity: float = 1.0) -> Dict[str, float]:
        """
        Apply intensity scaling to an emotion.
        
        Args:
            emotion: Emotion name
            intensity: Intensity factor (0.0 to 1.0)
            
        Returns:
            Emotion parameters scaled by intensity
        """
        if emotion not in self.emotions:
            raise ValueError(f"Unknown emotion: {emotion}")
        
        intensity = max(0.0, min(1.0, intensity))
        neutral = self.emotions.get("neutral", {})
        emotion_params = self.emotions[emotion]
        
        scaled = {}
        for key, value in emotion_params.items():
            neutral_val = neutral.get(
                key, 
                self.parameter_ranges.get(key, {}).get("default", 0.0)
            )
            scaled[key] = neutral_val + (value - neutral_val) * intensity
            scaled[key] = self.clamp_parameter(key, scaled[key])
        
        return scaled
    
    def blend_emotions(
        self, 
        emotion1: str, 
        emotion2: str, 
        blend: float = 0.5
    ) -> Dict[str, float]:
        """
        Blend two emotions together.
        
        Args:
            emotion1: First emotion name
            emotion2: Second emotion name
            blend: Blend factor (0.0 = full emotion1, 1.0 = full emotion2)
            
        Returns:
            Blended parameter dictionary
        """
        if emotion1 not in self.emotions or emotion2 not in self.emotions:
            raise ValueError(f"Unknown emotion: {emotion1} or {emotion2}")
        
        blend = max(0.0, min(1.0, blend))
        
        params1 = self.emotions[emotion1]
        params2 = self.emotions[emotion2]
        
        all_keys = set(params1.keys()) | set(params2.keys())
        
        blended = {}
        for key in all_keys:
            val1 = params1.get(
                key, 
                self.parameter_ranges.get(key, {}).get("default", 0.0)
            )
            val2 = params2.get(
                key, 
                self.parameter_ranges.get(key, {}).get("default", 0.0)
            )
            blended[key] = val1 * (1 - blend) + val2 * blend
            blended[key] = self.clamp_parameter(key, blended[key])
        
        return blended
    
    @property
    def available_emotions(self) -> List[str]:
        """Return list of available emotion names."""
        return list(self.emotions.keys())
    
    @property
    def available_micro_expressions(self) -> List[str]:
        """Return list of available micro-expression names."""
        return list(self.micro_expressions.keys())
    
    @property
    def available_composite_expressions(self) -> List[str]:
        """Return list of available composite expression names."""
        return list(self.composite_expressions.keys())
    
    def get_micro(self, action: str) -> Dict[str, float]:
        """
        Get micro-expression parameters by action name.
        
        Args:
            action: Micro-expression action name
            
        Returns:
            Parameter dictionary, empty if not found
        """
        return self.micro_expressions.get(action, {})
    
    def get_composite(self, expression: str) -> Dict[str, float]:
        """
        Get composite expression parameters by expression name.
        
        Args:
            expression: Composite expression name
            
        Returns:
            Parameter dictionary, empty if not found
        """
        return self.composite_expressions.get(expression, {})
    
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}: {self.model_name} "
            f"({len(self.parameter_ranges)} params, "
            f"{len(self.emotions)} emotions)>"
        )
