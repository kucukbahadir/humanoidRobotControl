from ComputerVisionModules import Utils
import numpy as np
from ComputerVisionModules import LandmarksModule

class Elbows(Utils.Utils):

    def __init__(self):
        super().__init__()
        self.elbows = ["left_elbow", "right_elbow"]
        self.joint_combinations = {   # 3 points needed to calculate an angle
            13: (11, 13, 15),   # left_elbow : (left_shoulder, left_elbow, left_wrist)
            14: (16, 14, 12)    # right_elbow : (right_shoulder, right_elbow, right_wrist)
        }
        self.elbows_output = {
          "Left": {
            "Roll": {
              "Degree": 180,
              "Radian": np.pi
            }
          },
          "Right": {
            "Roll": {
              "Degree": 180,
              "Radian": np.pi
            }
          }
        }
        self.textColor = (250 , 250 , 250)


    def get_elbows_info(self, image, body_landmarks, angle_type = "Degree", show_text=True):

        for elbow in self.elbows:
            elbow_id = self.landmarks_name_id_dict[elbow]
            p1, p2, p3 = self.joint_combinations[elbow_id]
            points = (body_landmarks[p1], body_landmarks[p2], body_landmarks[p3])

            x = int(body_landmarks[elbow_id][0])
            y = int(body_landmarks[elbow_id][1])

            if elbow == "left_elbow":
                left_angle_roll = self.get_angle(points, dimension="XY")
                self.elbows_output["Left"]["Roll"] = left_angle_roll

                if show_text:
                    text = "(" + str(abs(left_angle_roll[angle_type])) + ")"
                    self.visualize_text(image=image, coordinate=(x+20, y), text=text, color=self.textColor)
        #
            if elbow == "right_elbow":
                right_angle_roll = self.get_angle(points, dimension="XY")
                self.elbows_output["Right"]["Roll"] = right_angle_roll

                if show_text:
                    text = "(" + str(abs(right_angle_roll[angle_type])) + ")"
                    self.visualize_text(image, coordinate=(x-100, y), text=text, color=self.textColor)

        return self.elbows_output
