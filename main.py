from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
from UI import UI
from ComputerVisionModules import computerVision

from PyQt5 import QtWidgets


class Interface(UI.Ui_HumonoidRobotControl):
    def __init__(self):
        super().__init__()

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def start_video_feed(self, ui):
        self.CameraFeed = CameraFeed()
        self.CameraFeed.start()
        self.CameraFeed.ui = ui
        self.CameraFeed.ImageUpdate.connect(ui.ImageUpdateSlot)

    def CancelFeed(self):
        self.CameraFeed.stop()

    def is_head_on(self):
        return self.Head.isChecked()

    def is_shoulders_on(self):
        return self.Shoulders.isChecked()

    def is_elbows_on(self):
        return self.Elbows.isChecked()

    def is_hands_on(self):
        return self.Hands.isChecked()

    def is_black_background_on(self):
        return self.BlackBackground.isChecked()

    def is_head_text_on(self):
        return self.HeadInfo.isChecked()

    def is_hands_text_on(self):
        return self.HandsInfo.isChecked()

    def is_upper_body_text_on(self):
        return self.UpperBodyInfo.isChecked()



class CameraFeed(QThread):
    ImageUpdate = pyqtSignal(QImage)
    ui = None

    def run(self):

        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)

        while self.ThreadActive:

            interface_inputs = self.get_inputs_from_interface()
            ret, frame = Capture.read()
            if ret:
                Image = computerVision.run_computer_vision(frame , interface_inputs)
                ConvertToQtFormat = QImage(Image.data , Image.shape[1] , Image.shape[0] , QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(800, 640, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)


    def stop(self):
        self.ThreadActive = False
        self.quit()

    def get_inputs_from_interface(self):
        interface_input = {
            "Head": ui.is_head_on(),
            "Shoulders": ui.is_shoulders_on(),
            "Elbows": ui.is_elbows_on(),
            "Hands": ui.is_hands_on(),
            "BlackBackground": ui.is_black_background_on(),
            "HeadText": ui.is_head_text_on(),
            "UpperBodyText": ui.is_upper_body_text_on(),
            "HandsText": ui.is_hands_text_on()
        }

        return interface_input

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HumonoidRobotControl = QtWidgets.QMainWindow()
    ui = Interface()
    ui.setupUi(HumonoidRobotControl)

    ui.start_video_feed(ui)
    HumonoidRobotControl.show()
    sys.exit(app.exec_())


