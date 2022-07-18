from ComputerVisionModules import Utils

class Hips(Utils.Utils):

    def __init__(self):
        super().__init__()
        self.hips = ["left_hip", "right_hip"]
        self.joint_combinations = {   # 3 points needed to calculate an angle
            23: (11, 23, 25),     # left_hip : (left_shoulder, left_hip, left_knee)
            24: (12, 24, 26),     # right_hip : (right_shoulder, right_hip, right_knee)
        }
        self.hips_output = {
          "Left": {
            "Roll": {
              "Degree": None,
              "Radian": None
            },
            "Pitch": {
              "Degree": None,
              "Radian": None
            }
          },
          "Right": {
            "Roll": {
              "Degree": None,
              "Radian": None
            },
            "Pitch": {
              "Degree": None,
              "Radian": None
            }
          }
        }
        self.textColor = (250 , 250 , 250)


    def get_hips_info(self, image, body_landmarks, angle_type = "Degree", show_text=True):

        for hip in self.hips:
            hip_id = self.landmarks_name_id_dict[hip]
            p1, p2, p3 = self.joint_combinations[hip_id]
            points = (body_landmarks[p1], body_landmarks[p2], body_landmarks[p3])

            x = int(body_landmarks[hip_id][0])
            y = int(body_landmarks[hip_id][1])

            if hip == "left_hip":
                left_angle_roll = self.get_angle(points, dimension="XY")
                left_angle_pitch = self.get_angle(points, dimension="YZ")

                self.hips_output["Left"]["Roll"] = left_angle_roll
                self.hips_output["Left"]["Pitch"] = left_angle_pitch

                if show_text:
                    text = "(" + str(left_angle_roll[angle_type]) + "," + str(left_angle_pitch[angle_type]) + ")"
                    self.visualize_text(image=image, coordinate=(x, y), text=text, color=self.textColor)

            if hip == "right_hip":
                right_angle_roll = self.get_angle(points, dimension="XY")
                right_angle_pitch = self.get_angle(points, dimension="YZ")

                self.hips_output["Right"]["Roll"] = right_angle_roll
                self.hips_output["Right"]["Pitch"] = right_angle_pitch

                if show_text:
                    text = "(" + str(right_angle_roll[angle_type]) + "," + str(right_angle_pitch[angle_type]) + ")"
                    self.visualize_text(image, coordinate=(x-150, y), text=text, color=self.textColor)

        return self.hips_output
