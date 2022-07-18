import math

import numpy as np

from ComputerVisionModules import Utils


class Shoulders(Utils.Utils) :

    def __init__(self) :
        super().__init__()
        self.shoulders = ["left_shoulder" , "right_shoulder"]
        self.joint_combinations = {  # 3 points needed to calculate an angle
            11 : (13 , 11 , 23) ,  # left_shoulder : (left_elbow, left_shoulder, left_hip)
            12 : (14 , 12 , 24) ,  # right_shoulder : (right_elbow , right_shoulder, right_hip)
        }
        self.shoulders_output = {
            "Left" : {
                "Roll" : {
                    "Degree" : 0 ,
                    "Radian" : 0
                } ,
                "Pitch" : {
                    "Degree" : 0 ,
                    "Radian" : 0
                }
            } ,
            "Right" : {
                "Roll" : {
                    "Degree" : 0 ,
                    "Radian" : 0
                } ,
                "Pitch" : {
                    "Degree" : 0 ,
                    "Radian" : 0
                }
            }
        }
        self.textColor = (250, 250, 250)

    # def correct_pitch(self, angle, points):
    #     if angle["Degree"] > 45:
    #         if round(abs(points[0][0] - points[1][0]) // self.Z_MAGNITUDE) < 30:
    #             corrected_degree = round(math.sqrt(self.get_angle(points, dimension="YZ")["Degree"]))
    #             angle["Degree"] = corrected_degree
    #             angle["Radian"] = np.deg2rad(corrected_degree)
    #
    #     return angle
    #
    def correct_roll(self, roll_angle, pitch_angle, points):
        if round(abs(points[0][0] - points[1][0])) < 80:
            if pitch_angle["Degree"] > 80:
                roll_angle["Degree"] = 10
                roll_angle["Radian"] = np.deg2rad(roll_angle["Degree"])

        return roll_angle

    def get_shoulders_info(self, image, body_landmarks, angle_type, show_text=True) :

        for shoulder in self.shoulders:
            shoulder_id = self.landmarks_name_id_dict[shoulder]
            p1, p2, p3 = self.joint_combinations[shoulder_id]
            points = (body_landmarks[p1], body_landmarks[p2], body_landmarks[p3])

            x = int(body_landmarks[shoulder_id][0])
            y = int(body_landmarks[shoulder_id][1])

            if shoulder == "left_shoulder":
                left_angle_roll = self.get_angle(points , dimension="XY")
                # left_angle_pitch = self.correct_pitch(self.get_angle(points, dimension="YZ"), points)
                left_angle_pitch = self.get_angle(points , dimension="YZ")

                left_angle_roll = self.correct_roll(left_angle_roll, left_angle_pitch, points)

                self.shoulders_output["Left"]["Roll"] = left_angle_roll
                self.shoulders_output["Left"]["Pitch"] = left_angle_pitch

                if show_text:
                    text = "(" + str(abs(left_angle_roll[angle_type])) + "," + str(abs(left_angle_pitch[angle_type])) + ")"
                    self.visualize_text(image=image, coordinate=(x+20, y), text=text, color=self.textColor)

            if shoulder == "right_shoulder":
                right_angle_roll = self.get_angle(points , dimension="XY")
                # right_angle_pitch = self.correct_pitch(self.get_angle(points, dimension="YZ"), points)
                right_angle_pitch = self.get_angle(points, dimension="YZ")
                right_angle_roll = self.correct_roll(right_angle_roll, right_angle_pitch, points)

                self.shoulders_output["Right"]["Roll"] = right_angle_roll
                self.shoulders_output["Right"]["Pitch"] = right_angle_pitch

                if show_text:
                    text = "(" + str(abs(right_angle_roll[angle_type])) + "," + str(abs(right_angle_pitch[angle_type])) + ")"
                    self.visualize_text(image , coordinate=(x-130, y), text=text, color=self.textColor)

        return self.shoulders_output
