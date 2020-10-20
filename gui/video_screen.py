from PyQt5 import QtWidgets


class VideoScreen(QtWidgets.QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        available_geometry = QtWidgets.QDesktopWidget().availableGeometry()
        screen_center = available_geometry.center()

        width = available_geometry.width() // 2
        height = available_geometry.height() // 1.5

        x = screen_center.x() - width // 2
        y = screen_center.y() - height // 2

        self.setGeometry(x, y, width, height)

