#!/usr/bin/env python
# coding: utf-8

from secrets import randbelow
import sys
import time
import pybullet as p
import numpy as np
import json
from qibullet import SimulationManager
from qibullet import PepperVirtual
from qibullet import NaoVirtual


# Dict for mapping joints onto robot
def get_joint_values(data, joint_name, angle_type="Radian"):

    angles = data["Angles"]
    status = data["Status"] 
    
    joint_angle_dict = {
        "HeadPitch" : angles["Head"]["Pitch"][angle_type],
        "HeadYaw" : angles["Head"]["Yaw"][angle_type],
        
        "LShoulderRoll" : angles["Shoulders"]["Left"]["Roll"][angle_type],
        "LShoulderPitch" : angles["Shoulders"]["Left"]["Pitch"][angle_type],

        "RShoulderRoll" : angles["Shoulders"]["Right"]["Roll"][angle_type],
        "RShoulderPitch" : angles["Shoulders"]["Right"]["Pitch"][angle_type],

        "LElbowRoll" : angles["Elbows"]["Left"]["Roll"][angle_type],
        "RElbowRoll" : angles["Elbows"]["Right"]["Roll"][angle_type],

        "LHand" : status["Hands"]["Left"]["is_open"],
        "RHand" : status["Hands"]["Right"]["is_open"],

        # "LHipRoll" : angles["Hips"]["Left"]["Roll"][angle_type],
        # "RHipRoll" : angles["Hips"]["Right"]["Roll"][angle_type]
    }

        
    return joint_angle_dict[joint_name]


def get_json_file(path):
    try:
        with open(path,"r",encoding="utf-8") as dfile :
            return json.load(dfile)
    except:
        print("Couldn't read JSON file !!!!!!!!!!!!!!")
        pass


def scale_radian(value, joint_name):
    # Dict for getting max and min angles
    dictionaryAngles = {
        "HeadYaw" : {
            "Min" : -2.0857,
            "Max" : 2.0857
        },
        "HeadPitch" : {
            "Min" : -0.6720,
            "Max" : 0.5149
        },
        "LShoulderRoll" :{
            "Min" : -0.3142,
            "Max" : 1.3265
        },
        "LShoulderPitch" : {
            "Min" : -2.0857,
            "Max" : 2.0857
        },
        "RShoulderRoll" : {
            "Min" : -1.3265,
            "Max" : 0.3142
        },
        "RShoulderPitch" : {
            "Min" : -2.0857,
            "Max" : 2.0857
        },
        "LElbowYaw" : {
            "Min" : -2.0857,
            "Max" : 2.0857
        },
        "LElbowRoll" : {
            "Min" : -1.5446,
            "Max" : -0.0349
        },
        "LWristYaw" : {
            "Min" : -1.8238,
            "Max" : 1.8238
        },
        "RElbowYaw" : {
            "Min" : -2.0857,
            "Max" : 2.0857
        },
        "RElbowRoll" : {
            "Min" : 0.0349,
            "Max" : 1.5446
        },
        "RWristYaw" : {
            "Min" : -1.8238,
            "Max" : 1.8238
        },
        "LHipRoll" : {
            "Min" : -0.379472,
            "Max" : 0.790477,
        },    
        "RHipRoll" : {
            "Min" : -0.790477,
            "Max" : 0.379472,
        },
        "LHand" : {
            "Min" : 0.0,
            "Max" : 1.0
        },
        "RHand" : {
            "Min" : 0.0,
            "Max" : 1.0
        }
    }

    if value > dictionaryAngles[joint_name]["Max"]:
        value = dictionaryAngles[joint_name]["Max"]
    if value < dictionaryAngles[joint_name]["Min"]:
        value = dictionaryAngles[joint_name]["Min"]
    
    return value

def get_simulation_mouse_input(joint_parameters):
          
    for joint_parameter in joint_parameters:
        input = p.readUserDebugParameter(joint_parameter[0])
        
        robot.setAngles(
            joint_parameter[1],
            p.readUserDebugParameter(joint_parameter[0]), 1.0)

    # Step the simulation
    simulation_manager.stepSimulation(client)


def run_simulation():
    global simulation_manager
    simulation_manager = SimulationManager()

    if (sys.version_info > (3, 0)):
        # rob = input("Which robot should be spawned? (pepper/nao): ")
        rob = "nao"

    # Auto stepping set to False, the user has to manually step the simulation
    global client
    client = simulation_manager.launchSimulation(gui=True, auto_step=False)
    global robot

    if rob.lower() == "nao":
        robot = simulation_manager.spawnNao(client, spawn_ground_plane=True)
    elif rob.lower() == "pepper":
        robot = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    else:
        print("You have to specify a robot, pepper, nao or romeo.")
        simulation_manager.stopSimulation(client)
        sys.exit(1)

    time.sleep(1.0)
    joint_parameters = list()
    p.resetDebugVisualizerCamera( cameraDistance=1, cameraYaw=90, cameraPitch=-30, cameraTargetPosition=[0,0,0])


    for name, joint in robot.joint_dict.items():
        if "Finger" not in name and "Thumb" not in name:
            joint_parameters.append((
                p.addUserDebugParameter(
                    name,
                    joint.getLowerLimit(),
                    joint.getUpperLimit(),
                    robot.getAnglesPosition(name)),
                name))

    index = 0
    counter = 0

    path = "../output.json"

    try:
        while True:
            if counter % 10 == 0:
                try: 
                    data = get_json_file(path)

                except:
                    print("Couldn't read angle from JSON file.")
                    continue
                joint_names = ["LShoulderRoll", "LShoulderPitch","RShoulderRoll","RShoulderPitch",
                "HeadYaw","HeadPitch", "LElbowRoll", "RElbowRoll", "LHand", "RHand"]


                for i in range(len(joint_names)):

                    try:
                        radian = get_joint_values(data, joint_names[i])

                    except:
                        print("error but program continues")
                        continue

                    if radian == None:
                        continue
                    
                    if joint_names[i] == "LShoulderPitch" or joint_names[i] == "RShoulderPitch":
                        radian = 1.5708 - radian

                    elif joint_names[i] == "HeadPitch":
                        radian = -radian

                    elif joint_names[i] == "RShoulderRoll":
                        
                        if radian > np.pi/2:
                            radian = -radian
                        if data["Angles"]["Shoulders"]["Right"]["Pitch"]["Degree"] >40:
                            radian = radian + np.pi/10


                    elif joint_names[i] == "LShoulderRoll":
                        
                        if data["Angles"]["Shoulders"]["Right"]["Pitch"]["Degree"] >40:
                            radian = radian - np.pi/10
                        

                    elif joint_names[i] == "RElbowRoll":
                        if radian > 0:
                            radian = np.pi-radian
                        else:
                            radian = np.pi+radian

                    elif joint_names[i] == "LElbowRoll":

                        if radian < 0:
                            radian = -radian-np.pi
                        else:
                            radian = radian-np.pi

                        if radian > 0:
                            radian = -radian
                    
                    try:
                        
                        radian = scale_radian(radian,joint_names[i])
                        
                    except:
                        print("could not scaled")

                    if radian == None:
                        radian = 0
                    try:
                        robot.setAngles(
                        joint_names[i],
                        radian, 1.0)
                    except:
                        print("could not set angle")
            # Step the simulation
            simulation_manager.stepSimulation(client)
            counter += 1

        # # while True:
        #     get_simulation_mouse_input(joint_parameters)

       
    except KeyboardInterrupt:
        pass
    finally:
        simulation_manager.stopSimulation(client)


run_simulation()