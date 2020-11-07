from PyQt5 import QtCore
from gui.mappers import rgb_image_to_qt
from gui.video_streamer import VideoStreamer
from model.yolov4_dices_detector import YoloV4DicesDetector, Config
import numpy as np
import cv2

# todo set it in some config (ui interface for select from user files ?)
YOLO_V4_WEIGHT_PATH = '<your-path>'
YOLO_V4_CONFIG_PATH = '<your-path>'


def _place_class_label(img: np.ndarray, x: int, y: int, class_label: int) -> np.ndarray:
    org = (x, y)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 255)
    thickness = 2
    return cv2.putText(img, class_label, org, font, font_scale, color, thickness, cv2.LINE_AA)


_classes = {
    0: '1',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6'
}


class YoloV4DicesDetectionController(QtCore.QObject):
    images = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._create_and_start_streamer()
        # todo enable change config dynamically
        config = Config(
            confidence_threshold=0.3,
            nms_threshold=0.4,
            img_size=(608, 608)
        )
        self._detector = YoloV4DicesDetector(YOLO_V4_WEIGHT_PATH, YOLO_V4_CONFIG_PATH, config)

    def _create_and_start_streamer(self):
        self._thread = QtCore.QThread()
        self._streamer = VideoStreamer()
        self._streamer.moveToThread(self._thread)
        self._streamer.frames.connect(self._on_frame_received)
        self._thread.started.connect(self._streamer.run)
        self._thread.start()

    def _on_frame_received(self, frame: np.ndarray):
        dices = self._detector.detect(frame)
        for dice in dices:
            box = dice.box
            left, top = box.left, box.top
            right, bottom = box.left + box.width, box.top + box.height
            color = (0, 0, 255)
            frame = cv2.rectangle(frame, (left, top), (right, bottom), color)
            class_label_x = left + box.width // 2
            class_label_y = top + 10
            class_label = _classes[dice.class_id]
            frame = _place_class_label(frame, class_label_x, class_label_y, class_label)
        self.images.emit(rgb_image_to_qt(frame))

    def clear_resources(self):
        self._thread.stop()
