import asyncio

import websockets

from model_control.vts_movement import (
    move_brows,
    move_cheek_puff,
    move_eye_open_left,
    move_eye_open_right,
    move_face_angle_x,
    move_face_angle_y,
    move_face_angry,
    move_mouth_open,
    move_mouth_smile,
)
from vts_client import VTS_URL, vts_authenticate, vts_get_token

"""
High Level module expressions for VTube Studio model control. These functions are used for
guiding the llm client to select appropriate expressions based on detected emotions.

IMPORTANT: The function description / documentation is used by the LLM to determine when to call
each expression. Do NOT change the docstrings without understanding the impact on LLM behavior.
"""

# Global WebSocket connection
_ws = None


async def get_connection():
    """Returns a connected and authenticated WebSocket."""
    global _ws
    if _ws is None or getattr(_ws, "state", 0) != 1:  # 1 is State.OPEN
        print("Connecting to VTube Studio...")
        _ws = await websockets.connect(VTS_URL)
        _ws.lock = asyncio.Lock()  # Attach lock for threaded access
        token = await vts_get_token(_ws)
        await vts_authenticate(_ws, token)
        print("Connected and authenticated.")
    return _ws


async def smile():
    """
    Display a gentle, warm smile expression on the avatar's face.

    Use this when:
    - User expresses happiness, contentment, satisfaction, or pleasure
    - AI model responds with warmth, friendliness, or gentle positivity
    - Giving compliments, encouragement, or supportive responses
    - Greeting someone or expressing politeness
    - AI model feels pleased or satisfied with helping

    Emotional triggers: joy, happiness, contentment, warmth, friendliness,
    politeness, gentle pleasure, satisfaction, being helpful, encouragement.

    Do NOT use for: Intense laughter, excitement, or overwhelming joy
    (use laugh() instead).
    """
    print("Expression: Smile")
    ws = await get_connection()
    await move_mouth_smile(ws, 1.0)
    await move_eye_open_left(ws, 1.0)
    await move_eye_open_right(ws, 1.0)


async def laugh():
    """
    Display intense joy, laughter, or overwhelming happiness expression.

    Use this when:
    - User finds something hilarious or expresses intense joy
    - AI model responds with excitement, celebration, or genuine amusement
    - Making jokes or playful responses
    - AI model is thrilled about sharing exciting information
    - Expressing overwhelming positive emotion or euphoria

    Emotional triggers: hilarity, intense joy, excitement, amusement,
    celebration, euphoria, overwhelming happiness, finding something funny,
    playfulness, thrill, exuberance.

    Do NOT use for: Gentle happiness (use smile() instead) or sarcastic
    responses.
    """
    print("Expression: Laugh")
    ws = await get_connection()
    await move_mouth_smile(ws, 1.0)
    await move_mouth_open(ws, 1.0)
    await move_eye_open_left(ws, 0.0)  # Happy eyes often squint
    await move_eye_open_right(ws, 0.0)
    for _ in range(5):
        await asyncio.sleep(0.15)
        await move_mouth_open(ws, 0.0)
        await asyncio.sleep(0.15)
        await move_mouth_open(ws, 1.0)


async def angry():
    """
    Display anger, frustration, or irritation expression.

    Use this when:
    - User expresses anger, frustration, or strong displeasure
    - AI model responds with frustration about limitations or problems
    - Expressing indignation about injustice or unfairness
    - AI model feels annoyed by repeated misunderstandings
    - Responding strongly against harmful or inappropriate content

    Emotional triggers: anger, fury, frustration, irritation, annoyance,
    displeasure, indignation, outrage, being upset, strong disagreement,
    protective anger, righteous indignation.

    Do NOT use for: Mild disagreement (use disagree() instead) or sadness
    (use sad() instead).
    """
    print("Expression: Angry")
    ws = await get_connection()
    await move_face_angry(ws, 1.0)
    await move_brows(ws, 0.0)  # Or however brows map to angry for this model
    await move_mouth_smile(ws, 0.0)


async def blink():
    """
    Perform a simple blink expression for natural movement.

    Use this when: Adding natural, subtle animation during conversations,
    creating realistic eye movement, or during pauses in speech. This is
    for maintaining liveliness without strong emotional expression.

    Emotional triggers: neutral states, natural conversation flow,
    maintaining eye contact, subtle acknowledgment, thinking pause.

    Do NOT use for: Strong emotions - use specific emotion functions instead.
    """
    print("Expression: Blink")
    ws = await get_connection()
    await move_eye_open_left(ws, 0.0)
    await move_eye_open_right(ws, 0.0)
    await asyncio.sleep(0.15)
    await move_eye_open_left(ws, 1.0)
    await move_eye_open_right(ws, 1.0)


async def wow():
    """
    Display amazement, astonishment, or being impressed expression.

    Use this when:
    - User shares something surprising, impressive, or remarkable
    - AI model discovers something fascinating or learns new information
    - Expressing genuine amazement at user's achievements or abilities
    - AI model is impressed by creative ideas or solutions
    - Responding with wonder to unexpected positive developments

    Emotional triggers: amazement, astonishment, surprise (positive),
    wonder, being impressed, awe, revelation, unexpected positive news,
    fascination, admiration, discovery excitement.

    Do NOT use for: Negative surprises or shock (use surprised() if available,
    or sad()/angry() based on context).
    """
    print("Expression: Wow")
    ws = await get_connection()
    await move_mouth_open(ws, 1.0)
    await move_mouth_smile(ws, 1.0)
    await move_eye_open_left(ws, 1.0)
    await move_eye_open_right(ws, 1.0)


async def agree():
    """
    Show agreement, approval, or positive acknowledgment.

    Use this when: The user expresses agreement with something, approves
    of an idea, confirms understanding, says yes, or shows support for
    a statement or plan. Includes nodding-like agreement.

    Emotional triggers: agreement, approval, confirmation, consent,
    acceptance, understanding, saying yes, supporting an idea.

    Do NOT use for: Disagreement, uncertainty, or neutral acknowledgment
    without clear agreement.
    """
    print("Expression: Agree")
    ws = await get_connection()
    # Nodding: toggle FaceAngleY
    await move_face_angle_y(ws, 15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_y(ws, -15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_y(ws, 0.0)


async def disagree():
    """
    Show disagreement, disapproval, or negative response.

    Use this when: The user disagrees with something, disapproves,
    says no, rejects an idea, or expresses opposition to a statement
    or plan. Includes head-shaking-like disagreement.

    Emotional triggers: disagreement, disapproval, rejection, saying no,
    opposition, dissent, refusal, negative response to suggestions.

    Do NOT use for: Strong anger (use angry() instead) or agreement.
    """
    print("Expression: Disagree")
    ws = await get_connection()
    # Shaking: toggle FaceAngleX
    await move_face_angle_x(ws, 15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_x(ws, -15.0)
    await asyncio.sleep(0.15)
    await move_face_angle_x(ws, 0.0)


async def yap():
    """
    Show active talking, chatting, or animated conversation expression.

    Use this when: The user is being very talkative, chatty, engaging
    in animated conversation, explaining something enthusiastically,
    or when they're in a chatty, social mood. For ongoing speech animation.

    Emotional triggers: talkativeness, chattiness, animated explanation,
    social engagement, enthusiasm in conversation, storytelling.

    Do NOT use for: Single responses or brief answers - use appropriate
    emotion-based expressions instead.
    """
    print("Expression: Yapping")
    ws = await get_connection()
    for _ in range(5):
        await move_mouth_open(ws, 1.0)
        await asyncio.sleep(0.1)
        await move_mouth_open(ws, 0.0)
        await asyncio.sleep(0.1)


async def shy():
    """
    Display shyness, bashfulness, or timid expression.

    Use this when:
    - User expresses embarrassment, shyness, or awkwardness
    - AI model responds bashfully to compliments or praise
    - Admitting uncertainty or lack of knowledge humbly
    - AI model feels modest about its capabilities
    - Expressing timidity about making suggestions or recommendations

    Emotional triggers: shyness, bashfulness, embarrassment, timidity,
    awkwardness, humility, social anxiety, being flustered, modesty,
    uncertainty, humble admission, self-consciousness.

    Do NOT use for: Sadness (use sad() instead) or confidence.
    """
    print("Expression: Shy")
    ws = await get_connection()
    await move_cheek_puff(ws, 1.0)
    await move_face_angle_y(ws, -10.0)


async def sad():
    """
    Display sadness, melancholy, or disappointment expression.

    Use this when:
    - User expresses sadness, sorrow, or shares bad news
    - AI model responds with empathy and compassion for user's pain
    - Expressing disappointment about unfortunate situations
    - AI model feels sad about limitations in helping the user
    - Responding with genuine concern for difficult circumstances

    Emotional triggers: sadness, sorrow, disappointment, melancholy,
    grief, loss, bad news, misfortune, feeling down, depression,
    empathy, compassion, concern, sympathy.

    Do NOT use for: Anger (use angry() instead) or mild disappointment
    without clear sadness.
    """
    print("Expression: Sad")
    ws = await get_connection()
    await move_mouth_smile(ws, 0.0)
    await move_face_angry(ws, 1.0)
    await move_brows(ws, 0.0)
    await move_face_angle_y(ws, -10.0)


async def love():
    """
    Display affection, love, or deep positive emotion expression.

    Use this when: The user expresses love, deep affection, adoration,
    romantic feelings, or overwhelming positive emotion toward someone
    or something. For expressions of care, devotion, or heartfelt emotion.

    Emotional triggers: love, affection, adoration, romance, deep care,
    devotion, heartfelt emotion, expressing feelings, warm attachment.

    Do NOT use for: Simple happiness (use smile() instead) or friendship
    without romantic/deep emotional context.
    """
    print("Expression: Love")
    ws = await get_connection()
    await move_cheek_puff(ws, 1.0)
    await move_mouth_smile(ws, 1.0)
    # Could imply "Love" via eyes/blush if model supports it specifically


async def hello():
    print("Expression: Hello")
    ws = await get_connection()

    # Just yap (mouth movement) without hand wave
    for _ in range(2):
        await move_mouth_open(ws, 0.8)
        await asyncio.sleep(0.2)
        await move_mouth_open(ws, 0.0)
        await asyncio.sleep(0.2)


# Synchronous wrapper functions for Google Generative AI function calling
# These functions can be called directly by the LLM and handle async execution


def _run_async_expression(async_func):
    """Helper function to run async expression functions in a new event loop."""
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a task
            task = asyncio.create_task(async_func())
            # Since we can't wait in a sync function, we'll schedule it
            # This is a compromise - the function will execute but we won't wait
            return
    except RuntimeError:
        # No event loop is running, create a new one
        pass

    # Create and run a new event loop
    try:
        asyncio.run(async_func())
    except Exception as e:
        print(f"Warning: Could not execute expression function: {e}")


def smile_sync():
    """Synchronous wrapper for smile() expression function."""
    _run_async_expression(smile)


def laugh_sync():
    """Synchronous wrapper for laugh() expression function."""
    _run_async_expression(laugh)


def angry_sync():
    """Synchronous wrapper for angry() expression function."""
    _run_async_expression(angry)


def blink_sync():
    """Synchronous wrapper for blink() expression function."""
    _run_async_expression(blink)


def wow_sync():
    """Synchronous wrapper for wow() expression function."""
    _run_async_expression(wow)


def agree_sync():
    """Synchronous wrapper for agree() expression function."""
    _run_async_expression(agree)


def disagree_sync():
    """Synchronous wrapper for disagree() expression function."""
    _run_async_expression(disagree)


def yap_sync():
    """Synchronous wrapper for yap() expression function."""
    _run_async_expression(yap)


def shy_sync():
    """Synchronous wrapper for shy() expression function."""
    _run_async_expression(shy)


def sad_sync():
    """Synchronous wrapper for sad() expression function."""
    _run_async_expression(sad)


def love_sync():
    """Synchronous wrapper for love() expression function."""
    _run_async_expression(love)
