from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from gui.edge_based_dices_detection_controller import EdgeBasedDicesDetectionController
import numpy as np


class EdgeBasedDicesDetectionScreen(QtWidgets.QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self._init_gui()
        self._create_controller()

    def _init_gui(self):
        available_geometry = QtWidgets.QDesktopWidget().availableGeometry()
        screen_center = available_geometry.center()

        self.width = available_geometry.width() // 2
        self.height = available_geometry.height() // 3

        x = screen_center.x() - self.width // 2
        y = screen_center.y() - self.height // 2

        self.setGeometry(x, y, self.width, self.height)
        self.image = QtWidgets.QLabel(self)
        self.image.resize(self.width // 2, self.height)
        # temporary, remove later
        self.test_slider1 = QtWidgets.QSlider(Qt.Horizontal, self)
        self.test_slider1.setMaximumWidth(self.width // 2)
        self.test_slider2 = QtWidgets.QSlider(Qt.Horizontal, self)
        self.test_slider2.setMaximumWidth(self.width // 2)
        self.test_slider3 = QtWidgets.QSlider(Qt.Horizontal, self)
        self.test_slider3.setMaximumWidth(self.width // 2)

        main_h_box = QtWidgets.QHBoxLayout()

        main_h_box.addWidget(self.image)

        instrument_panel_v_box = QtWidgets.QVBoxLayout()
        instrument_panel_v_box.addWidget(self.test_slider1)
        instrument_panel_v_box.addWidget(self.test_slider2)
        instrument_panel_v_box.addWidget(self.test_slider3)

        main_h_box.addLayout(instrument_panel_v_box)

        self.setLayout(main_h_box)

    def _create_controller(self):
        self._controller = EdgeBasedDicesDetectionController()
        self._controller.images.connect(self._on_image_received)

    def _on_image_received(self, image: np.ndarray):
        scaled = image.scaled(self.width // 2, self.height, Qt.KeepAspectRatio)
        pix_map = QPixmap.fromImage(scaled)
        self.image.setPixmap(pix_map)

    def closeEvent(self, event):
        self._controller.clear_resources()
        event.accept()
