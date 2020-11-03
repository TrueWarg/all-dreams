from PyQt5 import QtCore

from gui.mappers import rgb_image_to_qt
from sensor.video import VideoFrameReader
from model.edge_based_dices_detector import EdgeBasedDicesDetector, Config, DiceSide
import cv2
import numpy as np
import math


def _add_score(img, dice_side: DiceSide):
    center = dice_side.rectangle[0]
    sizes = dice_side.rectangle[1]
    score = dice_side.score
    y_offset = math.sqrt(sizes[0]**2 + sizes[1]**2)/2 + 5
    org = (int(center[0]), max(int(center[1] - y_offset), 0))
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 255)
    thickness = 2
    return cv2.putText(img, str(score), org, font, font_scale, color, thickness, cv2.LINE_AA)


class EdgeBasedDicesDetectionController(QtCore.QObject):
    images = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._create_and_start_streamer()
        # todo enable change config dynamically
        config = Config(
            blur_kernel=(3, 3),
            binary_threshold=80,
            canny_low_threshold=80,
            canny_high_threshold=230,
            min_dice_side_area_px=2000,
            dice_side_padding_px=10,
            min_dot_area_px=50
        )
        self._detector = EdgeBasedDicesDetector(config)

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
            contours = [points]
            contour_idx = 0
            color = (0, 0, 255)
            thickness = 2
            frame = cv2.drawContours(frame, contours, contour_idx, color, thickness)
            frame = _add_score(frame, side)
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
