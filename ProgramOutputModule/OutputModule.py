import json

class Output:
  def __init__(self, angleType = "Degree"):
    self.angleType = angleType  # Degree or "Radian"

    self.output = {
      "Angles" : {
        "Head" : {
          "Pitch": {
            "Degree": None,
            "Radian": None
          },
          "Yaw": {
            "Degree": None,
            "Radian": None
          }
        },
        "Shoulders": {
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
        },
        "Elbows": {
          "Left":{
            "Roll": {
              "Degree": None,
              "Radian": None
            }
          },
          "Right": {
            "Roll": {
              "Degree": None,
              "Radian": None
            }
          }
        },
        "Wrists": {
          "Left":{
            "Roll": {
              "Degree": None,
              "Radian": None
            }
          },
          "Right": {
            "Roll": {
              "Degree": None,
              "Radian": None
            }
          }
        },
        "Hip": {
          "Left": {
            "Roll" : {
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
      },
      "Status": {
        "Hands" : {
          "Left" : {
            "is_open" : True
          } ,
          "Right" : {
            "is_open" : False
          }
        }
      }
    }

  def get_json_file(self,path):
      with open(path,"r",encoding="utf-8") as dfile :
        return json.load(dfile)

  def write_json_data(self, path):


    with open(path,"w",encoding="utf-8") as file:

      file.seek(0)

      json.dump(self.output, file, ensure_ascii=False)

      file.truncate()



# data = get_json_file("./ProgramOutputModule.json")
# print(data["Shoulders"]["Left"]["Pitch"])
# print(data["Hands"]["Left"]["is_open"])
# write_json_data(value,"./hello.json")