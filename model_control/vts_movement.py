from vts_client import vts_inject_parameters

async def move_face_position_x(ws, val):
    params = {"FacePositionX": val}
    await vts_inject_parameters(ws, params)

async def move_face_position_y(ws, val):
    params = {"FacePositionY": val}
    await vts_inject_parameters(ws, params)

async def move_face_position_z(ws, val):
    params = {"FacePositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_face_angle_x(ws, val):
    params = {"FaceAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_face_angle_y(ws, val):
    params = {"FaceAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_face_angle_z(ws, val):
    params = {"FaceAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mouth_smile(ws, val):
    params = {"MouthSmile": val}
    await vts_inject_parameters(ws, params)

async def move_mouth_open(ws, val):
    params = {"MouthOpen": val}
    await vts_inject_parameters(ws, params)

async def move_brows(ws, val):
    params = {"Brows": val}
    await vts_inject_parameters(ws, params)

async def move_tongue_out(ws, val):
    params = {"TongueOut": val}
    await vts_inject_parameters(ws, params)

async def move_cheek_puff(ws, val):
    params = {"CheekPuff": val}
    await vts_inject_parameters(ws, params)

async def move_face_angry(ws, val):
    params = {"FaceAngry": val}
    await vts_inject_parameters(ws, params)

async def move_brow_left_y(ws, val):
    params = {"BrowLeftY": val}
    await vts_inject_parameters(ws, params)

async def move_brow_right_y(ws, val):
    params = {"BrowRightY": val}
    await vts_inject_parameters(ws, params)

async def move_eye_open_left(ws, val):
    params = {"EyeOpenLeft": val}
    await vts_inject_parameters(ws, params)

async def move_eye_open_right(ws, val):
    params = {"EyeOpenRight": val}
    await vts_inject_parameters(ws, params)

async def move_eye_left_x(ws, val):
    params = {"EyeLeftX": val}
    await vts_inject_parameters(ws, params)

async def move_eye_left_y(ws, val):
    params = {"EyeLeftY": val}
    await vts_inject_parameters(ws, params)

async def move_eye_right_x(ws, val):
    params = {"EyeRightX": val}
    await vts_inject_parameters(ws, params)

async def move_eye_right_y(ws, val):
    params = {"EyeRightY": val}
    await vts_inject_parameters(ws, params)

async def move_mouse_position_x(ws, val):
    params = {"MousePositionX": val}
    await vts_inject_parameters(ws, params)

async def move_mouse_position_y(ws, val):
    params = {"MousePositionY": val}
    await vts_inject_parameters(ws, params)

async def move_voice_volume(ws, val):
    params = {"VoiceVolume": val}
    await vts_inject_parameters(ws, params)

async def move_voice_frequency(ws, val):
    params = {"VoiceFrequency": val}
    await vts_inject_parameters(ws, params)

async def move_voice_volume_plus_mouth_open(ws, val):
    params = {"VoiceVolumePlusMouthOpen": val}
    await vts_inject_parameters(ws, params)

async def move_voice_frequency_plus_mouth_smile(ws, val):
    params = {"VoiceFrequencyPlusMouthSmile": val}
    await vts_inject_parameters(ws, params)

async def move_voice_a(ws, val):
    params = {"VoiceA": val}
    await vts_inject_parameters(ws, params)

async def move_voice_i(ws, val):
    params = {"VoiceI": val}
    await vts_inject_parameters(ws, params)

async def move_voice_u(ws, val):
    params = {"VoiceU": val}
    await vts_inject_parameters(ws, params)

async def move_voice_e(ws, val):
    params = {"VoiceE": val}
    await vts_inject_parameters(ws, params)

async def move_voice_o(ws, val):
    params = {"VoiceO": val}
    await vts_inject_parameters(ws, params)

async def move_voice_silence(ws, val):
    params = {"VoiceSilence": val}
    await vts_inject_parameters(ws, params)

async def move_mouth_x(ws, val):
    params = {"MouthX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_found(ws, val):
    params = {"HandLeftFound": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_found(ws, val):
    params = {"HandRightFound": val}
    await vts_inject_parameters(ws, params)

async def move_both_hands_found(ws, val):
    params = {"BothHandsFound": val}
    await vts_inject_parameters(ws, params)

async def move_hand_distance(ws, val):
    params = {"HandDistance": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_position_x(ws, val):
    params = {"HandLeftPositionX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_position_y(ws, val):
    params = {"HandLeftPositionY": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_position_z(ws, val):
    params = {"HandLeftPositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_position_x(ws, val):
    params = {"HandRightPositionX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_position_y(ws, val):
    params = {"HandRightPositionY": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_position_z(ws, val):
    params = {"HandRightPositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_angle_x(ws, val):
    params = {"HandLeftAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_angle_z(ws, val):
    params = {"HandLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_angle_x(ws, val):
    params = {"HandRightAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_angle_z(ws, val):
    params = {"HandRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_open(ws, val):
    params = {"HandLeftOpen": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_open(ws, val):
    params = {"HandRightOpen": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_1__thumb(ws, val):
    params = {"HandLeftFinger_1_Thumb": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_2__index(ws, val):
    params = {"HandLeftFinger_2_Index": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_3__middle(ws, val):
    params = {"HandLeftFinger_3_Middle": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_4__ring(ws, val):
    params = {"HandLeftFinger_4_Ring": val}
    await vts_inject_parameters(ws, params)

async def move_hand_left_finger_5__pinky(ws, val):
    params = {"HandLeftFinger_5_Pinky": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_1__thumb(ws, val):
    params = {"HandRightFinger_1_Thumb": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_2__index(ws, val):
    params = {"HandRightFinger_2_Index": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_3__middle(ws, val):
    params = {"HandRightFinger_3_Middle": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_4__ring(ws, val):
    params = {"HandRightFinger_4_Ring": val}
    await vts_inject_parameters(ws, params)

async def move_hand_right_finger_5__pinky(ws, val):
    params = {"HandRightFinger_5_Pinky": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_connected(ws, val):
    params = {"MocopiConnected": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_hip_angle_z(ws, val):
    params = {"MocopiHipAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_angle_x(ws, val):
    params = {"MocopiAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_angle_y(ws, val):
    params = {"MocopiAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_angle_z(ws, val):
    params = {"MocopiAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_angle_x(ws, val):
    params = {"MocopiBodyAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_angle_y(ws, val):
    params = {"MocopiBodyAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_angle_z(ws, val):
    params = {"MocopiBodyAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_position_x(ws, val):
    params = {"MocopiBodyPositionX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_position_y(ws, val):
    params = {"MocopiBodyPositionY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_body_position_z(ws, val):
    params = {"MocopiBodyPositionZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_left_angle_y(ws, val):
    params = {"MocopiUpperArmLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_left_angle_z(ws, val):
    params = {"MocopiUpperArmLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_right_angle_y(ws, val):
    params = {"MocopiUpperArmRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_arm_right_angle_z(ws, val):
    params = {"MocopiUpperArmRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_left_angle_x(ws, val):
    params = {"MocopiLowerArmLeftAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_left_angle_y(ws, val):
    params = {"MocopiLowerArmLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_left_angle_z(ws, val):
    params = {"MocopiLowerArmLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_right_angle_x(ws, val):
    params = {"MocopiLowerArmRightAngleX": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_right_angle_y(ws, val):
    params = {"MocopiLowerArmRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_arm_right_angle_z(ws, val):
    params = {"MocopiLowerArmRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_left_angle_y(ws, val):
    params = {"MocopiUpperLegLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_left_angle_z(ws, val):
    params = {"MocopiUpperLegLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_right_angle_y(ws, val):
    params = {"MocopiUpperLegRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_upper_leg_right_angle_z(ws, val):
    params = {"MocopiUpperLegRightAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_left_angle_y(ws, val):
    params = {"MocopiLowerLegLeftAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_left_angle_z(ws, val):
    params = {"MocopiLowerLegLeftAngleZ": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_right_angle_y(ws, val):
    params = {"MocopiLowerLegRightAngleY": val}
    await vts_inject_parameters(ws, params)

async def move_mocopi_lower_leg_right_angle_z(ws, val):
    params = {"MocopiLowerLegRightAngleZ": val}
    await vts_inject_parameters(ws, params)

