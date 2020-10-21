from PyQt5 import QtWidgets
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

        width = available_geometry.width() // 2
        height = available_geometry.height() // 1.5

        x = screen_center.x() - width // 2
        y = screen_center.y() - height // 2

        self.setGeometry(x, y, width, height)

    def _create_controller(self):
        self._controller = VideoScreenController()
        self._controller.read_frame.connect(self._on_frame_read)

    def _on_frame_read(self, frame):
        print(frame)

    def closeEvent(self, event):
        self._controller.clear_resources()
        event.accept()
