import cv2
import numpy as np
from dataclasses import dataclass


@dataclass
class Config:
    backend: str
    target: str
    img_scale_factor: float
    img_size: tuple


class YoloV4DicesDetector:
    def __init__(self,
                 weight_path: str,
                 config_path: str,
                 config: Config
            ):
        net = cv2.dnn.readNet(weight_path, config_path)
        net.setPreferableBackend(config.backend)
        net.setPreferableTarget(config.target)
        self.config = config
        self.net = net

    def detect(self, img: np.array):
        blob = cv2.dnn.blobFromImage(
            img,
            scalefactor=self.config.img_scale_factor,
            size=self.config.img_size,
            swapRB=True
        )
        self.net.setInput(blob)
        predictions = self.net.forward(self.net.getUnconnectedOutLayersNames())