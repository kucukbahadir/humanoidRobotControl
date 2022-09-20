import cv2
import numpy as np
import mediapipe as mp

drawing_mp = mp.solutions.drawing_utils
pose_mp = mp.solutions.pose
face_mesh_mp = mp.solutions.face_mesh
mp_hands = mp.solutions.hands


def scale_angle(value, axis): # scaling for the degree of freedom of human head.
    if axis == "x":
        degree = value * 360 *3
        radian = degree * np.pi/180
        return round(degree), round(radian,4)
    if axis == "y":
        degree = value * 360 * 4.9
        radian = degree * np.pi/180
        return round(degree), round(radian,4)


def get_head_positions(image, results, angle_type, show_text=True):
    output = {
        "Pitch" : {
            "Degree" : None ,
            "Radian" : None
        } ,
        "Yaw" : {
            "Degree" : None ,
            "Radian" : None
        }
    }
    img_h , img_w , img_c = image.shape
    face_3d = []
    face_2d = []

    if results.multi_face_landmarks :
        for face_landmarks in results.multi_face_landmarks :
            drawing_spec = drawing_mp.DrawingSpec(thickness=1, circle_radius=1)

            for idx , landmark in enumerate(face_landmarks.landmark) :
                # borders of head mesh
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    x, y = int(landmark.x * img_w) , int(landmark.y * img_h)
                    face_2d.append([x , y]) # 2D Coordinates
                    face_3d.append([x , y , landmark.z]) # 3D Coordinates

            face_2d = np.array(face_2d , dtype=np.float64)
            face_3d = np.array(face_3d , dtype=np.float64)


            focal_length = 1 * img_w # default calibration
            camera_matrix = np.array([[focal_length, 0, img_h / 2], [0, focal_length, img_w / 2], [0 , 0 , 1]])
            # The distortion parameters
            distortion_matrix = np.zeros((4 , 1) , dtype=np.float64)
            # PnP Problem
            success , rotational_vector , trans_vec = cv2.solvePnP(face_3d , face_2d , camera_matrix , distortion_matrix)
            # Get rotational matrix
            rotational_matrix , jacobian = cv2.Rodrigues(rotational_vector)
            # Get angles
            angles , matrixR , matrixQ , QX , QY , QZ = cv2.RQDecomp3x3(rotational_matrix)

            head_pitch_degree, head_pitch_radian = scale_angle(angles[0],"x")
            head_yaw_degree, head_yaw_radian = scale_angle(angles[1],"y")

            drawing_mp.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=face_mesh_mp.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)

            if show_text:
                if angle_type == "Degree":
                    cv2.putText(image,"HeadPitch: " + str(head_pitch_degree) + "        HeadYaw: " + str(head_yaw_degree), (image.shape[1]//2-290,100), cv2.FONT_HERSHEY_SIMPLEX , 1 , (255 , 255 , 255) , 2)

            output["Pitch"]["Degree"] = head_pitch_degree
            output["Pitch"]["Radian"] = head_pitch_radian
            output["Yaw"]["Degree"] = head_yaw_degree
            output["Yaw"]["Radian"] = head_yaw_radian

    return output

