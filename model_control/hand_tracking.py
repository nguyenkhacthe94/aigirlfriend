"""
VTube Studio Hand Tracking Controller

Provides a high-level interface for controlling hand tracking parameters
with automatic validation, range clamping, and helper methods.

This module extends the basic hand tracking functions from vts_movement.py
with a comprehensive class-based interface for easier integration.
"""

from typing import Optional, Tuple, List
from model_control.vts_movement import (
    move_hand_left_found,
    move_hand_right_found,
    move_both_hands_found,
    move_hand_distance,
    move_hand_left_position_x,
    move_hand_left_position_y,
    move_hand_left_position_z,
    move_hand_right_position_x,
    move_hand_right_position_y,
    move_hand_right_position_z,
    move_hand_left_angle_x,
    move_hand_left_angle_z,
    move_hand_right_angle_x,
    move_hand_right_angle_z,
    move_hand_left_open,
    move_hand_right_open,
    move_hand_left_finger_1__thumb,
    move_hand_left_finger_2__index,
    move_hand_left_finger_3__middle,
    move_hand_left_finger_4__ring,
    move_hand_left_finger_5__pinky,
    move_hand_right_finger_1__thumb,
    move_hand_right_finger_2__index,
    move_hand_right_finger_3__middle,
    move_hand_right_finger_4__ring,
    move_hand_right_finger_5__pinky,
)


class HandTrackingController:
    """
    Comprehensive Hand Tracking Controller for VTube Studio.
    
    Provides validated control methods for:
    - Hand detection status (Left/Right/Both)
    - Hand distance tracking
    - 3D hand positioning (XYZ coordinates)
    - Hand rotation angles (X/Z axes)
    - Individual finger curl values
    
    All methods include automatic range validation according to VTS specifications:
    - Position: -10 to 10
    - Angles: -180 to 180 degrees
    - Finger curl: 0 to 1 (0=closed, 1=open)
    - Found status: 0 or 1 (boolean)
    """
    
    # Parameter range constants
    POSITION_MIN = -10.0
    POSITION_MAX = 10.0
    ANGLE_MIN = -180.0
    ANGLE_MAX = 180.0
    FINGER_MIN = 0.0
    FINGER_MAX = 1.0
    
    def __init__(self):
        """Initialize the Hand Tracking Controller."""
        self._left_hand_found = False
        self._right_hand_found = False
    
    @staticmethod
    def _clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value to specified range."""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def _to_binary(value: bool) -> int:
        """Convert boolean to binary (0 or 1)."""
        return 1 if value else 0
    
    # ====================
    # Hand Detection Status
    # ====================
    
    async def set_hand_left_found(self, ws, found: bool):
        """
        Set left hand detection status.
        
        Args:
            ws: WebSocket connection
            found: True if left hand is detected, False otherwise
        """
        self._left_hand_found = found
        await move_hand_left_found(ws, self._to_binary(found))
        await self._update_both_hands(ws)
    
    async def set_hand_right_found(self, ws, found: bool):
        """
        Set right hand detection status.
        
        Args:
            ws: WebSocket connection
            found: True if right hand is detected, False otherwise
        """
        self._right_hand_found = found
        await move_hand_right_found(ws, self._to_binary(found))
        await self._update_both_hands(ws)
    
    async def _update_both_hands(self, ws):
        """
        Automatically update BothHandsFound status based on individual hand states.
        This is called internally whenever left or right hand status changes.
        
        Args:
            ws: WebSocket connection
        """
        both_found = self._left_hand_found and self._right_hand_found
        await move_both_hands_found(ws, self._to_binary(both_found))
    
    async def set_both_hands_found(self, ws, found: bool):
        """
        Manually set both hands found status and sync individual hand states.
        
        Args:
            ws: WebSocket connection
            found: True if both hands are detected, False otherwise
        """
        self._left_hand_found = found
        self._right_hand_found = found
        await move_hand_left_found(ws, self._to_binary(found))
        await move_hand_right_found(ws, self._to_binary(found))
        await move_both_hands_found(ws, self._to_binary(found))
    
    # ====================
    # Hand Distance
    # ====================
    
    async def set_hand_distance(self, ws, distance: float):
        """
        Set the distance between both hands.
        
        Args:
            ws: WebSocket connection
            distance: Distance value (no specific range in docs, passed as-is)
        """
        await move_hand_distance(ws, distance)
    
    # ====================
    # Hand Positions (Range: -10 to 10)
    # ====================
    
    async def set_hand_left_position(self, ws, x: float, y: float, z: float):
        """
        Set left hand position in 3D space.
        Values are automatically clamped to [-10, 10] range.
        
        Args:
            ws: WebSocket connection
            x: X position (-10 to 10)
            y: Y position (-10 to 10)
            z: Z position (-10 to 10)
        """
        x = self._clamp(x, self.POSITION_MIN, self.POSITION_MAX)
        y = self._clamp(y, self.POSITION_MIN, self.POSITION_MAX)
        z = self._clamp(z, self.POSITION_MIN, self.POSITION_MAX)
        
        await move_hand_left_position_x(ws, x)
        await move_hand_left_position_y(ws, y)
        await move_hand_left_position_z(ws, z)
    
    async def set_hand_right_position(self, ws, x: float, y: float, z: float):
        """
        Set right hand position in 3D space.
        Values are automatically clamped to [-10, 10] range.
        
        Args:
            ws: WebSocket connection
            x: X position (-10 to 10)
            y: Y position (-10 to 10)
            z: Z position (-10 to 10)
        """
        x = self._clamp(x, self.POSITION_MIN, self.POSITION_MAX)
        y = self._clamp(y, self.POSITION_MIN, self.POSITION_MAX)
        z = self._clamp(z, self.POSITION_MIN, self.POSITION_MAX)
        
        await move_hand_right_position_x(ws, x)
        await move_hand_right_position_y(ws, y)
        await move_hand_right_position_z(ws, z)
    
    async def set_hand_left_position_x(self, ws, x: float):
        """Set left hand X position (-10 to 10)."""
        await move_hand_left_position_x(ws, self._clamp(x, self.POSITION_MIN, self.POSITION_MAX))
    
    async def set_hand_left_position_y(self, ws, y: float):
        """Set left hand Y position (-10 to 10)."""
        await move_hand_left_position_y(ws, self._clamp(y, self.POSITION_MIN, self.POSITION_MAX))
    
    async def set_hand_left_position_z(self, ws, z: float):
        """Set left hand Z position (-10 to 10)."""
        await move_hand_left_position_z(ws, self._clamp(z, self.POSITION_MIN, self.POSITION_MAX))
    
    async def set_hand_right_position_x(self, ws, x: float):
        """Set right hand X position (-10 to 10)."""
        await move_hand_right_position_x(ws, self._clamp(x, self.POSITION_MIN, self.POSITION_MAX))
    
    async def set_hand_right_position_y(self, ws, y: float):
        """Set right hand Y position (-10 to 10)."""
        await move_hand_right_position_y(ws, self._clamp(y, self.POSITION_MIN, self.POSITION_MAX))
    
    async def set_hand_right_position_z(self, ws, z: float):
        """Set right hand Z position (-10 to 10)."""
        await move_hand_right_position_z(ws, self._clamp(z, self.POSITION_MIN, self.POSITION_MAX))
    
    # ====================
    # Hand Angles (Range: -180 to 180 degrees)
    # ====================
    
    async def set_hand_left_angles(self, ws, angle_x: float, angle_z: float):
        """
        Set left hand rotation angles.
        Values are automatically clamped to [-180, 180] range.
        
        Args:
            ws: WebSocket connection
            angle_x: X-axis rotation in degrees (-180 to 180)
            angle_z: Z-axis rotation in degrees (-180 to 180)
        """
        angle_x = self._clamp(angle_x, self.ANGLE_MIN, self.ANGLE_MAX)
        angle_z = self._clamp(angle_z, self.ANGLE_MIN, self.ANGLE_MAX)
        
        await move_hand_left_angle_x(ws, angle_x)
        await move_hand_left_angle_z(ws, angle_z)
    
    async def set_hand_right_angles(self, ws, angle_x: float, angle_z: float):
        """
        Set right hand rotation angles.
        Values are automatically clamped to [-180, 180] range.
        
        Args:
            ws: WebSocket connection
            angle_x: X-axis rotation in degrees (-180 to 180)
            angle_z: Z-axis rotation in degrees (-180 to 180)
        """
        angle_x = self._clamp(angle_x, self.ANGLE_MIN, self.ANGLE_MAX)
        angle_z = self._clamp(angle_z, self.ANGLE_MIN, self.ANGLE_MAX)
        
        await move_hand_right_angle_x(ws, angle_x)
        await move_hand_right_angle_z(ws, angle_z)
    
    async def set_hand_left_angle_x(self, ws, angle_x: float):
        """Set left hand X-axis rotation (-180 to 180 degrees)."""
        await move_hand_left_angle_x(ws, self._clamp(angle_x, self.ANGLE_MIN, self.ANGLE_MAX))
    
    async def set_hand_left_angle_z(self, ws, angle_z: float):
        """Set left hand Z-axis rotation (-180 to 180 degrees)."""
        await move_hand_left_angle_z(ws, self._clamp(angle_z, self.ANGLE_MIN, self.ANGLE_MAX))
    
    async def set_hand_right_angle_x(self, ws, angle_x: float):
        """Set right hand X-axis rotation (-180 to 180 degrees)."""
        await move_hand_right_angle_x(ws, self._clamp(angle_x, self.ANGLE_MIN, self.ANGLE_MAX))
    
    async def set_hand_right_angle_z(self, ws, angle_z: float):
        """Set right hand Z-axis rotation (-180 to 180 degrees)."""
        await move_hand_right_angle_z(ws, self._clamp(angle_z, self.ANGLE_MIN, self.ANGLE_MAX))
    
    # ====================
    # Hand Open/Close (Range: 0 to 1)
    # ====================
    
    async def set_hand_left_open(self, ws, openness: float):
        """
        Set left hand openness (0=closed fist, 1=fully open).
        Value is automatically clamped to [0, 1] range.
        
        Args:
            ws: WebSocket connection
            openness: Hand openness value (0 to 1)
        """
        await move_hand_left_open(ws, self._clamp(openness, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_right_open(self, ws, openness: float):
        """
        Set right hand openness (0=closed fist, 1=fully open).
        Value is automatically clamped to [0, 1] range.
        
        Args:
            ws: WebSocket connection
            openness: Hand openness value (0 to 1)
        """
        await move_hand_right_open(ws, self._clamp(openness, self.FINGER_MIN, self.FINGER_MAX))
    
    # ====================
    # Individual Finger Control (Range: 0 to 1)
    # ====================
    
    async def set_hand_left_fingers(
        self,
        ws,
        thumb: float,
        index: float,
        middle: float,
        ring: float,
        pinky: float
    ):
        """
        Set all left hand finger curl values at once.
        Values are automatically clamped to [0, 1] range.
        
        Args:
            ws: WebSocket connection
            thumb: Thumb curl (0=closed, 1=open)
            index: Index finger curl (0=closed, 1=open)
            middle: Middle finger curl (0=closed, 1=open)
            ring: Ring finger curl (0=closed, 1=open)
            pinky: Pinky finger curl (0=closed, 1=open)
        """
        await move_hand_left_finger_1__thumb(ws, self._clamp(thumb, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_left_finger_2__index(ws, self._clamp(index, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_left_finger_3__middle(ws, self._clamp(middle, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_left_finger_4__ring(ws, self._clamp(ring, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_left_finger_5__pinky(ws, self._clamp(pinky, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_right_fingers(
        self,
        ws,
        thumb: float,
        index: float,
        middle: float,
        ring: float,
        pinky: float
    ):
        """
        Set all right hand finger curl values at once.
        Values are automatically clamped to [0, 1] range.
        
        Args:
            ws: WebSocket connection
            thumb: Thumb curl (0=closed, 1=open)
            index: Index finger curl (0=closed, 1=open)
            middle: Middle finger curl (0=closed, 1=open)
            ring: Ring finger curl (0=closed, 1=open)
            pinky: Pinky finger curl (0=closed, 1=open)
        """
        await move_hand_right_finger_1__thumb(ws, self._clamp(thumb, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_right_finger_2__index(ws, self._clamp(index, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_right_finger_3__middle(ws, self._clamp(middle, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_right_finger_4__ring(ws, self._clamp(ring, self.FINGER_MIN, self.FINGER_MAX))
        await move_hand_right_finger_5__pinky(ws, self._clamp(pinky, self.FINGER_MIN, self.FINGER_MAX))
    
    # Individual finger methods for left hand
    async def set_hand_left_thumb(self, ws, curl: float):
        """Set left thumb curl (0=closed, 1=open)."""
        await move_hand_left_finger_1__thumb(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_left_index(self, ws, curl: float):
        """Set left index finger curl (0=closed, 1=open)."""
        await move_hand_left_finger_2__index(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_left_middle(self, ws, curl: float):
        """Set left middle finger curl (0=closed, 1=open)."""
        await move_hand_left_finger_3__middle(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_left_ring(self, ws, curl: float):
        """Set left ring finger curl (0=closed, 1=open)."""
        await move_hand_left_finger_4__ring(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_left_pinky(self, ws, curl: float):
        """Set left pinky finger curl (0=closed, 1=open)."""
        await move_hand_left_finger_5__pinky(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    # Individual finger methods for right hand
    async def set_hand_right_thumb(self, ws, curl: float):
        """Set right thumb curl (0=closed, 1=open)."""
        await move_hand_right_finger_1__thumb(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_right_index(self, ws, curl: float):
        """Set right index finger curl (0=closed, 1=open)."""
        await move_hand_right_finger_2__index(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_right_middle(self, ws, curl: float):
        """Set right middle finger curl (0=closed, 1=open)."""
        await move_hand_right_finger_3__middle(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_right_ring(self, ws, curl: float):
        """Set right ring finger curl (0=closed, 1=open)."""
        await move_hand_right_finger_4__ring(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    async def set_hand_right_pinky(self, ws, curl: float):
        """Set right pinky finger curl (0=closed, 1=open)."""
        await move_hand_right_finger_5__pinky(ws, self._clamp(curl, self.FINGER_MIN, self.FINGER_MAX))
    
    # ====================
    # Convenience Methods
    # ====================
    
    async def make_fist_left(self, ws):
        """Close left hand into a fist (all fingers closed)."""
        await self.set_hand_left_fingers(ws, 0.0, 0.0, 0.0, 0.0, 0.0)
        await self.set_hand_left_open(ws, 0.0)
    
    async def make_fist_right(self, ws):
        """Close right hand into a fist (all fingers closed)."""
        await self.set_hand_right_fingers(ws, 0.0, 0.0, 0.0, 0.0, 0.0)
        await self.set_hand_right_open(ws, 0.0)
    
    async def open_hand_left(self, ws):
        """Fully open left hand (all fingers extended)."""
        await self.set_hand_left_fingers(ws, 1.0, 1.0, 1.0, 1.0, 1.0)
        await self.set_hand_left_open(ws, 1.0)
    
    async def open_hand_right(self, ws):
        """Fully open right hand (all fingers extended)."""
        await self.set_hand_right_fingers(ws, 1.0, 1.0, 1.0, 1.0, 1.0)
        await self.set_hand_right_open(ws, 1.0)
    
    async def make_pointing_left(self, ws):
        """Make left hand pointing gesture (index extended, others closed)."""
        await self.set_hand_left_fingers(
            ws,
            thumb=0.0,
            index=1.0,  # Extended
            middle=0.0,
            ring=0.0,
            pinky=0.0
        )
    
    async def make_pointing_right(self, ws):
        """Make right hand pointing gesture (index extended, others closed)."""
        await self.set_hand_right_fingers(
            ws,
            thumb=0.0,
            index=1.0,  # Extended
            middle=0.0,
            ring=0.0,
            pinky=0.0
        )
    
    async def make_peace_sign_left(self, ws):
        """Make left hand peace sign (index and middle extended)."""
        await self.set_hand_left_fingers(
            ws,
            thumb=0.0,
            index=1.0,   # Extended
            middle=1.0,  # Extended
            ring=0.0,
            pinky=0.0
        )
    
    async def make_peace_sign_right(self, ws):
        """Make right hand peace sign (index and middle extended)."""
        await self.set_hand_right_fingers(
            ws,
            thumb=0.0,
            index=1.0,   # Extended
            middle=1.0,  # Extended
            ring=0.0,
            pinky=0.0
        )
    
    async def make_thumbs_up_left(self, ws):
        """Make left hand thumbs up gesture."""
        await self.set_hand_left_fingers(
            ws,
            thumb=1.0,  # Extended
            index=0.0,
            middle=0.0,
            ring=0.0,
            pinky=0.0
        )
    
    async def make_thumbs_up_right(self, ws):
        """Make right hand thumbs up gesture."""
        await self.set_hand_right_fingers(
            ws,
            thumb=1.0,  # Extended
            index=0.0,
            middle=0.0,
            ring=0.0,
            pinky=0.0
        )
    
    async def reset_hands(self, ws):
        """Reset both hands to neutral position (open, centered, no rotation)."""
        # Reset detection status
        await self.set_both_hands_found(ws, False)
        
        # Reset positions to center
        await self.set_hand_left_position(ws, 0.0, 0.0, 0.0)
        await self.set_hand_right_position(ws, 0.0, 0.0, 0.0)
        
        # Reset angles
        await self.set_hand_left_angles(ws, 0.0, 0.0)
        await self.set_hand_right_angles(ws, 0.0, 0.0)
        
        # Reset to open hands
        await self.open_hand_left(ws)
        await self.open_hand_right(ws)
        
        # Reset distance
        await self.set_hand_distance(ws, 0.0)


# ====================
# Module-level convenience instance
# ====================

# Create a singleton instance for easy import
hand_tracker = HandTrackingController()


# ====================
# Usage Example
# ====================

if __name__ == "__main__":
    """
    Example usage of the HandTrackingController.
    
    To use this in your application:
    
    ```python
    from model_control.hand_tracking import hand_tracker
    import websockets
    
    async def demo_hand_tracking():
        # Connect to VTS (assuming you have a connection setup)
        ws = await websockets.connect("ws://localhost:8001")
        
        # Detect left hand
        await hand_tracker.set_hand_left_found(ws, True)
        
        # Position left hand
        await hand_tracker.set_hand_left_position(ws, x=5.0, y=3.0, z=2.0)
        
        # Rotate left hand
        await hand_tracker.set_hand_left_angles(ws, angle_x=45.0, angle_z=-30.0)
        
        # Make a fist
        await hand_tracker.make_fist_left(ws)
        
        # Make a peace sign
        await hand_tracker.make_peace_sign_left(ws)
        
        # Individual finger control
        await hand_tracker.set_hand_left_thumb(ws, 1.0)
        await hand_tracker.set_hand_left_index(ws, 0.5)
        
        # Reset everything
        await hand_tracker.reset_hands(ws)
    ```
    """
    print("HandTrackingController module loaded successfully!")
    print(f"Available gesture presets: fist, open, pointing, peace_sign, thumbs_up")
    print(f"Position range: {HandTrackingController.POSITION_MIN} to {HandTrackingController.POSITION_MAX}")
    print(f"Angle range: {HandTrackingController.ANGLE_MIN} to {HandTrackingController.ANGLE_MAX}")
    print(f"Finger curl range: {HandTrackingController.FINGER_MIN} to {HandTrackingController.FINGER_MAX}")
