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

async def move_hand_left_found(ws, val):
    """Whether the left hand acts as being found (1.0) or lost (0.0)."""
    params = {"HandLeftFound": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_found(ws, val):
    """Whether the right hand acts as being found (1.0) or lost (0.0)."""
    params = {"HandRightFound": val}
    await vts_inject_parameters(ws, params)

async def move_both_hands_found(ws, val):
    """Whether both hands act as being found."""
    params = {"BothHandsFound": val}
    await vts_inject_parameters(ws, params)

async def move_hand_distance(ws, val):
    """Distance of hands from camera."""
    params = {"HandDistance": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_position_x(ws, val):
    """X position of the left hand."""
    params = {"HandLeftPositionX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_position_y(ws, val):
    """Y position of the left hand."""
    params = {"HandLeftPositionY": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_position_z(ws, val):
    """Z position of the left hand."""
    params = {"HandLeftPositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_position_x(ws, val):
    """X position of the right hand."""
    params = {"HandRightPositionX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_position_y(ws, val):
    """Y position of the right hand."""
    params = {"HandRightPositionY": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_position_z(ws, val):
    """Z position of the right hand."""
    params = {"HandRightPositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_angle_x(ws, val):
    """Rotation X of left hand."""
    params = {"HandLeftAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_angle_z(ws, val):
    """Rotation Z of left hand."""
    params = {"HandLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_angle_x(ws, val):
    """Rotation X of right hand."""
    params = {"HandRightAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_angle_z(ws, val):
    """Rotation Z of right hand."""
    params = {"HandRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_open(ws, val):
    """How open the left hand is. 0.0=Fist, 1.0=Open palm."""
    params = {"HandLeftOpen": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_open(ws, val):
    """How open the right hand is. 0.0=Fist, 1.0=Open palm."""
    params = {"HandRightOpen": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_1__thumb(ws, val):
    """Left Thumb extension."""
    params = {"HandLeftFinger_1_Thumb": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_2__index(ws, val):
    """Left Index finger extension."""
    params = {"HandLeftFinger_2_Index": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_3__middle(ws, val):
    """Left Middle finger extension."""
    params = {"HandLeftFinger_3_Middle": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_4__ring(ws, val):
    """Left Ring finger extension."""
    params = {"HandLeftFinger_4_Ring": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_5__pinky(ws, val):
    """Left Pinky finger extension."""
    params = {"HandLeftFinger_5_Pinky": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_1__thumb(ws, val):
    """Right Thumb extension."""
    params = {"HandRightFinger_1_Thumb": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_2__index(ws, val):
    """Right Index finger extension."""
    params = {"HandRightFinger_2_Index": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_3__middle(ws, val):
    """Right Middle finger extension."""
    params = {"HandRightFinger_3_Middle": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_4__ring(ws, val):
    """Right Ring finger extension."""
    params = {"HandRightFinger_4_Ring": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_5__pinky(ws, val):
    """Right Pinky finger extension."""
    params = {"HandRightFinger_5_Pinky": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_connected(ws, val):
    """Mocopi tracking parameter for Connected."""
    params = {"MocopiConnected": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_hip_angle_z(ws, val):
    """Mocopi tracking parameter for HipAngleZ."""
    params = {"MocopiHipAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_angle_x(ws, val):
    """Mocopi tracking parameter for AngleX."""
    params = {"MocopiAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_angle_y(ws, val):
    """Mocopi tracking parameter for AngleY."""
    params = {"MocopiAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_angle_z(ws, val):
    """Mocopi tracking parameter for AngleZ."""
    params = {"MocopiAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_angle_x(ws, val):
    """Mocopi tracking parameter for BodyAngleX."""
    params = {"MocopiBodyAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_angle_y(ws, val):
    """Mocopi tracking parameter for BodyAngleY."""
    params = {"MocopiBodyAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_angle_z(ws, val):
    """Mocopi tracking parameter for BodyAngleZ."""
    params = {"MocopiBodyAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_position_x(ws, val):
    """Mocopi tracking parameter for BodyPositionX."""
    params = {"MocopiBodyPositionX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_position_y(ws, val):
    """Mocopi tracking parameter for BodyPositionY."""
    params = {"MocopiBodyPositionY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_position_z(ws, val):
    """Mocopi tracking parameter for BodyPositionZ."""
    params = {"MocopiBodyPositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_left_angle_y(ws, val):
    """Mocopi tracking parameter for UpperArmLeftAngleY."""
    params = {"MocopiUpperArmLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_left_angle_z(ws, val):
    """Mocopi tracking parameter for UpperArmLeftAngleZ."""
    params = {"MocopiUpperArmLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_right_angle_y(ws, val):
    """Mocopi tracking parameter for UpperArmRightAngleY."""
    params = {"MocopiUpperArmRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_right_angle_z(ws, val):
    """Mocopi tracking parameter for UpperArmRightAngleZ."""
    params = {"MocopiUpperArmRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_left_angle_x(ws, val):
    """Mocopi tracking parameter for LowerArmLeftAngleX."""
    params = {"MocopiLowerArmLeftAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_left_angle_y(ws, val):
    """Mocopi tracking parameter for LowerArmLeftAngleY."""
    params = {"MocopiLowerArmLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_left_angle_z(ws, val):
    """Mocopi tracking parameter for LowerArmLeftAngleZ."""
    params = {"MocopiLowerArmLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_right_angle_x(ws, val):
    """Mocopi tracking parameter for LowerArmRightAngleX."""
    params = {"MocopiLowerArmRightAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_right_angle_y(ws, val):
    """Mocopi tracking parameter for LowerArmRightAngleY."""
    params = {"MocopiLowerArmRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_right_angle_z(ws, val):
    """Mocopi tracking parameter for LowerArmRightAngleZ."""
    params = {"MocopiLowerArmRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_left_angle_y(ws, val):
    """Mocopi tracking parameter for UpperLegLeftAngleY."""
    params = {"MocopiUpperLegLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_left_angle_z(ws, val):
    """Mocopi tracking parameter for UpperLegLeftAngleZ."""
    params = {"MocopiUpperLegLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_right_angle_y(ws, val):
    """Mocopi tracking parameter for UpperLegRightAngleY."""
    params = {"MocopiUpperLegRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_right_angle_z(ws, val):
    """Mocopi tracking parameter for UpperLegRightAngleZ."""
    params = {"MocopiUpperLegRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_left_angle_y(ws, val):
    """Mocopi tracking parameter for LowerLegLeftAngleY."""
    params = {"MocopiLowerLegLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_left_angle_z(ws, val):
    """Mocopi tracking parameter for LowerLegLeftAngleZ."""
    params = {"MocopiLowerLegLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_right_angle_y(ws, val):
    """Mocopi tracking parameter for LowerLegRightAngleY."""
    params = {"MocopiLowerLegRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_right_angle_z(ws, val):
    """Mocopi tracking parameter for LowerLegRightAngleZ."""
    params = {"MocopiLowerLegRightAngleZ": val}
    await vts_inject_parameters(ws, params)

