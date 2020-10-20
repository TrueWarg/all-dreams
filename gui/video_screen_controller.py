from PyQt5 import QtCore
from sensor.video import VideoFrameReader


class VideoScreenController:
    def __init__(self):
        pass


class VideoStreamer(QtCore.QObject):
    def __init__(self):
        self.frame_reader = VideoFrameReader()

    def run(self):
        while True:
            image = self.frame_reader.read()
            if image:
                # send signal
                pass
