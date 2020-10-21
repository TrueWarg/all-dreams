from PyQt5 import QtCore
from sensor.video import VideoFrameReader


class VideoScreenController(QtCore.QObject):
    read_frame = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._create_and_start_streamer()

    def _create_and_start_streamer(self):
        self._thread = QtCore.QThread()
        self._streamer = VideoStreamer()
        self._streamer.moveToThread(self._thread)
        self._streamer.read_frame.connect(self._on_frame_read)
        self._thread.started.connect(self._streamer.run)
        self._thread.start()

    def _on_frame_read(self, frame):
        self.read_frame.emit(frame)

    def clear_resources(self):
        self._thread.stop()


class VideoStreamer(QtCore.QObject):
    read_frame = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._frame_reader = VideoFrameReader(device=0)

    def run(self):
        while True:
            image = self._frame_reader.read()
            if image is not None:
                self.read_frame.emit(image)
