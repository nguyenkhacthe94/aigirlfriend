import asyncio
import websockets
from vts_client import VTS_URL, vts_get_token, vts_authenticate
from model_control.vts_movement import (
    move_mouth_smile,
    move_mouth_open,
    move_face_angry,
    move_brows,
    move_eye_open_left,
    move_eye_open_right,
    move_cheek_puff,
    move_face_angle_y,
    move_face_angle_y,
    move_face_angle_x
)

# Global WebSocket connection
_ws = None

async def get_connection():
    """Returns a connected and authenticated WebSocket."""
    global _ws
    if _ws is None or getattr(_ws, "state", 0) != 1: # 1 is State.OPEN
        print("Connecting to VTube Studio...")
        _ws = await websockets.connect(VTS_URL)
        _ws.lock = asyncio.Lock() # Attach lock for threaded access
        token = await vts_get_token(_ws)
        await vts_authenticate(_ws, token)
        print("Connected and authenticated.")
    return _ws

async def smile():
    print("Expression: Smile")
    ws = await get_connection()
    await move_mouth_smile(ws, 1.0)
    await move_eye_open_left(ws, 1.0)
    await move_eye_open_right(ws, 1.0)

async def laugh():
    print("Expression: Laugh")
    ws = await get_connection()
    await move_mouth_smile(ws, 1.0)
    await move_mouth_open(ws, 1.0)
    await move_eye_open_left(ws, 0.0) # Happy eyes often squint
    await move_eye_open_right(ws, 0.0)
    for _ in range(5):
        await asyncio.sleep(0.15)
        await move_mouth_open(ws, 0.0)
        await asyncio.sleep(0.15)
        await move_mouth_open(ws, 1.0)

async def angry():
    print("Expression: Angry")
    ws = await get_connection()
    await move_face_angry(ws, 1.0)
    await move_brows(ws, 0.0) # Or however brows map to angry for this model
    await move_mouth_smile(ws, 0.0)

async def blink():
    print("Expression: Blink")
    ws = await get_connection()
    await move_eye_open_left(ws, 0.0)
    await move_eye_open_right(ws, 0.0)
    await asyncio.sleep(0.15)
    await move_eye_open_left(ws, 1.0)
    await move_eye_open_right(ws, 1.0)

async def wow():
    print("Expression: Wow")
    ws = await get_connection()
    await move_mouth_open(ws, 1.0)
    await move_mouth_smile(ws, 1.0)
    await move_eye_open_left(ws, 1.0)
    await move_eye_open_right(ws, 1.0)

async def agree():
    print("Expression: Agree")
    ws = await get_connection()
    # Nodding: toggle FaceAngleY
    await move_face_angle_y(ws, 15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_y(ws, -15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_y(ws, 0.0)

async def disagree():
    print("Expression: Disagree")
    ws = await get_connection()
    # Shaking: toggle FaceAngleX
    await move_face_angle_x(ws, 15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_x(ws, -15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_x(ws, 0.0)

async def yap():
    print("Expression: Yapping")
    ws = await get_connection()
    for _ in range(5):
        await move_mouth_open(ws, 1.0)
        await asyncio.sleep(0.1)
        await move_mouth_open(ws, 0.0)
        await asyncio.sleep(0.1)

async def shy():
    print("Expression: Shy")
    ws = await get_connection()
    await move_cheek_puff(ws, 1.0)
    await move_face_angle_y(ws, -10.0)

async def sad():
    print("Expression: Sad")
    ws = await get_connection()
    await move_mouth_smile(ws, 0.0)
    await move_face_angry(ws, 1.0)
    await move_brows(ws, 0.0)
    await move_face_angle_y(ws, -10.0)

async def love():
    print("Expression: Love")
    ws = await get_connection()
    await move_cheek_puff(ws, 1.0)
    await move_mouth_smile(ws, 1.0)
    # Could imply "Love" via eyes/blush if model supports it specifically

async def hello():
    print("Expression: Hello")
    ws = await get_connection()
    
    # Just yap (mouth movement) without hand wave
    for _ in range(3):
        await move_mouth_open(ws, 0.8)
        await asyncio.sleep(0.2)
        await move_mouth_open(ws, 0.0)
        await asyncio.sleep(0.2)