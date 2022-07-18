import json , os , cv2
from ComputerVisionModules import Utils
from ComputerVisionModules.ComputerVision import landmark_handler, body_pose, Shoulders, Elbows

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CMUPanopticDatasetModule() :
    def __init__(self , first_frame , last_frame , data_path) :
        self.data_path = data_path
        self.filter_on = False
        self.first_frame = first_frame
        self.last_frame = last_frame
        self.body_combinations = {
            "left_shoulder" : [6 , 3 , 4] ,  # left_hip, left_shoulder, left_elbow
            "right_shoulder" : [12 , 9 , 10] ,  # right_hip, right_shoulder, right_elbow
            "left_elbow" : [3 , 4 , 5] ,  # left_shoulder, left_elbow, left_wrist
            "right_elbow" : [9 , 10 , 11]  # right_shoulder, right_elbow, right_wrist
        }

        self.results = {
            "FramesBetween" : (self.first_frame , self.last_frame)
        }

    def get_json_data(self , frame) :
        skel_json_fname = self.data_path + 'body3DScene_{0:08d}.json'.format(frame)

        with open(skel_json_fname) as dfile :
            data = json.load(dfile)
            body_joints = data['bodies'][0]['joints19']

        return body_joints

    def split_array(self , coordinate_list) :
        joint_coordinates = {}

        for i in range(0 , len(coordinate_list) , 4) :
            joint_coordinates[i // 4] = coordinate_list[i :i + 4]

        return joint_coordinates

    def change_axis(self,points):
        # Dataset axis (z,y,x) but program axis (x,y,z) thus we have to change them
        return [(points[i][2], points[i][1], points[i][0],points[i][3]) for i in range(len(points))]

    def get_frames_angles(self , joint_name):
        angles = []
        for i in range(self.first_frame , self.last_frame) :
            landmarks_dict = self.split_array(self.get_json_data(i))

            p1, p2, p3 = self.body_combinations[joint_name]

            points = [landmarks_dict[p1] , landmarks_dict[p2], landmarks_dict[p3]]

            angleXY = abs(self.calculate_degree(points, "XY"))

            if joint_name == "left_shoulder" or joint_name == "right_shoulder":
                angleYZ = abs(self.calculate_degree(points, "YZ"))
                angles.append((angleXY, angleYZ))


            elif joint_name == "left_elbow" or joint_name == "right_elbow":
                angles.append(angleXY)

        return angles

    def calculate_degree(self, points , dimension) :
        point1 , point2 , point3 = points

        if (dimension == "XY") :
            radians = np.arctan2(point3[2] - point2[2] ,
                                 point3[1] - point2[1]) - np.arctan2(point1[2] - point2[2] ,
                                                                     point1[1] - point2[1])
        elif (dimension == "YZ") :
            radians = np.arctan2(point3[1] - point2[1] ,
                                 point3[0] - point2[0]) - np.arctan2(point1[1] - point2[1] ,
                                                                     point1[0] - point2[0])

        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0 : angle = 360 - angle

        return int(angle)



    def write_json(self , path) :
        for joint_name in self.body_combinations.keys():
            self.results[joint_name] = self.get_frames_angles(joint_name)

        with open(path + "CMU_Panoptic_Dataset_angles.json", 'w') as file:
            file.seek(0)

            json.dump(self.results, file, ensure_ascii=False)

            file.truncate()


class ProgramEvaluationModule(Utils.Utils):

    def __init__(self , first_frame , last_frame , video_path) :
        self.video_path = video_path
        self.first_frame = first_frame
        self.last_frame = last_frame
        self.filter_on = False
        self.results = {
            "FramesBetween" : (self.first_frame , self.last_frame),
            "left_shoulder" : [],
            "right_shoulder" : [],
            "left_elbow" : [],
            "right_elbow" : []
        }

    def run_video(self) :
        Capture = cv2.VideoCapture(self.video_path)

        frame_counter = 0


        while True :
            ret , frame = Capture.read()

            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image.flags.writeable = False

            if frame_counter >= self.first_frame:
                body_results = body_pose.process(image)

                if body_results.pose_landmarks:
                    body_info = landmark_handler.get_body_landmarks_info(body_results, image)



                    shoulders = Shoulders.Shoulders()
                    shoulders_angle = shoulders.get_shoulders_info(image, body_info)

                    self.results["left_shoulder"].append((shoulders_angle["Left"]["Roll"]["Degree"],
                                                          shoulders_angle["Left"]["Pitch"]["Degree"]))

                    self.results["right_shoulder"].append((shoulders_angle["Right"]["Roll"]["Degree"],
                                                           shoulders_angle["Right"]["Pitch"]["Degree"]))

                    elbows = Elbows.Elbows()
                    elbows_angle = elbows.get_elbows_info(image , body_info)

                    self.results["left_elbow"].append(elbows_angle["Left"]["Roll"]["Degree"])
                    self.results["right_elbow"].append(elbows_angle["Right"]["Roll"]["Degree"])

                else :
                    print("Couldn't get the landmarks")
                    break

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True

            cv2.waitKey(1)
            self.visualize_text(image, (50, 150), "Frame: " + str(frame_counter), 2, 4)
            cv2.imshow("Comparison Video",image)
            frame_counter += 1

            if frame_counter == self.last_frame:
                break

    def write_json(self, path):
        self.run_video()

        with open(path + "program_output_angles.json" , 'w') as file :
            file.seek(0)
            json.dump(self.results , file , ensure_ascii=False)
            file.truncate()

class ComparisonModule():
    def __init__(self, file1_path, file2_path):
        self.dataset_file_path = file1_path
        self.program_file_path = file2_path
        self.dataset_file_data = {}
        self.program_file_data = {}
        self.get_files_data()


    def get_files_data(self):
        self.dataset_file_data = self.get_JSON_file(self.dataset_file_path)
        self.program_file_data = self.get_JSON_file(self.program_file_path)

    def get_JSON_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def draw_line_chart(self, title_info):
        plt.plot( 'x_values', 'y_values', data=self.dataset_angles_df, color='black', label="CMU Panoptic Dataset")
        plt.plot( 'x_values', 'y_values', data=self.program_angles_df, color='green', label="Program")

        plt.xlabel("Frames")
        plt.ylabel("Angles")

        # displaying the title
        plt.title(title_info)
        plt.legend(loc='upper left')
        plt.show()

    def compare_results(self, path, joint_name, explanation):
        if joint_name == "left_shoulder":
            joint_text = "Left Shoulder"
        elif joint_name == "right_shoulder":
            joint_text = "Right Shoulder"

        self.get_dimension_values(joint_name, "XY")
        XY_dimension_results = self.make_results_text("XY")
        self.draw_line_chart(f"Abduction/Adduction Movement - {joint_text}")

        self.get_dimension_values(joint_name, "YZ")
        YZ_dimension_results = self.make_results_text("YZ")
        self.draw_line_chart(f"Flexion/Extension Movement - {joint_text}")

        self.write_result_txt(path, [explanation] + XY_dimension_results + YZ_dimension_results)


    def get_dimension_values(self, joint_name, dimension):
        if dimension == "XY":
            index = 0
        elif dimension == "YZ":
            index = 1
        self.dataset_values = [frame_angle[index] for frame_angle in self.dataset_file_data[joint_name]]

        self.dataset_angles_df = pd.DataFrame({'x_values': range(len(self.dataset_values)),
                                               'y_values': self.dataset_values })

        self.program_values = [frame_angle[index] for frame_angle in self.program_file_data[joint_name]]

        self.program_angles_df = pd.DataFrame({'x_values': range(len(self.program_values)),
                                                'y_values': self.program_values})

    def get_root_mean_square_error(self):
        return round(np.sqrt(np.square(np.subtract(self.dataset_values, self.program_values)).mean()),4)

    def get_standart_deviation(self):
        difference = [abs(self.program_values[i] - self.dataset_values[i]) for i in range(len(self.dataset_values))]
        return round(np.std(difference), 4)

    def make_results_text(self, dimension):
        dimension_text = "Dimension: " + dimension + "\n"
        root_mean_square_error = "Root Mean Square Error: " + str(self.get_root_mean_square_error()) + "\n"
        standard_deviation = "Standard Deviation: " + str(self.get_standart_deviation()) + "\n\n"

        result_text = [dimension_text, root_mean_square_error, standard_deviation]
        return result_text

    def write_result_txt(self, path, lines):
        with open(path + "results.txt", 'w') as file:
            file.writelines(lines)

joint_name = "left_shoulder"
test_number = f"10-{joint_name}"
video_name_dataset = "171204_pose2"
first_frame = 1200
last_frame = 1300
evaluation_results_dir = "../EvaluationResults/" + f"test{test_number}/"
if not os.path.exists(evaluation_results_dir) :
    os.makedirs(evaluation_results_dir)

data_set_dir = f"../../motionDataset/{video_name_dataset}/"
data_path = data_set_dir + "hdPose3d_stage1_coco19/"
video_path = data_set_dir + "hdVideos/hd_00_00.mp4"


test1_dataset_values = CMUPanopticDatasetModule(first_frame, last_frame, data_path)
test1_dataset_values.write_json(evaluation_results_dir)

test1_program_values = ProgramEvaluationModule(first_frame, last_frame, video_path)
test1_program_values.write_json(evaluation_results_dir)


file1_path = evaluation_results_dir + "CMU_Panoptic_Dataset_angles.json"
file2_path = evaluation_results_dir + "program_output_angles.json"
test = ComparisonModule(file1_path, file2_path)
explanation = f"""CMU Panoptic Range of Motion Dataset
Video name: f{video_name_dataset}
Frames between: {str(first_frame)} and {str(last_frame)} \n\n
"""

test.compare_results(evaluation_results_dir, joint_name, explanation)


