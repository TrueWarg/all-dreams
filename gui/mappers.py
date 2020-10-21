from PyQt5 import QtGui


def rgb_image_to_qt(frame):
    h, w, ch = frame.shape
    bytes_per_line = ch * w
    image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    return image
