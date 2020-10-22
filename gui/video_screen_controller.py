from PyQt5 import QtCore

from gui.mappers import rgb_image_to_qt
from sensor.video import VideoFrameReader
from model.edge_based_detector import EdgeBasedDetector, Config
import cv2


class VideoScreenController(QtCore.QObject):
    images = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._create_and_start_streamer()
        config = Config(blur_kernel=(3, 3), binary_threshold=150, canny_threshold1=80, canny_threshold2=230)
        self._detector = EdgeBasedDetector(config)

    def _create_and_start_streamer(self):
        self._thread = QtCore.QThread()
        self._streamer = VideoStreamer()
        self._streamer.moveToThread(self._thread)
        self._streamer.frames.connect(self._on_frame_received)
        self._thread.started.connect(self._streamer.run)
        self._thread.start()

    def _on_frame_received(self, frame):
        # todo remove temporary using row contours
        contours, hierarchy = self._detector.detect(frame)
        frame = cv2.drawContours(frame, contours, -1, (0, 120, 255), 2, cv2.LINE_AA, hierarchy, 1)
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
