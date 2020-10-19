import cv2
import numpy as np


class EdgeBasedDetector:
    def __init__(self, config):
        self.config = config
        pass

    def detect(self):
        pass

    def _find_counters(self, img: np.array):
        # use copy later?
        img = cv2.blur(img, self.config.blur_kernel)
        _, img = cv2.threshold(img, self.config.binary_threshold, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(img, self.config.canny_x, self.config.canny_y)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy
