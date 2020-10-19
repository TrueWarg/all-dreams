from PyQt5 import QtWidgets


class VideoScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Video')
        self.setGeometry(200, 200, 480, 320)