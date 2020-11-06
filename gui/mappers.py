from PyQt5 import QtGui
import numpy as np


def rgb_image_to_qt(frame: np.ndarray) -> QtGui.QImage:
    h, w, ch = frame.shape
    bytes_per_line = ch * w
    image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    return image
