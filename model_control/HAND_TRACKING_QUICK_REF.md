# Hand Tracking Quick Reference

## Import
```python
from model_control.hand_tracking import hand_tracker
```

## Detection
```python
await hand_tracker.set_hand_left_found(ws, True)
await hand_tracker.set_hand_right_found(ws, True)
await hand_tracker.set_both_hands_found(ws, True)  # Auto-syncs both
```

## Position (-10 to 10)
```python
await hand_tracker.set_hand_left_position(ws, x=5.0, y=3.0, z=2.0)
await hand_tracker.set_hand_right_position(ws, x=-5.0, y=3.0, z=2.0)
```

## Angles (±180°)
```python
await hand_tracker.set_hand_left_angles(ws, angle_x=45.0, angle_z=-30.0)
await hand_tracker.set_hand_right_angles(ws, angle_x=45.0, angle_z=-30.0)
```

## Gesture Presets
```python
await hand_tracker.make_fist_left(ws)          # Closed fist
await hand_tracker.open_hand_left(ws)          # Open hand
await hand_tracker.make_pointing_left(ws)      # Index finger pointing
await hand_tracker.make_peace_sign_left(ws)    # Peace/V sign
await hand_tracker.make_thumbs_up_left(ws)     # Thumbs up
```

## Individual Fingers (0=closed, 1=open)
```python
await hand_tracker.set_hand_left_thumb(ws, 1.0)
await hand_tracker.set_hand_left_index(ws, 1.0)
await hand_tracker.set_hand_left_middle(ws, 0.5)
await hand_tracker.set_hand_left_ring(ws, 0.0)
await hand_tracker.set_hand_left_pinky(ws, 1.0)
```

## Batch Operations
```python
# Set all fingers at once
await hand_tracker.set_hand_left_fingers(
    ws, thumb=1.0, index=1.0, middle=0.0, ring=0.0, pinky=0.0
)
```

## Reset
```python
await hand_tracker.reset_hands(ws)  # Reset everything to neutral
```

## Testing
```bash
python scripts/sanity/test_hand_tracking.py
```
