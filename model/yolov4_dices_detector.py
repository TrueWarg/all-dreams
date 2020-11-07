import cv2
import numpy as np
from dataclasses import dataclass
from model.bounding_box import Bbox
from typing import List, Tuple


def _create_box(img_width: int, img_height: int, detection: np.ndarray) -> Bbox:
    center_x = detection[0] * img_width
    center_y = detection[1] * img_height
    width = int(detection[2] * img_width)
    height = int(detection[3] * img_height)
    left = int(center_x - width / 2)
    top = int(center_y - height / 2)
    return Bbox(left, top, width, height)


@dataclass
class Config:
    confidence_threshold: float
    nms_threshold: float
    img_size: Tuple


# this version yolo can't detect angle...
@dataclass
class DetectedDice:
    box: Bbox
    confidence: float
    class_id: int


class YoloV4DicesDetector:
    def __init__(self,
                 weight_path: str,
                 config_path: str,
                 config: Config
                 ):
        net = cv2.dnn.readNet(weight_path, config_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.config = config
        self.net = net

    def detect(self, img: np.array) -> List[DetectedDice]:
        blob = cv2.dnn.blobFromImage(
            img,
            scalefactor=1.0 / 255,
            size=self.config.img_size,
            swapRB=True
        )
        self.net.setInput(blob)
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())
        return self._post_process(img, outputs)

    def _post_process(self, img: np.ndarray, outputs: List[np.ndarray]) -> List[DetectedDice]:
        img_width, img_height = img.shape[:2]
        boxes = []
        confidences = []
        class_ids = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.config.confidence_threshold:
                    boxes.append(_create_box(img_width, img_height, detection[0:5]))
                    confidences.append(confidence)
                    class_ids.append(class_id)
        indices = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            self.config.confidence_threshold,
            self.config.nms_threshold
        )
        dices = [DetectedDice(boxes[i], confidences[i], class_ids[i]) for i in indices]
        return dices
