from ComputerVisionModules import Utils


class Landmarks(Utils.Utils):
    def __init__(self):
        super().__init__()
        self.body_landmarks_info = {}
        self.head_landmarks_info = {}
        self.hand_landmarks_info = {}

    def get_body_landmarks_info(self, results, image) :

        for id, landmark in enumerate(results.pose_landmarks.landmark) :
            x = results.pose_landmarks.landmark[id].x
            y = results.pose_landmarks.landmark[id].y
            z = results.pose_landmarks.landmark[id].z
            visibility = results.pose_landmarks.landmark[13].visibility

            coordinates = self.get_coordinate_of_point((x, y, z), image)
            self.body_landmarks_info[id] = coordinates + (visibility,)

        return self.body_landmarks_info
