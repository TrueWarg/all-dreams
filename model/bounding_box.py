from dataclasses import dataclass


@dataclass()
class Bbox:
    left: int
    top: int
    width: int
    height: int
