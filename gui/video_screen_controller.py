from PyQt5 import QtCore

from gui.mappers import rgb_image_to_qt
from sensor.video import VideoFrameReader
from model.edge_based_detector import EdgeBasedDetector, Config
import cv2
import numpy as np


class VideoScreenController(QtCore.QObject):
    images = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._create_and_start_streamer()
        # todo enable change config dynamically
        config = Config(
            blur_kernel=(3, 3),
            binary_threshold=80,
            canny_threshold1=80,
            canny_threshold2=230,
            min_dice_side_area_px=2000,
            dice_side_padding_px=10,
            min_dot_area_px=50
        )
        self._detector = EdgeBasedDetector(config)

    def _create_and_start_streamer(self):
        self._thread = QtCore.QThread()
        self._streamer = VideoStreamer()
        self._streamer.moveToThread(self._thread)
        self._streamer.frames.connect(self._on_frame_received)
        self._thread.started.connect(self._streamer.run)
        self._thread.start()

    def _on_frame_received(self, frame):
        dice_sides = self._detector.detect(frame)
        for side in dice_sides:
            points = cv2.boxPoints(side.rectangle)
            points = np.int0(points)
            frame = cv2.drawContours(frame, [points], 0, (0, 0, 255), 2)
        self.images.emit(rgb_image_to_qt(frame))

    def clear_resources(self):
        self._thread.stop()


class VideoStreamer(QtCore.QObject):
    frames = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._frame_reader = VideoFrameReader(device=0)

    def run(self):
        while True:
            image = self._frame_reader.read()
            if image is not None:
                self.frames.emit(image)
