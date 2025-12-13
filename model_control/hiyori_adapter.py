"""
Hiyori Model Parameter Adapter

This module provides mapping between Hiyori's Live2D parameter names
and the existing VTS tracking control functions in vts_movement.py.

IMPORTANT: This adapter ONLY uses existing functions from vts_movement.py.
No new control functions are created - strict code reuse policy.

NOTE: Hiyori parameters (Live2D internal) != VTS tracking parameters
The mapping is conceptual/semantic, not direct parameter name mapping.
"""

from model_control import vts_movement


# =============================================================================
# Hiyori Parameter Ranges (Extracted from hiyori.vtube.json)
# =============================================================================
# These are the ACTUAL expected ranges for VTS API calls, NOT normalized 0-1.
# Source: ParameterSettings[].OutputRangeLower/Upper in hiyori.vtube.json
# Updated: 2025-12-13 (fix/parameter-ranges branch)

HIYORI_RANGES = {
    "ParamAngleX": {"min": -30.0, "max": 30.0, "default": 0.0},
    "ParamAngleY": {"min": -30.0, "max": 30.0, "default": 0.0},
    "ParamAngleZ": {"min": -30.0, "max": 30.0, "default": 0.0},
    "ParamArmLA": {"min": -10.0, "max": 10.0, "default": 0.0},
    "ParamBodyAngleX": {"min": -10.0, "max": 10.0, "default": 0.0},
    "ParamBodyAngleY": {"min": -10.0, "max": 10.0, "default": 0.0},
    "ParamBodyAngleZ": {"min": -10.0, "max": 10.0, "default": 0.0},
    "ParamBreath": {"min": 0.0, "max": 1.0, "default": 0.0},
    "ParamBrowLForm": {"min": -1.0, "max": 1.0, "default": 0.0},
    "ParamBrowLY": {"min": -1.0, "max": 1.0, "default": 0.0},
    "ParamBrowRForm": {"min": -1.0, "max": 1.0, "default": 0.0},
    "ParamBrowRY": {"min": -1.0, "max": 1.0, "default": 0.0},
    "ParamCheek": {"min": -1.0, "max": 1.0, "default": 0.0},
    "ParamEyeBallX": {"min": -1.0, "max": 1.0, "default": 0.0},  # Note: VTS inverts this (1.0 to -1.0)
    "ParamEyeBallY": {"min": -1.0, "max": 1.0, "default": 0.0},
    "ParamEyeLOpen": {"min": 0.0, "max": 1.9, "default": 0.0},
    "ParamEyeLSmile": {"min": 0.0, "max": 1.0, "default": 0.0},
    "ParamEyeROpen": {"min": 0.0, "max": 1.9, "default": 0.0},
    "ParamEyeRSmile": {"min": 0.0, "max": 1.0, "default": 0.0},
    "ParamHandL": {"min": -1.0, "max": 1.0, "default": 0.0},
    "ParamHandLB": {"min": -10.0, "max": 10.0, "default": 0.0},
    "ParamHandRB": {"min": -10.0, "max": 10.0, "default": 0.0},
    "ParamMouthForm": {"min": -2.0, "max": 1.0, "default": 0.0},
    "ParamMouthOpenY": {"min": 0.0, "max": 2.1, "default": 0.0},
    "ParamMouthX": {"min": -1.0, "max": 1.0, "default": 0.0},
    # Position parameters (not in vtube.json, using standard VTS ranges)
    "ParamPositionX": {"min": -100.0, "max": 100.0, "default": 0.0},
    "ParamPositionY": {"min": -100.0, "max": 100.0, "default": 0.0},
    "ParamPositionZ": {"min": -100.0, "max": 100.0, "default": 0.0},
}


# =============================================================================
# Hiyori Parameter → VTS Movement Function Mapping
# =============================================================================

HIYORI_TO_VTS_MAPPING = {
    # Position & Orientation - Maps to VTS Face tracking
    "ParamPositionX": vts_movement.move_face_position_x,
    "ParamPositionY": vts_movement.move_face_position_y,
    "ParamPositionZ": vts_movement.move_face_position_z,
    "ParamAngleX": vts_movement.move_face_angle_x,
    "ParamAngleY": vts_movement.move_face_angle_y,
    "ParamAngleZ": vts_movement.move_face_angle_z,
    
    # Body Movement
    # TODO: No handler for ParamBodyAngleX in vts_movement (VTS doesn't have separate body angle)
    # TODO: No handler for ParamBodyAngleY in vts_movement
    # TODO: No handler for ParamBodyAngleZ in vts_movement
    # TODO: No handler for ParamShoulder in vts_movement
    # TODO: No handler for ParamBreath in vts_movement
    # TODO: No handler for ParamBustY in vts_movement
    
    # Eyes - Maps to VTS Eye tracking
    "ParamEyeLOpen": vts_movement.move_eye_open_left,
    "ParamEyeROpen": vts_movement.move_eye_open_right,
    # TODO: No handler for ParamEyeLSmile in vts_movement (VTS doesn't have eye smile tracking)
    # TODO: No handler for ParamEyeRSmile in vts_movement
    "ParamEyeBallX": vts_movement.move_eye_left_x,  # Note: Controls both eyes in VTS
    "ParamEyeBallY": vts_movement.move_eye_left_y,  # Note: Controls both eyes in VTS
    
    # Eyebrows - Maps to VTS Brow tracking
    "ParamBrowLY": vts_movement.move_brow_left_y,
    "ParamBrowRY": vts_movement.move_brow_right_y,
    # TODO: No handler for ParamBrowLX in vts_movement (VTS only tracks Y axis)
    # TODO: No handler for ParamBrowRX in vts_movement
    # TODO: No handler for ParamBrowLAngle in vts_movement
    # TODO: No handler for ParamBrowRAngle in vts_movement
    # TODO: No handler for ParamBrowLForm in vts_movement
    # TODO: No handler for ParamBrowRForm in vts_movement
    
    # Mouth & Face - Maps to VTS Mouth tracking
    "ParamMouthForm": vts_movement.move_mouth_smile,  # Closest match: smile affects form
    "ParamMouthOpenY": vts_movement.move_mouth_open,
    "ParamMouthX": vts_movement.move_mouth_x,
    # TODO: No handler for ParamCheek in vts_movement (different from CheekPuff)
    
    # Arms & Hands
    # TODO: No handler for ParamArmLA in vts_movement (VTS doesn't track arm positions)
    # TODO: No handler for ParamArmRA in vts_movement
    # TODO: No handler for ParamArmLB in vts_movement
    # TODO: No handler for ParamArmRB in vts_movement
    # TODO: No handler for ParamHandLB in vts_movement
    # TODO: No handler for ParamHandRB in vts_movement
    # TODO: No handler for ParamHandL in vts_movement
    # TODO: No handler for ParamHandR in vts_movement
    
    # Hair Physics
    # TODO: No handler for ParamHairFront in vts_movement (VTS doesn't control hair physics)
    # TODO: No handler for ParamHairBack in vts_movement
    # TODO: No handler for ParamHairAhoge in vts_movement
    
    # Clothing Physics
    # TODO: No handler for ParamSkirt in vts_movement (VTS doesn't control clothing)
    # TODO: No handler for ParamSkirt2 in vts_movement
    # TODO: No handler for ParamSideupRibbon in vts_movement
    # TODO: No handler for ParamRibbon in vts_movement
    
    # Other
    # TODO: No handler for ParamStep in vts_movement
    
    # Advanced Hair Rotation Parameters (28 total)
    # TODO: No handler for Param_Angle_Rotation_1_ArtMesh62 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_2_ArtMesh62 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_3_ArtMesh62 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_4_ArtMesh62 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_5_ArtMesh62 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_6_ArtMesh62 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_7_ArtMesh62 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_1_ArtMesh61 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_2_ArtMesh61 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_3_ArtMesh61 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_4_ArtMesh61 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_5_ArtMesh61 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_6_ArtMesh61 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_7_ArtMesh61 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_1_ArtMesh55 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_2_ArtMesh55 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_3_ArtMesh55 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_4_ArtMesh55 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_5_ArtMesh55 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_6_ArtMesh55 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_7_ArtMesh55 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_1_ArtMesh54 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_2_ArtMesh54 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_3_ArtMesh54 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_4_ArtMesh54 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_5_ArtMesh54 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_6_ArtMesh54 in vts_movement
    # TODO: No handler for Param_Angle_Rotation_7_ArtMesh54 in vts_movement
}


# =============================================================================
# Helper Functions
# =============================================================================

def get_vts_function(hiyori_param_name: str):
    """
    Get the corresponding VTS movement function for a Hiyori parameter.
    
    Args:
        hiyori_param_name: Hiyori Live2D parameter name (e.g., "ParamAngleX")
        
    Returns:
        Corresponding vts_movement function, or None if no mapping exists
        
    Example:
        >>> func = get_vts_function("ParamAngleX")
        >>> await func(ws, 15.0)  # Tilts head
    """
    return HIYORI_TO_VTS_MAPPING.get(hiyori_param_name)


def list_supported_parameters():
    """
    List all Hiyori parameters that have VTS movement function mappings.
    
    Returns:
        List of supported Hiyori parameter names
    """
    return list(HIYORI_TO_VTS_MAPPING.keys())


def list_unsupported_parameters():
    """
    List Hiyori parameters that don't have VTS equivalents.
    
    Returns:
        List of parameter names without mappings
    """
    import json
    from pathlib import Path
    
    # Load all Hiyori parameters
    params_file = Path("model_control/hiyori_parameters.json")
    with open(params_file, 'r') as f:
        all_params = json.load(f)
    
    all_param_ids = {p['id'] for p in all_params}
    supported = set(HIYORI_TO_VTS_MAPPING.keys())
    
    return sorted(all_param_ids - supported)


async def control_hiyori_param(ws, param_name: str, value: float):
    """
    Control a Hiyori parameter using existing VTS movement functions.
    
    Args:
        ws: WebSocket connection to VTS
        param_name: Hiyori parameter name (e.g., "ParamMouthOpenY")
        value: Parameter value (will be clamped to valid range)
        
    Returns:
        True if parameter was controlled, False if no mapping exists
        
    Example:
        >>> await control_hiyori_param(ws, "ParamMouthOpenY", 1.0)
        True
        
    Note:
        Values are automatically clamped to the parameter's defined range.
        E.g., ParamAngleX accepts -30.0 to 30.0, NOT 0.0 to 1.0
    """
    func = get_vts_function(param_name)
    if not func:
        return False
    
    # Clamp value to valid range if range is defined
    if param_name in HIYORI_RANGES:
        param_range = HIYORI_RANGES[param_name]
        min_val = param_range["min"]
        max_val = param_range["max"]
        
        # Clamp the value
        original_value = value
        value = max(min_val, min(max_val, value))
        
        # Warn if value was clamped
        if value != original_value:
            print(f"⚠️  Warning: {param_name} value clamped from {original_value} to {value} (range: {min_val} to {max_val})")
    
    await func(ws, value)
    return True



def get_param_range(param_name: str):
    """
    Get the valid range for a Hiyori parameter.
    
    Args:
        param_name: Hiyori parameter name
        
    Returns:
        Dict with 'min', 'max', 'default' keys, or None if not found
        
    Example:
        >>> get_param_range("ParamAngleX")
        {'min': -30.0, 'max': 30.0, 'default': 0.0}
    """
    return HIYORI_RANGES.get(param_name)


def get_param_default(param_name: str):
    """
    Get the default value for a Hiyori parameter.
    
    Args:
        param_name: Hiyori parameter name
        
    Returns:
        Default value (float), or 0.0 if not found
    """
    param_range = HIYORI_RANGES.get(param_name)
    return param_range["default"] if param_range else 0.0


def clamp_value(param_name: str, value: float):
    """
    Clamp a value to the valid range for a parameter.
    
    Args:
        param_name: Hiyori parameter name
        value: Value to clamp
        
    Returns:
        Clamped value
    """
    param_range = HIYORI_RANGES.get(param_name)
    if not param_range:
        return value
    
    return max(param_range["min"], min(param_range["max"], value))


# =============================================================================
# Statistics & Information
# =============================================================================

def print_mapping_stats():
    """Print statistics about parameter mapping coverage."""
    import json
    from pathlib import Path
    
    # Load all parameters
    params_file = Path("model_control/hiyori_parameters.json")
    with open(params_file, 'r') as f:
        all_params = json.load(f)
    
    total = len(all_params)
    supported = len(HIYORI_TO_VTS_MAPPING)
    unsupported = total - supported
    coverage = (supported / total * 100) if total > 0 else 0
    
    print("=" * 60)
    print("HIYORI → VTS MAPPING STATISTICS")
    print("=" * 60)
    print(f"Total Hiyori Parameters: {total}")
    print(f"Mapped to VTS Functions: {supported}")
    print(f"No VTS Equivalent:       {unsupported}")
    print(f"Coverage:                {coverage:.1f}%")
    print("=" * 60)
    print(f"\nSupported categories:")
    print(f"  • Face Position (X, Y, Z)")
    print(f"  • Face Angles (X, Y, Z)")
    print(f"  • Eyes (Open L/R, Position X/Y)")
    print(f"  • Eyebrows (L/R Y position)")
    print(f"  • Mouth (Open, Form/Smile, X position)")
    print(f"\nUnsupported (no VTS tracking):")
    print(f"  • Body angles & breathing")
    print(f"  • Arms & hands")
    print(f"  • Hair physics & rotation")
    print(f"  • Clothing physics")
    print(f"  • Advanced mesh rotations (28 params)")


if __name__ == "__main__":
    # Print mapping information
    print_mapping_stats()
    
    print("\n" + "=" * 60)
    print("SUPPORTED PARAMETERS")
    print("=" * 60)
    for param in list_supported_parameters():
        print(f"  • {param}")
    
    # Display key parameter ranges
    print("\n" + "=" * 60)
    print("KEY PARAMETER RANGES (from hiyori.vtube.json)")
    print("=" * 60)
    key_params = ["ParamAngleX", "ParamAngleY", "ParamAngleZ", 
                  "ParamBodyAngleX", "ParamBodyAngleY", "ParamBodyAngleZ",
                  "ParamMouthOpenY", "ParamEyeLOpen", "ParamEyeROpen"]
    
    for param in key_params:
        param_range = get_param_range(param)
        if param_range:
            print(f"  • {param:20s} : {param_range['min']:6.1f} to {param_range['max']:6.1f} (default: {param_range['default']:6.1f})")
    
    print("\n" + "=" * 60)
    print("USAGE EXAMPLE")
    print("=" * 60)
    print("""
import asyncio
from model_control.hiyori_adapter import control_hiyori_param
import websockets

async def demo():
    ws = await websockets.connect("ws://localhost:8001")
    # ... authenticate ...
    
    # Control Hiyori parameters using existing VTS functions
    # NOTE: Values are now using REAL ranges, not 0-1!
    await control_hiyori_param(ws, "ParamMouthOpenY", 1.0)  # Open mouth
    await control_hiyori_param(ws, "ParamAngleX", 15.0)     # Tilt head 15 degrees (NOT 0.5!)
    await control_hiyori_param(ws, "ParamEyeLOpen", 0.0)    # Close left eye

asyncio.run(demo())
""")

