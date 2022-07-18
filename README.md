<h3 align="center">Bachelor Thesis</h3>
<h1 align="center">Humanoid Robot Control from Human Joint Angles via 2D Camera</h1>

---

<p align="center">by</p>

<h4 align="center">M. Bahadir Kucuk</h4>

<br>
<br>

<p align="center">Supervisor: Dr. Kim Baraka</p>
<p align="center">Second Reader: Prof. Dr. Koen Hindriks</p>

## Contribution
The goal of this research is to investigate how feasible it is to operate a humanoid robot using human joint angles captured by a 2D camera. 
- Open-closed hand status classifier
- Angles of the human head, shoulders, and elbows
- Tailoring angles to the robot
- Interface
- Ground truth angle comparison results
- Experiment results

## Packages
- Please see requirements.txt

## Installation
- Programming language: Python3 (recommended version is 3.7 or above)
- Clone the repository with
```bash
git clone https://github.com/kucukbahadir/BachelorThesis.git
```
- Install requirement packages with
```bash
pip install -r requirements.txt
```

## Usage
Run both separately
- main.py for the interface
- robot_joint_control.py in "Simulation" folder for the simulation

Place both windows side by side and fix your camera at the distance at least one and half meter in front of you and start to control your humanoid robot.


## Methodology
Please read the methodology section of the thesis.
[link example](M_Bahadir_Kucuk_mkk332_Bachelor_Thesis.pdf)


## Output
Our approach gives an output of JSON file and use this output angles in humanoid robot control.

### Output file example 
```json
{
  "Angles" : {
    "Head" : {
      "Pitch": {
        "Degree": null,
        "Radian": null
      },
      "Yaw": {
        "Degree": null,
        "Radian": null
      }
    },
    "Shoulders": {
      "Left": {
        "Roll": {
          "Degree": null,
          "Radian": null
        },
        "Pitch": {
          "Degree": null,
          "Radian": null
        }
      },
      "Right": {
        "Roll": {
          "Degree": null,
          "Radian": null
        },
        "Pitch": {
          "Degree": null,
          "Radian": null
        }
      }
    },
    "Elbows": {
      "Left":{
        "Roll": {
          "Degree": null,
          "Radian": null
        }
      },
      "Right": {
        "Roll": {
          "Degree": null,
          "Radian": null
        }
      }
    },
    "Wrists": {
      "Left":{
        "Roll": {
          "Degree": null,
          "Radian": null
        }
      },
      "Right": {
        "Roll": {
          "Degree": null,
          "Radian": null
        }
      }
    },
    "Hip": {
      "Left": {
        "Roll" : {
          "Degree": null,
          "Radian": null
        },
        "Pitch": {
          "Degree": null,
          "Radian": null
        }
      },
      "Right": {
        "Roll": {
          "Degree": null,
          "Radian": null
        },
        "Pitch": {
          "Degree": null,
          "Radian": null
        }
      }
    }
  },
  "Status": {
    "Hands" : {
      "Left" : {
        "is_open" : true
      } ,
      "Right" : {
        "is_open" : false
      }
    }
  }
}
```
