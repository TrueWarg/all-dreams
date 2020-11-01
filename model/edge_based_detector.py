import cv2
import numpy as np
from dataclasses import dataclass


def _center_is_contained(center, rectangles):
    for rect in rectangles:
        other_center = rect[0]
        other_sizes = rect[1]
        left, top = (other_center[0] - other_sizes[0] / 2, other_center[1] - other_sizes[1] / 2)
        right, bottom = (other_center[0] + other_sizes[0] / 2, other_center[1] + other_sizes[1] / 2)
        if left < center[0] < right and top < center[1] < bottom:
            return True

    return False


class EdgeBasedDetector:
    def __init__(self, config):
        self.config = config

    # todo remove temporary using row rotated rectangles
    def detect(self, img: np.array):
        return self._find_counters(img)

    def _find_counters(self, img: np.array):
        # use copy later?
        img = cv2.blur(img, self.config.blur_kernel)
        _, img = cv2.threshold(img, self.config.binary_threshold, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(img, self.config.canny_threshold1, self.config.canny_threshold2)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return self._create_rectangles(contours)

    def _create_rectangles(self, contours):
        rectangles = []
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            center = rect[0]
            sizes = rect[1]
            area = sizes[0] * sizes[1]
            if area > self.config.min_dice_side_area_px and _center_is_contained(center, rectangles):
                rectangles.append(rect)

        return rectangles

    def _calc_score(self, rect, img):
        center, sizes, angle = rect
        rotation = cv2.getRotationMatrix2D(center, angle, scale=1)
        rotated = cv2.warpAffine(img, rotation, (img.shape[0], img.shape[1]))
        padding = self.config.dice_side_padding_px
        cropped = cv2.getRectSubPix(rotated, (int(sizes[0]) - padding, int(sizes[1]) - padding), center)
        _, cropped = cv2.threshold(cropped, 64, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(cropped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


@dataclass
class Config:
    blur_kernel: tuple
    binary_threshold: int
    canny_threshold1: int
    canny_threshold2: int
    min_dice_side_area_px: int
    dice_side_padding_px: int


@dataclass
class DiceSide:
    rectangle: tuple
    score: int
