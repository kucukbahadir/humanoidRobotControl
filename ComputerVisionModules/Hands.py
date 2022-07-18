import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def get_label(index, hand, results, shape):
    output = None

    for idx, classification in enumerate(results.multi_handedness ):
        if classification.classification[0].index == index:

            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array
                    ((hand.landmark[mp_hands.HandLandmark.WRIST]. x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [shape[1] ,shape[0]]).astype(int))

            output = text, coords

    return output

joint_list = [[8,5,0], [12,9,0], [16,13,0], [20,17,0]]


def get_angles(image , hand, joint_combinations) :
    # Loop through hands
    angle_list = []

    # Loop through joint sets
    for joint in joint_combinations :
        a = np.array([hand.landmark[joint[0]].x , hand.landmark[joint[0]].y])  # First coord
        b = np.array([hand.landmark[joint[1]].x , hand.landmark[joint[1]].y])  # Second coord
        c = np.array([hand.landmark[joint[2]].x , hand.landmark[joint[2]].y])  # Third coord

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0 :
            angle = 360 - angle
        angle_list.append(angle)

        cv2.putText(image , str(round(angle)) , tuple(np.multiply(b , [image.shape[1] , image.shape[0]]).astype(int)) ,
                    cv2.FONT_HERSHEY_SIMPLEX , 0.5 , (255 , 255 , 255) , 2 , cv2.LINE_AA)
    return angle_list


def get_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def get_hand_status(image,results,show_text=True):

    output = {
        "Left" : {
            "is_open" : False
        } ,
        "Right" : {
            "is_open" : False
        }
    }
    # Flip on horizontal
    original_image = image
    image = cv2.flip(image , 1)

    if results.multi_hand_landmarks is not None:
        number_of_hands = len(results.multi_hand_landmarks)
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                              results.multi_handedness):

            if handedness.classification[0].label[0:] == "Left":
                angles = get_angles(image , hand_landmarks , joint_list)
                if all(map(lambda i : i > 80 , angles)):
                    output["Right"]["is_open"] = 1
                else:
                    output["Right"]["is_open"] = 0
                if number_of_hands != 2:
                    output["Left"]["is_open"] = None

            if handedness.classification[0].label[0:] == "Right":
                angles = get_angles(image , hand_landmarks , joint_list)
                if all(map(lambda i : i > 80 , angles)) :
                    output["Left"]["is_open"] = 1
                else :
                    output["Left"]["is_open"] = 0
                if number_of_hands != 2:
                    output["Right"]["is_open"] = None


    else:
        output["Left"]["is_open"] = None
        output["Right"]["is_open"] = None
    #

    if show_text:
        if output["Left"]["is_open"]:
            text = "open"
        elif output["Left"]["is_open"] is None:
            text = "No Hand"
        else:
            text = "closed"
        cv2.putText(original_image , "Left Hand" , (image.shape[1] - 200 , image.shape[0] // 2) ,
                    cv2.FONT_HERSHEY_SIMPLEX ,
                    1 , (255 , 255 , 255) , 2, cv2.LINE_AA)

        cv2.putText(original_image , text, (image.shape[1] - 200, image.shape[0] // 2 + 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255 , 255), 2, cv2.LINE_AA)


        if output["Right"]["is_open"]:
            text = "open"
        elif output["Right"]["is_open"] is None:
            text = "No Hand"
        else:
            text = "closed"

        cv2.putText(original_image , "Right Hand", (50, image.shape[0]//2),
                    cv2.FONT_HERSHEY_SIMPLEX ,
                    1 , (255 , 255 , 255) , 2 , cv2.LINE_AA)

        cv2.putText(original_image , text, (50, image.shape[0]//2 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return output
