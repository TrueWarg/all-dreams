import cv2
import numpy as np
from dataclasses import dataclass


class EdgeBasedDetector:
    def __init__(self, config):
        self.config = config

    # todo remove temporary using row contours
    def detect(self, img: np.array):
        return self._find_counters(img)

    def _find_counters(self, img: np.array):
        # use copy later?
        img = cv2.blur(img, self.config.blur_kernel)
        _, img = cv2.threshold(img, self.config.binary_threshold, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(img, self.config.canny_threshold1, self.config.canny_threshold2)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy


@dataclass
class Config:
    blur_kernel: tuple
    binary_threshold: int
    canny_threshold1: int
    canny_threshold2: int
