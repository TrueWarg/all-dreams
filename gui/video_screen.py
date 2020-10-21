from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from gui.video_screen_controller import VideoScreenController


class VideoScreen(QtWidgets.QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self._init_gui()
        self._create_controller()

    def _init_gui(self):
        available_geometry = QtWidgets.QDesktopWidget().availableGeometry()
        screen_center = available_geometry.center()

        self.width = available_geometry.width() // 2
        self.height = available_geometry.height() // 1.5

        x = screen_center.x() - self.width // 2
        y = screen_center.y() - self.height // 2

        self.setGeometry(x, y, self.width, self.height)
        self.image = QtWidgets.QLabel(self)
        self.image.resize(self.width, self.height)

    def _create_controller(self):
        self._controller = VideoScreenController()
        self._controller.images.connect(self._on_image_received)

    def _on_image_received(self, image):
        scaled = image.scaled(self.width, self.height, Qt.KeepAspectRatio)
        pix_map = QPixmap.fromImage(scaled)
        self.image.setPixmap(pix_map)

    def closeEvent(self, event):
        self._controller.clear_resources()
        event.accept()
