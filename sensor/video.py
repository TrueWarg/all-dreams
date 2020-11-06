import cv2
import numpy as np


class VideoFrameReader:
    def __init__(self, device):
        self.capture = cv2.VideoCapture(device)

    def read(self) -> np.ndarray:
        ret, frame = self.capture.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release(self):
        if self.capture:
            self.release()
