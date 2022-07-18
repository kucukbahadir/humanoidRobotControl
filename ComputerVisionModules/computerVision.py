import cv2
import mediapipe as mp
import numpy as np
from ComputerVisionModules import Shoulders, LandmarksModule, Elbows, Head, Hands, Hips
from ProgramOutputModule import OutputModule

drawing_mp = mp.solutions.drawing_utils
pose_mp = mp.solutions.pose
face_mesh_mp = mp.solutions.face_mesh
mp_hands = mp.solutions.hands


face_mesh = face_mesh_mp.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands_pose = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
pose = pose_mp.Pose(min_detection_confidence=0.5 , min_tracking_confidence=0.5)


shoulders = Shoulders.Shoulders()
elbows = Elbows.Elbows()
hips = Hips.Hips()
hands_module = Hands
landmark_handler = LandmarksModule.Landmarks()
program_output = OutputModule.Output()

ANGLE_TYPE = "Degree"
arr = []


def run_computer_vision(frame, interface_inputs):

    arr = []
    frame_counter = 1

    # Recolor image BGR to RGB
    image = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)
    image.flags.writeable = False

    face_results = face_mesh.process(image)
    body_results = pose.process(image)
    hand_results = hands_pose.process(image)

    if body_results.pose_landmarks:
        body_info = landmark_handler.get_body_landmarks_info(body_results , image)

    else :
        # print("Take a good position or there is an error")
        return image


    image.flags.writeable = True


    if interface_inputs["BlackBackground"]:
        image = np.zeros(image.shape, np.uint8)
    else:
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if interface_inputs["Head"]:
        head_angle = Head.get_head_positions(image , face_results , ANGLE_TYPE ,
                                             show_text=interface_inputs["HeadText"])
        program_output.output["Angles"]["Head"] = head_angle

    if interface_inputs["Shoulders"]:
        shoulders_angle = shoulders.get_shoulders_info(image, body_info, ANGLE_TYPE,
                                                       show_text=interface_inputs["UpperBodyText"])
        program_output.output["Angles"]["Shoulders"] = shoulders_angle

    if interface_inputs["Elbows"]:
        elbows_angle = elbows.get_elbows_info(image, body_info, ANGLE_TYPE,
                                              show_text=interface_inputs["UpperBodyText"])
        program_output.output["Angles"]["Elbows"] = elbows_angle

    if interface_inputs["Hands"]:
        hands_status = hands_module.get_hand_status(image, hand_results,
                                                    show_text=interface_inputs["HandsText"])
        program_output.output["Status"]["Hands"] = hands_status

    # //////////////////////// CAN BE DEVELOPED ///////////////////////////////////
    # hips_angle = hips.get_hips_info(image , body_info , ANGLE_TYPE , show_text=True)
    # program_output.ProgramOutputModule["Angles"]["Hips"] = hips_angle
    # //////////////////////// CAN BE DEVELOPED ///////////////////////////////////

    drawing_mp.draw_landmarks(image, body_results.pose_landmarks, pose_mp.POSE_CONNECTIONS,
                              drawing_mp.DrawingSpec(color=(255, 255, 255), thickness=5, circle_radius=5),
                              drawing_mp.DrawingSpec(color=(0, 94, 255), thickness=15, circle_radius=5)
                              )


    frame_counter += 1

    program_output.write_json_data("./output.json")

    cv2.waitKey(1)

    return image


