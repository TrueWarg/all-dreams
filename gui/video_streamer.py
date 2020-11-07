from PyQt5 import QtCore
from sensor.video import VideoFrameReader


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
