"""
chino11 Live2D Model Configuration
Generated from model analysis: 2025-12-12

This module contains parameter definitions and emotion mappings
for the chino11 Live2D model.
"""

from .base_model import VTuberModel


class Chino11Model(VTuberModel):
    """
    Configuration for the chino11 Live2D model.
    
    Usage:
        from models import get_model
        
        model = get_model("chino11")
        params = model.emotions["happy"]
        await vts_inject_parameters(ws, params)
    """
    
    @property
    def model_name(self) -> str:
        return "chino11"
    
    @property
    def parameter_map(self):
        """Friendly name mapping to actual Live2D parameter IDs."""
        return {
            # Head Movement
            "head_x": "PARAM_ANGLE_X",           # -30 to 30
            "head_y": "PARAM_ANGLE_Y",           # -30 to 30
            "head_z": "PARAM_ANGLE_Z",           # -30 to 30
            
            # Eye Control
            "eye_left_open": "PARAM_EYE_L_OPEN",      # 0 to 1
            "eye_right_open": "PARAM_EYE_R_OPEN",     # 0 to 1
            "eye_right_smile": "PARAM_EYE_R_SMILE",   # 0 to 1
            "eye_gaze_x": "PARAM_EYE_BALL_X",         # -1 to 1
            "eye_gaze_y": "PARAM_EYE_BALL_Y",         # -1 to 1
            
            # Eyebrows
            "brow_left": "PARAM_BROW_L_Y",       # -1 to 1
            "brow_right": "PARAM_BROW_R_Y",      # -1 to 1
            
            # Mouth
            "mouth_form": "PARAM_MOUTH_FORM",    # -1 to 1
            "mouth_open": "PARAM_MOUTH_OPEN_Y",  # 0 to 1
            
            # Body
            "body_rotation": "PARAM_BODY_ANGLE_Z",  # -10 to 10
            "breathing": "PARAM_BREATH",            # 0 to 1
            
            # Physics
            "hair_front": "PARAM_HAIR_FRONT",    # -10 to 10
            "hair_side": "PARAM_HAIR_SIDE",      # -10 to 10
            "hair_back": "PARAM_HAIR_BACK",      # -10 to 10
            "skirt": "Param",                    # -10 to 10
        }
    
    @property
    def parameter_ranges(self):
        """Standard Live2D parameter ranges for chino11 model."""
        return {
            # Head angles
            "PARAM_ANGLE_X": {"min": -30.0, "default": 0.0, "max": 30.0},
            "PARAM_ANGLE_Y": {"min": -30.0, "default": 0.0, "max": 30.0},
            "PARAM_ANGLE_Z": {"min": -30.0, "default": 0.0, "max": 30.0},
            
            # Eyes
            "PARAM_EYE_L_OPEN": {"min": 0.0, "default": 1.0, "max": 1.0},
            "PARAM_EYE_R_OPEN": {"min": 0.0, "default": 1.0, "max": 1.0},
            "PARAM_EYE_R_SMILE": {"min": 0.0, "default": 0.0, "max": 1.0},
            "PARAM_EYE_BALL_X": {"min": -1.0, "default": 0.0, "max": 1.0},
            "PARAM_EYE_BALL_Y": {"min": -1.0, "default": 0.0, "max": 1.0},
            
            # Eyebrows
            "PARAM_BROW_L_Y": {"min": -1.0, "default": 0.0, "max": 1.0},
            "PARAM_BROW_R_Y": {"min": -1.0, "default": 0.0, "max": 1.0},
            
            # Mouth
            "PARAM_MOUTH_FORM": {"min": -1.0, "default": 0.0, "max": 1.0},
            "PARAM_MOUTH_OPEN_Y": {"min": 0.0, "default": 0.0, "max": 1.0},
            
            # Body
            "PARAM_BODY_ANGLE_Z": {"min": -10.0, "default": 0.0, "max": 10.0},
            "PARAM_BREATH": {"min": 0.0, "default": 0.0, "max": 1.0},
            
            # Physics
            "PARAM_HAIR_FRONT": {"min": -10.0, "default": 0.0, "max": 10.0},
            "PARAM_HAIR_SIDE": {"min": -10.0, "default": 0.0, "max": 10.0},
            "PARAM_HAIR_BACK": {"min": -10.0, "default": 0.0, "max": 10.0},
            "Param": {"min": -10.0, "default": 0.0, "max": 10.0},  # Skirt
        }
    
    @property
    def emotions(self):
        """Predefined emotion parameter sets."""
        return {
            "neutral": {
                "PARAM_ANGLE_X": 0.0,
                "PARAM_ANGLE_Y": 0.0,
                "PARAM_EYE_L_OPEN": 1.0,
                "PARAM_EYE_R_OPEN": 1.0,
                "PARAM_MOUTH_FORM": 0.0,
                "PARAM_MOUTH_OPEN_Y": 0.0,
                "PARAM_BROW_L_Y": 0.0,
                "PARAM_BROW_R_Y": 0.0,
            },
            
            "happy": {
                "PARAM_ANGLE_X": 0.0,
                "PARAM_ANGLE_Y": 3.0,
                "PARAM_EYE_L_OPEN": 0.8,
                "PARAM_EYE_R_OPEN": 0.8,
                "PARAM_EYE_R_SMILE": 1.0,
                "PARAM_MOUTH_FORM": 0.8,
                "PARAM_MOUTH_OPEN_Y": 0.3,
                "PARAM_BROW_L_Y": 0.3,
                "PARAM_BROW_R_Y": 0.3,
            },
            
            "sad": {
                "PARAM_ANGLE_X": 0.0,
                "PARAM_ANGLE_Y": -5.0,
                "PARAM_EYE_L_OPEN": 0.6,
                "PARAM_EYE_R_OPEN": 0.6,
                "PARAM_MOUTH_FORM": -0.4,
                "PARAM_MOUTH_OPEN_Y": 0.0,
                "PARAM_BROW_L_Y": -0.5,
                "PARAM_BROW_R_Y": -0.5,
            },
            
            "angry": {
                "PARAM_ANGLE_X": 0.0,
                "PARAM_ANGLE_Y": 0.0,
                "PARAM_EYE_L_OPEN": 0.7,
                "PARAM_EYE_R_OPEN": 0.7,
                "PARAM_MOUTH_FORM": -0.6,
                "PARAM_MOUTH_OPEN_Y": 0.2,
                "PARAM_BROW_L_Y": -0.8,
                "PARAM_BROW_R_Y": -0.8,
            },
            
            "surprised": {
                "PARAM_ANGLE_X": 0.0,
                "PARAM_ANGLE_Y": 5.0,
                "PARAM_EYE_L_OPEN": 1.0,
                "PARAM_EYE_R_OPEN": 1.0,
                "PARAM_MOUTH_FORM": 0.0,
                "PARAM_MOUTH_OPEN_Y": 0.9,
                "PARAM_BROW_L_Y": 0.8,
                "PARAM_BROW_R_Y": 0.8,
            },
            
            "thinking": {
                "PARAM_ANGLE_X": 8.0,
                "PARAM_ANGLE_Y": 2.0,
                "PARAM_EYE_L_OPEN": 0.8,
                "PARAM_EYE_R_OPEN": 0.8,
                "PARAM_EYE_BALL_X": 0.5,
                "PARAM_EYE_BALL_Y": 0.3,
                "PARAM_MOUTH_FORM": 0.2,
                "PARAM_MOUTH_OPEN_Y": 0.0,
                "PARAM_BROW_L_Y": 0.2,
                "PARAM_BROW_R_Y": -0.1,
            },
            
            "confused": {
                "PARAM_ANGLE_X": -5.0,
                "PARAM_ANGLE_Y": 0.0,
                "PARAM_EYE_L_OPEN": 0.9,
                "PARAM_EYE_R_OPEN": 0.7,
                "PARAM_MOUTH_FORM": -0.2,
                "PARAM_MOUTH_OPEN_Y": 0.15,
                "PARAM_BROW_L_Y": 0.4,
                "PARAM_BROW_R_Y": -0.2,
            },
            
            "excited": {
                "PARAM_ANGLE_X": 0.0,
                "PARAM_ANGLE_Y": 5.0,
                "PARAM_EYE_L_OPEN": 1.0,
                "PARAM_EYE_R_OPEN": 1.0,
                "PARAM_EYE_R_SMILE": 0.5,
                "PARAM_MOUTH_FORM": 1.0,
                "PARAM_MOUTH_OPEN_Y": 0.7,
                "PARAM_BROW_L_Y": 0.6,
                "PARAM_BROW_R_Y": 0.6,
            },
            
            "sleepy": {
                "PARAM_ANGLE_X": 3.0,
                "PARAM_ANGLE_Y": -3.0,
                "PARAM_EYE_L_OPEN": 0.3,
                "PARAM_EYE_R_OPEN": 0.3,
                "PARAM_MOUTH_FORM": 0.0,
                "PARAM_MOUTH_OPEN_Y": 0.4,
                "PARAM_BROW_L_Y": -0.3,
                "PARAM_BROW_R_Y": -0.3,
            },
        }
    
    @property
    def micro_expressions(self):
        """Tier 2: Quick micro-reactions for subtle expressions."""
        return {
            "raise_eyebrows": {
                "PARAM_BROW_L_Y": 0.6,
                "PARAM_BROW_R_Y": 0.6
            },
            "furrow_brow": {
                "PARAM_BROW_L_Y": -0.5,
                "PARAM_BROW_R_Y": -0.5
            },
            "slight_smile": {
                "PARAM_MOUTH_FORM": 0.3,
                "PARAM_MOUTH_OPEN_Y": 0.1
            },
            "smirk": {
                "PARAM_MOUTH_FORM": 0.5,
                "PARAM_ANGLE_X": 2.0,
                "PARAM_BROW_R_Y": 0.3
            },
            "blink": {
                "PARAM_EYE_L_OPEN": 0.0,
                "PARAM_EYE_R_OPEN": 0.0
            },
            "wink_left": {
                "PARAM_EYE_L_OPEN": 0.0,
                "PARAM_EYE_R_OPEN": 1.0
            },
            "wink_right": {
                "PARAM_EYE_L_OPEN": 1.0,
                "PARAM_EYE_R_OPEN": 0.0
            },
            "look_away": {
                "PARAM_EYE_BALL_X": 0.7,
                "PARAM_ANGLE_X": 5.0
            },
            "look_down": {
                "PARAM_EYE_BALL_Y": -0.6,
                "PARAM_ANGLE_Y": -3.0
            },
            "look_up": {
                "PARAM_EYE_BALL_Y": 0.6,
                "PARAM_ANGLE_Y": 3.0
            },
            "tilt_head": {
                "PARAM_ANGLE_X": 8.0,
                "PARAM_ANGLE_Y": 2.0
            },
            "nod": {
                "PARAM_ANGLE_Y": 5.0
            },
            "shake_head": {
                "PARAM_ANGLE_X": -8.0
            },
        }
    
    @property
    def composite_expressions(self):
        """Tier 3: Complex expression combinations for nuanced reactions."""
        return {
            "sarcastic": {
                "PARAM_MOUTH_FORM": 0.5,
                "PARAM_ANGLE_X": 2.0,
                "PARAM_BROW_R_Y": 0.3,
                "PARAM_EYE_R_SMILE": 0.3,
                "PARAM_MOUTH_OPEN_Y": 0.1
            },
            "skeptical": {
                "PARAM_BROW_L_Y": -0.3,
                "PARAM_BROW_R_Y": 0.4,
                "PARAM_ANGLE_X": 8.0,
                "PARAM_ANGLE_Y": 2.0,
                "PARAM_MOUTH_FORM": -0.2
            },
            "empathetic": {
                "PARAM_MOUTH_FORM": 0.4,
                "PARAM_EYE_L_OPEN": 0.85,
                "PARAM_EYE_R_OPEN": 0.85,
                "PARAM_BROW_L_Y": -0.2,
                "PARAM_BROW_R_Y": -0.2,
                "PARAM_ANGLE_Y": -2.0
            },
            "playful": {
                "PARAM_MOUTH_FORM": 0.7,
                "PARAM_EYE_L_OPEN": 0.8,
                "PARAM_EYE_R_OPEN": 0.8,
                "PARAM_EYE_R_SMILE": 0.6,
                "PARAM_ANGLE_X": 5.0,
                "PARAM_BROW_L_Y": 0.3
            },
            "listening": {
                "PARAM_ANGLE_X": 8.0,
                "PARAM_EYE_BALL_X": 0.0,
                "PARAM_MOUTH_FORM": 0.1,
                "PARAM_EYE_L_OPEN": 0.95,
                "PARAM_EYE_R_OPEN": 0.95
            },
            "processing": {
                "PARAM_EYE_BALL_X": 0.5,
                "PARAM_EYE_BALL_Y": 0.4,
                "PARAM_BROW_L_Y": 0.2,
                "PARAM_BROW_R_Y": -0.1,
                "PARAM_MOUTH_FORM": 0.0
            },
            "concerned": {
                "PARAM_BROW_L_Y": -0.4,
                "PARAM_BROW_R_Y": -0.4,
                "PARAM_MOUTH_FORM": -0.3,
                "PARAM_EYE_L_OPEN": 0.9,
                "PARAM_EYE_R_OPEN": 0.9,
                "PARAM_ANGLE_Y": -2.0
            },
            "amused": {
                "PARAM_MOUTH_FORM": 0.6,
                "PARAM_EYE_L_OPEN": 0.7,
                "PARAM_EYE_R_OPEN": 0.7,
                "PARAM_EYE_R_SMILE": 0.8,
                "PARAM_BROW_L_Y": 0.2,
                "PARAM_BROW_R_Y": 0.4
            },
        }
    
    def get_micro(self, action: str) -> dict:
        """Get micro-expression parameters by action name."""
        return self.micro_expressions.get(action, {})
    
    def get_composite(self, expression: str) -> dict:
        """Get composite expression parameters by expression name."""
        return self.composite_expressions.get(expression, {})


# Backward compatibility exports
CHINO11_PARAMS = Chino11Model().parameter_map
CHINO11_RANGES = Chino11Model().parameter_ranges
CHINO11_EMOTIONS = Chino11Model().emotions



# Helper functions for backward compatibility
def clamp_parameter(param_id: str, value: float) -> float:
    """Clamp parameter value to valid range."""
    return Chino11Model().clamp_parameter(param_id, value)


def get_default_parameters() -> dict:
    """Get all parameters at default values."""
    return Chino11Model().get_default_parameters()


def blend_emotions(emotion1: str, emotion2: str, blend: float = 0.5) -> dict:
    """Blend two emotions together."""
    return Chino11Model().blend_emotions(emotion1, emotion2, blend)


def apply_intensity(emotion: str, intensity: float = 1.0) -> dict:
    """Apply intensity scaling to an emotion."""
    return Chino11Model().apply_intensity(emotion, intensity)


if __name__ == "__main__":
    model = Chino11Model()
    print(f"Model: {model}")
    print(f"\nTotal Parameters: {len(model.parameter_ranges)}")
    print(f"Available Emotions: {', '.join(model.available_emotions)}")
    
    print("\n--- Example: Happy Emotion ---")
    happy_params = model.emotions["happy"]
    for param_id, value in happy_params.items():
        print(f"  {param_id}: {value}")
