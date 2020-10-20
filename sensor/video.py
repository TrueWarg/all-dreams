import cv2


class VideoFrameReader:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def read(self):
        ret, frame = self.capture.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release(self):
        if self.capture:
            self.release()
        self.capture = None
