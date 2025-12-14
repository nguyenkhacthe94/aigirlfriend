from vts_client import vts_inject_parameters

async def move_face_position_x(ws, val):
    """Move the head/body horizontally (left/right)."""
    params = {"FacePositionX": val}
    await vts_inject_parameters(ws, params)

async def move_face_position_y(ws, val):
    """Move the head/body vertically (up/down)."""
    params = {"FacePositionY": val}
    await vts_inject_parameters(ws, params)

async def move_face_position_z(ws, val):
    """Move the head/body closer or further (zoom)."""
    params = {"FacePositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_face_angle_x(ws, val):
    """Rotate the head horizontally (turn left/right). Negative=Left, Positive=Right."""
    params = {"FaceAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_face_angle_y(ws, val):
    """Rotate the head vertically (look up/down). Negative=Down, Positive=Up."""
    params = {"FaceAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_face_angle_z(ws, val):
    """Tilt the head sideways (lean left/right). Negative=Left, Positive=Right."""
    params = {"FaceAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mouth_smile(ws, val):
    """Controls the smiling mouth shape. 0.0=Neutral, 1.0=Full Smile."""
    params = {"MouthSmile": val}
    await vts_inject_parameters(ws, params)

async def move_mouth_open(ws, val):
    """Controls how open the mouth is. 0.0=Closed, 1.0=Open."""
    params = {"MouthOpen": val}
    await vts_inject_parameters(ws, params)

async def move_brows(ws, val):
    """Controls the brow height. 0.0=Neutral, 1.0=Raised (or furrowed depending on model)."""
    params = {"Brows": val}
    await vts_inject_parameters(ws, params)

async def move_tongue_out(ws, val):
    """Controls tongue visibility. 0.0=Hidden, 1.0=Visible."""
    params = {"TongueOut": val}
    await vts_inject_parameters(ws, params)

async def move_cheek_puff(ws, val):
    """Controls cheek puffing. 0.0=None, 1.0=Max puff."""
    params = {"CheekPuff": val}
    await vts_inject_parameters(ws, params)

async def move_face_angry(ws, val):
    """Controls angry expression. 0.0=Neutral, 1.0=Angry."""
    params = {"FaceAngry": val}
    await vts_inject_parameters(ws, params)

async def move_brow_left_y(ws, val):
    """Controls the height of the left eyebrow."""
    params = {"BrowLeftY": val}
    await vts_inject_parameters(ws, params)

async def move_brow_right_y(ws, val):
    """Controls the height of the right eyebrow."""
    params = {"BrowRightY": val}
    await vts_inject_parameters(ws, params)

async def move_eye_open_left(ws, val):
    """Controls opening of the left eye. 0.0=Closed, 1.0=Open."""
    params = {"EyeOpenLeft": val}
    await vts_inject_parameters(ws, params)

async def move_eye_open_right(ws, val):
    """Controls opening of the right eye. 0.0=Closed, 1.0=Open."""
    params = {"EyeOpenRight": val}
    await vts_inject_parameters(ws, params)

async def move_eye_left_x(ws, val):
    """Controls horizontal gaze of the left eye (look left/right)."""
    params = {"EyeLeftX": val}
    await vts_inject_parameters(ws, params)

async def move_eye_left_y(ws, val):
    """Controls vertical gaze of the left eye (look up/down)."""
    params = {"EyeLeftY": val}
    await vts_inject_parameters(ws, params)

async def move_eye_right_x(ws, val):
    """Controls horizontal gaze of the right eye (look left/right)."""
    params = {"EyeRightX": val}
    await vts_inject_parameters(ws, params)

async def move_eye_right_y(ws, val):
    """Controls vertical gaze of the right eye (look up/down)."""
    params = {"EyeRightY": val}
    await vts_inject_parameters(ws, params)

async def move_mouse_position_x(ws, val):
    """Screen X position of the mouse."""
    params = {"MousePositionX": val}
    await vts_inject_parameters(ws, params)

async def move_mouse_position_y(ws, val):
    """Screen Y position of the mouse."""
    params = {"MousePositionY": val}
    await vts_inject_parameters(ws, params)

async def move_voice_volume(ws, val):
    """Parameter driven by microphone volume."""
    params = {"VoiceVolume": val}
    await vts_inject_parameters(ws, params)

async def move_voice_frequency(ws, val):
    """Parameter driven by microphone frequency."""
    params = {"VoiceFrequency": val}
    await vts_inject_parameters(ws, params)

async def move_voice_volume_plus_mouth_open(ws, val):
    """Combined parameter for lip sync (Volume + MouthOpen)."""
    params = {"VoiceVolumePlusMouthOpen": val}
    await vts_inject_parameters(ws, params)

async def move_voice_frequency_plus_mouth_smile(ws, val):
    """Combined parameter for lip sync (Freq + Smile)."""
    params = {"VoiceFrequencyPlusMouthSmile": val}
    await vts_inject_parameters(ws, params)

async def move_voice_a(ws, val):
    """Vowel shape 'A'."""
    params = {"VoiceA": val}
    await vts_inject_parameters(ws, params)

async def move_voice_i(ws, val):
    """Vowel shape 'I'."""
    params = {"VoiceI": val}
    await vts_inject_parameters(ws, params)

async def move_voice_u(ws, val):
    """Vowel shape 'U'."""
    params = {"VoiceU": val}
    await vts_inject_parameters(ws, params)

async def move_voice_e(ws, val):
    """Vowel shape 'E'."""
    params = {"VoiceE": val}
    await vts_inject_parameters(ws, params)

async def move_voice_o(ws, val):
    """Vowel shape 'O'."""
    params = {"VoiceO": val}
    await vts_inject_parameters(ws, params)

async def move_voice_silence(ws, val):
    """Likelihood of silence."""
    params = {"VoiceSilence": val}
    await vts_inject_parameters(ws, params)

async def move_mouth_x(ws, val):
    """Controls mouth width/form horizontally."""
    params = {"MouthX": val}
    await vts_inject_parameters(ws, params)


